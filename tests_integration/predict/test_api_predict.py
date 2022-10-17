import os
import requests
import time

time.sleep(10)

# API address definition
api_address = 'api'
# API port
api_port = 8000

# Request
file = {'media': open('nudibranch.jpg', 'rb')}
r = requests.post(
    url='http://{address}:{port}/predict'.format(address=api_address, port=api_port),
    params= {
        'username': 'thomas',
        'password': 'thomas'
    },
    files=file
)

output = '''
============================
        Predict test
============================

request done at "/ping"
| no params

expected result 200
actual restult = {status_code}

==>  {test_status}

'''

# Request status
status_code = r.status_code

# Show results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))

# Put in file if necessary
if os.environ.get('LOG') == 1:
    with open('/logs/api_test.log', 'a') as file:
        file.write(output)