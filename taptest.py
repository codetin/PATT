import os
import time
import random

# 针对不同手机不同屏幕需要自定义,以下只是作者的APP,要想使用需要重新进行自定义
# 华为 P30,荣耀20PRO
huawei = {
    # 待测程序的包名以及启动activity的名称,用以唤起app
    "appInfo": {
        "package": "com.catchers.viewkingdom.huawei",
        "activity": "com.catchers.viewkingdom.jrtt.SplashActivity",
    },
    # 待测平台的按钮屏幕位置
    # 预设值,各手机的ICON位置坐标
    # 当前点击位置的坐标(X,Y)像素为单位,取全屏,左上角为00点
    # 所有字典内包含的功能以及坐标轴都需要重新自定义,按照使用者自己的界面逻辑和坐标进行修改
    "tapPos": {
        "start": {
            "startGame": [1170, 862]
        },
        "main": {
            "monthAd": [1522, 360],
            "battle": [2140, 970],
            "factory": [460, 970],
            "starwar": [1660, 970]
        },
        "battle": {
            "returnMain": [2140, 970]
        },
        "factory": {
            "returnMain": [175, 60]
        },
        "starwar": {
            "returnMain": [175, 60]
        }
    }
}

# OPPO A57
oppo = {
    "appInfo": {
        "package": "com.catchers.viewkingdom.nearme.gamecenter",
        "activity": "com.catchers.viewkingdom.jrtt.SplashActivity",
    },
    "tapPos": {
        "start": {
            "startGame": [762, 580]
        },
        "main": {
            "adult": [1013, 103],
            # oppo有年龄验证
            "monthAd": [992, 239],
            "battle": [1382, 652],
            "factory": [306, 652],
            "starwar": [1080, 652]
        },
        "battle": {
            "returnMain": [1340, 652]
        },
        "factory": {
            "returnMain": [118, 40]
        },
        "starwar": {
            "returnMain": [118, 40]
        }
    }
}

# 环境变量,配置adb工具的所在位置,截屏的保存路径以及截图的起始文件名,记得自己修改
enviroment = {"adb": "e:\\platform-tools", "savePath": "e:\\pws\\"}

# 设置当前测试的位置信息,手机相关,由于屏幕分辨率以及比例,尺寸,包名等原因
# 目前测试平台设置为
#   huawei   (P30,荣耀20PRO)
#   oppo     (A57)
# 注:Python默认传引用,所以没有硬拷贝开销
platform = huawei


# 通过adb模拟点击,会在目标点的上下左右随机偏移(10像素内)
# activity: 需要点击的界面
# function: 需要点击的对应界面下的功能按钮
# delay: 点击后等待的延迟(秒),等待程序作出响应完成对应点击操作,按照不同功能其响应时间有变化,默认设定2秒
# offset: 随机偏移范围值(正负像素范围),使得点击位置位于目标值的设定区间内随机点取
def tap(activity, function, delay=2, offset=0):
    global platform
    if function not in platform['tapPos'][activity]:
        print("{act} : {func} not exsit".format(act=activity, func=function))
        return
    position = (str(platform['tapPos'][activity][function][0] +
                    random.randint(-offset, offset)) + " " +
                str(platform['tapPos'][activity][function][1] +
                    random.randint(-offset, offset)))
    os.system("adb shell input tap {pos}".format(pos=position))
    print("tap {act} : {func} : {pos}".format(act=activity,
                                              func=function,
                                              pos=position))
    time.sleep(delay)


# 唤起程序
# delay: 等待几秒后认为程序完全启动完毕
def startApp(delay=10):
    os.system("adb devices")
    os.system("adb shell input keyevent 3")
    time.sleep(2)
    os.system("adb shell am force-stop {app}".format(
        app=platform['appInfo']['package']))
    time.sleep(2)
    os.system("adb shell am start -n {app}/{act}".format(
        app=platform['appInfo']['package'],
        act=platform['appInfo']['activity']))
    time.sleep(delay)


def screencap(fileName="screenshot.png"):
    # 抓取截屏并传送到本地
    global enviroment
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png {fileName}".format(
        fileName=enviroment["savePath"] + str(fileName)))


# 设定ADB工具目录
# 先关闭程序,以防之前残留的程序进程
os.chdir(enviroment["adb"])

# 启动程序
startApp(10)

# 进入游戏主界面,点击开始按钮,跳过广告
tap("start", "startGame", 8)
tap("main", "adult")
tap("main", "monthAd")
# 循环测试200次,本来就是为了循环执行某个界面切换而写的简单应用,结果越写越多干脆封装一下
for i in range(0, 200):
    print("「Round: " + str(i) + "」")
    # 抓取截屏并传送到本地
    # fileName = str(i) + ".png"
    # screencap(fileName)

    # 测试主界面与抓僵尸界面切换
    tap("main", "battle")
    tap("battle", "returnMain")

    # 测试主界面与抓工厂界面切换
    # tap("main", "factory")
    # tap("factory", "returnMain")

    # 测试主界面与星球危机界面切换
    # tap("main", "starwar")
    # tap("starwar", "returnMain")
