# AI-Based Elderly Fall Detection System

## 📌 Project Overview

The **AI-Based Elderly Fall Detection System** is an intelligent safety system designed to automatically detect when an elderly person falls using a camera and Artificial Intelligence.

The system continuously monitors video captured by a camera, analyzes the person's body posture and movement, and identifies abnormal movements that may indicate a fall. When a fall is detected and confirmed, the system can trigger an **emergency alarm and SMS alert to a registered family member or caregiver**.

The main objective is to reduce the response time during elderly emergencies and provide continuous monitoring without requiring the person to manually press an emergency button.

---

## 🎯 Objectives

* Automatically detect elderly falls using AI.
* Monitor a person through a camera in real time.
* Analyze body posture and movement.
* Reduce false fall detections through fall confirmation.
* Generate an emergency alert when a fall is confirmed.
* Send an SMS notification to a registered family member/caregiver.
* Provide a simple web dashboard for monitoring.
* Store elderly-person and emergency-contact information.

---

## 🏗️ System Architecture

```text
                ┌──────────────────────┐
                │      Camera Input    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Video Preprocessing  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Person Detection     │
                │ & Tracking           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Human Pose           │
                │ Estimation           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Feature Extraction   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ AI Fall Detection    │
                │ Model                │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Fall Confirmation    │
                └──────────┬───────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          ┌──────────────┐     ┌──────────────┐
          │ Alarm        │     │ SMS Alert    │
          └──────────────┘     └──────┬───────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │ Family /     │
                              │ Caregiver    │
                              └──────────────┘
```

---

## 🧠 AI-Based Detection

The system uses human body movement and posture information to determine whether a person has fallen.

Important features can include:

* Body orientation
* Body height
* Shoulder position
* Hip position
* Knee position
* Joint relationships
* Vertical displacement
* Movement velocity
* Body posture
* Temporal movement patterns

Possible AI approaches include:

* LSTM
* GRU
* 1D-CNN
* CNN-LSTM
* Machine-learning classifiers

For a real-time prototype, pose estimation can be combined with temporal movement analysis to identify a potential fall.

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Web Camera API

### Backend

* Python
* Flask
* OpenCV
* MediaPipe / pose-estimation framework

### AI / Machine Learning

* Human pose estimation
* Feature extraction
* Fall classification
* Temporal movement analysis

### Alert System

* SMS API
* Emergency alarm
* Registered family/caregiver contact

---

## 📂 Project Structure

```text
AI-Elderly-Care/
│
├── backend/
│   ├── app.py
│   ├── fall_detection.py
│   ├── alert.py
│   ├── requirements.txt
│   └── .env
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│
├── alarm.mp3
│
└── README.md
```

---

## 📄 File Description

| File                | Purpose                                  |
| ------------------- | ---------------------------------------- |
| `app.py`            | Flask backend and API/server             |
| `fall_detection.py` | Fall detection and pose-processing logic |
| `alert.py`          | Emergency SMS/alert functionality        |
| `index.html`        | Main web interface                       |
| `style.css`         | Dashboard styling                        |
| `script.js`         | Frontend functionality                   |
| `requirements.txt`  | Python dependencies                      |
| `.env`              | API credentials and configuration        |
| `alarm.mp3`         | Emergency alarm sound                    |
| `uploads/`          | Stores uploaded files if required        |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Elderly-Care.git
cd AI-Elderly-Care
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements file yet, typical dependencies may include:

```bash
pip install flask opencv-python numpy python-dotenv
```

Install the pose-estimation package required by the implementation you are using.

---

## 🔐 Environment Variables

Create a `.env` file in the backend directory.

Example:

```env
SMS_API_KEY=your_api_key
SMS_API_SECRET=your_api_secret
FAMILY_PHONE_NUMBER=your_registered_number
```

**Do not upload your real API keys or secrets to GitHub.**

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

Navigate to the backend directory:

```bash
cd backend
```

Run the Flask application:

```bash
python app.py
```

If the server starts successfully, you should see something similar to:

```text
Running on http://127.0.0.1:5000
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

## 📷 Camera Monitoring

The system uses a camera to capture the monitored area.

The video is processed to:

1. Capture frames.
2. Detect the person.
3. Identify body landmarks.
4. Extract movement/posture features.
5. Analyze movement over time.
6. Determine whether a fall has occurred.
7. Confirm the fall.
8. Trigger an emergency response.

---

## 🚨 Emergency Alert Process

When the AI identifies a possible fall:

```text
Possible Fall
     ↓
Fall Confirmation
     ↓
Fall Confirmed
     ↓
Emergency Alarm
     ↓
SMS Alert
     ↓
