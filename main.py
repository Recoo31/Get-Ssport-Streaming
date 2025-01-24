import requests

def get_session_token():
    acc = requests.get("https://recoo.vercel.app/accountss").json()
    user = acc["user"]
    passw = acc["pass"]
    
    jsondata = {
        "action": "SubscriberLogin",
        "subscriber": {
            "LoginPreferedMethod": 0,
            "UILanguage": "tr",
            "Email": user,
            "PIN": passw
        },
        "Devices": [{"PlatformID": 10}]
    }
    
    response = requests.post('https://api.ssportplus.com/MW/SubscriberLogin', json=jsondata).json()
    token = response["SessionID"]
    return token

def get_live_content_url(token):
    json_data = {
        'action': 'GetCurrentLiveContents',
        'pageNumber': 1,
        'count': 100,
        'TSID': 1691847445,
    }
    
    response = requests.post('https://api.ssportplus.com/MW/GetCurrentLiveContents', headers=headers, json=json_data).json()
    contents = response["Categories"][0]["Contents"]
    
    available_titles = [(i["ID"], i["Title"]) for i in contents]

    print("Available Live Streams:")
    for idx, title in enumerate(available_titles):
        print(f"{idx + 1}. {title[1]}")

    choice = int(input("Enter Number: ")) - 1
    requested_id = available_titles[choice][0]

    json_data = {
        'action': 'GetContentById',
        'RequestedID': requested_id,
        'TSID': 1691847445,
    }

    response = requests.post('https://api.ssportplus.com/MW/GetContentById', headers=headers, json=json_data).json()
    url_la = response["Categories"][0]["Contents"][0]["Medias"][2]["URL"]
    return url_la

def get_original_url(url_la):
    xml = requests.get(url_la, headers=headers).text
    url = xml.split('StreamLink="')[1].split('" DRM="0')[0]
    return "https://"+url

def main():
    token = get_session_token()
    global headers
    headers = {
        'authority': 'api.ssportplus.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'tr-TR,tr;q=0.7',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://app.ssportplus.com',
        'referer': 'https://app.ssportplus.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'sngt': '127781610010541133424187944339',
        'uilanguage': 'tr',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    url_la = get_live_content_url(token)
    org_url = get_original_url(url_la)
    print(org_url)
    open("Ssport_Live.txt","w").write(org_url)

if __name__ == "__main__":
    main()
