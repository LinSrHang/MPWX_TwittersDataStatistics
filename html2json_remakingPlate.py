import json
from bs4 import BeautifulSoup
from re import findall

STATUS_RE_1 = r"<span class=\"weui-desktop-mass__status_text\">.+?<i class=\"weui-desktop-mass__status_text_arrow\">"
STATUS_RE_2 = r"<span class=\"weui-desktop-mass_status_text\">.+?<i class=\"weui-desktop-mass__status_text_arrow\">"
TITLE_RE_1 = r"title=\".+?\""
TITLE_RE_2 = r"title=\'.+?\'"
VIEW_RE_1 = r"appmsg-view\">.<span class=\"weui-desktop-mass-media__data__inner\">.+?</span>"
VIEW_RE_2 = r"appmsg-view\"><span class=\"weui-desktop-mass-media__data__inner\">.+?</span>"
VIEW_RE_3 = r"r\">.+?</s"
KEYTAG_RE = r"key-tag\">.+?</b>"
EM_RE = r"time\">.+?</em>"
MID_RE = r"mid=.+?&amp;idx=.&amp;sn"
HREF_RE_1 = r"<div><a href=\".+?\"target=\"_blank\""
HREF_RE_2 = r"<div>.+?<a class=\"weui-desktop-mass-appmsg__title\".+?href=\".+?\" target=\"_blank\""
HREF_RE_3 = r"href=\".+?\""
HREF_RE_4 = r"\".\""

def readjson():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write('[]')
        return readjson()
    
def readhtml():
    html = ''
    with open('html.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            html += line.replace('\n', ' ')
    return html
    
def OBJ(mid, title, view, keytag, time, href):
    return dict(mids=mid, titles=title, views=view, keytags=keytag, times=time, hrefs=href)

def updateDic(dic, mid, title, view, keytag, time, href):
    obj = OBJ(mid, title, view, keytag, time, href)
    flag = True
    for i in dic:
        if i['mids'] == mid:
            flag = False
            i = obj
            break
    if flag == True:
        dic.append(obj)
    return dic

def processPHC(phc, defaultTime) -> tuple[str, str, str, str, str, str, str, bool]:
    sphc = str(phc)

    status = findall(STATUS_RE_1, sphc)
    if len(status) == 0:
        status = findall(STATUS_RE_2, sphc)
        status = '已群发' if len(status) == 0 else '已发表'
    else:
        status = status[0]
    if status.find('已发表') == -1 and status.find('已群发') == -1:
        return None, None, None, None, None, None, None, True

    title = findall(TITLE_RE_1, sphc)
    title = findall(TITLE_RE_2, sphc)[0] if len(title) == 0 else title[0]
    title = title[7 : len(title) - 1].replace('&amp;nbsp;', ' ').replace('&amp;ZeroWidthSpace;', '')

    view = findall(VIEW_RE_1, sphc)
    if len(view) == 0:
        view = findall(VIEW_RE_2, sphc)[0]
    else:
        view = view[0]
    view = findall(VIEW_RE_3, view)[0]
    view = (view[3:len(view)-3]).replace(',', '')

    keytag = findall(KEYTAG_RE, sphc)
    keytag = '非原创' if len(keytag) == 0 else '原创'

    em = findall(EM_RE, sphc)
    em = defaultTime if len(em) == 0 else em[0][6 : len(em) - 6]

    mid = findall(MID_RE, sphc)[0]
    mid = mid[4 : len(mid)-17] + mid[len(mid) - 8 : len(mid) - 7]

    href = findall(HREF_RE_1, sphc)
    if len(href) == 0:
        href = findall(HREF_RE_3, findall(HREF_RE_2, sphc)[0])[0]
        href = href[6 : len(href) - 1]
    else:
        href = findall(HREF_RE_4, href)[0]
        href = href[1 : len(href) - 1]

    return mid, title, view, keytag, em, href, em, False

def debug(mid, title, view, keytag, time, href):
    print('[')
    print('\t', mid)
    print('\t', title)
    print('\t', view)
    print('\t', keytag)
    print('\t', time)
    print('\t', href)
    print(']\n')

def write(dic):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(dic, f)

if __name__ == '__main__':
    dic = readjson()
    defaultTime = ''    # 缺省时间

    while True:
        isQuit = input('输入任意字符以继续，输入Q或q以退出: ')
        if isQuit == 'q' or isQuit == 'Q':
            break

        try:
            html = readhtml()
            soup = BeautifulSoup(html, 'lxml')
            publish_hover_content = soup.find_all('div', class_='publish_hover_content')

            for phc in publish_hover_content:
                mid, title, view, keytag, time, href, defaultTime, err = processPHC(phc, defaultTime)
                if err == True:
                    continue
                debug(mid, title, view, keytag, time, href)
                dic = updateDic(dic, mid, title, view, keytag, time, href)
        except Exception:
            print(Exception)
            dic = write(dic)

    dic = write(dic)