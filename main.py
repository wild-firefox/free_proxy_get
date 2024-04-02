#import sys
from utils import get_free_list, get_proxy_list, get_66_ip, get_kx_ip,get_ihuan_ip,get_zdy_ip,test_connection,test_pressure,test_post
import random
import datetime



def random_proxy():
    func_inland =[get_free_list, get_proxy_list]
    func_outland =[get_66_ip, get_kx_ip, get_ihuan_ip, get_zdy_ip]
    # 从代理池中随机获取一个代理
    D = int(datetime.datetime.now().strftime('%d'))
    if D % 2 == 0:
        ip =get_zdy_ip
    else:
        ip =[]
        pass
    ip_i = random.choice(func_inland)()+ip
    ip_o = random.choice(func_outland)()+ip
    return ip_i+ip_o

def save_proxy(ip):
    #如果没有此文件就创建一个
    print(ip)
    with open('./proxy.txt', 'w') as f:
        for i in ip:
            f.write(i+'\n') 
    #在当前文件夹也保存一份(可选，为了方便)
    # with open('proxy.txt', 'w') as f:
    #     for i in ip:
    #         f.write(i+'\n') 
def open_proxy():
    with open('./proxy.txt', 'r') as f:
        #一行一行读取
        ip = [line.strip() for line in f]
    return ip



def main():
    ip = open_proxy() #1.打开已经保存的代理，若少于6个则重新获取
    if len(ip) == 0:
        ip = random_proxy()
    ip = test_connection(ip) #2.测试https
    ip = test_post(ip) #3.测试post(可选)
    ip = test_pressure(ip,40) #4.测试压力 max =40
    save_proxy(ip)#5.保存代理 从快到慢排


if __name__ == '__main__':
    main()




