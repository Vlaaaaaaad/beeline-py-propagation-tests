import os
import time
import json

from entrypoint import beeline
from beeline.middleware.awslambda import beeline_wrapper

@beeline_wrapper
def main(event, context):
    try:
        with beeline.tracer(name="lambda22"):
            beeline.add_context({
                'payload': event,
            })

            time.sleep(2)

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
