#tool
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import json
import datetime
import threading

# post 翻译
import hashlib
import base64
from Crypto.Cipher import AES  # pip install pycryptodome
from Crypto.Util.Padding import unpad





USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
]

headers = {'User-Agent': UserAgent().random,
    #'Cookie':'closeu4883316=%7B%22time%22%3A1674492704670%7D; __utmc=56961525; PHPSESSID=48c481b77957553dd8c89467251abf913fc0fadc; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1674492390; pm=; LastUrl=; __utma=56961525.1440023439.1674397148.1674485064.1674492388.7; __utmz=56961525.1674397148.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_213d524a1d07274f17dfa17b79db318f=1674397150; __bid_n=185d9d8f0f250db83b4207; FPTOKEN=/4F2ptU7OVeG3xjz5snAgvKjXQQz9UqPdL76G/B3jpT1TWQG4z7Tu2yJNxfPDB7hubeh4QdiSH50oOK3vAlyPXixzDbz3qITLfCpwa9v549GVLAhAq5QgjMxAaTPqSKCnt4B0QWWAlWnhMKBnlhk0/n78gNTCPTNjpOia5q40d+gHt0c0n//UKpOqiWURp9gQXT33hRJct4VWxwdjvhpLWNQq9nmF2BiReAGrHwYHkhal0ORMVP+1i9LpJDrwzLT7QSFie+uilyieQzwq29cIbYt53oJKJ3zOzx2OtQHYbE42+UltSZe+kOD0eoRvE1RR8MBSC8y4+b0OJWktNQhljmNtiqKhgE8vVjjR/AQsF0=|QpL0+jz0mPqD/Ug6VFupu2SBREsFXtrzrI8AO312G2s=|10|c97c2e47dd3ae9abce5c2b7a87118c76; FirstOKURL=https%3A//www.okooo.com/soccer/match/1195946/history/; First_Source=www.okooo.com; __utmb=56961525.3.9.1674492393947; LStatus=N; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%u652F%u4ED8%u5B9D%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%u4EBA%u4EBA%u7F51%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%u767E%u5EA6%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%u76DB%u5927%u767B%u5F55%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%22%22%2C%22loginSession%22%3A%22___GlobalSession%22%7D; acw_tc=2f624a0516744652547357096e5a8cfb2058bee732ba0416eb48b82e110346',
            }

# 获取free-proxy-list.net上的代理 一整页代理
def get_free_list():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    for row in soup.find('table', class_='table table-striped table-bordered').tbody.find_all('tr'):
        columns = row.find_all('td')
        ip_address = columns[0].text
        port = columns[1].text
        https = columns[6].text
        anonymity = columns[4].text
        if https == 'yes' and anonymity == 'elite proxy':
            proxies.append(f"{ip_address}:{port}")
    return proxies

# proxy-list.download 一整页代理 随机20个
def get_proxy_list():
    # 发送请求获取网页内容
    url ='https://www.proxy-list.download/api/v2/get?l=en&t=https'
    response = requests.get(url, headers={'User-Agent': UserAgent().random})
    if response.status_code == 200:
        # 解析网页内容
        #soup = BeautifulSoup(response.text, 'html.parser')
        data =json.loads(response.text)
        # 提取IP和端口
        ip_port_list = [ item['IP']+':'+item['PORT'] for item in data['LISTA']]
        if len(ip_port_list) >= 20:
            return random.sample(ip_port_list,20) #随机选20个
        else:
            return ip_port_list
    else:
        print('Failed to retrieve the webpage')
        print(response.status_code)


    return ip_port_list
        
# 66ip.cn 获取20个
def get_66_ip():
    # 发送请求获取网页内容 #20个
    url ='http://www.66ip.cn/nmtq.php?getnum=20&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
    response = requests.get(url, headers={'User-Agent': UserAgent().random})
    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取IP和端口
        ip_port_list = soup.text.split('\r\n')
        ip_port_list = ip_port_list[2:]
        ip_port_list = [item.strip() for item in ip_port_list]
    else:
        print('Failed to retrieve the webpage')
        print(response.status_code)
    return ip_port_list

