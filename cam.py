import picamera
import RPi.GPIO as GPIO
import time
import boto3
from subprocess import call

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #PIR
boto3.set_stream_logger('')
s3 = boto3.resource('s3')

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(23):
            millis = int(round(time.time() * 1000))
            print("Motion detected, taking photo...")
	    picname = 'capture-{}-pic.jpg'.format(millis) 
            videoname = 'capture-{}-video.h264'.format(millis)
            camera.resolution = (1920, 1080)
            camera.capture(picname)
            print("Done taking photo, making video")
	    camera.resolution = (1280, 720)
            camera.start_recording(videoname)
	    camera.wait_recording(45)
            while GPIO.input(23):
		camera.wait_recording(10)
                print("There still is motion. Extending...")

            camera.stop_recording()
	    print("Done recording")
            try:
	           print("Uploading video to S3...")
		   mp4videoname = 'capture-{}-video.mp4'.format(millis)
 	   	   call(["ffmpeg","-framerate","24","-i",videoname,"-c","copy",mp4videoname])
		   call(["rm",videoname])
		   data = open(mp4videoname, 'rb')
		   s3.Bucket('zuzuthecat').put_object(Key=mp4videoname, Body=data)
		   print("Done")
	 	   print("Uploading photo to S3...")
	           data = open(picname, 'rb')
            	   s3.Bucket('zuzuthecat').put_object(Key=picname, Body=data)
            	   print("Done with video. Resuming motion detection...")

            except:
		   print("Failed to upload videos. Check wifi!")

	time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()
