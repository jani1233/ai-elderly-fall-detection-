import cv2
import math
import time
import os
import urllib.request

import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FallDetector:

    def __init__(self):

        # -------------------------------------------------
        # MediaPipe Pose Landmarker
        # -------------------------------------------------

        self.model_path = "pose_landmarker_lite.task"

        # Download the model automatically if it does not exist
        if not os.path.exists(self.model_path):

            print("Downloading MediaPipe Pose model...")

            url = (
                "https://storage.googleapis.com/mediapipe-models/"
                "pose_landmarker/pose_landmarker_lite/float16/1/"
                "pose_landmarker_lite.task"
            )

            urllib.request.urlretrieve(
                url,
                self.model_path
            )

            print("Pose model downloaded.")

        # MediaPipe Base Options
        base_options = python.BaseOptions(
            model_asset_path=self.model_path
        )

        options = vision.PoseLandmarkerOptions(

            base_options=base_options,

            running_mode=vision.RunningMode.VIDEO,

            num_poses=1,

            min_pose_detection_confidence=0.5,

            min_pose_presence_confidence=0.5,

            min_tracking_confidence=0.5
        )

        self.detector = vision.PoseLandmarker.create_from_options(
            options
        )

        # -------------------------------------------------
        # Fall confirmation
        # -------------------------------------------------

        self.fall_start_time = None

        self.FALL_CONFIRM_TIME = 1.0

        # Current status

        self.fall_detected = False

        self.confidence = 0

        self.movement = "Normal"

        self.timestamp_ms = 0

    # -----------------------------------------------------
    # Distance between two landmarks
    # -----------------------------------------------------

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    # -----------------------------------------------------
    # Process frame
    # -----------------------------------------------------

    def process_frame(self, frame):

        height, width, _ = frame.shape

        # -------------------------------------------------
        # Convert OpenCV BGR → RGB
        # -------------------------------------------------

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        # Timestamp must continuously increase

        self.timestamp_ms += 33

        # -------------------------------------------------
        # MediaPipe Pose Detection
        # -------------------------------------------------

        results = self.detector.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        fall = False

        confidence = 0

        movement = "No Person"

        # -------------------------------------------------
        # Check if person detected
        # -------------------------------------------------

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            # -------------------------------------------------
            # MediaPipe landmark indexes
            # -------------------------------------------------

            LEFT_SHOULDER = 11
            RIGHT_SHOULDER = 12

            LEFT_HIP = 23
            RIGHT_HIP = 24

            LEFT_KNEE = 25
            RIGHT_KNEE = 26

            # Get landmarks

            left_shoulder = landmarks[LEFT_SHOULDER]

            right_shoulder = landmarks[RIGHT_SHOULDER]

            left_hip = landmarks[LEFT_HIP]

            right_hip = landmarks[RIGHT_HIP]

            left_knee = landmarks[LEFT_KNEE]

            right_knee = landmarks[RIGHT_KNEE]

            # -------------------------------------------------
            # Average shoulder position
            # -------------------------------------------------

            shoulder_x = (
                left_shoulder.x +
                right_shoulder.x
            ) / 2

            shoulder_y = (
                left_shoulder.y +
                right_shoulder.y
            ) / 2

            # -------------------------------------------------
            # Average hip position
            # -------------------------------------------------

            hip_x = (
                left_hip.x +
                right_hip.x
            ) / 2

            hip_y = (
                left_hip.y +
                right_hip.y
            ) / 2

            # -------------------------------------------------
            # Body width
            # -------------------------------------------------

            shoulder_width = self.distance(
                left_shoulder,
                right_shoulder
            )

            # -------------------------------------------------
            # Body height approximation
            # -------------------------------------------------

            body_height = abs(
                hip_y - shoulder_y
            )

            # -------------------------------------------------
            # Calculate body angle
            # -------------------------------------------------

            dx = hip_x - shoulder_x

            dy = hip_y - shoulder_y

            angle = abs(
                math.degrees(
                    math.atan2(
                        dy,
                        dx
                    )
                )
            )

            # Normalize angle

            if angle > 90:

                angle = 180 - angle

            # -------------------------------------------------
            # FALL DETECTION RULES
            # -------------------------------------------------

            horizontal_body = (
                body_height <
                0.55 *
                max(
                    shoulder_width,
                    0.01
                )
            )

            low_body = (
                shoulder_y > 0.60
            )

            body_tilted = (
                angle < 45
            )

            # Combine conditions

            possible_fall = (
                horizontal_body
                and
                low_body
                and
                body_tilted
            )

            # -------------------------------------------------
            # Fall confirmation
            # -------------------------------------------------

            if possible_fall:

                if self.fall_start_time is None:

                    self.fall_start_time = time.time()

                elapsed = (
                    time.time()
                    -
                    self.fall_start_time
                )

                if elapsed >= self.FALL_CONFIRM_TIME:

                    fall = True

                    confidence = min(
                        99,
                        int(
                            75 +
                            elapsed * 10
                        )
                    )

                    movement = "Fall Detected"

                else:

                    movement = "Possible Fall"

                    confidence = 65

            else:

                self.fall_start_time = None

                movement = "Normal"

                confidence = 95

            # -------------------------------------------------
            # Draw pose skeleton
            # -------------------------------------------------

            self.draw_pose(
                frame,
                landmarks,
                width,
                height
            )

            # -------------------------------------------------
            # Draw status
            # -------------------------------------------------

            if fall:

                cv2.rectangle(
                    frame,
                    (0, 0),
                    (width, 80),
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "FALL DETECTED!",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.3,
                    (255, 255, 255),
                    3
                )

            elif movement == "Possible Fall":

                cv2.rectangle(
                    frame,
                    (0, 0),
                    (width, 65),
                    (0, 165, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "POSSIBLE FALL",
                    (20, 43),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                    2
                )

            else:

                cv2.rectangle(
                    frame,
                    (0, 0),
                    (width, 65),
                    (0, 120, 0),
                    -1
                )

                cv2.putText(
                    frame,
                    "NORMAL",
                    (20, 43),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                    2
                )

        else:

            self.fall_start_time = None

            movement = "No Person"

            confidence = 0

            cv2.putText(
                frame,
                "NO PERSON DETECTED",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

        # -------------------------------------------------
        # Save current state
        # -------------------------------------------------

        self.fall_detected = fall

        self.confidence = confidence

        self.movement = movement

        return frame, {

            "fall_detected": fall,

            "confidence": confidence,

            "movement": movement
        }

    # -----------------------------------------------------
    # Draw pose
    # -----------------------------------------------------

    def draw_pose(
        self,
        frame,
        landmarks,
        width,
        height
    ):

        # MediaPipe pose connections

        connections = [

            (11, 12),

            (11, 13),
            (13, 15),

            (12, 14),
            (14, 16),

            (11, 23),
            (12, 24),

            (23, 24),

            (23, 25),
            (25, 27),

            (24, 26),
            (26, 28),

            (27, 29),
            (28, 30),

            (29, 31),
            (30, 32)
        ]

        # Draw connections

        for start, end in connections:

            if (
                start >= len(landmarks)
                or
                end >= len(landmarks)
            ):
                continue

            p1 = landmarks[start]

            p2 = landmarks[end]

            x1 = int(p1.x * width)

            y1 = int(p1.y * height)

            x2 = int(p2.x * width)

            y2 = int(p2.y * height)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

        # Draw landmarks

        for landmark in landmarks:

            x = int(
                landmark.x *
                width
            )

            y = int(
                landmark.y *
                height
            )

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 0),
                -1
            )

    # -----------------------------------------------------
    # Close detector
    # -----------------------------------------------------

    def close(self):

        self.detector.close()