# 开心代理 随机三页代理
def get_kx_ip():
    # 发送请求获取网页内容
    url ='http://www.kxdaili.com/dailiip/1/1.html'
    response = requests.get(url, headers={'User-Agent': UserAgent().random})
    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        url = soup.find('div', id='listnav')
        num = int(url.find_all('li')[-2].text)
        #print(num)
    else:
        print('Failed to retrieve the webpage')
        print(response.status_code)
    li = random.sample(range(1, num+1), 3)
    #print(li)
    ip_port_list = []
    for i in li:
        #time.sleep(1) #随机休眠0-0.3秒
        url = f'http://www.kxdaili.com/dailiip/1/{i}.html' #f {i}表示格式化字符串
        response = requests.get(url, headers={'User-Agent': UserAgent().random})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取IP和端口
            ip_table = soup.find('table', class_='active')
            ip_rows = ip_table.find_all('tr')
            ip_rows = ip_rows[1:]
            #遍历表格中的每一行
            for row in ip_rows:
                # 提取IP和端口号，这里需要根据实际页面结构进行调整
                #print(row)
                tds = row.find_all('td')
                #print(tds[4].text[0])
                if tds[3].text == 'HTTP,HTTPS' and tds[4].text[0] in ['1','2','0']:
                    ip = tds[0].text
                    #print(ip)
                    port = tds[1].text
                    ip_port_list.append(f"{ip}:{port}")
        else:
            print('Failed to retrieve the webpage')
            print(response.status_code)

    #print(ip_port_list)
    return ip_port_list

# 小幻代理 20个
def get_ihuan_ip():
    Y = datetime.datetime.now().strftime('%Y')
    M = datetime.datetime.now().strftime('%m')
    D = datetime.datetime.now().strftime('%d')
    H = datetime.datetime.now().strftime('%H')
    t = Y +'/'+M+'/'+D+'/'+ H
    # 发送请求获取网页内容
    url ='https://ip.ihuan.me/today/'+t+'.html'

    response = requests.get(url, headers={'User-Agent':UserAgent().random})
    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取IP和端口
        soup=soup.find('p', class_='text-left')
        ip_port_list=[]
        #print(soup)
        for i in soup:
            if '#支持HTTPS#支持POST' in i and '#[高匿]' in i and ':' in i:
                ip_port_list.append(str(i).split('@')[0])
        if len(ip_port_list) >= 20:
            return random.sample(ip_port_list,20) #随机选20个
        else:
            return ip_port_list
    else:
        print('Failed to retrieve the webpage')
        print(response.status_code)
    return ip_port_list

#  站大爷一页  选择了 响应时间3s内，存活时间1h以上，高匿 支持https,支持post,排序方式为响应时间从小到大（概率爬取）
def get_zdy_ip():
    # 目标网站的URL
    url = 'https://www.zdaye.com/free/?ip=&adr=&checktime=&sleep=2&cunhuo=3&dengji=1&nadr=&https=1&yys=&post=%E6%94%AF%E6%8C%81&px=3'
    response = requests.get(url= url,headers= {'User-Agent': UserAgent().random,}) #params 表示URL中的参数
    #print(response.text)
    #检查请求是否成功
    if response.status_code == 200:
        # 解析HTML内容
        soup = BeautifulSoup(response.content, 'html.parser')
        ip_port_list=[]
        ip_table = soup.find('table', id='ipc')
        ip_rows = ip_table.find_all('tr')
        #遍历表格中的每一行
        for row in ip_rows:
            # 提取IP和端口号，这里需要根据实际页面结构进行调整
            tds = row.find_all('td')
            #print(tds)
            ip = tds[0].text
            port = tds[1].text
            ip_port_list.append(f"{ip}:{port}")
        #print(ip_port_list)
        return ip_port_list
    else:
        print('Failed to retrieve the webpage')
        print(response.status_code)


## 弃用
def test_proxies(proxies):
    print(len(proxies))
    to_delete = []  # 存储需要删除的代理索引
    busy_time = []
    for i in range(len(proxies)):
        print(proxies[i])
        #retry_count = 1
        r = None
        next =0
        #while(retry_count > 0):
        try:
            start = time.time()  #timeout = 5表示5秒内没有响应就超时 进入except
            r = requests.get(url='https://www.example.com', headers={'User-Agent': UserAgent().random,}, proxies={"http": "http://{}".format(proxies[i])},timeout=5)
            end = time.time()
            t = end - start
            busy_time.append(t)
            if  t > 3:  # 如果响应时间超过3秒
                to_delete.append(i)  # 添加索引到删除列表
                next =1
                continue  # 继续下一个代理
            break
        except Exception as e:
            end = time.time()
            t = end - start
            busy_time.append(t)
            to_delete.append(i)
            #retry_count -= 1
            next =1
            continue
            # print(e)
    if r is not None and r.status_code == 200 and next ==0:
        r.encoding = r.apparent_encoding  # 解决乱码问题
        page = r.text
        soup = BeautifulSoup(page, 'lxml')
        title = soup.find('h1').text
        if title == 'Example Domain':
            print('Success:', proxies[i], '响应时间:', t)
        else:
            to_delete.append(i)  # 添加索引到删除列表


    print(to_delete)
    print(busy_time)
    print(proxies)
    # 创建一个新列表，不包含to_delete中的位置
    busy_time = [busy_time[i] for i in range(len(busy_time)) if i not in to_delete]
    new_proxies =[proxies[i] for i in range(len(proxies)) if i not in to_delete]
    print("-----")
    print(new_proxies)
    print(busy_time)
    # 使用zip函数将两个列表合并，并根据数值排序
    sorted_pairs = sorted(zip(busy_time, new_proxies))

    # 解压缩排序后的列表，获取排序后的IP地址
    sorted_ips = [ip for _, ip in sorted_pairs]
    print(sorted_ips)

    #print(sorted_ips)
    return sorted_ips


