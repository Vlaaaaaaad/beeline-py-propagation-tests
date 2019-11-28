import os
import time
import json
import boto3

from entrypoint import beeline
from beeline.middleware.awslambda import beeline_wrapper

@beeline_wrapper
def main(event, context):
    try:
      with beeline.tracer(name="lambda2"):
          beeline.add_context({
              'payload': event,
          })

          time.sleep(1)

      with beeline.tracer(name="send to SNS"):

        client = boto3.client('sns')

        response = client.publish(
          TargetArn=os.getenv('SNS_TO_PUBLISH_TO'),
          MessageStructure='json',
          Message=json.dumps({'default': 'myMessage'}),
          MessageAttributes={
            'x-honeycomb-trace': {
              'DataType': 'String',
              'StringValue': str(beeline.marshal_trace_context()),
            }
          },
        )

      return {
        "statusCode": 200,
        "body": json.dumps('Heeeeey')
      }

    except Exception as e:
        # Throw exception so Lambda retries
        exception_type = e.__class__.__name__
        exception_message = str(e)

        beeline.add_context({
            'error.type': exception_type,
            'error.message': exception_message,
        })

        api_exception_obj = {
            "isError": True,
            "type": exception_type,
            "message": exception_message,
        }
        api_exception_json = json.dumps(api_exception_obj)

        raise LambdaException(api_exception_json)
    finally:
        beeline.get_beeline().client.flush()

class LambdaException(Exception):
  '''Exception wrapper class to get prettier output '''
