# -*-encoding: utf-8-*-

import os
import json
import time
import random
import logging
import requests

from locust import HttpLocust, TaskSet, task

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S'
                    )

# 创建普通账户的数量
ACCOUNT_NUM = 1000

# rpc接口
RPC_URL = 'http://127.0.0.1:6765'


def account_read():
    try:
        with open('account.txt', 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def accounts_write(data_list):
    with open('account.txt', 'a') as f:
        data_list = ["{}\n".format(i) for i in data_list]
        f.writelines(data_list)


def account_init():
    account_current_list = [i.strip() for i in account_read() if i.strip()]
    account_save_list = []
    data = {
        "action": "account_create",
        "password": "12345678"
    }
    create_num = ACCOUNT_NUM + 1 if account_current_list == [] else ACCOUNT_NUM
    while create_num:
        html = requests.post(url=RPC_URL, data=json.dumps(data))
        if html.status_code == 200:
            json_data = json.loads(html.text)
            if json_data['code'] == 0:
                account_save_list.append(json_data['account'])
                create_num -= 1
    accounts_write(account_save_list)

    account_current_list = [i.strip() for i in account_read() if i.strip()]
    # 往第一个账户转10000000czr
    src = "czr_33EuccjKjcZgwbHYp8eLhoFiaKGARVigZojeHzySD9fQ1ysd7u"
    account = account_current_list[0]
    logging.debug('往发钱账户打钱')
    transfer_accounts(src, account, 10000000)
    time.sleep(15)

    # 往用户账户转10czr
    user_account_list = account_current_list[1:]
    logging.debug('往用户账户打钱')
    for dst in user_account_list:
        transfer_accounts(account, dst, 10)
    time.sleep(15)


def account_import():
    data = {
        "action": "account_import",
        "json": "{\"account\":\"czr_33EuccjKjcZgwbHYp8eLhoFiaKGARVigZojeHzySD9fQ1ysd7u\",\"kdf_salt\":\"774DDE2B6D01D6A2B000BB42F8118E2C\",\"iv\":\"5EF469016DB117B4437FB46D37BFA925\",\"ciphertext\":\"2B9567F4184B4D0A4AD9D5A3BF94805662B562167AFBEC575B06C23F708F0CA0\"}"
    }
    html = requests.post(url=RPC_URL, data=json.dumps(data))
    if html.status_code == 200:
        json_data = json.loads(html.text)
        if json_data['code'] != 0:
            logging.error("code: {} \nmsg: {}".format(json_data['code'], json_data['msg']))


def transfer_accounts(src, dst, coin):
    account_import()
    data = {
        "action": "send_block",
        "from": src,
        "to": dst,
        "amount": str(coin * 10 ** 18),
        "password": "12345678",
        "data": "",
        "need_wait": "1",
        "gas": 60000,
        "gas_price": "10000001"
    }
    html = requests.post(url=RPC_URL, data=json.dumps(data))
    if html.status_code == 200:
        json_data = json.loads(html.text)
        if json_data['code'] != 0:
            logging.error("code: {} \nmsg: {}".format(json_data['code'], json_data['msg']))


def account_balance(account):
    data = {
        "action": "account_balance",
        "account": account
    }
    html = requests.post(url=RPC_URL, data=json.dumps(data))
    if html.status_code == 200:
        json_data = json.loads(html.text)
        logging.debug(json_data)


def randint_two(size):
    while True:
        a = random.randint(0, size - 1)
        b = random.randint(0, size - 1)
        if a != b:
            return a, b


class UserBehavior(TaskSet):
    @staticmethod
    def account_list_read():
        return account_read()
        
    @task
    def test_transfer_accounts(self):
        user_account_list = UserBehavior.account_list_read()
        size = len(user_account_list)
        a, b = randint_two(size)
        coin = random.randint(1, 100)
        data = {
            "action": "send_block",
            "from": user_account_list[a],
            "to": user_account_list[b],
            "amount": str(coin * 10 ** 15),
            "password": "12345678",
            "data": "",
            "need_wait": "1",
            "gas": 60000,
            "gas_price": "10000001"
        }
        html = self.client.post(url='/', data=json.dumps(data))
        if html.status_code == 200:
            json_data = json.loads(html.text)
            if json_data['code'] != 0:
                print("error: \n\tcode: {} \n\tmsg: {}".format(json_data['code'], json_data['msg']))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    host = RPC_URL


if __name__ == "__main__":
    account_init()
    master_ip = "172.17.184.78"
    os.system("locust -f locust_test.py --slave --master-host={}".format(master_ip))






