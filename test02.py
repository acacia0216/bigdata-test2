import requests, json
from datetime import datetime, timedelta


def get_json_result(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            json_result = res.json()
            print(json_result)
        return json_result
    except Exception:
        print("서버통신 에러 이거나 오류발생")
        return "%s 에러 [%s]" % (datetime.now(), url)


def get_pagename_id(base_homepage, pagename, user_token):
    url = "%s/%s/?access_token=%s" % (base_homepage, pagename, user_token)
    get_id = get_json_result(url)
    return get_id["id"]


def get_list(dic):
    fields = "/?fields=id,message,link,name,type,shares,created_time,comments.limit(0).summary(true),reactions.limit(0).summary(true)"
    duration = "&since=%s&until=%s" % (dic["from"], dic["end"])
    params = "&limit=%s&access_token=%s" % (dic["limit"], dic["token"])
    url = "%s/%s/posts/?access_token=%s" % (dic["base"], dic["page_id"],dic["token"])
    url += fields + duration + params

    postList = []
    isNext = True
    while isNext:
        tmpPostList = get_json_result(url)
        for post in tmpPostList["data"]:
            postVO = preprocess_post(post)
            postList.append(postVO)

        # paging = tmpPostList["paging"]["next"]
        paging = tmpPostList.get("paging").get("next")
        if paging != None:
            url = paging
        else:
            isNext = False

    with open("d:/javaStudy/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return postList


def preprocess_post(post):
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

    # 공유수
    if "shares" not in post:
        shares_count = 0
    else:
        shares_count = post["shares"]["count"]

    # 리액션 수
    if "reaction" not in post:
        reaction_count = 0
    else:
        reaction_count = post["shares"]["summary"]["total_count"]
    # 댓글수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]
    # 메시지 수
    if "message" not in post:
        message_str = ""
    else:
        message_str = post["message"]
    postVO = {
        "created_time": created_time,
        "shares_count": shares_count,
        "reaction_count": reaction_count,
        "comments_count": comments_count,
        "message_str": message_str
    }
    return postVO


base_homepage = "https://graph.facebook.com/v3.0"
user_token = "EAACEdEose0cBAOqRIDb3PnuVZBLakhTuXNRvv9WnEBNrvZBNYUIS71bykBdch9px7EUvYp1ywa2lOHVEvoVJY2g6XStobyLwRN4Gmu0u7mDNVncrmWcG3aKdKMaZAy0Fd0id3gmft2VgQ48fZAgLr7gjVQSi6HBGxssKKd4OJwV4atamOPslKOiwTWx13ljJHIKHxuZBp0gZDZD"
pagename = "chosun"
limit = 20
from_date = "2017-01-01"
end_date = "2018-05-23"
dic = {"base": base_homepage, "page_id": get_pagename_id(base_homepage,pagename,user_token), "pagename": "chosun", "limit": limit, "from": from_date, "end": end_date, "token": "EAACEdEose0cBAOqRIDb3PnuVZBLakhTuXNRvv9WnEBNrvZBNYUIS71bykBdch9px7EUvYp1ywa2lOHVEvoVJY2g6XStobyLwRN4Gmu0u7mDNVncrmWcG3aKdKMaZAy0Fd0id3gmft2VgQ48fZAgLr7gjVQSi6HBGxssKKd4OJwV4atamOPslKOiwTWx13ljJHIKHxuZBp0gZDZD"}

result = get_list(dic)
print(result)
