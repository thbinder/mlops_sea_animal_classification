import os
import time

import requests

time.sleep(15)

# API address definition
api_address = "api"
# API port
api_port = 8000

# Request
r = requests.get(
    url="http://{address}:{port}/ping".format(address=api_address, port=api_port)
)

output = """
============================
        Health test
============================

request done at "/ping"
| no params

expected result 200
actual restult = {status_code}

==>  {test_status}

"""

# Request status
status_code = r.status_code

# Show results
if status_code == 200:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"
print(output.format(status_code=status_code, test_status=test_status))

# Put in file if necessary
if os.environ.get("LOG") == 1:
    with open("/logs/api_test.log", "a") as file:
        file.write(output)
