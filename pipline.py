import cv2
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time

from face import detect_face, detect_face_new, match_face, match_face_new
from telegram import send_message, send_image, get_message
from door import open_box, open_door, speakout



def run_survillance_1():
    cap = cv2.VideoCapture(0)
    print("service started")
    while True:
        ret , img = cap.read()
        #print(img)
        #input("cp 1")
        #cv2.imshow("display", img)

        face_detected, frame , results = detect_face(img)
        if not face_detected:
            continue
        else:
            speakout("please stand by while scanning")
            print("face detected , matching")
            face_matched = match_face(frame, results)
            # if known person is infront of door
            if face_matched:
                
                #send message that opening door and open a door
                send_message("looks like "+ face_matched.split(".")[0] + "is infront of house , opening the door")
                send_image(frame)
                speakout("opening door please stand by")
                open_door()
            
            # unknown person is infront of door
            else :

                # send message for asking confirmation
                send_message("unknown persion is infront of door, send reply 'Y' to open door, 'D' for delivery and 'N' to not open door")
                send_image(frame)

                # wait for message and check for valid reply
                reply = get_message()
                while reply not in ('Y', 'D', 'N'):
                    send_message("invalid reply, please choose -> 'Y' to open door, 'D' for delivery and 'N' to not open door")
                    reply = get_message()
                
                if reply == 'Y':
                    speakout("opening door please stand by")
                    open_door()
                elif reply == 'D':
                    speakout("please put the delivery in delivery box")
                    open_box()
                elif reply == 'N':
                    speakout("you are not authorized to enter house")



def run_survillance_2():
    vs = VideoStream(framerate=30).start()
    time.sleep(2.0)

    # start the FPS counter
    fps = FPS().start()

    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        faces_encs, boxes = detect_face_new(frame)
        frame, names = match_face_new(faces_encs, frame, boxes)
        cv2.imshow("Facial Recognition is Running", frame)
        
        # check if there is known person in camera
        kname = None
        for name in names:
            kname = name
            if name!="Unknown":
                #kname = name
                break
        print("the kname is : ", kname)
        if kname:
            if kname != "Unknown":
                send_message("looks like "+ kname + "is infront of house , opening the door")
                send_image(frame)
                speakout("opening door please stand by")
                open_door()
        
            else :

                # send message for asking confirmation
                send_message("unknown persion is infront of door, send reply 'Y' to open door, 'D' for delivery and 'N' to not open door")
                send_image(frame)
                speakout("please stand by, while authenticating")
                # wait for message and check for valid reply
                reply = get_message()
                while reply not in ('Y', 'D', 'N'):
                    send_message("invalid reply, please choose -> 'Y' to open door, 'D' for delivery and 'N' to not open door")
                    reply = get_message()
                    
                if reply == 'Y':
                    speakout("opening door please stand by")
                    open_door()
                elif reply == 'D':
                    speakout("please put the delivery in delivery box")
                    open_box()
                elif reply == 'N':
                    speakout("you are not authorized to enter house")

        
        key = cv2.waitKey(1) & 0xFF

        # quit when 'q' key is pressed
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()