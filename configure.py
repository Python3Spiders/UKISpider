import os

# 平台
PLATFORM = 'Android'

# 设备名称 通过 adb devices -l 获取
DEVICE_NAME = 'HUAWEI_TAG_AL00'

# APP包名
APP_PACKAGE = 'cn.neoclub.uki'

# 入口类名
APP_ACTIVITY = '.home.SplashActivity'

# Appium地址
DRIVER_SERVER = 'http://localhost:4723/wd/hub'
# 等待元素加载时间
TIMEOUT = 300

# uki手机号密码
PHONE_NUMBER = '你的手机号'
PASSWORD = '你的密码'

# 滑动点
FLICK_START_X = 100
FLICK_START_Y = 100
FLICK_DISTANCE = 800

# MongoDB配置
MONGO_URL = 'localhost'
MONGO_DB = 'uki'
MONGO_TABLE = 'uki'

# 滑动间隔
SCROLL_SLEEP_TIME = 0.2

# platformName : Android
# deviceName : HUAWEI_TAG_AL00
# appPackage : com.tencent.mm
# appActivity : .ui.LauncherUI