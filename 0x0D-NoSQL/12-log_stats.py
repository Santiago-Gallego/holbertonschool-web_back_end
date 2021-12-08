#!/usr/bin/env python3
""" Module that holds log stats
    Script that provides some stats about
    Nginx logs stored in MongoDB
"""

from pymongo import MongoClient

mngclient = MongoClient()
logs = mngclient.logs.nginx


totallogs = logs.count_documents({})
get = logs.count_documents({"method": "GET"})
post = logs.count_documents({"method": "POST"})
put = logs.count_documents({"method": "PUT"})
patch = logs.count_documents({"method": "PATCH"})
delete = logs.count_documents({"method": "DELETE"})
status = logs.count_documents({"method": "GET", "path": "/status"})

if __name__ == "__main__":
    print("{} logs".format(totallogs))
    print("Methods:")
    print("\tmethod GET: {}".format(get))
    print("\tmethod POST: {}".format(post))
    print("\tmethod PUT: {}".format(put))
    print("\tmethod PATCH: {}".format(patch))
    print("\tmethod DELETE: {}".format(delete))
    print("{} status check".format(status))