import json
import random
import time

import requests

import db
import exec_sh
from weibo import logger
import urllib.parse


def fetch_latest_news(page, cursor):
    logger.info(f"""cursor: {cursor}，正在获取第{page}页""")
    url = f"https://www.toutiao.com/api/pc/list/user/feed?category=pc_profile_ugc&token=MS4wLjABAAAAg8mQwYyj-soFFv04MS_y4FHXz7BBhvlBHhzbrLws3k4&max_behot_time={cursor}&aid=24&app_name=toutiao_web&_signature=_02B4Z6wo00901Vmf7vgAAIDBizbHBzJec91Zu-pAADP.VODR5LteVtr5WITEbWrDs043dtSB09pcMkx9ppWz0iVhLI9uYEBTHsDiWeiYJHTNmSOm9q4VUbPuAZ17OcXLtpk2s2ecokXUbBC0a6"
    headers = {
        'authority': 'www.toutiao.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'passport_csrf_token=f9e7f6172fa33915c73e94a383b7ba23; passport_csrf_token_default=f9e7f6172fa33915c73e94a383b7ba23; _ga_1Y7TBPV8DE=GS1.1.1703422697.1.0.1703422705.0.0.0; tt_webid=7316144642309785129; s_v_web_id=verify_lqjhzi6d_TWotEWyj_IAHt_4l9f_AZLv_NFwzwTDbMMBM; local_city_cache=%E5%BC%A0%E5%AE%B6%E5%8F%A3; csrftoken=2c906a01e488f75e825c63fe104c20f9; n_mh=tprivy3dg15BYM7h7vJM7C5MT2dBnEegPgDePNbwA-U; sso_uid_tt=a8daec2a263370ce85a96bb7fedfcf20; sso_uid_tt_ss=a8daec2a263370ce85a96bb7fedfcf20; toutiao_sso_user=a73a716ba205cc0ff5fd8cab4926fb8e; toutiao_sso_user_ss=a73a716ba205cc0ff5fd8cab4926fb8e; sid_ucp_sso_v1=1.0.0-KDYzODE3MmZkMmE5YTRhZjg5ZWM5M2VjYTk3NTJkYTZhYjJlYTMzZTYKHgirlICC5MzKAxDZ2KCsBhgYIAwwl4mQqwY4BkD0BxoCaGwiIGE3M2E3MTZiYTIwNWNjMGZmNWZkOGNhYjQ5MjZmYjhl; ssid_ucp_sso_v1=1.0.0-KDYzODE3MmZkMmE5YTRhZjg5ZWM5M2VjYTk3NTJkYTZhYjJlYTMzZTYKHgirlICC5MzKAxDZ2KCsBhgYIAwwl4mQqwY4BkD0BxoCaGwiIGE3M2E3MTZiYTIwNWNjMGZmNWZkOGNhYjQ5MjZmYjhl; passport_auth_status=c4ed6d115a39502da35cf611d21abb69%2C; passport_auth_status_ss=c4ed6d115a39502da35cf611d21abb69%2C; sid_guard=613f05efd78ed366b4b7083e9c1456f6%7C1703423066%7C5184001%7CThu%2C+22-Feb-2024+13%3A04%3A27+GMT; uid_tt=42b1b24ce18554cc8d2ed8fb1225a760; uid_tt_ss=42b1b24ce18554cc8d2ed8fb1225a760; sid_tt=613f05efd78ed366b4b7083e9c1456f6; sessionid=613f05efd78ed366b4b7083e9c1456f6; sessionid_ss=613f05efd78ed366b4b7083e9c1456f6; sid_ucp_v1=1.0.0-KDE3YjFjZmVmYjY2MjVkN2VjOWZjOTBhNzBkYzcxMWIxYWYyNTgwMDYKGAirlICC5MzKAxDa2KCsBhgYIAw4BkD0BxoCbGYiIDYxM2YwNWVmZDc4ZWQzNjZiNGI3MDgzZTljMTQ1NmY2; ssid_ucp_v1=1.0.0-KDE3YjFjZmVmYjY2MjVkN2VjOWZjOTBhNzBkYzcxMWIxYWYyNTgwMDYKGAirlICC5MzKAxDa2KCsBhgYIAw4BkD0BxoCbGYiIDYxM2YwNWVmZDc4ZWQzNjZiNGI3MDgzZTljMTQ1NmY2; store-region=cn-he; store-region-src=uid; odin_tt=5a405d493ae8689989b04ee9d15249c5522a4c3d55118e5770e1d7935dfd2281ac20badff320018dc7433fe0f625c6fe; msToken=wDc7U1VNr5xcJOOcFUp08xKFPXxfktrnvLK81NH_rNLlPJRLms5xwNXJZ6LUkqW-2XY-KJmup1dpd-dsfUHdzvQ7rxoZeKv_CvHsNWk-; _S_WIN_WH=1613_818; _S_DPR=2; _S_IPAD=0; _gid=GA1.2.1032098757.1704725571; _gat=1; tt_anti_token=sutAaFDR-23e392c10363a4c1d48900bd0d825d3b62de98a0718be5635d19928751e8dad0; tt_scid=RF3iuN-3Z.9dfOofWLmX2VWzD8eZQFNAO5YJtAFKObEP7iYPx7saqT2egANOU3d0f02e; ttwid=1%7CZHQng6r5yFY3Bvi5y2YnkFJAvONxHylim2aUS95w17Y%7C1704726437%7C12dcbeac4636050130d1448929a382d742e4d040f075cd0027957a1c4357e22b; _ga_34B604LFFQ=GS1.1.1704725571.10.1.1704726437.17.0.0; _ga=GA1.1.97861797.1703422681; _ga_QEHZPBE5HH=GS1.1.1704725579.9.1.1704726447.0.0.0',
        'referer': 'https://www.toutiao.com/c/user/token/MS4wLjABAAAAg8mQwYyj-soFFv04MS_y4FHXz7BBhvlBHhzbrLws3k4/?tab=wtt',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    ret = response.json()
    return ret


def fetch_all_page():
    has_more = True
    cursor = 0
    next_page = 1
    while has_more:
        ret = fetch_latest_news(next_page, cursor)
        if ret.get("message") != "success":
            continue
        next_page = next_page + 1
        has_more = ret.get("has_more")
        cursor = ret.get("next").get("max_behot_time")
        resolve_contents(ret.get("data"))


def sleep():
    sleep_time = random.randint(1, 2)
    # 添加log，否则一般用户不知道以为程序卡了
    logger.info(f"""短暂sleep {sleep_time}秒，避免被ban""")
    time.sleep(sleep_time)


def resolve_contents(data):
    with open('toutiao/huxijin_weitoutiao.txt', 'a') as file:
        for item in data:
            file.write(item.get("content"))
            file.write("\n#########ITEM_END#########\n")


# curl --location --request POST 'https://api.coze.com/open_api/v1/chat' \
# --header 'Authorization: Bearer {API_KEY}' \
# --header 'Content-Type: application/json' \
# --header 'Accept: */*' \
# --header 'Host: bots.bytedance.net' \
# --header 'Connection: keep-alive' \
# --data-raw '{
#     "conversation_id": "",
#     "bot_id": "{Bot_Id}",
#     "user": "1",
#     "query": "",
#     "stream":true
# }'
# def generate_content(from_content):
#     query = f'你是老胡，点评下这篇文章中讨论的事件: {from_content}'
#     API_KEY = "EuZH0uUMz97C9siQYHOm0Im2sY8BPqiZXg6mbK7XtQXcxPeeOVuVlLZKv8rQNsfM"
#     Bot_Id = 7320599778369224712
#
#     headers = {
#         'Authorization': f'Bearer {API_KEY}',
#         'Content-Type': 'application/json',
#         'Accept': '*/*',
#         'Connection': 'keep-alive',
#     }
#
#     json_data = {
#         'conversation_id': '',
#         'bot_id': f'{Bot_Id}',
#         'user': '1',
#         'query': f'{query}',
#         'stream': True,
#     }
#
#     response = requests.post('https://api.coze.com/open_api/v1/chat', headers=headers, json=json_data)
#     res_str = ""
#     for line in response.iter_lines():
#         if line:
#             print(f"line is :{line}")
#             if line == b'event:done' or line == b'data:':
#                 return res_str
#             if line == b'event:message':
#                 continue
#             line_str = line.decode('UTF-8')
#             if not line_str.startswith("data:"):
#                 continue
#             line_json = json.loads(line_str[len("data:"):])
#             res_str = res_str + line_json.get("message", "{}").get("content", "")
#     return res_str

def parse_and_concat(string):
    # 根据换行符分隔字符串
    lines = string.split('\n')

    # 初始化结果字符串
    result = ""

    # 遍历每行
    for line in lines:
        # 确保这一行以data:开头
        if line.startswith('data:'):
            print(f"line:{line}")
            # 获取'data:'之后的部分，即是JSON字符串
            json_str = line[5:]
            if json_str is None or not json_str.strip().startswith("{"):
                continue
            # 使用json模块的loads函数将字符串解析成Python对象
            data = json.loads(json_str)
            # 把message.content字段的值添加到结果字符串中
            if data.get("message", {}).get("type", "") == "answer":
                result += data.get("message", {}).get("content", "")

    return result


def generate_content(from_content):
    query = f'你是老胡，点评下这篇文章中讨论的事件: {from_content}'

    # 对查询参数进行URL编码
    query_encoded = urllib.parse.quote(query)
    cmd = f'''
        curl --location --request POST 'https://api.coze.com/open_api/v1/chat' \
    --header 'Authorization: Bearer EuZH0uUMz97C9siQYHOm0Im2sY8BPqiZXg6mbK7XtQXcxPeeOVuVlLZKv8rQNsfM' \
    --header 'Content-Type: application/json' \
    --header 'Accept: */*' \
    --header 'Connection: keep-alive' \
    --data-raw '{{
        "conversation_id": "",
        "bot_id": "7320599778369224712",
        "user": "1",
        "query": "{query_encoded}",
        "stream":true
    }}'
    '''
    res = exec_sh.exec_sh(cmd)
    if res is None:
        return ""
    return parse_and_concat(res)


def do_publish_toutiao(content):
    decode_content = urllib.parse.quote(content)
    cmd = '''
    curl 'https://mp.toutiao.com/mp/agw/article/wtt?msToken=jfWzI20dYzSLYllTDSiyTIikT9bc8vsJhFArd-QtarlVyVQsP-BLeE2uCnQNrn6FhFkQntp9x3Fpt0dTEZIFbsjL25JYsv-eICQK7GTOb7JVtVWRnTG8&a_bogus=QfUdDO2aMsm1zvMJiwkz9CkimdS0YW4-gZENc-ScmzLn' \
  -H 'authority: mp.toutiao.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'cookie: _ga_1Y7TBPV8DE=GS1.1.1703422697.1.0.1703422705.0.0.0; tt_webid=7316144642309785129; n_mh=tprivy3dg15BYM7h7vJM7C5MT2dBnEegPgDePNbwA-U; store-region=cn-he; store-region-src=uid; csrf_session_id=2ff16fc6a471a77fcf0bdac7b473184d; ttcid=9d805b903aed430b989cd1c8b96aef8a31; _S_DPR=2; _S_IPAD=0; xigua_csrf_token=5lvUBymIQG9f4Lz9HrxjpX4v; xg_p_tos_token=1a7a5136161030f043a40094f37d8578; passport_csrf_token=da78940676d47ffa2b081d4e771b7689; passport_csrf_token_default=da78940676d47ffa2b081d4e771b7689; s_v_web_id=verify_ltfufqu9_lABWPsNx_mOv8_4FV6_85Ag_mI7xl9poWGiY; sso_uid_tt=400d97fcf3c1df36f12fc7496c72f4ee; sso_uid_tt_ss=400d97fcf3c1df36f12fc7496c72f4ee; toutiao_sso_user=15db5799bf90604ae82292ddffaf2693; toutiao_sso_user_ss=15db5799bf90604ae82292ddffaf2693; sid_ucp_sso_v1=1.0.0-KGQxMmU4YjFjOTdlZmIwOTllYzY5YTVkMWNlNGQzYTk5MDQ3MTIxODEKHgirlICC5MzKAxDX46GvBhgYIAwwl4mQqwY4BkD0BxoCaGwiIDE1ZGI1Nzk5YmY5MDYwNGFlODIyOTJkZGZmYWYyNjkz; ssid_ucp_sso_v1=1.0.0-KGQxMmU4YjFjOTdlZmIwOTllYzY5YTVkMWNlNGQzYTk5MDQ3MTIxODEKHgirlICC5MzKAxDX46GvBhgYIAwwl4mQqwY4BkD0BxoCaGwiIDE1ZGI1Nzk5YmY5MDYwNGFlODIyOTJkZGZmYWYyNjkz; passport_auth_status=1dafbbe88d54e2b91ef928fdc8d18322%2C; passport_auth_status_ss=1dafbbe88d54e2b91ef928fdc8d18322%2C; sid_guard=6ec6ab06c2b29c15fa1d1d5f2f5f7d31%7C1709732312%7C5184001%7CSun%2C+05-May-2024+13%3A38%3A33+GMT; uid_tt=6702f00be98a899dc88b9fcbfaed6605; uid_tt_ss=6702f00be98a899dc88b9fcbfaed6605; sid_tt=6ec6ab06c2b29c15fa1d1d5f2f5f7d31; sessionid=6ec6ab06c2b29c15fa1d1d5f2f5f7d31; sessionid_ss=6ec6ab06c2b29c15fa1d1d5f2f5f7d31; sid_ucp_v1=1.0.0-KDUzZWM0ODU0MWU1ODY2ZTZmNDczZWJhNTVhZjUxNWM0ZDdhOTU4NjAKGAirlICC5MzKAxDY46GvBhgYIAw4BkD0BxoCbHEiIDZlYzZhYjA2YzJiMjljMTVmYTFkMWQ1ZjJmNWY3ZDMx; ssid_ucp_v1=1.0.0-KDUzZWM0ODU0MWU1ODY2ZTZmNDczZWJhNTVhZjUxNWM0ZDdhOTU4NjAKGAirlICC5MzKAxDY46GvBhgYIAw4BkD0BxoCbHEiIDZlYzZhYjA2YzJiMjljMTVmYTFkMWQ1ZjJmNWY3ZDMx; odin_tt=2a3840b009d89f48d847008478ad5f596e046af2ebb619fa8c9fe3b596ac73d3a61fb8e2fe32e8c8184fff00ebe63204; _S_WIN_WH=1824_849; gftoken=NmVjNmFiMDZjMnwxNzA5ODI0ODU3NzB8fDAGBgYGBgY; _ga_QEHZPBE5HH=GS1.1.1709824608.21.1.1709826339.0.0.0; tt_scid=TgFwaQAvdPaS8rq7EH6y77ydhtxoXIcqtrZ7JEkth2lsX3Lg-LU7Ja8ai.J6W6C4e722; msToken=05OXe8KgPC0gNRJR7zmGh-UiqdCc_h8VsiZWvY_twvwAIkQOu009KEMKlbUH9M1ruGxZowpqd-Qg2r28q7ICXOOIhakr8T-k_qomJMiswJRSQ4bzX_Ca; _gid=GA1.2.1306584952.1709999128; _ga_34B604LFFQ=GS1.1.1709999118.22.1.1709999156.22.0.0; _ga=GA1.1.97861797.1703422681; ttwid=1%7CZHQng6r5yFY3Bvi5y2YnkFJAvONxHylim2aUS95w17Y%7C1709999156%7Cd780344586f1961084dfb4cb7a700ba2f54f20153a8ae49fefe2f9cf4729b6bc' \
  -H 'origin: https://mp.toutiao.com' \
  -H 'referer: https://mp.toutiao.com/profile_v4/weitoutiao/publish' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'tt-anti-token: OybXNjdt-d489fd1ea3d213e367f272456a42c41aa658e24601bcf9521e7cd3068b10574c' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36' \
  -H 'x-secsdk-csrf-token: 0001000000017c36327b0eb6927fee7d95b45368faadf64cf8e4ea7c3c40cf357173d41452b917bb232c819ec785' \
  --data-raw '{"content":"''' + decode_content + '''","image_list":[],"is_fans_article":2,"extra":"{\"tuwen_wtt_trans_flag\":\"0\",\"info_source\":\"{\\\"source_type\\\":-1}\"}","pre_upload":1,"welfare_card":""}\''''

    ret = exec_sh.exec_sh(cmd)
    ret = json.loads(ret)
    print(f"publish result:{ret}")
    return ret.get("code") == 0


def get_last_n_news(limit):
    ret = fetch_latest_news(1, 0)
    if ret.get("message") != "success":
        print("not success")
        return []
    if len(ret.get("data")) == 0:
        print("empty data")
        return []
    return reversed(ret.get("data")[:limit])


def main():
    try:
        while True:
            fetch_and_publish()
            time.sleep(random.uniform(120, 300))
    except Exception as e:
        print(e)


def fetch_and_publish():
    cur, conn = db.connect_to_db("articles.db")
    for item in get_last_n_news(3):
        # time.sleep(random.uniform(1, 1.5))
        raw_id = item.get("id")
        if raw_id is None:
            print(f"raw_id is null, item:{json.dumps(item)}")
            continue
        raw_url = item.get("share_info", {}).get("share_url")
        # 检查是否已发布id为3的文章
        if db.check_published_article(cur, raw_id):
            print(f"Article with raw_id {raw_id} is already published.")
        else:
            print(f"Article with raw_id {raw_id} is not published yet.")
            content = generate_content(item.get("content"))
            if call_with_retry(content, do_publish_weibo):
                # 插入新的文章
                db.insert_article(cur, conn, raw_id, content)
                print(f"publish article, raw_id:{raw_id}, raw_url:{raw_url} content:{content}")
    conn.close()


def call_with_retry(param, call):
    for i in range(2):
        if call(param):
            return True
        time.sleep(random.uniform(1, 3))
    return False  # 在调用 do_publish 10次后，如果都未成功则返回 False


def do_publish_weibo(content):
    decode_content = urllib.parse.quote(content)
    cmd = f'''
    curl 'https://weibo.com/ajax/statuses/update' \
  -H 'authority: weibo.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'client-version: v2.44.75' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'cookie: XSRF-TOKEN=HXFw4b8NZMUxDpMm5eKtsrch; _s_tentry=www.google.com.hk; Apache=1996442261467.5237.1704340399461; SINAGLOBAL=1996442261467.5237.1704340399461; ULV=1704340399463:1:1:1:1996442261467.5237.1704340399461:; WBtopGlobal_register_version=2024010518; UOR=www.google.com.hk,open.weibo.com,www.google.com.hk; _gid=GA1.2.2003830231.1710084773; ALF=1712676873; SUB=_2A25I6aNZDeRhGeNM7FMZ8ijPwj-IHXVrhrqRrDV8PUJbkNAGLXHWkW1NSesgRnsH0yvNvl4IPmfbFv-lO1vTm0t-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhJMvRWzarQOdFaCzqCHfw75JpX5KzhUgL.Fo-ES02Reoq01Ke2dJLoIpfWCCH81F-ReEHWeCH81C-4SFHWeCH81C-ReF-Re5tt; _gat=1; WBPSESS=MWIoLOlZ6-26XzF0WpUaXf_ojTp8CJOD211m1VbwPucx3Sr_bQIHy38hMa1G3g-QVhBnxNxxRpd1MHjJjiTWy73hgbXoRG3XdRDlUuWhzaxYR27ZgeAU2sTwBvFlpkc90CX4XREamZgFnVy2A-nt9g==; _ga_34B604LFFQ=GS1.1.1710084772.15.1.1710084978.45.0.0; _ga=GA1.1.2030487639.1704279045' \
  -H 'origin: https://weibo.com' \
  -H 'referer: https://weibo.com/' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'server-version: v2024.03.06.1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'x-xsrf-token: HXFw4b8NZMUxDpMm5eKtsrch' \
  --data-raw 'content={decode_content}&visible=0&share_id=&media=&vote='
    '''
    ret = exec_sh.exec_sh(cmd)
    ret = json.loads(ret)
    print(f"publish result:{ret}")
    return ret.get("ok") == 1


if __name__ == "__main__":
    main()
    # fetch_and_publish()
