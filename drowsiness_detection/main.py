import cv2
import mediapipe as mp
import math
import os
import subprocess
import time

# ===========================
# EAR (Eye Aspect Ratio)
# ===========================
def calculate_EAR(landmarks, eye_indices):
    p1 = landmarks[eye_indices[0]]
    p2 = landmarks[eye_indices[1]]
    p3 = landmarks[eye_indices[2]]
    p4 = landmarks[eye_indices[3]]
    p5 = landmarks[eye_indices[4]]
    p6 = landmarks[eye_indices[5]]

    # Vertical distances
    dist1 = math.dist((p2.x, p2.y), (p6.x, p6.y))
    dist2 = math.dist((p3.x, p3.y), (p5.x, p5.y))

    # Horizontal distance
    dist3 = math.dist((p1.x, p1.y), (p4.x, p4.y))

    EAR = (dist1 + dist2) / (2.0 * dist3)
    return EAR


# ===========================
# Alarm Management
# ===========================
alarm_process = None
last_alarm_time = 0
ALARM_COOLDOWN = 3.0  # Cooldown between alarms in seconds

def play_alarm():
    global alarm_process, last_alarm_time
    current_time = time.time()

    # Only play alarm if cooldown has passed
    if current_time - last_alarm_time > ALARM_COOLDOWN:
        if alarm_process is not None and alarm_process.poll() is None:
            return  # Already playing

        script_dir = os.path.dirname(os.path.abspath(__file__))
        alarm_path = os.path.join(script_dir, "alarm.wav")

        try:
            # Use subprocess to manage the sound process so we can terminate it
            alarm_process = subprocess.Popen(["afplay", alarm_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            last_alarm_time = current_time
        except Exception as e:
            print(f"Error playing alarm: {e}")

def stop_alarm():
    global alarm_process
    if alarm_process is not None and alarm_process.poll() is None:
        try:
            alarm_process.terminate()
            alarm_process.wait(timeout=0.2)
        except Exception:
            try:
                alarm_process.kill()
            except Exception:
                pass


# ===========================
# Setup
# ===========================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)

cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.21              # EAR value below which eyes are considered closed
DROWSINESS_TIME_LIMIT = 15.0      # Detect drowsiness after 15 seconds of eye closure

closed_start_time = None

# Eye landmark indices (Mediapipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# ===========================
# Main Loop
# ===========================
while True:
    success, frame = cap.read()
    if not success:
        break

    # Resize frame to standard size so it is not too large and processing is faster
    frame = cv2.resize(frame, (640, 480))

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_EAR = calculate_EAR(landmarks, LEFT_EYE)
        right_EAR = calculate_EAR(landmarks, RIGHT_EYE)

        avg_EAR = (left_EAR + right_EAR) / 2

        # Display EAR on screen
        cv2.putText(frame, f"EAR: {avg_EAR:.2f}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Drowsiness logic based on duration in seconds
        if avg_EAR < EAR_THRESHOLD:
            if closed_start_time is None:
                closed_start_time = time.time()
            
            closed_duration = time.time() - closed_start_time
            
            # Show closed duration countdown/timer on screen
            cv2.putText(frame, f"Closed for: {closed_duration:.1f}s", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            if closed_duration >= DROWSINESS_TIME_LIMIT:
                cv2.putText(frame, "DROWSINESS DETECTED!", (30, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                play_alarm()
        else:
            closed_start_time = None
            stop_alarm()  # Stop the alarm immediately if the eyes are open

    cv2.imshow("Drowsiness Detection", frame)

    # Allow closing by pressing ESC, 'q', or clicking the window close button
    if cv2.getWindowProperty("Drowsiness Detection", cv2.WND_PROP_VISIBLE) < 1:
        break

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):  # ESC or 'q' to close
        break

cap.release()
cv2.destroyAllWindows()
stop_alarm()
