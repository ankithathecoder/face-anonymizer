import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output/blurred_webcam.avi', fourcc, 20.0, (640, 480))

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        if results.detections:
            h, w, _ = frame.shape

            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                face = frame[y:y+height, x:x+width]

                if face.size > 0:
                    blurred = cv2.GaussianBlur(face, (99, 99), 30)
                    frame[y:y+height, x:x+width] = blurred

        cv2.imshow("Face Blur Webcam", frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == 27:   # press ESC to exit
            break

out.write(frame)
cap.release()
cv2.destroyAllWindows()