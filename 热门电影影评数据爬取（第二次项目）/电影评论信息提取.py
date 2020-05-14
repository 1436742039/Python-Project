import requests
import bs4
import re
import time
import random
import pandas


def getHTMLText(url):
    kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/80.0.3987.163 Safari/537.36 '
          }
    try:
        get = requests.get(url, headers=kv, timeout=30)
        get.raise_for_status()
        get.encoding = 'utf-8'
        return get.text
    except:
        return ""


def ye_mian_chu_li1(html, datelist):   # 页面处理及数据提取   豆瓣影评提取
    soup = bs4.BeautifulSoup(html, 'lxml')
    for div in soup.find_all('div', 'main review-item'):
        li = []
        # if isinstance(div, bs4.element.Tag):  # 去除不符合的标签
        try:
            # li.append(len(datelist))   # 为数据添加序号
            score = div.find('span').get('class')  # 获取评分
            li.append(score[0] + ' ' + score[1])
            li.append(div.find('span').get('title'))  # 获取推荐
            li.append(div.find('span', "main-meta").string)  # 获取时间
            vote = div.find('span', id=re.compile(r'r-useful_count')).string  # 获取支持数
            vote_new = vote.replace('\n', '')
            li.append(vote_new.strip(' '))
            pinglun = div.find('a', href="javascript:;").previous_sibling.string.replace('\n', '').replace('\xa0(', '')
            li.append(pinglun.strip(' '))
            li.append(div.find('a', 'name').string)  # 获取姓名
            datelist.append(li)
        except:
            pass


def ye_mian_chu_li2(html, datelist):   # 豆瓣短评提取
    soup = bs4.BeautifulSoup(html, 'lxml')
    n = 0
    for div in soup.find_all('div', "comment-item"):
        li = []
        try:
            n +=1
            score = div.find('span', re.compile('allstar')).get('class')  # 获取评分
            li.append(score[0] + ' ' + score[1])
            li.append(div.find('span', re.compile('allstar')).get('title'))  # 获取推荐
            li.append(div.find('span', 'comment-time').get('title'))  # 获取时间
            li.append(div.find('span', 'votes').text)  # 获取支持数
            li.append(div.find('span','short').string)    # 获取短评
            li.append(div.find('div','avatar').find('a').get('title'))  # 获取姓名
            datelist.append(li)
        except:
            pass

def time_delay(done, depth, start, delay):  # 随机延迟
    print('翻页数{}/{},已花费时间{:.2f}s'.format(done+1, depth, time.perf_counter()-start))
    time.sleep(delay*random.uniform(0.5, 1.5))  # 产生随机延迟


def save_to_csv(date_list):
    save = pandas.DataFrame(list(date_list))
    try:
        save.to_csv('热门电影影评数据爬取.csv', encoding='utf-8_sig', header=False, index=False)
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")


def main():
    start = time.perf_counter()
    datelist = []  # 数据列表
    head = ['scores', 'evaluate', 'times', 'votes', 'content', 'user_names']   # 数据标题
    datelist.append(head)
    depth = 11  # 爬取的页数 测试流浪地球短评只让爬到第11页，其后的页面要登陆
    delay = 0.2    # 延迟时间，最小为0
    start_url = "https://movie.douban.com/subject/26266893/comments?start="  # 链接前半部分
    end_url = '&limit=20&sort=new_score&status=P'    # 链接后半部分
    for i in range(depth):  # 翻页
        try:
            url = start_url + str(20 * i) + end_url  # 翻页操作
            html = getHTMLText(url)
            ye_mian_chu_li2(html, datelist)
            time_delay(i, depth, start, delay)      # 不需要延迟时间可直接去除
        except:
            continue  # 出问题则直接进行下一页面的解析
    save_to_csv(datelist)
    print('数据量：{}'.format(len(datelist)-1))
    print('程序完成爬取并存储，运行时间：{:.2f}s'.format(time.perf_counter()-start))


main()
