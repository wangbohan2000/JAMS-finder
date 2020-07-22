import re
import sys
from concurrent.futures.thread import ThreadPoolExecutor

import requests

from jams_finder.config import global_ip_q, login_path, port, header, global_file_lock, data_file


def print_safe(msg):
    sys.stdout.write(f"{msg}\n")


def validate_login(url, headers):
    resp = requests.get(url, headers=headers, timeout=20)
    return re.search(r'''errno="0"''', resp.content.decode("UTF-8")) is not None


def put_ip():
    for i in range(1, 255):
        for j in range(0, 255):
            for k in range(0, 255):
                for x in range(0, 254):
                    global_ip_q.put(f"{i}.{j}.{k}.{x}")


def spider():
    while True:
        if not global_ip_q.empty():
            ip = global_ip_q.get()
            to_login = login_path("http://" + ip + ":" + port)
            try:
                if validate_login(to_login, headers=header()):
                    print_safe(f" [*] 验证成功 {ip} {port}")
                    write_line(ip)
                else:
                    print_safe(f" [*] 验证失败 {ip} {port}")
            except OSError:
                print_safe(f"请求地址无效 {ip} {port}")
            except Exception:
                print_safe("出现未知异常")


def write_line(msg: str, file=data_file):
    global_file_lock.acquire()
    with open(file, "a") as f:
        f.write(msg + "\n")
        f.flush()
    global_file_lock.release()


def main():
    pool = ThreadPoolExecutor(max_workers=100)
    pool.submit(put_ip)
    while True:
        pool.submit(spider)


if __name__ == '__main__':
    main()
