import sys
import time
import os
import pymysql
import requests
import random
import traceback
from bs4 import BeautifulSoup

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'pw123456',
    'charset': 'utf8',
    'db': 'autohome',
    'cursorclass': pymysql.cursors.DictCursor,
}

from_cache_first = True

request_headers = [
    {
        'Accept': '*/*',
        'Referer': 'https://www.autohome.com.cn/car/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
]

try:

    urls = [
        'https://www.autohome.com.cn/grade/carhtml/A.html',
        'https://www.autohome.com.cn/grade/carhtml/B.html',
        'https://www.autohome.com.cn/grade/carhtml/C.html',
        'https://www.autohome.com.cn/grade/carhtml/D.html',
        'https://www.autohome.com.cn/grade/carhtml/E.html',
        'https://www.autohome.com.cn/grade/carhtml/F.html',
        'https://www.autohome.com.cn/grade/carhtml/G.html',
        'https://www.autohome.com.cn/grade/carhtml/H.html',
        'https://www.autohome.com.cn/grade/carhtml/I.html',
        'https://www.autohome.com.cn/grade/carhtml/J.html',
        'https://www.autohome.com.cn/grade/carhtml/K.html',
        'https://www.autohome.com.cn/grade/carhtml/L.html',
        'https://www.autohome.com.cn/grade/carhtml/M.html',
        'https://www.autohome.com.cn/grade/carhtml/N.html',
        'https://www.autohome.com.cn/grade/carhtml/O.html',
        'https://www.autohome.com.cn/grade/carhtml/P.html',
        'https://www.autohome.com.cn/grade/carhtml/Q.html',
        'https://www.autohome.com.cn/grade/carhtml/R.html',
        'https://www.autohome.com.cn/grade/carhtml/S.html',
        'https://www.autohome.com.cn/grade/carhtml/T.html',
        'https://www.autohome.com.cn/grade/carhtml/U.html',
        'https://www.autohome.com.cn/grade/carhtml/V.html',
        'https://www.autohome.com.cn/grade/carhtml/W.html',
        'https://www.autohome.com.cn/grade/carhtml/X.html',
        'https://www.autohome.com.cn/grade/carhtml/Y.html',
        'https://www.autohome.com.cn/grade/carhtml/Z.html'
    ]

    dbconnect = pymysql.connect(**db_config)
    cursor = dbconnect.cursor()

    brands_demo = [
        {
            'initial':'B',
            'name':'宝马',
            'logo': '',
            'sub_brands':[
                {
                    'name':'华晨宝马',
                    'autos':['宝马1系','宝马2系旅行车']
                },
                {
                    'name': '宝马（进口）',
                    'autos': ['宝马8系', '宝马i3']
                }
            ]
        }
    ]

    brands = []

    for url in iter(urls):

        brand_initial = url[-6:-5]
        html_file = os.path.abspath('.') + os.path.sep + 'data' + os.path.sep + url[-6:]
        print('爬取链接:', url, "存储到:", html_file)
        # continue

        if os.path.exists(html_file) and from_cache_first:

            f = open(html_file, 'r', encoding='utf-8')
            page_data = f.read()
            f.close()

        else:

            header_index = random.randint(0, len(request_headers) - 1)
            response = requests.get(url, headers=request_headers[header_index])
            page_data = response.text
            print(response)

            if response.status_code != 200:

                print('爬取链接:',url,'失败！')
                continue

            else:

                # 保存页面数据
                file_handler = open(html_file, 'w', encoding='utf-8')
                file_handler.write(page_data)
                file_handler.close()

        # 清洗数据
        try:
            soup = BeautifulSoup(page_data, 'lxml')

            # 找出所有品牌
            brand_tages = soup.find_all('dl')

            for brand_index,brand_tag in enumerate(brand_tages):

                brand_name = brand_tag.find('dt').find('div').find('a').get_text()
                brand_logo_file = os.path.abspath('.') + os.path.sep + 'logo' + os.path.sep + str(brand_index) + '.png'
                brand_logo_path = 'catalog/autobrand/'+ str(brand_index) + '.png'

                if not os.path.exists(brand_logo_file) or not from_cache_first:
                    brand_logo = brand_tag.find('dt').find('a').find('img').attrs['src']
                    brand_logo_response = requests.get('https:'+brand_logo)
                    with open(brand_logo_file,'wb') as logo:
                        logo.write(brand_logo_response.content)
                        logo.close()


                date_added = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                date_modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                # 品牌
                sql = "insert into af_ymp_autobrand (parent_id, logo, sort_order, status, date_added, date_modified) values (%s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, ['0', brand_logo_path,'0','1',date_added,date_modified])
                dbconnect.commit()
                autobrand_id = cursor.lastrowid

                sql_description = "insert into af_ymp_autobrand_description (autobrand_id, language_id, name, initial) values (%s, %s, %s, %s);"
                brand_descriptions = [
                    (autobrand_id, 1, brand_name, ''),
                    (autobrand_id, 2, brand_name, '')
                ]

                cursor.executemany(sql_description, brand_descriptions)
                dbconnect.commit()

                # 子品牌
                sub_brand_tags = brand_tag.find('dd').find_all("div", class_="h3-tit")
                sub_brand_model_tags = brand_tag.find('dd').find_all("ul", class_="rank-list-ul")
                for sub_brand_index,sub_brand_tag in enumerate(sub_brand_tags):
                    sub_brand_name = sub_brand_tag.find('a').get_text()

                    # 定义要执行的sql语句
                    sub_sql = "insert into af_ymp_autobrand (parent_id, logo, sort_order, status, date_added, date_modified) values (%s, %s, %s, %s, %s, %s);"
                    cursor.execute(sql, [autobrand_id, '', '0', '1', date_added, date_modified])
                    dbconnect.commit()
                    sub_autobrand_id = cursor.lastrowid

                    sub_sql_description = "insert into af_ymp_autobrand_description (autobrand_id, language_id, name, initial) values (%s, %s, %s, %s);"
                    sub_brand_descriptions = [
                        (sub_autobrand_id, 1, sub_brand_name, ''),
                        (sub_autobrand_id, 2, sub_brand_name, '')
                    ]

                    cursor.executemany(sub_sql_description, sub_brand_descriptions)
                    dbconnect.commit()

                    # 子品牌车型
                    brand_model_tags = sub_brand_model_tags[sub_brand_index].find_all('li')
                    # print(brand_model_tags)
                    # exit()


                    for brand_model_tag in brand_model_tags:

                        if brand_model_tag.find('h4') is None:
                            continue

                        brand_model_name = brand_model_tag.find('h4').find('a').get_text()
                        sql_model = "insert into af_ymp_automodel (autobrand_id, sort_order, status, date_added, date_modified) values (%s, %s, %s, %s, %s);"
                        cursor.execute(sql_model, [sub_autobrand_id, '0', '1', date_added, date_modified])
                        dbconnect.commit()

                        automodel_id = cursor.lastrowid

                        sql_model_description = "insert into af_ymp_automodel_description (automodel_id, language_id, name) values (%s, %s, %s);"
                        brand_model_descriptions = [
                            (automodel_id, 1, brand_model_name),
                            (automodel_id, 2, brand_model_name)
                        ]

                        cursor.executemany(sql_model_description, brand_model_descriptions)
                        dbconnect.commit()


        except Exception as e:

            # print('清洗数据异常:')
            traceback.print_exc()
            # print(brand_model_tag.prettify())
            # exit()

    cursor.close()
    dbconnect.close()

except Exception as e:
    print(e)
else:
    dbconnect.close()
finally:
    sys.exit(0)

if __name__ == '__main__':
    pass
