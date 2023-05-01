import requests
from flask import jsonify
import json


errors = 0

#############################
# md5 test 

response = requests.get("http://localhost:4000/md5/Hello World")
data = response.json()
if response.status_code == 200 or response.status_code == 404:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/md5/    white   space")
data = response.json()
if response.status_code == 200 or response.status_code == 404:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/md5/37258943570265410")
data = response.json()
if response.status_code == 200 or response.status_code == 404:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/md5/String_Value")
data = response.json()
if response.status_code == 200 or response.status_code == 404:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/md5/GROUP4 TEST CASES")
data = response.json()
if response.status_code == 200 or response.status_code == 404:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1


#############################
# factorial test 

response = requests.get("http://localhost:4000/factorial/20")
data = response.json()
if ((response.status_code == 200) and data['output'] == 2432902008176640000):
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1


response = requests.get("http://localhost:4000/factorial/100")
data = response.json()
if ((response.status_code == 200) and data['output'] == 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000):
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1
    


response = requests.get("http://localhost:4000/factorial/0")
data = response.json()
if ((response.status_code == 200) and data['output'] == 1):
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/factorial/1")
data = response.json()
if ((response.status_code == 200) and data['output'] == 1):
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

#############################
# fibonacci test 

response = requests.get("http://localhost:4000/fibonacci/2355463")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/fibonacci/31")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/fibonacci/10")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/fibonacci/239402548032")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/fibonacci/0")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

#############################
# is prime test 

response = requests.get("http://localhost:4000/is-prime/4")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/is-prime/32478329481")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/is-prime/0")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/is-prime/1")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

response = requests.get("http://localhost:4000/is-prime/1000000000")
data = response.json()
if response.status_code == 200:
    print("Test Passed")
else:
    print("Test Failed")
    errors += 1

#############################
# slack alert - only one test as this test is primarily for functionality, input would not matter as the function is built to take in anything as input and post it directly to our Slack channel.

#response = requests.get("http://localhost:4000/slack-alert/Post this string into our Slack Channel to test API functionality")
#data = response.json()
#if response.status_code == 200:
#    print("Test Passed")
#else:
#    print("Test Failed")
#    errors += 1


def noErrors():
    return 0

if errors == 0:
    noErrors()
else:
    print("You have errors within your API. Edit accordingly and rerun test file!")

####################################################################
count = 0

#POST
url = "http://127.0.0.1:4000/keyval"
response = requests.post(url, json={"storage-key": "new key", "storage-val": "new value"})
if (response.status_code == 200):
    print("New storage-key and storage-val created ✅")
else:
    print("ERROR! Did not pass ❌")
    count += 1 

url = "http://127.0.0.1:4000/keyval"
response = requests.post(url, json={"storage-key": "new key", "storage-val": "some value"})
j = response.json()
if (response.status_code >= 400 and response.status_code < 500):
    print("Key already exists ✅")
else: 
    print("ERROR! Did not pass ❌")
    count += 1 

#GET
url = "http://127.0.0.1:4000/keyval/testing"
response = requests.get(url)
if (response.status_code == 200 ):
    print("Succesfully retrieved ✅ ")
else:
    print("ERROR! Did not pass ❌")
    count += 1 

url = "http://127.0.0.1:4000/keyval/92"
response = requests.get(url)
if (response.status_code >= 400 and response.status_code < 500) or (j["result"] == False):
    print("Invalid request ✅")
else: 
    print("ERROR! Did not pass ❌")
    count += 1 

url = "http://127.0.0.1:4000/keyval/program"
response = requests.get(url)
j = response.json()
if (response.status_code >= 400 and response.status_code < 500) or (j["result"] == False):
    print("Key does not exist ✅")
else: 
    print("ERROR! Did not pass ❌")
    count += 1 

#PUT
url = "http://127.0.0.1:4000/keyval"
response = requests.put(url, json={"storage-key": "new key", "storage-val": "new value"})
if (response.status_code == 200):
   print("New storage-key and storage-val Updated ✅")
else:
   print("ERROR! Did not pass ❌")
   count += 1

url = "http://127.0.0.1:4000/keyval"
response = requests.put(url, json={"storage-key": "existing key", "storage-val": "new value"})
j = response.json()
if (response.status_code >= 400 and response.status_code < 500) or (j["result"] == False):
   print("Key does not already exist ✅")
else:
   print("ERROR! Did not pass❌")
   count += 1

#DELETE
url = "http://127.0.0.1:4000/keyval/testdelete"
response = requests.delete(url)
j = response.json()
if (response.status_code >= 400 and response.status_code < 500) or (j["result"] == False):
    print("Key does not exist ✅")
else: 
    print("ERROR! Did not pass ❌")
    count += 1

url = "http://127.0.0.1:4000/keyval/testing"
response = requests.delete(url)
j = response.json()
if (response.status_code == 200) or (j["result"] == True):
    print("Key deleted ✅")
else: 
    print("ERROR! Did not pass ❌")
    count += 1


if count == 0:
    print("successful")
else:
    print(count, "test cases did not pass.")