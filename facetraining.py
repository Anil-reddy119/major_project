#import tensorflow as tf


#from keras_vggface.vggface import VGGFace
#from keras_vggface.utils import preprocess_input

#import matplotlib
#import matplotlib.pyplot as plt
#from PIL import Image
#from numpy import asarray
#from scipy.spatial.distance import cosine
#from mtcnn import MTCNN
#from werkzeug.datastructures import FileStorage

import face_recognition

import cv2
#import matplotlib.pyplot as plt
import os

#detector = MTCNN()
#model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')


# -----------------------------------new faces
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

def get_faceasarray(frame, results):
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    face = frame[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize((224, 224))
    face_array = asarray(image)
    return face_array



def detect_face(frame):
    """
    will return true if face detected is true and sends cropped image of face
    """

    pil_img = plt.imread(frame) if isinstance(frame, FileStorage) else  frame    
    results = detector.detect_faces(pil_img)

    """if len(results)>1:
        return False, pil_img, None"""
    if len(results)==0:
        return False, pil_img, None
    return True, pil_img, results


#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"
# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
try:
    data = pickle.loads(open(encodingsP, "rb").read())
except e:
    print("data not trained , please run the face_train file first to train the project")

def detect_face_new(frame):
    # Detect the fce boxes
    boxes = face_recognition.face_locations(frame)
    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(frame, boxes)
    return encodings, boxes


def _get_embeddings(face_frame, known_img):
    detect, frame , det_res = detect_face(known_img)
    if not detect:
        return "please check the known images once "
    im1, im2 = face_frame, get_faceasarray(  frame, det_res)

    
    faces = [im1, im2]
    samples = asarray(faces, 'float32')
    samples = preprocess_input(samples, version=2)
    return model.predict(samples)

def _match_embeddings(known_embedding, candidate_embedding, thresh=0.5):
    # calculate distance between embeddings
    score = cosine(known_embedding, candidate_embedding) 
    if score <= thresh:
        return True
    else:
        return False

def match_face(frame, det_results) :
    """
    will return true and name of persion of facematch is true else false
    """
    face_frame = get_faceasarray(frame, det_results)
    faces_path = "known_faces/"
    face_files = os.listdir(faces_path)

    for face in face_files:
        known_face = cv2.imread(faces_path + face)
        embeddings = _get_embeddings(face_frame, known_face)
        if _match_embeddings(embeddings[0], embeddings[1]):
            return face
        
    return False

def match_face_new(frame_face_en,  frame, boxes):
    names= []
    #Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    
    for encoding in frame_face_en:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown" #if face is not recognized, then print Unknown

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

            #If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
                print(currentname)

        # update the list of names
        names.append(name)
    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)
    return frame, names

if _name_ == "_main_":
    im1 = cv2.imread("im1.jpeg")
    
    det, frame, res = detect_face(im1)
    if not det:
        print("not detected a face")
    else:
        print(match_face(frame, res))