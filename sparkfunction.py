#!/usr/bin/env python

import json
import requests
import ssl
import sys

devID = "xxxx"
AToken = "yyyy"


def VarUpdate(varName):
    spark_url = "https://api.spark.io/v1/devices/%s/%s?access_token=%s" % (
        devID, varName, AToken)
    r = requests.get(spark_url)
    data = r.json()
    jsonData = "result"
    OutputData = data[jsonData]
    return OutputData


def sparkLED(appName):
    spark_url = "https://api.spark.io/v1/devices/%s/%s" % (devID, appName)
    payload = {'access_token': AToken}
    r = requests.post(spark_url, params=payload)
    data = r.json()
    jsonData = "return_value"
    OutputData = data[jsonData]
    return OutputData
