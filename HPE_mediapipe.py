import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

# Initiating holistic model

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recoloring Feed
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # To make Detections
        
        results = holistic.process(image)

        # Recoloring image back to BGR for rendering
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Face landmarks
        
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION ,landmark_drawing_spec=None,connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,landmark_drawing_spec=None,connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())

        # Right hand with specific colour
        
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec((0, 0, 255), 6, 3),
                    mp_drawing.DrawingSpec((0, 255, 0), 4, 2)
                    )


        # Left Hand
        
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Pose Detections
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        cv2.namedWindow("Resize", cv2.WINDOW_NORMAL)

        # Using resizeWindow()
        
        cv2.resizeWindow("Resize", 1000, 700)

        # Displaying the image
        
        cv2.imshow("Resize", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
