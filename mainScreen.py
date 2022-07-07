# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color

#opencv, imutils and other required imports
from turtle import color
from cv2 import rectangle
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import numpy 
import dlib
import cv2
import playsound
from threading import Thread

class MainScreen(Screen): #mainScreen subclass
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs) #init parent
        layout = BoxLayout(orientation='vertical')
        layout.cols =1
        self.img1 = Image(size_hint=(1,.9))
        layout.add_widget(self.img1)
        # Button widget
        button1 = Button(
            text="Exit",
            size_hint=(0.2,0.07),
            pos_hint= {'center_x':0.5,'center_y':0.5},
            background_color = '#1663e0',
            on_press = self.callback
            )
        layout.add_widget(button1)

        predictor_path = 'shape_predictor_68_face_landmarks.dat'
        # define constants for aspect ratios
        self.EYE_AR_THRESH = 0.30
        self.EYE_AR_CONSEC_FRAMES = 48
        self.MOU_AR_THRESH = 0.78
        self.ALARM_ON=False

        self.COUNTER = 0
        self.yawnStatus = False
        self.yawns = 0
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)


        #capture video
        self.camera = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update,1.0/33.0)
        self.add_widget(layout)


    def callback(self, instance):
        self.manager.current = 'welcomeScreen'
        

    #calculating eye aspect ratio
    def eye_aspect_ratio(self,eye):
        # compute the euclidean distances between the vertical
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        return ear

    #calculating mouth aspect ratio
    def mouth_aspect_ratio(self,mou):
        # compute the euclidean distances between the horizontal
        X   = dist.euclidean(mou[0], mou[6])
        # compute the euclidean distances between the vertical
        Y1  = dist.euclidean(mou[2], mou[10])
        Y2  = dist.euclidean(mou[4], mou[8])
        # taking average
        Y   = (Y1+Y2)/2.0
        # compute mouth aspect ratio
        mar = Y/X
        return mar

    def sound_alarm(self,alarm_file):
        # Function specifically used for Playing the sound
        playsound.playsound(alarm_file)

    def update(self,*args):
        #Read frame from openCV
        ret,frame = self.camera.read()
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_yawn_status = self.yawnStatus
        rects = self.detector(gray, 0)
        self.detect(prev_yawn_status,rects,gray)
        #Convert img to texture
        buf = cv2.flip(gray,0).tostring()
        img_texture = Texture.create(size=(gray.shape[1],gray.shape[0]),colorfmt='luminance')
        img_texture.blit_buffer(buf,colorfmt='luminance',bufferfmt='ubyte')
        self.img1.texture = img_texture

    def detect(self,prev_yawn_status,rects,gray):
        
        # grab the indexes of the facial landmarks for the left and right eye
        # also for the mouth
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
        
        # detect faces in the grayscale frame
        
        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            mouth = shape[mStart:mEnd]
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            mouEAR = self.mouth_aspect_ratio(mouth)
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            mouthHull = cv2.convexHull(mouth)
            cv2.drawContours(gray, [leftEyeHull], -1, (0, 255, 255), 1)
            cv2.drawContours(gray, [rightEyeHull], -1, (0, 255, 255), 1)
            cv2.drawContours(gray, [mouthHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < self.EYE_AR_THRESH:
                self.COUNTER += 1
                cv2.putText(gray, "Eyes Closed ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # if the eyes were closed for a sufficient number of
                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                    # draw an alarm on the frame
                    cv2.putText(gray, "DROWSINESS ALERT!", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    if not self.ALARM_ON:
                        self.ALARM_ON = True
                        t = Thread(target=self.sound_alarm,
                                args=('alarm.wav',))
                        t.deamon = True
                        t.start()
                    # count1+=1


            # otherwise, the eye aspect ratio is not below the blink
            # threshold, so reset the counter and alarm
            else:
                self.COUNTER = 0
                cv2.putText(gray, "Eyes Open ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                self.ALARM_ON = False

            cv2.putText(gray, "EAR: {:.2f}".format(ear), (480, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # yawning detections

            if mouEAR > self.MOU_AR_THRESH:
                cv2.putText(gray, "Yawning ", (10, 70),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                self.yawnStatus = True
                output_text = "Yawn Count: " + str(self.yawns + 1)
                cv2.putText(gray, output_text, (10,100),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0),2)
            else:
                self.yawnStatus = False

            if prev_yawn_status == True and self.yawnStatus == False:
                self.yawns+=1

            if self.yawns >= 15:
                if not self.ALARM_ON:
                    self.ALARM_ON = True
                    t = Thread(target=self.sound_alarm,
                            args=('alarm.wav',))
                    t.deamon = True
                    t.start()
                cv2.putText(gray, "Drowsy", (800, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                self.yawns = 0
                break

            cv2.putText(gray, "MAR: {:.2f}".format(mouEAR), (480, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(frame,"Lusip Project @ Swarnim",(370,470),cv2.FONT_HERSHEY_COMPLEX,0.6,(153,51,102),1)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        return gray
