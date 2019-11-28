import sys
import json
import beeline
from beeline.patch import requests
import requests

def main():
    from libhoney.transmission import FileTransmission

    beeline.init(
      service_name='client-beeline-py-propagation-tests',
      debug=True,
    )


    with beeline.tracer(name="prepare"):
      headers = {
        'Content-Type': 'application/json',
      }

      payload = {
        'name': 'value',
        '1': 'not 2',
      }

      with beeline.tracer(name="send to SQS"):
        response = requests.post(
          url = 'https://xxx.execute-api.eu-west-1.amazonaws.com/live/sqs',
          data=json.dumps(payload),
          headers=headers,
        )

        print(response.status_code)
        print(response.content)

      with beeline.tracer(name="send to SNS"):
        response = requests.post(
            url = 'https://xxx.execute-api.eu-west-1.amazonaws.com/live/sns',
          data=json.dumps(payload),
          headers=headers,
        )

        print(response.status_code)
        print(response.content)

      with beeline.tracer(name="send to Lambda"):
        beeline.add_context({
          'yo': 'yoooooo',
        })

        response = requests.post(
          url = 'https://xxx.execute-api.eu-west-1.amazonaws.com/live/lambda',
          data=json.dumps(payload),
          headers=headers,
        )

        print(response.status_code)
        print(response.content)

    beeline.close()

if __name__ == "__main__":
    main()
