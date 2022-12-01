import cv2
import pynvml
import numpy as np
import os
import sys
import time
import random
import datetime
import win32api
import win32gui
import win32con
import logging
from os import path
from PIL import ImageGrab
from GetKeys import key_check
from skimage.metrics import structural_similarity


# 远程启动模拟器游戏
def RemoteStartGame(android):
    print("ACTION: 启动游戏")
    android.start_app('com.sunborn.girlsfrontline.cn')


# 远程关闭模拟器游戏
def RemoteCloseGame(android):
    print("ACTION: 关闭游戏")
    android.stop_app('com.sunborn.girlsfrontline.cn')


class BaseAutoGFL:
    # 游戏基本参数常量
    def __init__(self):
        self.app_dir = r'D:\Program Files (x86)\mumu\emulator\nemu\EmulatorShell\NemuPlayer.exe'  # 模拟器所在分区路径
        self.windowName = "少女前线 - MuMu模拟器"
        self.windowNameDesktop = "MuMu模拟器"
        self.paused = False  # 暂停脚本进程

        self.IMAGE_PATH = 'D:/Repositories/Auto-Girls-Frontline/autoIntegrationEdition/initial_IMG/'  # 读取截图路径
        self.SIMULATOR_WIDTH = 750  # 模拟器总宽度
        self.SIMULATOR_HEIGHT = 589  # 模拟器总高度
        self.BOX_TOP = 37  # 画面边框顶部到模拟器顶部的距离
        self.BOX_BOTTOM = 52  # 画面边框底部到模拟器底部的距离

        # 图像状态判断区域 #
        self.DESKTOP_IMAGE_BOX = [75, 80, 165, 170, 'desktop.png']  # 模拟器桌面状态判断区域
        self.FIRST_LOGIN_IMAGE_BOX = [675, 77, 690, 90, 'first_login.png']  # 每日第一次登录弹出活动对话框状态判断区域
        self.L_SUPPORT_IMAGE_BOX = [85, 44, 187, 74, 'L_support.png']  # 后勤完成界面判断区域
        self.MAIN_MENU_IMAGE_BOX = [472, 269, 562, 304, 'main_menu.png']  # 主界面判断区域
        self.NAVIGATE_IMAGE_BOX = [109, 15, 136, 40, 'navigate.png']  # 导航条判断区域

        # 控制动作区域 #
        # 安全机制触发
        self.SAVE_MODE_CLICK_BOX = [0, 0, 750, 500]  # 安全机制尝试触发战斗中断

        # 启动游戏
        self.START_GAME_STEP1_CLICK_BOX = [98, 96, 130, 124]  # 点击图标启动游戏
        self.START_GAME_STEP2_CLICK_BOX = [210, 127, 450, 350]  # 点击一次画面
        self.START_GAME_STEP3_CLICK_BOX = [210, 127, 450, 350]  # 点击画面开始

        # 关闭游戏
        self.CLOSE_GAME_CLICK_BOX = [393, -25, 401, -13]  # 关闭模拟器中游戏进程

        # 每日首次登陆确认活动消息
        self.CHECK_INFORMATION_CLICK_BOX = [195, 322, 202, 334]  # 勾选今日不再弹出(deprecated)
        self.CONFIRM_INFORMATION_CLICK_BOX = [675, 77, 690, 90]  # 点击关闭活动框
        self.CONFIRM_REGISTRATION_CLICK_BOX = [36, 12, 55, 30]  # 点击关闭签到框

        # 后勤支援归来确认
        self.L_SUPPORT_STEP1_CLICK_BOX = [639, 432, 696, 439]  # 确认后勤完成
        self.L_SUPPORT_STEP2_CLICK_BOX = [397, 319, 476, 342]  # 再次派出

        # 战役结算
        self.COMBAT_END_CLICK_BOX = [360, 10, 390, 21]  # 战役结算，需要偏右，否则捞出人形会点到分享按钮

    # 脚本进程的扉页（其实就是倒计时XD
    @staticmethod
    def preface():
        # 进行倒计时由x秒开始
        for x in range(3, -1, -1):
            mystr = ">>> " + str(x) + "s 后将开始操作，请切换至模拟器界面"
            print(mystr, end="")
            print("\b" * (len(mystr) * 2), end="", flush=True)
            time.sleep(1)
        print("开始操作")

    def getClassAttr(self):
        for attr in dir(BaseAutoGFL()):
            if "_CLICK_BOX" in attr:
                value = self.__getattribute__(attr)
                print("{} 坐标值: {}".format(attr, value))
            if "_IMAGE_BOX" in attr:
                value = self.__getattribute__(attr)
                print("{} 坐标值: {}".format(attr, value))

    # 权重单位换算（像素具体值坐标->像素百分比坐标）
    def trans(self, box):
        b_box = [box[0] / self.SIMULATOR_WIDTH,
                 (box[1] + self.BOX_TOP) / self.SIMULATOR_HEIGHT,
                 box[2] / self.SIMULATOR_WIDTH,
                 (box[3] + self.BOX_TOP) / self.SIMULATOR_HEIGHT]
        # print(box)
        return b_box

    # （测试用）
    def transback(self, box):
        print("原始像素坐标:")
        print(box)
        box[0] = int(box[0] * self.SIMULATOR_WIDTH)
        box[1] = int(box[1] * self.SIMULATOR_HEIGHT - self.BOX_TOP)
        box[2] = int(box[2] * self.SIMULATOR_WIDTH)
        box[3] = int(box[3] * self.SIMULATOR_HEIGHT - self.BOX_TOP)
        print(box)

    # 脚本前期制作状态机所需状态图像集
    def saveStatusImage(self, CONSTANT_IMAGE_BOX):
        image_box = self.trans(CONSTANT_IMAGE_BOX)  # 转换为百分比坐标
        capImage = self.getImage(image_box)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        cv2.imwrite('./initial_IMG/' + CONSTANT_IMAGE_BOX[4], capImage)
        print("状态图像保存成功")

    # 随机等待一段时间,时间控制在minTime至maxTime之间
    def wait(self, minTime, maxTime):
        waitTime = minTime + (maxTime - minTime) * random.random()
        time.sleep(waitTime)

    # 获取模拟器窗口坐标数据
    def getWindowData(self):
        hwnd = win32gui.FindWindow(None, self.windowName)  # 根据窗口名称找到窗口句柄
        hwnd_desktop = win32gui.FindWindow(None, self.windowNameDesktop)
        if hwnd == 0 and hwnd_desktop == 0:
            print("未找到窗口界面,程序将自动退出！")
            exit(0)
        elif hwnd != 0:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口的位置数据
        elif hwnd_desktop != 0:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd_desktop)  # 获取窗口的位置数据
        width = right - left
        height = bottom - top
        return [left, top, right, bottom, width, height]

    # 获取游戏画面内指定区域box的截图
    def getImage(self, box):
        # windowData = [left,top,right,bottom,width,height]
        windowData = self.getWindowData()
        imgLeft = windowData[0] + int(windowData[4] * box[0])
        imgTop = windowData[1] + int(windowData[5] * box[1])
        imgRight = windowData[0] + int(windowData[4] * box[2])
        imgBottom = windowData[1] + int(windowData[5] * box[3])
        img = ImageGrab.grab((imgLeft, imgTop, imgRight, imgBottom))
        return img

    # 比较两图片吻合度/置信度，结构相似性比较法（真的好用）
    def imageCompare(self, img1, img2):
        gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # ground_truth img
        gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # test img
        (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
        return score > 0.95

    # 点击box内随机一点，如果提供具体xy偏量，则点击精确的点
    def mouseClick(self, box, minTime, maxTime, exact_x=0, exact_y=0):
        # box参数 : [left,top,right,bottom] #
        box = self.trans(box)  # 转换为百分比坐标
        windowData = self.getWindowData()
        width = box[2] - box[0]
        height = box[3] - box[1]
        if exact_x == 0 and exact_y == 0:
            clickX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width * random.random())
            clickY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
        else:
            clickX = windowData[0] + int(windowData[4] * box[0]) + exact_x
            clickY = windowData[1] + int(windowData[5] * box[1]) + exact_y
        clickPos = (clickX, clickY)
        win32api.SetCursorPos(clickPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        self.wait(minTime, maxTime)

    # 模拟鼠标拖动，box为起始区域,times为拖动次数,distance为单次拖动距离
    # dx,dy为组成移动方向向量，frame_interval为鼠标拖动帧间隔,越小鼠标拖动越快
    # multi_interval为连续拖动时的时间间隔
    def mouseDrag(self, box, dx, dy, times, distance, frame_interval, multi_interval):
        box = self.trans(box)  # 转换为百分比坐标
        windowData = self.getWindowData()
        width = box[2] - box[0]
        height = box[3] - box[1]
        for i in range(times):
            dragX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width * random.random())
            dragY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
            dragPos = (dragX, dragY)
            win32api.SetCursorPos(dragPos)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            for i in range(distance):
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
                time.sleep(frame_interval)
            time.sleep(0.2)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(multi_interval)

    # 释放GPU显存占用，防止因内存占用满而导致模拟器崩溃
    def freeGraphicProcessUnitMemory(self):
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # GPU编号
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem_usage = mem_info.free / mem_info.total  # 显存占用比

        mem_total = np.asarray(mem_info.total / 1024 / 1024).round()
        mem_used = np.asarray(mem_info.used / 1024 / 1024).round()
        mem_free = np.asarray(mem_info.free / 1024 / 1024).round()
        # 计算可用显存占比当可分配显存不足10%时关闭游戏进行释放
        if mem_usage < 0.1:
            print("可用显存已严重不足")
            print("总显存: {}MB  已用显存: {}MB  可用显存: {}MB".format(mem_total, mem_used, mem_free))
            self.closeGame()

    # 图像循环判断当前状态方法
    def ImagesJudgeLoop(self, box, check_count):
        checkCount = 0  # 设置计时器强制while跳出最低时限
        # 若在（0.3 * check_count至0.4 * check_count）秒内未成功执行while条件内判断操作则抛出异常
        while not self.isCorrectImage(box) and checkCount < check_count:
            # 作战终止状态对应动作
            if check_count == 100:
                self.mouseClick(self.COMBAT_END_CLICK_BOX, 0.2, 0.3)
            # 其他状态
            else:
                self.wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= check_count:
            return False
        # 若判断正常则返回True
        return True

    # 检测图像所处的状态函数 Image on Status（有限状态机） #
    # 判断图像状态抽象方法
    def isCorrectImage(self, CONSTANT_BOX):
        IMAGE_BOX = CONSTANT_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + CONSTANT_BOX[4])
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否是模拟器桌面
    def isDesktop(self):
        IMAGE_BOX = self.DESKTOP_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "desktop.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否是每日首次登陆的确认界面
    def isFirstLogin(self):
        IMAGE_BOX = self.FIRST_LOGIN_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "first_login.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否是委托完成界面
    def isLSupport(self):
        IMAGE_BOX = self.L_SUPPORT_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "L_support.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否是主界面
    def isMainMenu(self):
        IMAGE_BOX = self.MAIN_MENU_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "main_menu.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 当不知道在哪时，判断是否有导航栏，有就可以通过导航栏回到作战菜单
    def isNavigate(self):
        IMAGE_BOX = self.NAVIGATE_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "navigate.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 控制脚本行动逻辑函数 Action on Image #
    # 启动模拟器
    def openSimulator(self):
        print("ACTION: 启动mumu模拟器")
        os.startfile(self.app_dir)  # 打开外部应用程序

    # 启动游戏
    def startGame(self):
        print("ACTION: 启动游戏")
        self.mouseClick(self.START_GAME_STEP1_CLICK_BOX, 30, 30)
        self.mouseClick(self.START_GAME_STEP2_CLICK_BOX, 30, 30)
        self.mouseClick(self.START_GAME_STEP3_CLICK_BOX, 30, 30)

    # 关闭游戏
    def closeGame(self):
        print("ACTION: 关闭游戏")
        self.mouseClick(self.CLOSE_GAME_CLICK_BOX, 5, 5)

    # 每日首次登陆确认活动消息
    def confirmAnnouncement(self):
        print("ACTION: 每日首次登录公告板")
        while self.isFirstLogin():
            self.mouseClick(self.CONFIRM_INFORMATION_CLICK_BOX, 2, 2)
        self.mouseClick(self.CONFIRM_REGISTRATION_CLICK_BOX, 2, 2)
        self.mouseClick(self.CONFIRM_REGISTRATION_CLICK_BOX, 2, 2)

    # 后勤支援归来确认
    def takeLSupport(self):
        print("ACTION: 收派后勤")
        self.mouseClick(self.L_SUPPORT_STEP1_CLICK_BOX, 2, 3)
        self.mouseClick(self.L_SUPPORT_STEP2_CLICK_BOX, 4, 5)


if __name__ == '__main__':
    baseautoGFL = BaseAutoGFL()
    baseautoGFL.__getattribute__()
