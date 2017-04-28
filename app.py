#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import psycopg2


# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def makeWebhookResult(req):
    print(req)
    print(req.text)
    newdata = json.loads(req.text())
    print(newdata)
    if req.get("result").get("action") == "myNameIsHanoma":
        str = getDB()
        return { "speech" : str,
        "displayText": str,
        "source": "TestGP"
        }
    else:
        return {}

def getDB():


    conn = psycopg2.connect(database="d8892l088pogrv", user="vrohnqnmsxxafb", password="4a1b7ec8d80b8d7a0223134363005eb4075c127faead65eba2c672a3675189ba", host="ec2-54-235-153-124.compute-1.amazonaws.com", port="5432")

    cur = conn.cursor()
    cur.execute('''SELECT * from "user" where ID = 1''')
    rows = cur.fetchall()
    for row in rows:
        return str(row[0])+" "+row[1]+" "+str(row[2]) 
    conn.close()



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    # print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
