import cv2
import mediapipe as mp
import numpy as np
import time
from playsound import playsound

# EAR calculation function
def eye_aspect_ratio(landmarks, eye_indices):
    p1 = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    p2 = np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y])
    p3 = np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])
    p4 = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])
    p5 = np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y])
    p6 = np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y])

    A = np.linalg.norm(p2 - p6)
    B = np.linalg.norm(p3 - p5)
    C = np.linalg.norm(p1 - p4)

    ear = (A + B) / (2.0 * C)
    return ear

# Mediapipe face mesh
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.24
CLOSED_FRAMES = 0
DROWSY_LIMIT = 15  # how many frames eyes need to be closed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            # Mediapipe eye landmark indices
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]

            landmarks = face_landmarks.landmark

            left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
            right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
            ear = (left_ear + right_ear) / 2

            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # drowsy logic
            if ear < EAR_THRESHOLD:
                CLOSED_FRAMES += 1
            else:
                CLOSED_FRAMES = 0

            if CLOSED_FRAMES >= DROWSY_LIMIT:
                cv2.putText(frame, "DROWSINESS ALERT!", (100, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

                try:
                    playsound("alarm.wav")
                except:
                    pass

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        break

cap.release()
cv2.destroyAllWindows()
