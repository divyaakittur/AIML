import os
from ultralytics import YOLO
import cv2
import datetime
import pywhatkit as pwt

IMAGE_DIR = os.path.join('.', 'videos')
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')

threshold = 0.5
class_name_dict = {0: 'capsules', 1: 'tablets'}  # Add the additional class and its corresponding class ID

model = YOLO(model_path)

# Get a list of all image files in the directory
image_files = [file for file in os.listdir(IMAGE_DIR) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

for image_file in image_files:
    image_path = os.path.join(IMAGE_DIR, image_file)
    frame = cv2.imread(image_path)

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, class_name_dict[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Create a named window and move it to a new position on the screen
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Image", 500, 200)

    cv2.imshow("Image", frame)
    cv2.waitKey(0)



year = datetime.datetime.now().strftime("%Y")
month = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
time = datetime.datetime.now().strftime("%H:%M:%S")
name = day + "-" + month + "-" + year
img_path= "ImagefromImage//"+name+'.jpg'
cv2.imwrite(img_path, frame)
cv2.imshow('Alert ! Tablet detected ! Please take action', frame)

pwt.sendwhats_image('+919900980055', img_path, "Tablet detected "+name, 15, False, 3)

cv2.destroyAllWindows()