from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from botocore.exceptions import NoCredentialsError
import configparser
import boto3
import os

config_path = (os.getcwd() + '\\BackEnd\\config.ini').replace("\\", "/")
config = configparser.ConfigParser()
config.read(config_path)
setting = config['s3-aws']
prefix_path = setting['multimedia_path']


router = APIRouter(
    prefix="/audio",
    tags=["audio"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_audio", description='Get audio from cloud (S3)')
async def get_audio():
    bucket_name = setting['bucket_name']
    object_key = prefix_path + 'Aimer-1.mp3'

    try:
        s3 = boto3.client('s3', aws_access_key_id = setting['aws_access_key_id'], 
                          aws_secret_access_key = setting['aws_secret_access_key'], region_name =setting['region_name'])
        
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        audio_data = response['Body'].read()

        return 'success'
    
    except NoCredentialsError:
        return JSONResponse({'error': 'Credentials not available or not valid. Please check your AWS credentials.'}), 500
    except Exception as e:
        return JSONResponse({'error': str(e)}), 500

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
