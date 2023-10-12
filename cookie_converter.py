import os
import json
import random
import shutil


input_path = "cookies"
output_path = "json_cookies"
rand_number = random.randint(1, 99999)

def convert_netscape_cookie_to_json(cookie_file_content):
    cookies = []
    for line in cookie_file_content.splitlines():
        fields = line.strip().split("\t")
        if len(fields) >= 7:
            cookie = {
                "domain": fields[0].replace("www", ""),
                "flag": fields[1],
                "path": fields[2],
                "secure": fields[3] == "TRUE",
                "expiration": fields[4],
                "name": fields[5],
                "value": fields[6],
            }
            cookies.append(cookie)

    JSON_DATA = json.dumps(cookies, indent=4)
    return JSON_DATA


try:
    os.mkdir(output_path)
    print(f"Folder {output_path} created!")
except FileExistsError:
    print(f"Folder {output_path} already exists! New cookies will be appended.")
    pass
    
for filename in os.listdir(input_path):
    filepath = os.path.join(input_path, filename)
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        json_data = convert_netscape_cookie_to_json(content)

        with open(f"{output_path}/{filename}", "w", encoding="utf-8") as f:
            f.write(json_data)
            print(f"{filename} - DONE!")
