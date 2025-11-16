import cv2
import mediapipe as mp
import math
import winsound

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
# Winsound Alarm Function
# ===========================
def play_alarm():
    winsound.Beep(2000, 800)  # frequency 2000 Hz, duration 800 ms


# ===========================
# Setup
# ===========================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)

cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.21      # EAR value below which eyes are considered closed
CONSEC_FRAMES = 20        # Number of frames to confirm drowsiness

counter = 0

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

        # Drowsiness logic
        if avg_EAR < EAR_THRESHOLD:
            counter += 1
        else:
            counter = 0

        if counter > CONSEC_FRAMES:
            cv2.putText(frame, "DROWSINESS DETECTED!", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

            play_alarm()  # Alarm beep

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to close
        break

cap.release()
cv2.destroyAllWindows()
