#!./__venv__/bin/python3.6

import getopt
import hashlib
import sys

from flask import Flask
from pymongo import MongoClient
from prettytable import PrettyTable
from urllib.parse import urlsplit

from bson import ObjectId
from server.model import Model

app = Flask(__name__)
app.config.from_pyfile('server/config.py')

parsed = urlsplit(app.config['MONGODB_URI'])
mongo_client = MongoClient(app.config['MONGODB_URI'])
db = mongo_client[parsed.path[1:]]

model = Model(db=db)


def create_user(data):
    # Validate data
    if "password" not in data or not data["password"]:
        print("password must be set for user addition")
        sys.exit(3)

    if "email" not in data or not data["email"]:
        print("email must be set for user addition")
        sys.exit(3)

    data["name"] = data["name"] if "name" in data else data["email"].lower()
    data["admin"] = data["admin"] if "admin" in data else False
    data["active"] = data["active"] if "active" in data else True

    # Check that user doesn't exist yet
    users = model.users.find_query({"name": data["name"]})
    if users:
        print(f"user with username {data['name']} already exists")
        sys.exit(3)

    model.users.create(data)


def delete_users(data):
    users = model.users.find_query(data)
    count = len(users)

    for user in users:
        model.users.delete(user)

    print(f"deleted {count} users")


def lists_users(data):
    table = PrettyTable(["id", "Name", "Email", "active", "admin"])

    users = model.users.find_query(data)
    for user in users:
        table.add_row([user.id, user.name, user.email, user.active, user.admin])

    print(table)


def modify_user(user_id, data):
    user = model.users.find_one(user_id)
    if not user:
        print(f"No user with id {user_id} found")
        sys.exit(3)

    if "name" in data:
        users = model.users.find_query({"name": data["name"]})
        if users:
            print(f"user with username {data['name']} already exists")
            sys.exit(3)
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]
    if "active" in data:
        user.active = data["active"]
    if "admin" in data:
        user.admin = data["admin"]

    model.users.save(user)

    print(f"user {user.id} modified")


def usage(error):
    print(error)


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "cdlm",
                                ["id=", "name=", "password=", "active=", "email=", "admin="])
    except getopt.GetoptError as err:
        usage(err)
        sys.exit(2)

    data = {}
    mode = None

    for opt, value in opts:
        if opt in ("-c", "-d", "-l", "-m"):
            if mode is not None:
                usage("Only one mode can be selected at the time")
                sys.exit(1)
            mode = opt[1:]
        elif opt == "--id":
            user_id = value
        elif opt == "--name":
            data[opt[2:]] = value.lower()
        elif opt == "--password":
            data[opt[2:]] = hashlib.sha256(value.encode("utf-8")).hexdigest()
        elif opt == "--email":
            data[opt[2:]] = value
        elif opt in ("--active", "--admin"):
            data[opt[2:]] = value.lower() not in ("", "0", "false")
        else:
            assert False, "unhandled option"

    if mode == "c":
        create_user(data)
    elif mode == "d":
        delete_users(data)
    elif mode == "l":
        lists_users(data)
    elif mode == "m":
        modify_user(user_id, data)


if __name__ == "__main__":
    main()
