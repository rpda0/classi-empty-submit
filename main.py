import requests,time,threading

ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
root = "https://platform.classi.jp/api/questionnaire/examination"
urls = {
    "login":"https://auth.classi.jp/students",
    "validate_login":"https://auth.classi.jp/login/validate",
    "list":f"{root}/list",
    "create":f"{root}/???/answer/header/create",
    "start":f"{root}/???/start",
    "detail":f"{root}/???/detail",
    "save":f"{root}/???/save",
    "submit":f"{root}/???/submit"
    }


headers = {
        "connection" : "keep-alive",
        "content-type" : "application/x-www-form-urlencoded",
        "user-agent": ua,
        "accept" : "*/*",
    }
def login(user_name,pswd):
    r = requests.get(urls["login"],headers=headers)
    val = r.text.find("value")
    token = r.text[val+7:val+95]
    data = {
        "authenticity_token": token,
        "classi_id":user_name,
        "password":pswd,
        "login_form":"student"
    }
    cookie = requests.post(urls["validate_login"],headers=headers,data=data,allow_redirects=False,cookies=r.cookies.get_dict()).cookies.get_dict()         
    if "classi_account" in cookie:
        print("ログインに成功しました")
        return cookie
    else:
        print("ログインに失敗しました")
        print(cookie)
        return None

def ans_que(dist_id):
    dist_id = str(dist_id)
    sec = []
    create = urls["create"].replace("???",dist_id)
    start = urls["start"].replace("???",dist_id)
    detail = urls["detail"].replace("???",dist_id)
    save = urls["save"].replace("???",dist_id)
    submit = urls["submit"].replace("???",dist_id)

    
    requests.post(create,headers=headers,cookies=ca)
    requests.post(start,headers=headers,cookies=ca)
    d = requests.get(detail,headers=headers,cookies=ca).json()
    data = '{"answer_data":{"sections":['
    for i in range(len(d["test_data"]["sections"])):
        ans_type = d["test_data"]["sections"][i]["questions"][0]["format"]["type"]
        if i == 0:
            data += '{"section_no":'+str(i+1)+',"questions":[{"type":"'+ans_type+'","question_no":1,"user_answer":null,"attached":null,"score":null,"result":null}]}'
        if i != 0:
            data += ',{"section_no":'+str(i+1)+',"questions":[{"type":"'+ans_type+'","question_no":1,"user_answer":null,"attached":null,"score":null,"result":null}]}'
    data += ']}}'
    r = requests.post(save,headers=headers,data=data,cookies=ca).text
    if 'パラメーター' in r:
        print(f"!!!!{title}はセーブできませんでした")
        return
    requests.post(submit,headers=headers,data='{"status":1}',cookies=ca)
    title = d["test_data"]["title"]
    print(f'{title}は提出されました')


ca = login(input('enter your username'),input('enter your password'))
i = 0
que_list = requests.get(urls["list"],headers={"user-agent":ua},cookies=ca).json()
for t in que_list:
    i += 1
    threading.Thread(target=ans_que,args=(t["distribution_id"],)).start()
    if i > 10:
        time.sleep(2)
        i = 0
print(f"{len(que_list)}個のアンケートを提出しました")
    
