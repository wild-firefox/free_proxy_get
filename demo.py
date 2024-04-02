def open_proxy():
    with open('./free_proxy_get/proxy.txt', 'r') as f:
        #一行一行读取
        ip = [line.strip() for line in f]
    return ip

if __name__ == '__main__':
    ip = open_proxy()
    print(ip)
    pass