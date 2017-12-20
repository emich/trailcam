from os import listdir
from os.path import isfile, join
import boto3
import sys
from subprocess import call
boto3.set_stream_logger('')
s3 = boto3.resource('s3')
mypath = sys.argv[1]
storagepath = sys.argv[2]
files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and (f.endswith('.mp4') or f.endswith('.jpg'))]
for f in files:
    fullpath = join(mypath,f)
    fullstoragepath = join(storagepath,f)
    data = open(fullpath, 'rb')
    s3.Bucket('zuzuthecat').put_object(Key=f, Body=data)
    call(['mv',fullpath,storagepath])
    print('Uploaded and moved '+fullpath+' to '+fullstoragepath)
