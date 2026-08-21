// ============================================================
// GLOBAL
// ============================================================

let statusTimer = null;


// ============================================================
// POPUP
// ============================================================

function showPopup(
    title,
    message,
    type = "success"
) {

    const popup =
        document.getElementById("popup");

    const popupTitle =
        document.getElementById("popupTitle");

    const popupMessage =
        document.getElementById("popupMessage");

    const popupIcon =
        document.getElementById("popupIcon");

    popupTitle.textContent = title;

    popupMessage.textContent = message;

    if (type === "error") {

        popupIcon.textContent = "!";

        popupIcon.style.background = "#fee2e2";

        popupIcon.style.color = "#dc2626";

        popup.style.borderLeftColor = "#dc2626";

    } else {

        popupIcon.textContent = "✓";

        popupIcon.style.background = "#dcfce7";

        popupIcon.style.color = "#16a34a";

        popup.style.borderLeftColor = "#16a34a";
    }

    popup.classList.add("show");

    setTimeout(() => {

        popup.classList.remove("show");

    }, 4000);
}


function closePopup() {

    document
        .getElementById("popup")
        .classList.remove("show");
}


// ============================================================
// START CAMERA
// ============================================================

async function startCamera() {

    try {

        const response =
            await fetch(
                "/api/start-camera",
                {
                    method: "POST"
                }
            );

        const result =
            await response.json();

        if (!result.success) {

            showPopup(
                "Camera Error",
                result.message,
                "error"
            );

            return;
        }

        const cameraFeed =
            document.getElementById(
                "cameraFeed"
            );

        const cameraMessage =
            document.getElementById(
                "cameraMessage"
            );

        cameraFeed.src =
            "/video_feed?t=" +
            Date.now();

        cameraMessage.style.display =
            "none";

        showPopup(
            "Camera Started",
            "Live camera monitoring has started."
        );

        updateCameraStatus(true);

        startStatusUpdates();

    } catch (error) {

        showPopup(
            "Camera Error",
            error.message,
            "error"
        );
    }
}


// ============================================================
// STOP CAMERA
// ============================================================

async function stopCamera() {

    try {

        const response =
            await fetch(
                "/api/stop-camera",
                {
                    method: "POST"
                }
            );

        const result =
            await response.json();

        const cameraFeed =
            document.getElementById(
                "cameraFeed"
            );

        const cameraMessage =
            document.getElementById(
                "cameraMessage"
            );

        cameraFeed.src = "";

        cameraMessage.textContent =
            "Camera is stopped";

        cameraMessage.style.display =
            "block";

        updateCameraStatus(false);

        showPopup(
            "Camera Stopped",
            "Camera monitoring has been stopped."
        );

    } catch (error) {

        showPopup(
            "Error",
            error.message,
            "error"
        );
    }
}


// ============================================================
// CAMERA STATUS
// ============================================================

function updateCameraStatus(
    running
) {

    const status =
        document.getElementById(
            "cameraStatus"
        );

    if (running) {

        status.textContent =
            "● ONLINE";

        status.className =
            "camera-online";

    } else {

        status.textContent =
            "● OFFLINE";

        status.className =
            "camera-offline";
    }
}


// ============================================================
// SAVE DETAILS
// ============================================================

