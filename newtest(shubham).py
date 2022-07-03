import collections
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import playsound
from threading import Thread
import pymongo
from pymongo import MongoClient
from datetime import date, timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt

#------------------------------------------MongoDB Part----------------------------------------------------------------------------------------------------
cluster = MongoClient("mongodb+srv://Shub:ydaFUqp90RymHLw9@cluster0.ceaym1j.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
datestr= str(date.today())
countinstance = collection.count_documents({})

#collection.insert_one({"_id": 0, "date":datestr ,"eyes": 0, "yawn": 0,"long_alarm": 0})

#check current date with database
def checkDate():
	bolleanval = False
	NowDateDict={"date":datestr}
	filterDate = collection.find({ "_id": countinstance - 1},{"date": 1, "_id": 0})
	for c in filterDate:
		if c == NowDateDict:
			bolleanval = True
			return bolleanval	
	return bolleanval

#Function That Create new post in Database
def newEntry():
	collection.insert_one({"_id": countinstance, "date":datestr ,"eyes": 0, "yawn": 0,"long_alarm": 0})

#update the values in database
def updateData(incValue):
	if checkDate():
		if(incValue=="eyes" and incValue=="yawn"):
			collection.update_one({"_id": countinstance - 1},{"$inc": {"eyes": 1,"yawn": 1}})
		if(incValue=="eyes"):
			collection.update_one({"_id": countinstance - 1},{"$inc": {"eyes": 1}})
		if(incValue=="yawn"):
			collection.update_one({"_id": countinstance - 1},{"$inc": {"yawn": 1}})
	else:
		newEntry()
	return 0

#for retriving data and for visualization
def fetchData(dataVar):
	#no. of post is countinstance variable
	dataDictVar = {}
	filterData = collection.find({ "_id": 0},{"eyes": 1, "_id": 0})
	if(dataVar=="eyes"):
		for i in range(0,countinstance):
			filterData = collection.find({ "_id": i},{"eyes": 1, "_id": 0})
			for j in filterData:
				dataDictVar = j
	if(dataVar=="yawn"):
		for i in range(0,countinstance):
			filterData = collection.find({ "_id": i},{"yawn": 1, "_id": 0})
			for j in filterData:
				dataDictVar = j
	if(dataVar=="date"):
		for i in range(0,countinstance):
			filterData = collection.find({ "_id": i},{"date": 1, "_id": 0})
			for j in filterData:
				dataDictVar = j
	print(dataDictVar)
	return 0

#fetchData("eyes")

#for Visualization
def dataViz():
	dataDictVar = {}
	filterData = collection.find({})
	for i in range(0,countinstance):
		filterData = collection.find({})
		for j in filterData:
			dataDictVar = j
	pd.DataFrame(dataDictVar, index=[0]).plot.bar()
	plt.show()

dataViz()

#------------------------------------------Driver Code----------------------------------------------------------------------------------------------------
#calculating eye aspect ratio
def eye_aspect_ratio(eye):
	# compute the euclidean distances between the vertical
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	return ear

#calculating mouth aspect ratio
def mouth_aspect_ratio(mou):
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

def sound_alarm(alarm_file):
    # Function specifically used for Playing the sound
    playsound.playsound(alarm_file)

camera = cv2.VideoCapture(0)
predictor_path = 'C:/Users/shubh/OneDrive/Desktop/Codes/Mini-Project-sem-2-main/Mini-Project-sem-2-main/shape_predictor_68_face_landmarks.dat'

# define constants for aspect ratios(Room for improvement in these values)
EYE_AR_THRESH = 0.30
EYE_AR_CONSEC_FRAMES = 48
MOU_AR_THRESH = 0.78
ALARM_ON=False

COUNTER = 0
yawnStatus = False
yawns = 0
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# grab the indexes of the facial landmarks for the left and right eye
# also for the mouth
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]


# loop over captuing video
while True:
	# grab the frame from the camera, resize
	# it, and convert it to grayscale
	# channels)
	ret, frame = camera.read()
	frame = imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	prev_yawn_status = yawnStatus
	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		mouth = shape[mStart:mEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		mouEAR = mouth_aspect_ratio(mouth)
		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		mouthHull = cv2.convexHull(mouth)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 255), 1)
		cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			COUNTER += 1
			cv2.putText(frame, "Eyes Closed ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			# if the eyes were closed for a sufficient number of
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				# draw an alarm on the frame
				cv2.putText(frame, "DROWSINESS ALERT!", (10, 50),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

				if not ALARM_ON:
					updateData("eyes")
					ALARM_ON = True
					t = Thread(target=sound_alarm,
							   args=('C:/Users/shubh/OneDrive/Desktop/Codes/Mini-Project-sem-2-main/Mini-Project-sem-2-main/alarm.wav',))
					t.deamon = True
					t.start()
				# count1+=1


		# otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
			COUNTER = 0
			cv2.putText(frame, "Eyes Open ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
			ALARM_ON = False

		cv2.putText(frame, "EAR: {:.2f}".format(ear), (480, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		# yawning detections

		if mouEAR > MOU_AR_THRESH:
			cv2.putText(frame, "Yawning ", (10, 70),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			yawnStatus = True
			output_text = "Yawn Count: " + str(yawns + 1)
			cv2.putText(frame, output_text, (10,100),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0),2)
		else:
			yawnStatus = False

		if prev_yawn_status == True and yawnStatus == False:
			yawns+=1

		if yawns >= 15:
			if not ALARM_ON:
				updateData("yawn")
				ALARM_ON = True
				t = Thread(target=sound_alarm,
						   args=('C:/Users/shubh/OneDrive/Desktop/Codes/Mini-Project-sem-2-main/Mini-Project-sem-2-main/alarm.wav',))
				t.deamon = True
				t.start()
			cv2.putText(frame, "Drowsy", (800, 20),
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			yawns = 0
			break

		cv2.putText(frame, "MAR: {:.2f}".format(mouEAR), (480, 60),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
camera.release()
