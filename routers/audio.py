from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response, StreamingResponse
from botocore.exceptions import NoCredentialsError
from ..utils.read_config import read_config
import boto3

setting = read_config('s3-aws')
prefix_path = setting['multimedia_path']

router = APIRouter(
    prefix="/audio",
    tags=["audio"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_audio", description='Get audio from cloud (S3)')
async def get_audio(id: str = "Aimer-1.mp3"):
    """
        return audio bytes by chunk using StreamingResponse
        id: id of mp3 file
    """
    CHUNK_SIZE = 1024*1024
    bucket_name = setting['bucket_name']
    object_key = prefix_path + id
    
    try:
        s3 = boto3.client('s3', aws_access_key_id = setting['aws_access_key_id'], 
                          aws_secret_access_key = setting['aws_secret_access_key'], region_name =setting['region_name'])
        
        # get info about object
        response_head = s3.head_object(Bucket=bucket_name, Key=object_key)
        object_size = response_head['ContentLength']    
        num_chunks = (object_size + CHUNK_SIZE - 1) // CHUNK_SIZE

        # generate object by chunk to send
        def generate_audio_by_chunk():
            for chunk_number in range(num_chunks):
                start_byte = chunk_number * CHUNK_SIZE
                end_byte = min((chunk_number + 1) * CHUNK_SIZE - 1, object_size - 1)
                range_header = f'bytes={start_byte}-{end_byte}'

                response = s3.get_object(Bucket=bucket_name, Key=object_key, Range = range_header)
                yield response['Body'].read()
                
        headers = {
            'Content-Range': f'bytes {0}-{object_size}/{object_size}',
            'Accept-Ranges': 'bytes'
        }

        return StreamingResponse(generate_audio_by_chunk(), status_code=206, media_type='audio/mp3', headers=headers)
    
    except NoCredentialsError:
        return JSONResponse({'error': 'Credentials not available or not valid. Please check your AWS credentials.'}), 500
    except Exception as e:
        return JSONResponse({'error': str(e)}), 500

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
