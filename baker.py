import json
import os


def bake():
    cookies = []

    if os.path.exists(os.getcwd() + os.path.sep + "cookies.txt"):
        with open('cookies.txt', 'r') as f:
            lines = f.readlines()
    else:
        raise Exception('The "cookies.txt" file was not found')

    for line in lines:
        if line.startswith('#') or not line.startswith('.') or not line.startswith('app.') or (len(line.strip()) == 0):
            pass
        else:
            line = line.replace('\n', '').split('\t')
            if line.__len__() == 7:
                cookie = dict(domain=line[0].strip(), flag=bool((line[1].strip() == 'TRUE')), path=line[2].strip(),
                              secure=bool((line[3].strip() == 'TRUE')), expiration=line[4].strip(), name=line[5].strip(), value=line[6].strip())
                cookies.append(cookie)
            else:
                raise Exception('Malformed cookies.txt file')

    with open('cookies.json', 'w') as f:
        f.write(json.dumps(cookies, indent=4))
        print("Cookies baked!")
