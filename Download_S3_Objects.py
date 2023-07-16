import boto3
import os
import logging

from botocore.config import Config
from dotenv import load_dotenv

if __name__ == '__main__':
	load_dotenv()
	logging.basicConfig(
		level = logging.INFO,
		format = '[{levelname}]: {message}',
		style = '{'
	)

	s3_client = boto3.client(
		service_name = 's3',
		region_name = os.getenv(key = 'S3_REGION_NAME'),
		aws_access_key_id = os.getenv(key = 'S3_ACCESS_KEY_ID'),
		aws_secret_access_key = os.getenv(key = 'S3_SECRET_ACCESS_KEY'),
		config = Config(
			signature_version = 'v4',
			retries = {'max_attempts': 2},
			connect_timeout = 30,
			read_timeout = 60,
			parameter_validation = True
		)
	)

	bucket_name: str = ''
	object_list: dict = s3_client.list_objects_v2(
		Bucket = bucket_name,
		Prefix = '',
		MaxKeys = 1000,
	)

	if object_list['IsTruncated'] == False:
		count: int = 1
		total_count: int = len(object_list['Contents'])
		for object in object_list['Contents']:
			if object['Key'][-1] != '/' and object['Size'] != 0:
				logging.info(msg = f'▼ 処理開始: {count}/{total_count}件 ▼')
				file_name: str = object['Key'].split('/')[-1]

				s3_client.download_file(
					Bucket = bucket_name,
					Key = object['Key'],
					Filename = f'./Downloads/{file_name}'
				)

				logging.info(msg = f'ダウンロード完了: {file_name}')

				s3_client.delete_object(
					Bucket = bucket_name,
					Key = object['Key'],
				)

				logging.info(msg = f'削除完了（S3）: {file_name}')

				count += 1
				logging.info(msg = f'──────────────────────────────')
	else:
		logging.warning(msg = '1,000件以上、取得されました。')

	logging.info(msg = '処理が正常に終了しました。')
