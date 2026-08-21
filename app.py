import cv2
import json
import os
import threading
import time

from flask import (
    Flask,
    render_template,
    Response,
    jsonify,
    request
)

from fall_detection import FallDetector
from alert import SMSAlert
FAMILY_FILE = "family.json"

sms_alert = SMSAlert()


def load_family():
    if not os.path.exists(FAMILY_FILE):
        return {
            "name": "",
            "phone": "",
            "relationship": ""
        }

    with open(FAMILY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_family(family):
    with open(FAMILY_FILE, "w", encoding="utf-8") as file:
        json.dump(family, file, indent=4)


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)


# ============================================================
# FILES
# ============================================================

DATA_FILE = "data.json"


# ============================================================
# DEFAULT DATA
# ============================================================

DEFAULT_DATA = {

    "person": {
        "name": "",
        "age": "",
        "gender": "",
        "room": "",
        "medical_info": ""
    },

    "family": {
        "name": "",
        "relationship": "",
        "phone": ""
    }
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not os.path.exists(DATA_FILE):

        save_data(DEFAULT_DATA)

        return DEFAULT_DATA.copy()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return DEFAULT_DATA.copy()


# ============================================================
# SAVE DATA
# ============================================================

def save_data(data):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


data = load_data()


# ============================================================
# DETECTOR
# ============================================================

detector = FallDetector()


# ============================================================
# SMS
# ============================================================

sms_alert = SMSAlert()


# ============================================================
# CAMERA VARIABLES
# ============================================================

camera = None

camera_running = False

camera_lock = threading.Lock()

camera_thread = None


# ============================================================
# SYSTEM STATE
# ============================================================

system_state = {

    "person": "Waiting",

    "movement": "Camera Off",

    "confidence": 0,

    "fall_detected": False,

    "camera_running": False,

    "last_event": "System Ready",

    "last_sms": "No SMS sent",

    "last_sms_success": False
}


# ============================================================
# ALERT CONTROL
# ============================================================

last_fall_alert_time = 0

SMS_COOLDOWN = 30


# ============================================================
# ALERT HISTORY
# ============================================================

alert_history = []


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    family = load_family()

    return render_template(
        "index.html",
        family=family
    )
# ============================================================
# GET DATA
# ============================================================

@app.route("/api/data")
def get_data():

    return jsonify({
        "person": data["person"],
        "family": data["family"]
    })


# ============================================================
# SAVE PERSON AND FAMILY INFORMATION
# ============================================================

@app.route(
    "/api/save-details",
    methods=["POST"]
)
def save_details():

    global data

    try:

        new_data = request.get_json()

        person = new_data.get(
            "person",
            {}
        )

        family = new_data.get(
            "family",
            {}
        )

        # ----------------------------------------------------
        # Basic validation
        # ----------------------------------------------------

        if not person.get("name"):

            return jsonify({
                "success": False,
                "message": "Person name is required."
            }), 400

        if not family.get("name"):

            return jsonify({
                "success": False,
                "message": "Family member name is required."
            }), 400

        if not family.get("phone"):

            return jsonify({
                "success": False,
                "message": "Family member phone number is required."
            }), 400

        data = {

            "person": person,

            "family": family
        }

        save_data(data)

        return jsonify({
            "success": True,
            "message": "Person and family details saved."
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# CAMERA GENERATOR
# ============================================================

def generate_frames():

    global camera
    global camera_running
    global last_fall_alert_time

    while camera_running:

        with camera_lock:

            if camera is None:

                break

            success, frame = camera.read()

        if not success:

            time.sleep(0.1)

            continue

        # ----------------------------------------------------
        # FALL DETECTION
        # ----------------------------------------------------

        processed_frame, result = detector.process_frame(
            frame
        )

        # ----------------------------------------------------
        # UPDATE STATE
        # ----------------------------------------------------

        system_state["person"] = (
            "Detected"
            if result["movement"] != "No Person"
            else "Not Detected"
        )

        system_state["movement"] = result[
            "movement"
        ]

        system_state["confidence"] = result[
            "confidence"
        ]

        system_state["fall_detected"] = result[
            "fall_detected"
        ]

        # ----------------------------------------------------
        # AUTOMATIC SMS
        # ----------------------------------------------------

        if result["fall_detected"]:

            current_time = time.time()

            if (
                current_time -
                last_fall_alert_time
                >
                SMS_COOLDOWN
            ):

                last_fall_alert_time = current_time

                system_state[
                    "last_event"
                ] = "Fall Detected"

                alert_history.append({

                    "time": time.strftime(
                        "%H:%M:%S"
                    ),

                    "event": "Fall Detected",

                    "confidence": result[
                        "confidence"
                    ],

                    "status": "SMS Sending"
                })

                # Send SMS in another thread
                threading.Thread(
                    target=send_fall_sms,
                    daemon=True
                ).start()

        # ----------------------------------------------------
        # ENCODE FRAME
        # ----------------------------------------------------

        ret, buffer = cv2.imencode(
            ".jpg",
            processed_frame
        )

        if not ret:

            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            +
            frame_bytes
            +
            b"\r\n"
        )


# ============================================================
# FALL SMS
# ============================================================

def send_fall_sms():

    result = sms_alert.send_fall_alert(
        data["person"],
        data["family"]
    )

    if result["success"]:

        system_state[
            "last_sms"
        ] = "Fall SMS sent successfully"

        system_state[
            "last_sms_success"
        ] = True

        if alert_history:

            alert_history[-1][
                "status"
            ] = "SMS Sent"

    else:

        system_state[
            "last_sms"
        ] = result["message"]

        system_state[
            "last_sms_success"
        ] = False

        if alert_history:

            alert_history[-1][
                "status"
            ] = "SMS Failed"


# ============================================================
# VIDEO STREAM
# ============================================================

@app.route("/video_feed")
def video_feed():

    if not camera_running:

        return (
            "Camera is stopped.",
            200
        )

    return Response(
        generate_frames(),
        mimetype=(
            "multipart/x-mixed-replace; "
            "boundary=frame"
        )
    )


# ============================================================
# START CAMERA
# ============================================================

@app.route(
    "/api/start-camera",
    methods=["POST"]
)
def start_camera():

    global camera
    global camera_running

    if camera_running:

        return jsonify({
            "success": False,
            "message": "Camera is already running."
        })

    try:

        camera = cv2.VideoCapture(0)

        # Windows camera backend
        if not camera.isOpened():

            camera.release()

            camera = cv2.VideoCapture(
                0,
                cv2.CAP_DSHOW
            )

        if not camera.isOpened():

            camera = None

            return jsonify({
                "success": False,
                "message": (
                    "Could not open camera. "
                    "Check camera connection "
                    "and permissions."
                )
            }), 500

        # ----------------------------------------------------
        # Camera settings
        # ----------------------------------------------------

        camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            1280
        )

        camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            720
        )

        camera.set(
            cv2.CAP_PROP_FPS,
            30
        )

        camera_running = True

        system_state[
            "camera_running"
        ] = True

        system_state[
            "movement"
        ] = "Waiting for person"

        system_state[
            "last_event"
        ] = "Camera Started"

        return jsonify({

            "success": True,

            "message": "Camera started successfully."
        })

    except Exception as e:

        camera_running = False

        camera = None

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# ============================================================
# STOP CAMERA
# ============================================================

@app.route(
    "/api/stop-camera",
    methods=["POST"]
)
def stop_camera():

    global camera
    global camera_running

    camera_running = False

    system_state[
        "camera_running"
    ] = False

    system_state[
        "person"
    ] = "Waiting"

    system_state[
        "movement"
    ] = "Camera Off"

    system_state[
        "confidence"
    ] = 0

    system_state[
        "fall_detected"
    ] = False

    system_state[
        "last_event"
    ] = "Camera Stopped"

    with camera_lock:

        if camera is not None:

            camera.release()

            camera = None

    return jsonify({

        "success": True,

        "message": "Camera stopped."
    })


# ============================================================
# STATUS
# ============================================================

@app.route("/api/status")
def status():

    return jsonify({

        "camera_running":
            camera_running,

        "person":
            system_state["person"],

        "movement":
            system_state["movement"],

        "confidence":
            system_state["confidence"],

        "fall_detected":
            system_state["fall_detected"],

        "last_event":
            system_state["last_event"],

        "last_sms":
            system_state["last_sms"],

        "last_sms_success":
            system_state["last_sms_success"]
    })


# ============================================================
# MANUAL EMERGENCY SMS
# ============================================================

@app.route(
    "/api/emergency-sms",
    methods=["POST"]
)
def emergency_sms():

    family = data["family"]

    if not family.get("phone"):

        return jsonify({

            "success": False,

            "message": (
                "Please save the family "
                "member phone number first."
            )
        }), 400

    result = sms_alert.send_emergency_alert(
        data["person"],
        data["family"]
    )

    if result["success"]:

        system_state[
            "last_sms"
        ] = "Emergency SMS sent"

        alert_history.append({

            "time": time.strftime(
                "%H:%M:%S"
            ),

            "event": "Manual Emergency",

            "confidence": "-",

            "status": "SMS Sent"
        })

    return jsonify(result)


# ============================================================
# ALERT HISTORY
# ============================================================

@app.route("/api/history")
def history():

    return jsonify(
        alert_history[-20:]
    )


# ============================================================
# CLEAR HISTORY
# ============================================================

@app.route(
    "/api/clear-history",
    methods=["POST"]
)
def clear_history():

    alert_history.clear()

    return jsonify({

        "success": True
    })


# ============================================================
# MAIN
# ============================================================
@app.route("/save-family", methods=["POST"])
def save_family_details():

    data = request.get_json()

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    relationship = data.get("relationship", "").strip()

    if not name:
        return jsonify({
            "success": False,
            "message": "Enter family member name."
        }), 400

    if not phone:
        return jsonify({
            "success": False,
            "message": "Enter family member phone number."
        }), 400

    if not phone.startswith("+"):
        return jsonify({
            "success": False,
            "message": "Use international format, example: +919876543210"
        }), 400

    family = {
        "name": name,
        "phone": phone,
        "relationship": relationship
    }

    save_family(family)

    return jsonify({
        "success": True,
        "message": "Family details saved successfully."
    })
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )