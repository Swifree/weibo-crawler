import requests

app_id = "wxb844854ebefe6013"
app_secret = "e2c791f8dc129e661d4b42ed40d729ab"
token = "78_AsTdy2wobINcQDWtD10aFelNf820kxrKH6r9ajiPKQQYbo1aY_PB6xG5gJO-UFTo4fjkBQaAumGJkrclriqhgSjqyFHbiqSMe3wBnCFFK1L_YYj3rSsnckbHvOgSWYgADALPR"

def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
    payload = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    }
    response = requests.post(url, json=payload)  # 使用 POST 方法发送请求
    data = response.json()  # 解析返回的JSON数据
    return data['access_token'], data['expires_in']  # 返回 access_token 和 expires_in


# def publish(content):
    