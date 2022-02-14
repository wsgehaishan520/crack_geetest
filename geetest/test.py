import requests
import time
import json
from PIL import Image
import io
import execjs

from yolo5.detect import get_labels
from nlp import get_xy


with open('encryption.js', encoding='utf-8') as f:
    js_data = f.read()


def get_w(xy, pic, nc, ns, gt, challenge):
    passtime = 710
    t = int(time.time() * 1000)
    click = [
    [
        "blur",
        t
    ],
    [
        "focus",
        t+100
    ],
    [
        "focus",
        t+100
    ],
    [
        "down",
        318,
        349,
        t+200,
        "pointerdown"
    ],
    [
        "move",
        318,
        349,
        t+250,
        "pointermove"
    ],
    [
        "up",
        318,
        349,
        t+300,
        "pointerup"
    ],
    [
        "move",
        318,
        349,
        t+302,
        "mousemove"
    ],
    [
        "down",
        318,
        349,
        t+303,
        "mousedown"
    ],
    [
        "up",
        318,
        349,
        t+304,
        "mouseup"
    ],
    [
        "down",
        327,
        520,
        t+400,
        "pointerdown"
    ],
    [
        "up",
        327,
        520,
        t+450,
        "pointerup"
    ],
    [
        "move",
        327,
        520,
        t+470,
        "mousemove"
    ],
    [
        "down",
        327,
        520,
        t+470,
        "mousedown"
    ],
    [
        "focus",
        t+470
    ],
    [
        "up",
        327,
        520,
        t+471,
        "mouseup"
    ]
]

    js = execjs.compile(js_data)
    return js.call('getW', click, xy, pic, nc, ns, gt, challenge, passtime)


def geetest_crack():
    session = requests.session()
    session.proxies = {'https': '42.6.114.104:2357'}
    start_time = time.time()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'
    }

    register_url = 'https://www.geetest.com/api/user/show/register-space?t=' + str(int(time.time()) * 1000)

    res = session.get(url=register_url, headers=headers)
    res = json.loads(res.text)
    gt = res['gt']
    challenge = res['challenge']

    get_url = f"https://api.geetest.com/get.php?gt={gt}&challenge={challenge}" \
              f"&lang=zh-cn&pt=0&client_type=web&w=&callback=geetest_{str(int(time.time()) * 1000)}"

    res1 = session.get(url=get_url, headers=headers)

    ajax_url = 'https://api.geetest.com/ajax.php?' \
                       'gt='+gt+'&' \
                       'challenge='+challenge+'&' \
                       'lang=zh-cn&pt=0&client_type=web_mobile&' \
                       'w=&' \
                       'callback=geetest_' + str(int(time.time())*1000)
    res2 = session.get(url=ajax_url, headers=headers)

    get_spcae_url = 'https://api.geetest.com/get.php?is_next=true&type=click&' \
                    'gt=' + gt + '&' \
                    'challenge=' + challenge + '&' \
                    'lang=zh-cn&https=true&protocol=https%3A%2F%2F&offline=false&' \
                    'product=popup&api_server=api.geetest.com&isPC=true&autoReset=true&' \
                    'width=100%25&callback=geetest_' + str(int(time.time()) * 1000)
    data = session.get(url=get_spcae_url, headers=headers).text
    data = json.loads(data[22:-1])['data']

    pic = data['pic']
    pic_url = 'https://static.geetest.com' + pic + '?challenge=' + challenge
    nc, ns, sign = data['c'], data['s'], data['sign'].split('_')[2]

    t = time.time()

    image = requests.get(pic_url, headers=headers)
    data_stream = io.BytesIO(image.content)
    pil_image = Image.open(data_stream)
    labels = get_labels(pil_image)
    print(labels)
    xy = get_xy(sign, labels)

    w_value = get_w(xy, pic, nc, ns, gt, challenge)
    delay = time.time() - start_time
    print(delay)
    time.sleep(delay)
    value_url = 'https://api.geetest.com/ajax.php?' \
                'gt='+gt+'&' \
                'challenge='+challenge+'&lang=zh-cn&pt=3&client_type=web_mobile&' \
                'w='+w_value+'&' \
                'callback=geetest_' + str(int(time.time()) * 1000)

    response = session.get(value_url, headers=headers).text
    response = json.loads(response[22:-1])['data']
    value = response['validate']
    print(value)


geetest_crack()
