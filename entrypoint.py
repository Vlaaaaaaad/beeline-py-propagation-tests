# Single entrypoint for all functions
#  This is required for library usage

# Import needed libraries
import os
import sys
import beeline
from beeline.middleware.awslambda import beeline_wrapper

# Import actual Lambda function handler
from functions.lambda1 import main as lambda1
from functions.lambda2 import main as lambda2
from functions.lambda3 import main as lambda3
from functions.lambda21 import main as lambda21
from functions.lambda22 import main as lambda22
from functions.lambda23 import main as lambda23



if os.getenv('AWS_EXECUTION_ENV') is None:
    # If not running in AWS Lambda disable Honeycomb sending
    from libhoney.transmission import FileTransmission

    beeline.init(
        transmission_impl=FileTransmission(output=sys.stdout),
        debug=True,
    )

else:
    beeline.init()

    beeline.add_context({
        'app.name': 'beeline-py-propagation-tests',
        'meta.memory_limit': os.getenv('AWS_LAMBDA_FUNCTION_MEMORY_SIZE'),
        'meta.aws_region': os.getenv('AWS_REGION'),
    })
