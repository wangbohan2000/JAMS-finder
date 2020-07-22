import os
import re
from queue import Queue
from threading import Lock
from typing import Dict

_login_addr = "/cgi-bin/gw.cgi?xml=%3Cjuan%20ver=%22%22%20squ=%22%22%20dir=%220%22%3E%3Crpermission%20usr=%22admin%22" \
              "%20pwd" \
              "=%22%22%3E%3Cconfig%20base=%22%22/%3E%3Cplayback%20base=%22%22/%3E%3C/rpermission%3E%3C/juan%3E&_" \
              "=1595317373323 "

example_url = "http://80.181.205.231:60001/"
pattern = re.compile(r'''type="password" id="dvr_pwd"''')
global_ip_q = Queue()
global_file_lock = Lock()
port = "60001"
data_file = os.path.join(os.path.expanduser('~'), "cam_ip.txt")


def login_path(url: str) -> str:
    return url + _login_addr


def header() -> Dict[str, str]:
    res = {}
    with open("../../../Desktop/新建文件夹/res/header", "r") as f:
        lines = f.readlines()
        for line in lines:
            kv = line.split(":")
            k = kv[0].strip()
            v = kv[1].strip()
            res[k] = v
    return res
