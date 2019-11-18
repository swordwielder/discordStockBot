import boto3
from dotenv import load_dotenv
import os


load_dotenv()


def s3upload(imagename):
    client = boto3.client('s3', region_name='us-west-2')
    client.upload_file(f'{os.getcwd()}/content_detection/imagebank/Analysedimage.jpg', 'discordimage', f'{imagename}.jpg')