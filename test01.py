import requests, json
from datetime import datetime, timedelta

BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBAFojCbhNnTG46p4qqsraHZBvUPHvu77vUv3cbuFNp52K9OuXZCfZCZC6z2bEXOcT6GdZCYsS3xvOspvDDHbyls9JBLfmb9zDytNRhpP9fLkxZAjHJBZA5L3OOKdJGzmujLdpN2Ip9lGa7FueEwbbDVQsXpQDl3DgrWJAnoLHTx1rWvqzftqwTr8tux4Aikb2AZDZD"
LIMIT_REQUEST = 20
pagename = "chosun"
from_date = "2017-01-22"
to_date = "2018-05-23"


def get_json_result(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("정상 경로가 아닙니다.", e)
        return "%s : Error for request[%s]" % (datetime.now(), url)


def fb_name_to_id(pagename):
    base = BASE_URL_FB_API
    node = "/%s" % pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params
    json_result = get_json_result(url)
    return json_result["id"]


def fb_get_post_list(pagename, from_date, to_date):
    page_id = fb_name_to_id(pagename)
    base = BASE_URL_FB_API
    node = "/%s/posts" % page_id
    fields = "/?fields=id,message,link,name,type,shares,created_time,comments.limit(0).summary(true),reactions.limit(0).summary(true)"
    duration = "&since=%s&until=%s" % (from_date, to_date)
    parameters = "&limit=%s&access_token=%s" % (LIMIT_REQUEST, ACCESS_TOKEN)
    url = base + node + fields + duration + parameters

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
    # 작성일 +9시간 해줘야함
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

result = fb_get_post_list(pagename, from_date, to_date)
print(result)

# url = "http://192.168.1.14:8088/mysite4/api/gb/list2"
# result = requests.get(url)
# print(result)

# result = fb_name_to_id("facebook")
# print(result)
