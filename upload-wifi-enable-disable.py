from os import listdir
from os.path import isfile, join
import boto3
import sys
from subprocess import call
from time import sleep

boto3.set_stream_logger('')
s3 = boto3.resource('s3')
call(['/usr/sbin/rfkill','unblock','wifi'])
sleep(30)
mypath = sys.argv[1]
storagepath = sys.argv[2]
files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and (f.endswith('.mp4') or f.endswith('.jpg'))]
for f in files:
    fullpath = join(mypath,f)
    fullstoragepath = join(storagepath,f)
    data = open(fullpath, 'rb')
    try:
    	s3.Bucket('zuzuthecat').put_object(Key=f, Body=data)

    except:
	print('Failed to upload. Check wifi.')

    call(['mv',fullpath,storagepath])
    print('Uploaded and moved '+fullpath+' to '+fullstoragepath)

call(['/usr/sbin/rfkill','block','wifi'])
