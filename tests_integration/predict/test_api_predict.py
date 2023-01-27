import os
import time

import requests

time.sleep(15)

# API address definition
api_address = "api"
# API port
api_port = 8081

# Request
file = {"file": open("nudibranch.jpg", "rb")}
r = requests.post(
    url="http://{address}:{port}/predict".format(address=api_address, port=api_port),
    auth=("thomas", "thomas"),
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
actual restult = {status_code}
predicted class = {pred}

==>  {test_status}

"""

# Request status
status_code = r.status_code
pred = r.json().get("class label")

# Show results
if status_code == 200:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"
print(output.format(status_code=status_code, test_status=test_status, pred=pred))

# Put in file if necessary
if os.environ.get("LOG") == 1:
    with open("/logs/api_test.log", "a") as file:
        file.write(output)
