import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

image = cv2.imread("data/test_img.png")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

    results = face_detection.process(image_rgb)

    if results.detections:
        h, w, _ = image.shape

        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)

            face = image[y:y+height, x:x+width]

            blurred = cv2.GaussianBlur(face, (99, 99), 30)

            image[y:y+height, x:x+width] = blurred

cv2.imwrite("output/blurred_test_img.png", image)
cv2.imshow("Blurred_Face", image)
cv2.waitKey(0)
cv2.destroyAllWindows()