# 测试代理的函数
def test_connection(IP):
    length = len(IP)
    print(length)
    # 创建一个空字典来存储代理及其响应时间
    proxy_response_times = {}
    
    for i in range(length):
        try:
            # 记录请求开始的时间
            start_time = time.time()
            # 发送带有负载的GET请求
            r = requests.get('https://www.example.com', proxies={"http": "http://{}".format(IP[i])}, headers={'User-Agent': UserAgent().random}, timeout=10)
            # 计算响应时间
            response_time = time.time() - start_time
            # 如果请求成功，将代理和响应时间添加到字典中
            if r.status_code == 200:
                r.encoding = r.apparent_encoding  # 解决乱码问题
                page = r.text
                soup = BeautifulSoup(page, 'lxml')
                title = soup.find('h1').text
                if title == 'Example Domain' :
                    if response_time < 3: #比加入 and快
                        print(f"获取数据成功，ip: {IP[i]}, 响应时间: {response_time:.3f}秒")
                        proxy_response_times[IP[i]] = response_time
            else:
                print(f"获取数据失败，状态码: {r.status_code}")
        except Exception as e:
            print(e)
    
    # 根据响应时间对代理进行排序，从快到慢
    sorted_proxies = sorted(proxy_response_times.items(), key=lambda item: item[1])  # 1表示按值排序，0表示按键排序

    print(len(sorted_proxies))
    s_proxies =[]
    # 打印排序后的代理列表
    for proxy, t in sorted_proxies:
        s_proxies.append(proxy)
        print(f"{proxy}: {t:.3f}秒")
    return s_proxies

# 测试单个
# Function to test a single proxy
def test_proxy(IP, proxy_response_times, lock, MAX_Times):
    try:
        # Record the start time
        start_time = time.time()
        for j in range(MAX_Times):
            # Send a GET request with payload
            r = requests.get('https://www.example.com', proxies={"http": f"http://{IP}"}, headers={'User-Agent': UserAgent().random,}, timeout=5)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding  # Solve garbled characters
                page = r.text
                soup = BeautifulSoup(page, 'lxml')
                title = soup.find('h1').text  # Generally, if the h1 tag is not found here, it will report an error and enter except
                if title == 'Example Domain':
                    if (j+1) % 10 == 0:
                        print("success", j+1, IP)
            else:
                print(f"Failed to fetch data, status code: {r.status_code}")
        # Calculate the response time
        response_time = (time.time() - start_time) / 40
        # Store the proxy and its response time in the dictionary
        if response_time < 2:
            with lock: #使用锁
                proxy_response_times[IP] = response_time
    except Exception as e:
        print(e)

# 压力测试 启用线程测试多个
# Main function to test a list of proxies
def test_pressure(IP, MAX_Times = 40):
    length = len(IP)
    print(length)
    proxy_response_times = {}
    threads = []
    lock = threading.Lock() #创建锁

 # 每16个线程一次
    for i in range(0, length, 16):  # 每次处理16个IP
        # 创建并启动每个代理的线程
        for j in range(i, min(i + 16, length)):  # 确保不会超出IP列表的范围
            t = threading.Thread(target=test_proxy, args=(IP[j], proxy_response_times, lock, MAX_Times))
            threads.append(t)
            t.start()

        # 等待当前批次的16个线程完成
        for t in threads[i:i + 16]:  # 只等待当前批次的线程
            t.join()  # 等待所有线程结束
        print(f"第{i//16+1}批次线程已完成")

    # Sort the proxies by response time, from fastest to slowest
    sorted_proxies = sorted(proxy_response_times.items(), key=lambda item: item[1])
    s_proxies =[]
    # Print the sorted list of proxies
    for proxy, t in sorted_proxies:
        print(f"{proxy}: {t:.3f}秒")
        s_proxies.append(proxy)
    return s_proxies

