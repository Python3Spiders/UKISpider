# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_date:      2019/3/2
# file_name:        uki_scrapy.py
# github            https://github.com/inspurer
# qq_mail           2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

# pip install Appium-Python-Client
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from time import sleep
from configure import *
import re


class UKI():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.client = MongoClient(MONGO_URL, connect=False)
        self.db = self.client[MONGO_DB]
        self.table = self.db[MONGO_TABLE]

    def spilt_emoji(self,string):
        return re.sub("#[0-9]{5}","",re.S)

    def login(self):
        """
        登录 uki
        :return:
        """
        # 欢迎页iv按钮
        button_splash = self.wait.until(EC.presence_of_element_located((By.ID, 'cn.neoclub.uki:id/app_start')))
        button_splash.click()
        # 手机输入
        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'cn.neoclub.uki:id/et_input_phone')))
        phone.set_text(PHONE_NUMBER)

        tip = self.wait.until(EC.presence_of_element_located((By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.TextView[1]")))
        tip.click()

        # 下一步
        next = self.wait.until(EC.element_to_be_clickable((By.ID, 'cn.neoclub.uki:id/tv_next')))
        next.click()
        # 密码
        password = self.wait.until(
            EC.presence_of_element_located((By.ID, 'cn.neoclub.uki:id/et_input_pwd')))
        password.set_text(PASSWORD)
        # 登录提交
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'cn.neoclub.uki:id/tv_next')))
        submit.click()


    def enter(self):
        """
        进入动态广场
        :return:
        """
        # community = self.wait.until(
        #     EC.presence_of_element_located((By.ID, 'cn.neoclub.uki:id/iv_community')))
        community = self.wait.until(EC.presence_of_element_located((By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.LinearLayout/android.widget.ImageView[2]')))
        community.click()
    
    def crawl(self):
        """
        爬取
        :return:
        """
        while True:
            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.view.View/android.support.v4.view.ViewPager/android.view.View/android.support.v7.widget.RecyclerView/android.view.View')))
            # 上滑
            print(len(items))
            # 遍历每条状态
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('cn.neoclub.uki:id/tv_name').get_attribute('text')

                    print("nk",nickname)

                    age = item.find_element_by_id('cn.neoclub.uki:id/tv_gender').get_attribute('text')

                    print("age",age)

                    content = item.find_element_by_id('cn.neoclub.uki:id/expandable_text').get_attribute('text')

                    print("content",content)

                    data = {
                        'nickname': nickname,
                        'content': content,
                        'age': age,
                    }
                    # 插入MongoDB
                    result = self.table.update({'nickname': nickname}, {'$set': data}, True)
                    if result["ok"] == 1:
                        print("sucess insert")
                    sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                    print("element not found")
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)

    def main(self):
        """
        入口
        :return:
        """
        # 登录
        self.login()
        # 进入动态广场
        self.enter()
        # 爬取
        self.crawl()


if __name__ == '__main__':
    uki = UKI()
    uki.main()
