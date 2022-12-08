import boto3
import uuid
import json


def lambda_handler(event, context):
    
    print(json.dumps(event))
    
    record = event['Records'][0]
    
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    s3Path = "s3://" + s3bucket + "/" + s3object
    jobName = s3object + '-' + str(uuid.uuid4())


    client = boto3.client('transcribe') # transcribe 엔진 불러옴


    response = client.start_transcription_job( #  transcribe 파라미터 설정
        TranscriptionJobName=jobName, # Transcribe 할 객체 
        LanguageCode='ko-KR', # 언어
        MediaFormat='wav', # 타입
        Media={ # 인풋 파일 경로
            'MediaFileUri': s3Path
        },
        OutputBucketName='stt-output', # 출력물 저장될 버킷 이름만 넣기 (전체 경로 X , prefix X. Only 버킷 이름만)
    )


    print(json.dumps(response, default=str))


    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }
