#encoding=utf8
'''
    __author__ = 'Administrator'
    2016.3.13 19:50 first version
    从caixin网的html页面里提取结构化新闻数据
'''
import csv
import os
import sys
import bs4
import datetime
import requests, html2text
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
zhongshen_dir = r"C:\Users\Administrator\Desktop\Working Folder\Holmes\data\news\zhongshen"



columns = "item_id,item_type,source,url,author,title,content,item_pub_time,tags,cmt_cnt,fav_cnt,gmt_create,exinfo1,exinfo2".split(',')
item_id_dict = {}
writer = csv.writer(file("../data/news/zhongshen.csv", 'wb'))
writer.writerow(columns)
def extract_news(soup, news_cnt):
    try:
        infomain = soup.find(class_="InfoMain")
        key_words = ""
        is_article = 0
        title = infomain.find("h1").string
        #print title
        url = ""
        description = ""
        image_url = ""
        info1 = infomain.find(class_="info1")
        item_pub_time =  info1.find_all("span")[0].string.split(" ")[0]
        #print item_pub_time
        p_list = infomain.find(id="hiddenContent").find_all("p")
        content = ""
        for i in xrange(len(p_list)):
            if p_list[i].find("span") != None and p_list[i].find("span").string != None:
                content += p_list[i].find("span").string + "\n"
        content = content.replace("\n", "###n###")
        content = content.replace("\r", "###r###")
        item_id = "zhongshen-" + str(news_cnt)
        # print item_id
        if item_id not in item_id_dict:
            item_id_dict.setdefault(item_id, 0)
        else:
            return

        gmt_create = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %M:%S")
        cmt_cnt = 0
        fav_cnt = 0
        source = u"zhongshen"


        # print item_id
        item_type = "news"
        tags = key_words.replace(" ", ",")
        exinfo1 = ""
        exinfo2 = ""
        if image_url != "":
            exinfo2 = "image_url:" + image_url

        result = {}
        result['url'] = url
        result['item_id'] = item_id
        result['item_type'] = item_type
        result['author'] = 'caixin_jizhe'
        result['source'] = source
        result['title'] = title
        result['content'] = content
        result['item_pub_time'] = item_pub_time
        result['tags'] = tags
        result['cmt_cnt'] = cmt_cnt
        result['fav_cnt'] = fav_cnt
        result['exinfo1'] = exinfo1
        result['exinfo2'] = exinfo2
        result['gmt_create'] = gmt_create

        line = []
        for col in columns:
            if col not in result:
                line.append('')
            else:
                line.append(str(result[col]).encode('utf-8'))
        writer.writerow(line)
    except Exception, e:
       return -1
    return 0


news_cnt = 0
for cur,dirnames,filenames in os.walk(zhongshen_dir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for f in os.listdir(cur):
        try:
            f_path = os.path.join(cur, f)
            content = open(f_path, "r").read()
            #print content
            if content.find("AjaxPage_Click_NEWSID") == -1:
                continue
            soup = BeautifulSoup(content)
            if soup == None or soup.find("title") == None:
                continue
            title =  soup.find("title").string

            ##初步过滤
            if len(title.split("-")) < 2:
                continue
            # print f_path
            # print title
            flag = extract_news(soup, news_cnt)
            if flag == 0:
                news_cnt += 1
                print title
                if news_cnt % 1000 == 1:
                    print news_cnt
        except Exception, e:
            print e
            continue

    #break
print news_cnt
print len(item_id_dict)