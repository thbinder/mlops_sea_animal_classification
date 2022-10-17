import os
import time

import requests

time.sleep(15)

# API address definition
api_address = "api"
# API port
api_port = 8000

# Request
file = {"file": open("nudibranch.jpg", "rb")}
r1 = requests.post(
    url="http://{address}:{port}/predict".format(address=api_address, port=api_port),
    auth=("thomas", "thomas"),
    files=file,
)

r2 = requests.post(
    url="http://{address}:{port}/predict".format(address=api_address, port=api_port),
    files=file,
)

output = """
============================
        Predict test
============================

request done at "/predict"
| auth thomas thomas
| file nudibranch.jpg

expected result 200
actual restult = {status_code_1}
predicted class = {pred}

==>  {test_status_1}

request done at "/predict"
| no auth
| file nudibranch.jpg

expected result 401
actual restult = {status_code_2}

==>  {test_status_2}

"""

# Request status
status_code_1 = r1.status_code
pred = r1.json().get("class label")
status_code_2 = r2.status_code

# Show results
if status_code_1 == 200:
    test_status_1 = "SUCCESS"
else:
    test_status_1 = "FAILURE"

if status_code_2 == 401:
    test_status_2 = "SUCCESS"
else:
    test_status_2 = "FAILURE"

print(
    output.format(
        status_code_1=status_code_1,
        test_status_1=test_status_1,
        pred=pred,
        status_code_2=status_code_2,
        test_status_2=test_status_2,
    )
)

# Put in file if necessary
if os.environ.get("LOG") == 1:
    with open("/logs/api_test.log", "a") as file:
        file.write(output)
