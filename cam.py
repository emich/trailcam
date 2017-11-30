import picamera
import RPi.GPIO as GPIO
import time

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #PIR

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(23):
            millis = int(round(time.time() * 1000))
            print("Motion detected, taking photo...")
	    camera.resolution = (1920, 1080)
            camera.capture('capture-{}-pic.jpg'.format(millis))
            print("Done taking photo, making video")
	    camera.resolution = (1280, 720)
            camera.start_recording('capture-{}-video.h264'.format(millis))
            while GPIO.input(23): #do not stop recording while stuff is moving
		camera.wait_recording(15)
                print("Extending...")

            camera.stop_recording()
	    print("Done with video. Resuming motion detection...")
            time.sleep(5) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()