# 测试post
 
class YoudaoTranslate(object):
    #初始化参数
    def __init__(self):
        #请求的url
        self.url="https://dict.youdao.com/webtranslate"
        #封装请求头，要求和网易请求一致
        self.headers={
        "Cookie":'OUTFOX_SEARCH_USER_ID_NCOO=1948382659.381789; OUTFOX_SEARCH_USER_ID=1775497575@183.219.26.105; __yadk_uid=5QwMgTGcByPM5Fdhip58d5m1lBPBpGCW; rollNum=true; ___rl__test__cookies=1708157820132',
        "Referer": "https://fanyi.youdao.com/",
        "User-Agent": UserAgent().random    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
 
    #该函数用于封装data
    def make_Data(self):
        e = str(int(time.time()*1000))
        t= 'fsdsogkndfokasodnaso'
        u = "fanyideskweb"
        d = "webfanyi"
        string ='client={u}&mysticTime={e}&product={d}&key={t}'.format(u=u,e=e,d=d,t=t)
        sign=hashlib.md5(string.encode()).hexdigest()
        return e,sign
 
    #该函数用于请求翻译结果
    def translate(self,text,ip = None):
        e,sign=self.make_Data()
        #定义data
        data = {
            'i': text,
            'from': 'auto',
            'to': '',
            'dictResult': 'true',
            'keyid': 'webfanyi',
            'sign': sign,
            'client': 'fanyideskweb',
            'product': 'webfanyi',
            'appVersion': '1.0.0',
            'vendor': 'web',
            'pointParam':'client,mysticTime,product',
            'mysticTime': e,
            'keyfrom': 'fanyi.web',
            'mid':'1',
            'screen':'1',
            'model':'1',
            'netword':'wifi',
            'abtest':'0',
            'yduuid':'abcdefg',
        }
        #用post做请求,获得json输出，便于我们提取数据
        #请求结果格式为：{"code":0,"dictResult":{"ec":{"exam_type":["初中","高中","CET4","CET6","考研"],"word":{"usphone":"ˈæp(ə)l","ukphone":"ˈæp(ə)l","ukspeech":"apple&type=1","trs":[{"pos":"n.","tran":"苹果"}],"wfs":[{"wf":{"name":"复数","value":"apples"}}],"return-phrase":"apple","usspeech":"apple&type=2"}}},"translateResult":[[{"tgt":"苹果","src":"apple","tgtPronounce":"pín guŏ"}]],"type":"en2zh-CHS"}
        if ip:
            response=requests.post(url=self.url,data=data,headers=self.headers,proxies={"http": f"http://{ip}"}).text
        else:
            response=requests.post(url=self.url,data=data,headers=self.headers).text
        result = self.encryptdata(response)
        result = json.loads(result)['translateResult'][0][0]['tgt']
        return result
 
   #入口函数
    def run(self):
        text=input("输入被翻译内容：")
        result=self.translate(text)
        print("翻译结果为：",result)

    def test(self,ip = None):
        text = '你好'
        result = self.translate(text,ip)
        return result
        #print(result)

    def b(self,e):
        return hashlib.md5(e.encode()).digest() #.digest()返回二进制的值

    # 数据解密
    def encryptdata(self,t):
        o = 'ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl'
        n = 'ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4'
        a = self.b(o)[:16] # 取前16位
        i = self.b(n)[:16] # 取前16位
        r = AES.new(a, AES.MODE_CBC, i) #创建一个AES对象（密钥，模式，偏移量）aes.MODE_CBC是加密模式,a表示密钥，i表示偏移量
        s = r.decrypt(base64.urlsafe_b64decode(t))#解码为原始的字节串 
        return unpad(s, AES.block_size).decode('utf-8')# AES.block_size = 16 ,解密后去掉填充的字符 返回解密后的字符串
    # 例子
    # translate=YoudaoTranslate()
    # print(translate.test(ip ='36.6.144.112:8089'))

def test_post(IP):
    s_proxies =[]
    translate=YoudaoTranslate()
    for i in range(len(IP)):
        try:
            if translate.test(ip =IP[i]) == 'hello.':
                print(IP[i],"post success")
                s_proxies.append(IP[i])
        except Exception as e:
            print(e)
    return s_proxies