async function saveDetails() {

    const data = {

        person: {

            name:
                document.getElementById(
                    "personName"
                ).value.trim(),

            age:
                document.getElementById(
                    "personAge"
                ).value,

            gender:
                document.getElementById(
                    "personGender"
                ).value,

            room:
                document.getElementById(
                    "personRoom"
                ).value.trim(),

            medical_info:
                document.getElementById(
                    "medicalInfo"
                ).value.trim()
        },

        family: {

            name:
                document.getElementById(
                    "familyName"
                ).value.trim(),

            relationship:
                document.getElementById(
                    "familyRelationship"
                ).value.trim(),

            phone:
                document.getElementById(
                    "familyPhone"
                ).value.trim()
        }
    };


    if (!data.person.name) {

        showPopup(
            "Missing Information",
            "Please enter the person's name.",
            "error"
        );

        return;
    }


    if (!data.family.name) {

        showPopup(
            "Missing Information",
            "Please enter the family member name.",
            "error"
        );

        return;
    }


    if (!data.family.phone) {

        showPopup(
            "Missing Information",
            "Please enter the family member phone number.",
            "error"
        );

        return;
    }


    try {

        const response =
            await fetch(
                "/api/save-details",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        const result =
            await response.json();


        if (result.success) {

            updateRecipient(
                data.family
            );

            showPopup(
                "Details Saved",
                "Person and family information saved successfully."
            );

        } else {

            showPopup(
                "Save Failed",
                result.message,
                "error"
            );
        }

    } catch (error) {

        showPopup(
            "Error",
            error.message,
            "error"
        );
    }
}


// ============================================================
// LOAD DETAILS
// ============================================================

async function loadDetails() {

    try {

        const response =
            await fetch(
                "/api/data"
            );

        const data =
            await response.json();


        const person =
            data.person;

        const family =
            data.family;


        document.getElementById(
            "personName"
        ).value =
            person.name || "";


        document.getElementById(
            "personAge"
        ).value =
            person.age || "";


        document.getElementById(
            "personGender"
        ).value =
            person.gender || "";


        document.getElementById(
            "personRoom"
        ).value =
            person.room || "";


        document.getElementById(
            "medicalInfo"
        ).value =
            person.medical_info || "";


        document.getElementById(
            "familyName"
        ).value =
            family.name || "";


        document.getElementById(
            "familyRelationship"
        ).value =
            family.relationship || "";


        document.getElementById(
            "familyPhone"
        ).value =
            family.phone || "";


        updateRecipient(
            family
        );

    } catch (error) {

        console.error(
            "Could not load details:",
            error
        );
    }
}


// ============================================================
// RECIPIENT
// ============================================================

function updateRecipient(
    family
) {

    const element =
        document.getElementById(
            "recipientDisplay"
        );

    if (
        family.name &&
        family.phone
    ) {

        element.textContent =
            `${family.name} (${family.phone})`;

    } else {

        element.textContent =
            "Not configured";
    }
}


// ============================================================
// EMERGENCY SMS
// ============================================================

async function sendEmergencySMS() {

    const button =
        document.getElementById("smsButton");


    button.disabled = true;

    button.innerText =
        "📱 Sending...";


    try {

        const response = await fetch(
            "/send-emergency-sms",
            {
                method: "POST"
            }
        );


        const data =
            await response.json();


        if (data.success) {

            alert(
                "SMS sent successfully!"
            );

        } else {

            alert(
                "SMS failed: " +
                data.message
            );
        }


    } catch (error) {

        console.error(error);

        alert(
            "Cannot connect to Flask server."
        );

    } finally {

        button.disabled = false;

        button.innerText =
            "🚨 Send Emergency SMS";
    }
}

// ============================================================
// STATUS UPDATE
// ============================================================

async function updateStatus() {

    try {

        const response =
            await fetch(
                "/api/status"
            );

        const data =
            await response.json();


        updateCameraStatus(
            data.camera_running
        );


        document.getElementById(
            "personStatus"
        ).textContent =
            data.person;


        document.getElementById(
            "movementStatus"
        ).textContent =
            data.movement;


        document.getElementById(
            "confidenceStatus"
        ).textContent =
            data.confidence + "%";


        const detection =
            document.getElementById(
                "detectionAlert"
            );


        const title =
            document.getElementById(
                "fallTitle"
            );


        const description =
            document.getElementById(
                "fallDescription"
            );


        if (data.fall_detected) {

            detection.className =
                "detection-fall";

            title.textContent =
                "🚨 FALL DETECTED";

            description.textContent =
                "Please check the person immediately.";

        } else {

            detection.className =
                "detection-normal";

            title.textContent =
                "No Fall Detected";

            description.textContent =
                "The system is ready for monitoring.";
        }


        if (
            data.camera_running
        ) {

            document.getElementById(
                "cameraMessage"
            ).style.display =
                "none";
        }


    } catch (error) {

        console.error(
            "Status error:",
            error
        );
    }
}


// ============================================================
// START STATUS POLLING
// ============================================================

function startStatusUpdates() {

    if (statusTimer) {

        return;
    }

    statusTimer =
        setInterval(
            updateStatus,
            1000
        );
}


// ============================================================
// HISTORY
// ============================================================

async function loadHistory() {

    try {

        const response =
            await fetch(
                "/api/history"
            );

        const history =
            await response.json();


        const body =
            document.getElementById(
                "historyBody"
            );


        if (!history.length) {

            body.innerHTML = `
                <tr>
                    <td colspan="4">
                        No alerts yet
                    </td>
                </tr>
            `;

            return;
        }


        body.innerHTML =
            history
                .slice()
                .reverse()
                .map(item => `

                    <tr>

                        <td>
                            ${item.time}
                        </td>

                        <td>
                            ${item.event}
                        </td>

                        <td>
                            ${item.confidence}
                        </td>

                        <td>
                            ${item.status}
                        </td>

                    </tr>

                `)
                .join("");

    } catch (error) {

        console.error(
            "History error:",
            error
        );
    }
}


// ============================================================
// CLEAR HISTORY
// ============================================================

async function clearHistory() {

    await fetch(
        "/api/clear-history",
        {
            method: "POST"
        }
    );

    loadHistory();

    showPopup(
        "History Cleared",
        "Alert history has been cleared."
    );
}


// ============================================================
// INITIALIZE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadDetails();

        updateStatus();

        loadHistory();

        startStatusUpdates();

    }
);