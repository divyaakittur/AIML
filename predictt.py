import os
#from pywin32 import win32clipboard
from ultralytics import YOLO
import cv2
import datetime
import pywhatkit as pwt
import winsound


def play_alert_sound():
    frequency = 2500  # Set the desired frequency in Hz
    duration = 2000  # Set the desired duration in milliseconds
    winsound.Beep(frequency, duration)

IMAGE_DIR = os.path.join('.', 'videos')
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')

threshold = 0.5
class_name_dict = {0: 'capsules', 1: 'tablets'}  # Add the additional class and its corresponding class ID

model = YOLO(model_path)

# Get a list of all image files in the directory
image_files = [file for file in os.listdir(IMAGE_DIR) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

# for image_file in image_files:
def predict_img(image_path):
    # image_path = os.path.join(IMAGE_DIR, image_file)
    frame = cv2.imread(image_path)

    results = model(frame)[0]

    tablet_detected = False  # Flag to check if a tablet is detected in the image
    capsule_detected = False  # Flag to check if a capsule is detected in the image

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        class_name = class_name_dict.get(int(class_id))

        if score > threshold:
            if class_name == 'tablets':
                tablet_detected = True
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, class_name.upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                #cv2.imwrite(img_path, frame)
            elif class_name == 'capsules':
                capsule_detected = True
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                cv2.putText(frame, class_name.upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)

    # Create a named window and move it to a new position on the screen
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    # cv2.moveWindow("Image", 500, 200)
    #
    # cv2.imshow("Image", frame)
    # cv2.waitKey(0)
    img_path = "output.jpeg"
    cv2.imwrite(img_path, frame)
    if tablet_detected:
        # year = datetime.datetime.now().strftime("%Y")
        # month = datetime.datetime.now().strftime("%m")
        # day = datetime.datetime.now().strftime("%d")
        # current_time = datetime.datetime.now().strftime("%H:%M:%S")
        # name = day + "-" + month + "-" + year

        play_alert_sound()  # Play the alert sound before sending the WhatsApp message



        pwt.sendwhats_image('+919900980055', img_path, "Alert!! Tablet detected" , 15, False, 3)
        # Replace '+919900980055' with the recipient's phone number


    #if capsule_detected:
        #cv2.imwrite(img_path, frame)



