import json


def main(filename):

        with open(f'data.json', 'r', encoding='utf-8') as jfile:
            data = json.load(jfile)
        name=data["data"][0]["username"]
        lv=data["data"][0]["progressionStats"]["level"]
        kd=data["data"][0]["genericStats"]["general"]["kd"]
        return name, lv, kd

if __name__ == '__main__':
    data="./data.json"
    name,lv,kd=main(data)
    print(name)
    print(lv)
    print(kd)
