from flask import Flask, jsonify, request, Response, abort
from redis import Redis, RedisError
import redis
import hashlib                                              # used for MD5 Hash
import requests                                             # used for slack alert
import os
import socket
import json 


r = redis.Redis(host="myredis", port=6379, decode_responses=True)


app = Flask(__name__)

slackURL = "" 

#default local host page
@app.route("/")

def hello_world():
    return "<p>Howdy! We are Group 4. This is our API.</p>"


#MD5
@app.route("/md5/<string:strvalue>")

def md5(strvalue):
    md5val = hashlib.md5(strvalue.encode())
    hexval = md5val.hexdigest()
    return jsonify(
        input=strvalue,
        output=hexval
    )


#factorial
@app.route("/factorial/<int:x>")

def factorial(x):

    fact = 1
    if x < 0:
        return jsonify(
            input=x,
            output="Error, the input must be a positive integer"
        )       
    elif x == 0:
        return jsonify(
            input=x,
            output=1
        )    
    else:
        for i in range(1,x+1):
            fact = fact * i
        return jsonify(
            input=x,
            output=fact
        )
     
        
# fibonacci
@app.route("/fibonacci/<int:x>")

def fibonacci_num(x):
    num1= 0
    num2 = 1
    seq=[0]

    if x < 0:
        return jsonify(
            input=x,
            output="Please enter a positive integer"
        )
       
    elif x == 0:
        return jsonify(
            input=x,
            output=seq
            )

    elif x == 1:
        while num2 < 2:
            seq.append(num2)
            num1, num2 = num2, num1+num2
        return jsonify(
            input=x,
            output=seq
        )

    else:
        while num2 <= x:
            seq.append(num2)
            num1, num2 = num2, num1+num2
            
        return jsonify(
            input=x, 
            output=seq
        )              


# is-prime
@app.route("/is-prime/<int:n>")

def prime(n):
    flag = True
    
    if n == 1 or n == 0:
        flag = False
        return jsonify(
            input=n,
            output=flag
        )
    elif n > 1:
        for i in range(2, n):
            if n % i == 0:
                flag = False
                return jsonify(
                    input=n,
                    output=flag
                )
    else:
        return jsonify(
            input=n,
            output="Error, Input is Invalid"
        )
    return jsonify(
        input=n,
        output=flag
    )    


#slack-alert
@app.route("/slack-alert/<string:post>")

def slack_alert(post):
    flag = True
    response = requests.post(slackURL, json={'text': post, 'username':"Group4restAPI_Bot"})
    if response.status_code == 200:
        return jsonify(
            input=post,
            output=flag
        )
    else:
        flag = False
        return jsonify(
            input=post,
            output=flag
        )

# ----------------------------------------------------------------------------------------------------------------------

@app.route("/keyval", methods=["POST"])
def post():
    payload = request.get_json()
       
    if r.exists(payload["key"]):
        #create object to return if it exists
        
        keypair_found = {
            "storage-key": payload["key"],
            "storage-val": payload["value"],
            "command": f"CREATE {payload['key']}/{payload['value']}",
            "result": False,
            "error": "Key already exists"
        } 
        return jsonify(keypair_found), 409

    else:
        r.set(payload['key'], payload['value'])
        
        keypair = {
            "storage-key": payload["key"],
            "storage-val": payload["value"],
            "command": f"CREATE {payload['key']}/{payload['value']}",
            "result": True,
            "error": ""
        }
        return jsonify(keypair), 200

@app.route("/keyval", methods=["PUT"])
def put():
    payload = request.get_json()

    if r.exists(payload["key"]):
        r.set(payload['key'], payload['value'])
        keypair = {
            "storage-key": payload["key"],
            "storage-val": payload["value"],
            "command": f"UPDATE {payload['key']}/{payload['value']}",
            "result": True,
            "error": ""
        }
        return jsonify(keypair), 200
    else:
        keypair_notfound = {
            "storage-key": payload["key"],
            "storage-val": payload["value"],
            "command": f"UPDATE {payload['key']}/{payload['value']}",
            "result": False,
            "error": "Key does not exist"
        } 
        return jsonify(keypair_notfound), 404

@app.route("/keyval/<string:inputval>", methods=["GET"])
def get(inputval):
        command = "READ value for the following key: " + inputval
        
        if r.exists(inputval):
            storage_value = r.get(inputval)
            keypair = {
               "storage-key": inputval,
               "storage-val": storage_value,
               "command": command,
               "result": True,
               "error": ""
           }
            return jsonify(keypair), 200
        
        else:
             keypair_notfound = {
               "storage-key": inputval,
               "storage-val": "Not found",
               "command": command,
               "result": False,
               "error": "Key does not exist"
           }
             return jsonify(keypair_notfound), 404

@app.route("/keyval/<string:inputval>", methods=["DELETE"])
def delete(inputval):
    command = "Delete the stored value for key: " + inputval
        
    if r.exists(inputval): # 1 is True
        storage_value = r.get(inputval)
        r.delete(inputval)
          
        keypair_deleted = {
            "storage-key": inputval,
            "storage-val": storage_value,
            "command": command,
            "result": True,
            "error": "Key pair was found and deleted from database"
        }
        return jsonify(keypair_deleted), 200
        
    else:
        keypair_notfound = {
            "storage-key": inputval,
            "storage-val": "Not found",
            "command": command,
            "result": False,
            "error": "Unable to delete key: Key does not exist"
        }
        return jsonify(keypair_notfound), 404

   
if __name__ == "__main__":                                  # debug mode for testing, port 4000 as per assignment instructions
    app.run(host='0.0.0.0',port=4000, debug=True)
