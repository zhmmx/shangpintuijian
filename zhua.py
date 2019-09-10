import requests
import re


def getHTMLText(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "cookie": "t=c1e8231792f007e72593175d60586f3a; cna=HthOFWZZfEoCAZkiYyMw5eUw; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=tb313659628; lgc=tb313659628; tg=0; enc=C%2B2%2F0QsEwiUFmf00owySlc7hJiEsY4t4EIGdIzzH6ih9ajzhcMJCs7wzlX4%2B4gJrv2IlLviuxk0B1VAXlVwD8Q%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=1314040285196636905; uc3=vt3=F8dBy3vI3wKCeS4bgiY%3D&id2=VyyWskFTTiu0DA%3D%3D&nk2=F5RGNwsJzCC9CC4%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; _m_h5_tk=ec90707af142ccf8ce83ead2feda4969_1560657185501; _m_h5_tk_enc=2bc06ae5460366b0574ed70da887384e; mt=ci=-1_0; cookie2=14c413b3748cc81714471780a70976ec; v=0; _tb_token_=e33ef3765ebe5; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; swfstore=97544; JSESSIONID=80EAAE22FC218875CFF8AC3162273ABF; uc1=cookie14=UoTaGdxLydcugw%3D%3D; l=bBjUTZ8cvDlwwyKtBOCNCuI8Li7OsIRAguPRwC4Xi_5Z86L6Zg7OkX_2fFp6Vj5RsX8B41jxjk99-etki; isg=BP__g37OnjviDJvk_MB_0lRbjtNJTFLqmxNfMJHMlK71oB8imbTI1uey5jD7-Cv-"
        }
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html):
    try:
      #  plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        ult = re.findall(r'\"detail_url\"\:\".*?\"', html)
        for i in range(len(tlt)):
          #  price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            urls = eval(ult[i].split(':')[1])
            #ilt.append([price, title])
            ilt.append(title)

    except:
        return ""


def printGoodsList(ilt):
    #tply = "{:4}\t{:8}\t{:16}"
    tply = "{:50}"
    #print(tply.format("序号", "价格", "商品名称"))
    print(tply.format("商品名称"))
    count = 1
    for g in ilt:
        count = count + 1
        #print(tply.format(count, g[0], g[1]))
        print(tply.format(g[0]))


def get_shangpin(infoList):
    goods = "手机"
    depth = 5
    strat_url = 'https://s.taobao.com/search?q=' + goods
    #infoList = []
    for i in range(depth):
        try:
            url = strat_url + "&s=" + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    #printGoodsList(infoList)



