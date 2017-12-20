import picamera
import RPi.GPIO as GPIO
import time
import boto3
from subprocess import call
from os.path import join
import sys
import os

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #PIR
boto3.set_stream_logger('')
s3 = boto3.resource('s3')

mediapath = sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.realpath(__file__))

print('Starting camera, media path is {}'.format(mediapath))

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(23):
            millis = int(round(time.time() * 1000))
            print("Motion detected, taking photo...")
	    picname = 'capture-{}-pic.jpg'.format(millis) 
            videoname = 'capture-{}-video.h264'.format(millis)
            fullpicname = join(mediapath,picname)
	    fullvideoname = join(mediapath,videoname)
            camera.resolution = (1920, 1080)
            camera.capture(fullpicname)
            print("Done taking photo, making video")
	    camera.resolution = (1280, 720)
            camera.start_recording(fullvideoname)
	    camera.wait_recording(45)
            while GPIO.input(23):
		camera.wait_recording(10)
                print("There still is motion. Extending...")

            camera.stop_recording()
	    print("Done recording")
            try:
	           print("Converting h264 to mp4...")
		   mp4videoname = 'capture-{}-video.mp4'.format(millis)
 	   	   call(["ffmpeg","-framerate","24","-i",fullvideoname,"-c","copy",join(mediapath,mp4videoname)])
		   call(["rm",fullvideoname])
		   print("Done. Resuming motion detection.")

            except:
		   print("Failed to upload videos. Check wifi!")

	time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()
