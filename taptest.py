import os
import time
import random

# ��Բ�ͬ�ֻ���ͬ��Ļ��Ҫ�Զ���,����ֻ�����ߵ�APP,Ҫ��ʹ����Ҫ���½����Զ���
# ��Ϊ P30,��ҫ20PRO
huawei = {
    # �������İ����Լ�����activity������,���Ի���app
    "appInfo": {
        "package": "com.catchers.viewkingdom.huawei",
        "activity": "com.catchers.viewkingdom.jrtt.SplashActivity",
    },
    # ����ƽ̨�İ�ť��Ļλ��
    # Ԥ��ֵ,���ֻ���ICONλ������
    # ��ǰ���λ�õ�����(X,Y)����Ϊ��λ,ȡȫ��,���Ͻ�Ϊ00��
    # �����ֵ��ڰ����Ĺ����Լ������ᶼ��Ҫ�����Զ���,����ʹ�����Լ��Ľ����߼�����������޸�
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
            # oppo��������֤
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

# ��������,����adb���ߵ�����λ��,�����ı���·���Լ���ͼ����ʼ�ļ���,�ǵ��Լ��޸�
enviroment = {"adb": "e:\\platform-tools", "savePath": "e:\\pws\\"}

# ���õ�ǰ���Ե�λ����Ϣ,�ֻ����,������Ļ�ֱ����Լ�����,�ߴ�,������ԭ��
# Ŀǰ����ƽ̨����Ϊ
#   huawei   (P30,��ҫ20PRO)
#   oppo     (A57)
# ע:PythonĬ�ϴ�����,����û��Ӳ��������
platform = huawei


def tap(activity, function, delay=2, offset=0):
    """
    # ͨ��adbģ����,����Ŀ���������������ƫ��(10������)
    :param activity: ��Ҫ����Ľ���
    :param function: ��Ҫ����Ķ�Ӧ�����µĹ��ܰ�ť
    :param delay: �����ȴ����ӳ�(��),�ȴ�����������Ӧ��ɶ�Ӧ�������
                  ���ղ�ͬ��������Ӧʱ���б仯
                  (Default value = 2)
    :param offset: ���ƫ�Ʒ�Χֵ(�������ط�Χ),
                   ʹ�õ��λ��λ��Ŀ��ֵ���趨�����������ȡ
                   (Default value = 0)
    """
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


def startApp(delay=10):
    """
    # ͸��ADB���ֻ��ϻ������
    :param delay: �ȴ��������Ϊ������ȫ�������
                  (Default value = 10)
    """
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
    """# ץȡ���������͵�����
    :param fileName: ָֻ���ļ���,
                     ����·����environmentȫ�ֱ���ָ��
                     (Default value = "screenshot.png")
    """
    global enviroment
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png {fileName}".format(
        fileName=enviroment["savePath"] + str(fileName)))


# �趨ADB����Ŀ¼
# �ȹرճ���,�Է�֮ǰ�����ĳ������
os.chdir(enviroment["adb"])

# ��������
startApp(10)

# ������Ϸ������,�����ʼ��ť,�������
tap("start", "startGame", 8)
tap("main", "adult")
tap("main", "monthAd")
# ѭ������200��,��������Ϊ��ѭ��ִ��ĳ�������л���д�ļ�Ӧ��,���ԽдԽ��ɴ��װһ��
for i in range(0, 200):
    print("��Round: " + str(i) + "��")
    # ץȡ���������͵�����
    # fileName = str(i) + ".png"
    # screencap(fileName)

    # ������������ץ��ʬ�����л�
    tap("main", "battle")
    tap("battle", "returnMain")

    # ������������ץ���������л�
    # tap("main", "factory")
    # tap("factory", "returnMain")

    # ����������������Σ�������л�
    # tap("main", "starwar")
    # tap("starwar", "returnMain")