Family / Caregiver Notification
```

A sample SMS can be:

```text
EMERGENCY ALERT:
A possible fall has been detected for the monitored elderly person.
Please check immediately.
```

---

## 👨‍👩‍👧 Person and Family Details

The dashboard can contain information such as:

### Elderly Person

* Name
* Age
* Phone number
* Address
* Emergency information

### Family / Caregiver

* Name
* Relationship
* Phone number

The registered family contact is used for emergency notifications.

---

## 🌐 Web Dashboard

The web interface can provide:

* Live camera feed
* Fall detection status
* Person details
* Family/caregiver details
* Emergency status
* Alert history
* Alarm controls
* System status

Example:

```text
┌────────────────────────────────────────┐
│       AI ELDERLY FALL DETECTION        │
├────────────────────────────────────────┤
│                                        │
│          [ LIVE CAMERA ]               │
│                                        │
├────────────────────────────────────────┤
│ Status: NORMAL                         │
│                                        │
│ Elderly Person: John Doe               │
│ Age: 72                                │
│                                        │
│ Family Contact: XXXXXXXX               │
│                                        │
│ Emergency Alert: OFF                   │
└────────────────────────────────────────┘
```

---

## 📱 Accessing From Another Mobile

If the computer and mobile phone are connected to the **same Wi-Fi network**, the Flask application can be accessed using the computer's local IP address.

For example:

```text
http://192.168.71.104:5000
```

The IP address can be found using:

```powershell
ipconfig
```

The computer firewall must also allow the Flask application/port if another device cannot connect.

For access over the internet, additional secure deployment/network configuration is required.

---

## 🔌 API Endpoints

Example endpoints:

```text
GET  /
GET  /api/status
GET  /video_feed
POST /send-emergency-sms
```

### `/api/status`

Returns the current monitoring status.

Example:

```json
{
    "status": "normal",
    "fall_detected": false,
    "person": "John Doe"
}
```

### `/send-emergency-sms`

Used by the backend to initiate an emergency SMS through the configured SMS service.

---

## 🧪 Testing

The system should be tested using different activities:

* Normal walking
* Sitting
* Standing
* Lying down intentionally
* Bending
* Walking quickly
* Falling forward
* Falling backward
* Falling sideways

Testing should include different lighting conditions, camera angles, distances, clothing, and body positions.

---

## ⚠️ Limitations

* Camera positioning can affect detection accuracy.
* Poor lighting may reduce detection performance.
* Occlusion can hide body landmarks.
* Multiple people may create detection challenges.
* Sudden movements can sometimes be classified incorrectly.
* Internet connectivity may be required for cloud-based SMS services.
* SMS delivery depends on the configured SMS provider and network.
* The prototype should not be considered a replacement for professional medical or emergency monitoring.

---

## 🔒 Privacy and Security

Because the system processes camera footage and personal information:

* Protect stored personal information.
* Never expose API keys in frontend code.
* Use HTTPS when deployed publicly.
* Restrict access to authorized users.
* Avoid unnecessary storage of camera footage.
* Secure emergency contact information.
* Use authentication for production deployments.

---

## 🚀 Future Enhancements

Future versions can include:

* Mobile application
* Cloud monitoring
* Multiple-camera support
* Improved deep-learning models
* Voice emergency assistance
* GPS-based emergency location
* Automatic hospital notification
* WhatsApp or other notification integrations where legally and technically appropriate
* Fall severity estimation
* Multiple elderly-person monitoring
* Automatic incident recording
* Real-time caregiver dashboard
* Wearable-device integration

---

## 📊 Expected Outcome

The proposed system is expected to provide an automated method for detecting elderly falls and notifying caregivers quickly.

The system combines:

**Camera → Computer Vision → Pose Estimation → AI Analysis → Fall Confirmation → Emergency Alert**

This can help reduce the delay between a fall occurring and a caregiver becoming aware of the incident.

---

## 👥 Project Use Case

The system can be useful in:

* Homes
* Elderly-care centers
* Assisted-living facilities
* Hospitals
* Nursing homes
* Rehabilitation centers

---

## 📜 Disclaimer

This project is intended as an **academic/research prototype** for elderly safety monitoring. It should not be relied upon as the sole emergency-response mechanism or as a medical diagnostic system.

---

## 👨‍💻 Author

**AI-Based Elderly Fall Detection System**

Developed as an academic project using Artificial Intelligence, Computer Vision, and Web Technologies.

---

## ⭐ Project Keywords

```text
AI
Artificial Intelligence
Elderly Care
Fall Detection
Computer Vision
Human Pose Estimation
OpenCV
MediaPipe
Python
Flask
Machine Learning
Deep Learning
Real-Time Monitoring
SMS Alert
Emergency Alert
Elderly Safety
```
Deploy link : https://jani1233.github.io/ai-elderly-fall-detection-/
