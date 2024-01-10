import random
import time

import requests

from weibo import logger


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


def main():
    try:
        fetch_all_page()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
