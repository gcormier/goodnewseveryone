import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime

my_config = Config(
    region_name = 'ca-central-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)


def send_email(destination, body_content, ses_user, ses_key):
    SENDER = "goodnewseveryone@ses.gregular.com"
    AWS_REGION = "ca-central-1"
    today_date = datetime.now().strftime('%A %b %d')
    SUBJECT = f"Good news everyone! {today_date}"
    BODY_HTML = f"<html><body>{body_content}</body></html>"
    CHARSET = "UTF-8"
    
    client = boto3.client('ses', config=my_config, region_name=AWS_REGION, aws_access_key_id=ses_user, aws_secret_access_key=ses_key)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    destination,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
