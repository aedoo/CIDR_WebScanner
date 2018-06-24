#coding:utf-8
#code by yangguang

import socket,requests
import threading,Queue
import sys,ipaddr
import time

Port = (80,81,82,88,90,91,443,5000,5001,7001,8000,8001,8009,8080,8081,8088,8089,8443,8888,9000,9001,9090)   #此处放置默认扫描的Web端口

headers = {
    "Accept":"application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
    "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Content-Type":"application/x-www-form-urlencoded"
}

class PortScan(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):

        while True:

            if self._queue.empty():
                break

            try:

                ip = str(self._queue.get(timeout=5))

                for port in Port:
                    addr = (ip, port)
                    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

                    try:
                        s.settimeout(5)
                        s.connect(addr)

                        try:
                            if int(port) == 443:
                                url = 'https://' + str(ip)

                            elif int(port) == 8443:
                                url = 'https://' + str(ip) + ':' + str(port)

                            else:
                                url = 'http://' + str(ip) + ':' + str(port)

                            r = requests.get(url=url,headers=headers,timeout=5)

                            # banner = 'Not Found'

                            # try:
                            #     banner = r.headers['Server']
                            # except:
                            #     pass

                            status = r.status_code

                            if status:
                                sys.stdout.write("%-27s\n" % (url))

                        except Exception:
                            pass

                    except:
                        s.close()
                        continue
            except Exception:
                pass
def main():
    if len(sys.argv) != 2:
        print 'Usage: python webscan.py 192.168.1.1/24'
    else:
        time_start = time.time()
        threads = []
        thread_count = 200        #线程数
        queue = Queue.Queue()
        cidrip = sys.argv[1]      #接收输入IP段
        ips = ipaddr.IPNetwork(cidrip)

        for ip in ips:
            queue.put(ip)

        for i in xrange(thread_count):
            threads.append(PortScan(queue))

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        print 'ALL Finished, Running Time:' + str(time.time() - time_start)

if __name__ == '__main__':
    main()