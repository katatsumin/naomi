from ctypes import windll, wintypes
import time
import threading
import random
import os
import msvcrt
import unicodedata

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

def output_screen(default_time, los_time):
    kernel32.SetConsoleCursorPosition(hOut, wintypes._COORD(0, 0))
    print('{:.2f} + {:.2f}  {}ペイトン       '.format(default_time, los_time, point))
    print('1:{} 2:{}'.format(choices[0], choices[1]))
    print('3:{} 4:{}'.format(choices[2], choices[3]))
    if 0 < point:
        print(str(x) + ' 正解!')

def output_result(reason):
    kernel32.SetConsoleCursorPosition(hOut, wintypes._COORD(0, 3))
    print(reason)
    print('あなたの得点は {}ペイトンでした。'.format(point))
    if point == 0:
        print('こんな得点だったら、こんなゲーム、やる意味ないもの')
    elif point < 100:
        print('クソゲームの世界を甘く見ないで！')
    elif point < 300:
        print('納得できないわ……。納得できないったらできないの！')
    elif point < 500:
        print('もう、私ってば、いつもこう……')
    elif point < 1000:
        print('ギャラクシーーー！！')
    else:
        print('何、意地になってんのよ！')

def loop():
    global default_time
    global los_time
    while 0 < default_time + los_time:
        output_screen(default_time, los_time)
        time.sleep(0.1)
        if 0 < default_time:
            default_time -= 0.1
            # 浮動小数点計算補正
            if 0 > default_time:
                default_time = 0
        elif 0 < los_time:
            los_time -= 0.1
        if game_over == True:
            output_result(str(x) + ' 不正解!')
            return
    los_time = 0
    output_screen(default_time, los_time)
    output_result('時間切れ!')

STD_OUTPUT_HANDLE = -11

kernel32 = windll.kernel32
hOut = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

ok_list = ('Naomi Payton','ペイトン尚未')
ng_list = ('Naomi Python','ペイトン尚美','ペイント尚未','ペイント尚美','Naomi Paytan','Naomi PayPay')
default_time_init = 3
default_time = default_time_init
los_time = 20
point = 0
game_over = False
x = ''

os.system('CLS')

while True:
    correct_num = random.randint(1,4)
    choices = random.sample(ng_list,4)
    choices[correct_num - 1] = ok_list[random.randint(0,1)]

    # 半角全角文字幅調整
    for index, item in enumerate(choices):
        choices[index] = item + ' ' * (20 - get_east_asian_width_count(item))

    if point == 0:
        t = threading.Thread(target=loop)
        t.setDaemon(True)
        t.start()

    x = msvcrt.getwch()
    if x == str(correct_num):
        point += 10
        default_time = default_time_init
    else:
        game_over = True
        break

t.join()
