import json
from bs4 import BeautifulSoup
import re

try:
    with open('data.json', 'r') as f:
        dic = json.load(f)
except:
    with open('data.json', 'w') as f:
        f.write('[]')
    with open('data.json', 'r') as f:
        dic = json.load(f)

titles = []     # 标题
views = []      # 阅读量
keytags = []    # 原创
times = []      # 时间
mids = []       # 文章mid
hrefs = []      # 文章链接
time = ''

while True:
    continueORexit = input('输入c继续，输入q退出: ')
    if continueORexit == 'q':
        break

    html = ''
    with open('html.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            html += line.replace('\n', ' ')

    soup = BeautifulSoup(html, 'lxml')

    publish_hover_content = soup.find_all('div', class_='publish_hover_content')

    for phc in publish_hover_content:
        sphc = str(phc)
        deleted = re.findall(r"<span class=\"weui-desktop-mass__status_text\">.+?<i class=\"weui-desktop-mass__status_text_arrow\">", sphc)
        if len(deleted) == 0:
            deleted = re.findall(r"<span class=\"weui-desktop-mass_status_text\">.+?<i class=\"weui-desktop-mass__status_text_arrow\">", sphc)
            if len(deleted) == 0:
                deleted = '已群发'
            else:
                deleted = '已发表'
        else:
            deleted = re.findall(r">.+?<", deleted[0])[0]
            deleted = deleted[1:len(deleted) - 1]
        if deleted != '已发表' and deleted != '已群发':
            continue
        print('[')
        print('\t', deleted)
        title = re.findall(r"title=\".+?\"", sphc)
        if len(title) == 0:
            title = re.findall(r"title=\'.+?\'", sphc)[0]
        else:
            title = title[0]
        title = title[7:len(title) - 1].replace('&amp;nbsp;', ' ').replace('&amp;ZeroWidthSpace;', '')
        print('\t', title)
        view = re.findall(r"appmsg-view\">.<span class=\"weui-desktop-mass-media__data__inner\">.+?</span>", sphc)
        if len(view) == 0:
            view = re.findall(r"appmsg-view\"><span class=\"weui-desktop-mass-media__data__inner\">.+?</span>", sphc)[0]
        else:
            view = view[0]
        view = re.findall(r"r\">.+?</s", view)[0]
        view = str(view[3:len(view)-3])
        view = view.replace(',', '')
        print('\t', view)
        keytag = re.findall(r"key-tag\">.+?</b>", sphc)
        if len(keytag) == 0:
            keytag = '非原创'
        else:
            keytag = '原创'
        print('\t', keytag)
        em = re.findall(r"time\">.+?</em>", sphc)
        if len(em) == 0:
            em = time
        else:
            em = em[0][6:len(em)-6]
            time = em
        print('\t', em)
        mid = re.findall(r"mid=.+?&amp;idx=.&amp;sn", sphc)[0]
        mid = mid[4:len(mid)-17] + mid[len(mid)-8:len(mid)-7]
        print('\t', mid)
        # print(sphc)
        href = re.findall(r"<div><a href=\".+?\"target=\"_blank\"", sphc)
        if len(href) == 0:
            href = re.findall(r"<div>.+?<a class=\"weui-desktop-mass-appmsg__title\".+?href=\".+?\" target=\"_blank\"", sphc)[0]
            href = re.findall(r"href=\".+?\"", href)[0]
            href = href[6:len(href) - 1]
        else:
            href = re.findall(r"\".\"", href)[0]
            href = href[1:len(href) - 1]
        print('\t', href)

        print(']')
        print('')

        titles.append(title)
        views.append(view)
        keytags.append(keytag)
        times.append(em)
        mids.append(mid)
        hrefs.append(href)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        for i in range(len(mids)):
            obj = dict(mids=mids[i], titles=titles[i], views=views[i], keytags=keytags[i], times=times[i], hrefs=hrefs[i])
            flag = True
            for j in range(len(dic)):
                if dic[j]['mids'] == mids[i]:
                    flag = False
                    dic[j] = obj
                    break
            if flag == True:
                dic.append(obj)
        json.dump(dic, f)