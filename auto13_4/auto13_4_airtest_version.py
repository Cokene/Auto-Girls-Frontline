# =============================================#
#                                             #
#                 导入所需模块                 #
#                                             #
# =============================================#

import os
import logging
import cv2
import time
import random
import datetime
import win32api
import win32gui
import win32con
from os import path
import numpy as np
from io import BytesIO
from PIL import Image
from PIL import ImageGrab
from skimage.metrics import structural_similarity
from airtest.core.android import Android

# =============================================#
#                                             #
#                 定义所需常量                 #
#                                             #
# =============================================#

# =================模拟器分辨率区域=================#
TOP_WIDTH = 37  # 模拟器顶部宽度
BOTTOM_WIDTH = 52  # 模拟器底部宽度

# =================截图比对区域=================#
IMAGE_PATH = 'C:/Users/shliz/Desktop/Auto_GirlsFrontline/auto13_4/initial_IMG/airtest/'  # 读取截图的路径
FIRST_LOGIN_IMAGE_BOX = [0.60, 0.58, 0.75, 0.65]  # 每日第一次登录时那个确认窗口判断区域
MAIN_MENU_IMAGE_BOX = [0.63, 0.52, 0.75, 0.58]  # 主界面判断区域
L_SUPPORT_IMAGE_BOX = [0.05, 0.30, 0.18, 0.39]  # 后勤完成界面判断区域
COMBAT_MENU_IMAGE_BOX = [0.05, 0.70, 0.12, 0.80]  # 战斗菜单界面判断区域
CHOOSE_13_4_IMAGE_BOX = [0.50, 0.67, 0.60, 0.75]  # 13-4菜单界面判断区域
MAP_13_4_IMAGE_BOX = [0.82, 0.80, 0.95, 0.88]  # 进入13-4判断区域
SET_TEAM_IMAGE_BOX = [0.85, 0.75, 0.92, 0.78]  # 队伍放置判断区域
SET_WE_TEAM_IMAGE_BOX = [0.12, 0.28, 0.20, 0.32]  # 重装队伍队伍放置判断区域
FORM_TEAM_IMAGE_BOX = [0.28, 0.38, 0.38, 0.50]  # 队伍编成判断区域
CHANGE_MEMBER_IMAGE_BOX = [0.90, 0.30, 0.95, 0.40]  # 人员选择判断区域
COMBAT_START_IMAGE_BOX = [0.80, 0.82, 0.97, 0.88]  # 开启作战判断区域
COMBAT_FINISH_IMAGE_BOX = [0.669, 0.597, 0.7, 0.641]  # 战役完成判断区域
TEAM_INFO_IMAGE_BOX = [0.85, 0.67, 0.94, 0.71]  # 队伍详情页判断区域
GOTO_POWERUP_IMAGE_BOX = [0.62, 0.435, 0.711, 0.472]  # 提醒强化判断区域
NAVIGATE_IMAGE_BOX = [0.15, 0.10, 0.20, 0.15]  # 导航条判断区域
DESKTOP_IMAGE_BOX = [0.10, 0.20, 0.22, 0.35]  # 模拟器桌面判断区域
COMBAT_PAUSE_IMAGE_BOX = [0.45, 0.62, 0.55, 0.67]  # 战斗终止提示判断区域
RETURN_COMBAT_IMAGE_BOX = [0.75, 0.63, 0.90, 0.70]  # 回到作战界面判断区域
NON_RETIRE_IMAGE_BOX = [0.23, 0.33, 0.27, 0.39]  # 人形回收判断区域
FIGURE_DETECT_IMAGE_BOX = [0.127, 0.565, 0.24, 0.616]  # 燃烧弹人形更换检测判断区域
RESUME_COMBAT_IMAGE_BOX = [0.77, 0.81, 0.84, 0.89]  # 重新结束战役判断区域

# =================点击拖动区域=================#

# 从主菜单进入作战选择界面
COMBAT_CLICK_BOX = [0.65, 0.50, 0.75, 0.58]  # 在主菜单点击战斗（无作战进行中情况）
COMBAT_BREAK_CLICK_BOX = [0.65, 0.50, 0.75, 0.58]  # 在主菜单点击战斗（作战中断情况）

# 从作战选择界面进入13-4界面
COMBAT_MISSION_CLICK_BOX = [0.05, 0.28, 0.10, 0.31]  # 点击作战任务
CHAPTER_DRAG_BOX = [0.18, 0.75, 0.22, 0.80]  # 向上拖章节选择条
CHAPTER_13_CLICK_BOX = [0.17, 0.78, 0.20, 0.81]  # 选择第13章
NORMAL_CLICK_BOX = [0.76, 0.24, 0.79, 0.28]  # 选择普通难度
EPISODE_DRAG_BOX = [0.40, 0.35, 0.80, 0.40]  # 向下拖小节选择条

# 开始13-4
EPISODE_4_CLICK_BOX = [0.50, 0.69, 0.60, 0.74]  # 选择第4节
ENTER_COMBAT_CLICK_BOX = [0.72, 0.70, 0.80, 0.75]  # 进入作战
END_COMBAT_STEP1_CLICK_BOX = [0.72, 0.62, 0.80, 0.66]  # 终止作战
END_COMBAT_STEP2_CLICK_BOX = [0.52, 0.60, 0.60, 0.65]  # 确认终止作战

# 缩小地图，拖动地图
MAP_SCALE_BOX = [0.65, 0.30, 0.75, 0.40]
MAP_DRAG_BOX = [0.15, 0.20, 0.25, 0.25]

# 机场位置点
AIRPORT_1_CLICK_BOX = [0.752, 0.42, 0.77, 0.436]  # 右机场
AIRPORT_2_CLICK_BOX = [0.408, 0.48, 0.42, 0.50]  # 左机场

# 更换打手
CHANGE_FORCE_V_STEP1_CLICK_BOX = [0.16, 0.748, 0.23, 0.765]  # 点击梯队编成
CHANGE_FORCE_V_STEP2_CLICK_BOX = [0.15, 0.35, 0.25, 0.55]  # 点击Vector
CHANGE_FORCE_V_STEP3_CLICK_BOX = [0.89, 0.34, 0.96, 0.37]  # 点击显示种类
CHANGE_FORCE_V_STEP4_CLICK_BOX = [0.75, 0.23, 0.77, 0.25]  # 点击四星
CHANGE_FORCE_V_STEP5_CLICK_BOX = [0.60, 0.45, 0.63, 0.47]  # 点击冲锋枪
CHANGE_FORCE_V_STEP6_CLICK_BOX = [0.71, 0.73, 0.76, 0.75]  # 点击确认
CHANGE_FORCE_V_STEP7_CLICK_BOX = [0.19, 0.27, 0.26, 0.34]  # 选择MicroUZI
CHANGE_FORCE_V_STEP8_CLICK_BOX = [0.07, 0.097, 0.1, 0.13]  # 点击返回

CHANGE_FORCE_U_STEP1_CLICK_BOX = [0.16, 0.748, 0.23, 0.765]  # 点击梯队编成
CHANGE_FORCE_U_STEP2_CLICK_BOX = [0.15, 0.35, 0.25, 0.55]  # 点击MicroUZI
CHANGE_FORCE_U_STEP3_CLICK_BOX = [0.89, 0.34, 0.96, 0.37]  # 点击显示种类
CHANGE_FORCE_U_STEP4_CLICK_BOX = [0.60, 0.23, 0.63, 0.25]  # 点击五星
CHANGE_FORCE_U_STEP5_CLICK_BOX = [0.60, 0.45, 0.63, 0.47]  # 点击冲锋枪
CHANGE_FORCE_U_STEP6_CLICK_BOX = [0.71, 0.73, 0.76, 0.75]  # 点击确认
CHANGE_FORCE_U_STEP7_CLICK_BOX = [0.18, 0.75, 0.22, 0.80]  # 拖动人形菜单
CHANGE_FORCE_U_STEP8_CLICK_BOX = [0.07, 0.73, 0.10, 0.80]  # 选择Vector
CHANGE_FORCE_U_STEP9_CLICK_BOX = [0.07, 0.097, 0.1, 0.13]  # 点击返回

# 放置队伍
TEAM_SHIFT_CLICK_BOX = [0.42, 0.20, 0.48, 0.24]  # 切换成普通梯队
TEAM_SET_CLICK_BOX = [0.85, 0.75, 0.92, 0.78]  # 放置梯队

# 开始作战
START_COMBAT_CLICK_BOX = [0.85, 0.82, 0.92, 0.86]  # 点击开始作战

# 结束作战
END_COMBAT_CLICK_BOX = [0.90, 0.84, 0.94, 0.86]  # 点击结束作战

# 返回作战
RETURN_COMBAT_CLICK_BOX = [0.75, 0.66, 0.90, 0.69]  # 返回战役作战界面

# 计划模式
PLAN_MODE_CLICK_BOX = [0.04, 0.77, 0.10, 0.79]  # 点击计划模式
PLAN_POINT1_CLICK_BOX = [0.7, 0.419, 0.716, 0.436]  # 点击计划点1
PLAN_POINT2_CLICK_BOX = [0.75, 0.616, 0.768, 0.63]  # 点击计划点2
PLAN_START_CLICK_BOX = [0.88, 0.82, 0.98, 0.85]  # 点击执行计划

# 战役结算
COMBAT_END_CLICK_BOX = [0.48, 0.08, 0.52, 0.10]  # 战役结算，需要偏右，否则捞出人形会点到分享按钮

# 补给
SUPPLY_CLICK_BOX = [0.85, 0.68, 0.94, 0.70]  # 点击补给

# 撤退
WITHDRAW_STEP1_CLICK_BOX = [0.72, 0.76, 0.78, 0.78]  # 点击撤退
WITHDRAW_STEP2_CLICK_BOX = [0.55, 0.61, 0.62, 0.64]  # 确认撤退

# 重启作战
RESTART_STEP1_CLICK_BOX = [0.22, 0.09, 0.26, 0.14]  # 点击终止作战
RESTART_STEP2_CLICK_BOX = [0.34, 0.61, 0.43, 0.63]  # 点击重新作战

# 拆解
GOTO_POWERUP_CLICK_BOX = [0.67, 0.51, 0.73, 0.58]  # 前往强化界面
CHOOSE_RETIRE_CLICK_BOX = [0.06, 0.46, 0.12, 0.50]  # 选择回收拆解选项
CHOOSE_RETIRE_CHARACTER_CLICK_BOX = [0.25, 0.26, 0.3, 0.33]  # 选择拆解人形
RETIRE_CHARACTER_1_CLICK_BOX = [0.12, 0.3, 0.14, 0.36]  # 第一行第一只人形
RETIRE_CHARACTER_2_CLICK_BOX = [0.24, 0.3, 0.26, 0.36]  # 第一行第二只人形
RETIRE_CHARACTER_3_CLICK_BOX = [0.36, 0.3, 0.38, 0.36]  # 第一行第三只人形
RETIRE_CHARACTER_4_CLICK_BOX = [0.48, 0.3, 0.50, 0.36]  # 第一行第四只人形
RETIRE_CHARACTER_5_CLICK_BOX = [0.60, 0.3, 0.62, 0.36]  # 第一行第五只人形
RETIRE_CHARACTER_6_CLICK_BOX = [0.72, 0.3, 0.74, 0.36]  # 第一行第六只人形
RETIRE_DRAG_BOX = [0.40, 0.60, 0.60, 0.60]  # 往上拖一行
CHOOSE_FINISH_RETIRE_CLICK_BOX = [0.88, 0.68, 0.92, 0.74]  # 完成选择
RETIRE_CLICK_BOX = [0.84, 0.77, 0.90, 0.80]  # 点击拆解
CONFIRM_RETIRE_CLICK_BOX = [0.54, 0.74, 0.64, 0.78]  # 确认拆解高星人形

# 强化
CHOOSE_POWERUP_CHARACTER_CLICK_BOX = [0.20, 0.40, 0.3, 0.50]  # 选择被强化人形
FIRST_CHARACTER_CLICK_BOX = [0.10, 0.3, 0.14, 0.36]  # 选择第一只人形
CHOOSE_EXP_CHARACTER_CLICK_BOX = [0.40, 0.32, 0.43, 0.36]  # 选择狗粮
AUTO_CHOOSE_CLICK_BOX = [0.88, 0.66, 0.94, 0.72]  # 智能选择
CHOOSE_CONFIRM_CLICK_BOX = [0.88, 0.66, 0.94, 0.72]  # 完成选择
POWERUP_CLICK_BOX = [0.86, 0.75, 0.92, 0.78]  # 点击强化
POWERUP_FINISH_CLICK_BOX = [0.46, 0.64, 0.54, 0.66]  # 完成强化

# 跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.15, 0.10, 0.18, 0.15]  # 打开导航条
NAVIGATE_BAR_DRAG_BOX = [0.10, 0.28, 0.17, 0.32]  # 向右拖导航条
NAVIGATE_COMBAT_CLICK_BOX = [0.10, 0.28, 0.12, 0.32]  # 跳转至作战菜单
NAVIGATE_FACTORY_CLICK_BOX = [0.38, 0.28, 0.39, 0.32]  # 跳转至工厂菜单
NAVIGATE_MAIN_MENU_CLICK_BOX = [0.20, 0.18, 0.28, 0.20]  # 跳转至主菜单

# 收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50, 0.50, 0.60, 0.60]  # 确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53, 0.60, 0.62, 0.65]  # 再次派出

# 启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14, 0.23, 0.18, 0.28]  # 点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50, 0.70, 0.50, 0.70]  # 点击一次
START_GAME_STEP3_CLICK_BOX = [0.50, 0.75, 0.50, 0.75]  # 点击开始

# 每日第一次登录的确认
CHECK_INFORMATION_CLICK_BOX = [0.26, 0.61, 0.27, 0.63]  # 勾选今日不在弹出
CONFIRM_INFORMATION_CLICK_BOX = [0.65, 0.60, 0.72, 0.63]  # 点击确认

# 关闭游戏
CLOSE_GAME_CLICK_BOX = [0.525, 0.02, 0.535, 0.04]

# 关闭作战断开提醒
CLOSE_TIP_CLICK_BOX = [0.45, 0.62, 0.55, 0.67]


# =============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
# =============================================#

# 一个好程序都应该有一个较为优雅的启动提醒界面？
def preface():
    for x in range(3, -1, -1):
        mystr = ">>> " + str(x) + "s 后将开始操作，请切换至模拟器界面"
        print(mystr, end="")
        print("\b" * (len(mystr) * 2), end="", flush=True)
        time.sleep(1)
    print("开始操作")


# 随机等待一段时间,控制在minTime~maxTime之间
def wait(minTime, maxTime):
    waitTime = minTime + (maxTime - minTime) * random.random()
    time.sleep(waitTime)


# 获取指定区域box的截图
def getImage(box):
    # simData = {'width', 'height', 'density', 'orientation', 'rotation', 'max_x', 'max_y'}
    simData = sim.get_display_info()
    boxData = calibrate(box)
    imgLeft = int(simData['width'] * boxData[0])
    imgTop = int(simData['height'] * boxData[1])
    imgRight = int(simData['width'] * boxData[2])
    imgBottom = int(simData['height'] * boxData[3])

    imgBytes = sim.screen_proxy.get_frame()
    imgFullSize = Image.open(BytesIO(imgBytes))
    img = imgFullSize.crop([imgLeft, imgTop, imgRight, imgBottom])

    # （弃用）img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom)
    return img


# 点击box内随机一点，如果提供具体xy偏量，则点击精确的点
def mouseClick(box, minTime, maxTime, exact_x=0, exact_y=0):
    simData = sim.get_display_info()
    # box = [left,top,right,bottom]
    width = box[2] - box[0]
    height = box[3] - box[1]
    boxData = calibrate(box)
    if exact_x == 0 and exact_y == 0:
        clickX = (int)(simData['width'] * boxData[0] + simData['width'] * width * random.random())
        clickY = (int)(simData['height'] * boxData[1] + simData['height'] * height * random.random())
    else:
        clickX = (int)(simData['width'] * boxData[0]) + exact_x
        clickY = (int)(simData['height'] * boxData[1]) + exact_y
    clickPos = (clickX, clickY)
    sim.touch(clickPos)
    wait(minTime, maxTime)


# 模拟手指拖动，box为起始区域,times为拖动次数,distance为单次拖动距离
# dx,dy为组成移动方向向量，frame_interval(已弃用)为鼠标拖动帧间隔,越小鼠标拖动越快
# multi_interval为连续拖动时的时间间隔
def mouseDrag(box, dx, dy, times, distance, frame_interval, multi_interval):
    simData = sim.get_display_info()
    width = box[2] - box[0]
    height = box[3] - box[1]
    boxData = calibrate(box)
    dragX = int(simData['width'] * boxData[0] + simData['width'] * width * random.random())
    dragY = int(simData['height'] * boxData[1] + simData['height'] * height * random.random())
    dragPos = (dragX, dragY)
    if dx == 0:
        if dy == 0:
            dragPosEnd = dragPos
        elif dy == -1:
            dragPosEnd = (dragX, dragY - distance)
        elif dy == 1:
            dragPosEnd = (dragX, dragY + distance)
    elif dx == -1:
        if dy == 0:
            dragPosEnd = (dragX - distance, dragY)
        elif dy == -1:
            dragPosEnd = (
            dragX + distance * dx / np.sqrt(dx * dx) + (dy * dy), dragY + distance * dy / np.sqrt(dx * dx) + (dy * dy))
        elif dy == 1:
            dragPosEnd = (
            dragX + distance * dx / np.sqrt(dx * dx) + (dy * dy), dragY + distance * dy / np.sqrt(dx * dx) + (dy * dy))
    elif dx == 1:
        if dy == 0:
            dragPosEnd = (dragX + distance, dragY)
        elif dy == -1:
            dragPosEnd = (
            dragX + distance * dx / np.sqrt(dx * dx) + (dy * dy), dragY + distance * dy / np.sqrt(dx * dx) + (dy * dy))
        elif dy == 1:
            dragPosEnd = (
            dragX + distance * dx / np.sqrt(dx * dx) + (dy * dy), dragY + distance * dy / np.sqrt(dx * dx) + (dy * dy))
    for i in range(times):
        # 开始构造滑动
        sim.swipe(dragPos, dragPosEnd)
        time.sleep(multi_interval)


# 模拟双指缩放地图
# direct = 0 : 放大      direct = 1 : 缩小   times为连续缩放次数
def scaleMap(box, direct, times):
    simData = sim.get_display_info()
    width = box[2] - box[0]
    height = box[3] - box[1]
    boxData = calibrate(box)
    scaleX = int(simData['width'] * boxData[0] + simData['width'] * width * random.random())
    scaleY = int(simData['height'] * boxData[1] + simData['height'] * height * random.random())
    scalePos = (scaleX, scaleY)
    for i in range(times):
        # 放大
        if direct == 0:
            sim.pinch(scalePos, 0, 35, 0.1, 10, in_or_out='out')
        # 缩小
        else:
            sim.pinch(scalePos, in_or_out='in')
        wait(0.5, 0.7)
    time.sleep(1)


# 将windowsData获取的数据转化为模拟器内部的参数
def calibrate(box):
    height = sim.display_info['height']
    box[1] = ((box[1] * 589) - TOP_WIDTH) / height
    box[3] = ((box[3] * 589) - TOP_WIDTH) / height
    return box


# 权重单位换算（测试用）
def trans(box):
    box[0] = box[0] / 750
    box[1] = (box[1] + TOP_WIDTH) / 589
    box[2] = box[2] / 750
    box[3] = (box[3] + TOP_WIDTH) / 589
    print(box)


# 比较两图片吻合度/置信度，结构相似性比较法（真的好用）
def imageCompare(img1, img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # ground_truth img
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # test img
    (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
    return score > 0.95


# =============================================#
#                                             #
#                 高级功能函数                 #
#                                             #
# =============================================#

# 判断是否战役结束
def isCombatFinished():
    initImage = cv2.imread(IMAGE_PATH + "combat_finish.png")
    capImage = getImage(COMBAT_FINISH_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否进入了13-4地图
def isInMap():
    initImage = cv2.imread(IMAGE_PATH + "map.png")
    capImage = getImage(MAP_13_4_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否作战正常开启
def isCombatStart():
    initImage = cv2.imread(IMAGE_PATH + "combat_start.png")
    capImage = getImage(COMBAT_START_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是提醒强化界面
def isGotoPowerup():
    initImage = cv2.imread(IMAGE_PATH + "goto_powerup.png")
    capImage = getImage(GOTO_POWERUP_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是可以选择13-4的界面
def is13_4():
    initImage = cv2.imread(IMAGE_PATH + "_13_4.png")
    capImage = getImage(CHOOSE_13_4_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是战斗选择菜单
def isCombatMenu():
    initImage = cv2.imread(IMAGE_PATH + "combat_menu.png")
    capImage = getImage(COMBAT_MENU_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是主界面
def isMainMenu():
    initImage = cv2.imread(IMAGE_PATH + "main_menu.png")
    capImage = getImage(MAIN_MENU_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 在工厂资源回收界面
def isNonRetire():
    initImage = cv2.imread(IMAGE_PATH + "non_retire.png")
    capImage = getImage(NON_RETIRE_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是每日第一次登录的确认界面
def isFirstLogin():
    initImage = cv2.imread(IMAGE_PATH + "first_login.png")
    capImage = getImage(FIRST_LOGIN_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是委托完成界面
def isLSupport():
    initImage = cv2.imread(IMAGE_PATH + "L_support.png")
    capImage = getImage(L_SUPPORT_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是模拟器桌面
def isDesktop():
    initImage = cv2.imread(IMAGE_PATH + "desktop.png")
    capImage = getImage(DESKTOP_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否是战斗中断提示界面
def isCombatPause():
    initImage = cv2.imread(IMAGE_PATH + "combat_pause.png")
    capImage = getImage(COMBAT_PAUSE_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否有回到作战界面
def isReturnCombat():
    initImage = cv2.imread(IMAGE_PATH + "return_combat.png")
    capImage = getImage(RETURN_COMBAT_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断是否需要重新结束战役
def isResumeCombat():
    initImage = cv2.imread(IMAGE_PATH + "resume_combat.png")
    capImage = getImage(RESUME_COMBAT_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 当不知道在哪时，判断是否有导航栏，有就可以通过导航栏回到作战菜单
def isNavigate():
    initImage = cv2.imread(IMAGE_PATH + "navigate.png")
    capImage = getImage(NAVIGATE_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 在队伍放置界面
def isSetTeam():
    initImage = cv2.imread(IMAGE_PATH + "set_team.png")
    capImage = getImage(SET_TEAM_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 在布置重装的界面
def isSetWETeam():
    initImage = cv2.imread(IMAGE_PATH + "set_we_team.png")
    capImage = getImage(SET_WE_TEAM_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 在队伍编成界面
def isFormTeam():
    initImage = cv2.imread(IMAGE_PATH + "form_team.png")
    capImage = getImage(FORM_TEAM_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 判断更换的人形名称
def isVector():
    initImage = cv2.imread(IMAGE_PATH + "ventor.png")
    capImage = getImage(FIGURE_DETECT_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


def isMicroUZI():
    initImage = cv2.imread(IMAGE_PATH + "microuzi.png")
    capImage = getImage(FIGURE_DETECT_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 在人员选择界面
def isChangeMember():
    initImage = cv2.imread(IMAGE_PATH + "change_member.png")
    capImage = getImage(CHANGE_MEMBER_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 在队伍详情界面
def isTeamInfo():
    initImage = cv2.imread(IMAGE_PATH + "team_info.png")
    capImage = getImage(TEAM_INFO_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
    capImage = cv2.resize(capImage, (initImage.shape[1], initImage.shape[0]))
    return imageCompare(initImage, capImage)


# 从主菜单进入作战菜单
def mainMenuToCombatMenu():
    print("ACTION: 前往作战菜单")
    mouseClick(COMBAT_CLICK_BOX, 2, 3)


# 从主菜单进入作战菜单（战斗中断情况）
def mainMenuToCombatMenu_combatOn():
    print("ACTION: 前往作战菜单-战斗中断")
    mouseClick(COMBAT_BREAK_CLICK_BOX, 5, 6)


# 从作战菜单进入13-4界面
def combatMenuTo13_4():
    print("ACTION: 前往13-4选择界面")
    mouseClick(COMBAT_MISSION_CLICK_BOX, 1, 2)
    mouseDrag(CHAPTER_DRAG_BOX, 0, -1, 2, 400, 0.001, 0.8)
    mouseClick(CHAPTER_13_CLICK_BOX, 1, 2)
    mouseClick(NORMAL_CLICK_BOX, 1, 2)
    mouseDrag(EPISODE_DRAG_BOX, 0, 1, 1, 300, 0.001, 1)


# 开始13-4
def start13_4():
    print("ACTION: 启动13-4")
    mouseClick(EPISODE_4_CLICK_BOX, 1, 1)
    mouseClick(ENTER_COMBAT_CLICK_BOX, 6, 7)


# 终止13-4
def end13_4():
    print("ACTION: 终止13-4")
    mouseClick(EPISODE_4_CLICK_BOX, 2, 3)
    mouseClick(END_COMBAT_STEP1_CLICK_BOX, 2, 3)
    mouseClick(END_COMBAT_STEP2_CLICK_BOX, 2, 3)


# 战前准备，调整地图，补给1队（旧版逻辑）
def combatPrepare_old():
    print("STATE: 战前整备")
    mouseClick(MAP_SCALE_BOX, 0.5, 0.6)
    scaleMap(MAP_SCALE_BOX, 1, 12)
    mouseDrag(MAP_DRAG_BOX, 1, 1, 1, 240, 0.001, 1)
    # 保证了战损排序第一的zas在第一队
    changeForce(False)
    # 补给一队
    mouseDrag(MAP_DRAG_BOX, 1, 1, 1, 240, 0.001, 1)
    setTeam()
    startCombat()
    mouseClick(AIRPORT_2_CLICK_BOX, 1, 2)
    mouseClick(AIRPORT_2_CLICK_BOX, 1, 2)
    mouseClick(SUPPLY_CLICK_BOX, 2, 3)
    mouseClick(AIRPORT_2_CLICK_BOX, 1, 2)
    mouseClick(WITHDRAW_STEP1_CLICK_BOX, 2, 3)
    mouseClick(WITHDRAW_STEP2_CLICK_BOX, 2, 3)
    restartCombat()
    return True


# 战前准备，调整地图（新）
def combatPrepare():
    print("STATE: 战前整备")
    mouseClick(MAP_SCALE_BOX, 0.5, 0.6)
    scaleMap(MAP_SCALE_BOX, 1, 3)
    mouseDrag(MAP_DRAG_BOX, 1, 1, 1, 240, 0.001, 1)
    return True


# 更换打手
def changeForce():
    print("ACTION: 更换打手")
    mouseClick(AIRPORT_2_CLICK_BOX, 0, 0)  # 点击左方机场
    checkCount = 0
    while not (isSetTeam() or isSetWETeam()) and checkCount < 20:
        wait(0.3, 0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.6)
    if isSetWETeam():
        mouseClick(TEAM_SHIFT_CLICK_BOX, 1, 2)  # 切换普通队伍

    if isVector():
        mouseClick(CHANGE_FORCE_V_STEP1_CLICK_BOX, 0, 0)  # 点击队伍编成
        checkCount = 0
        while not isFormTeam() and checkCount < 20:
            wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= 20:
            return False
        time.sleep(0.8)
        mouseClick(CHANGE_FORCE_V_STEP2_CLICK_BOX, 0.5, 0.5)  # 点击打手
        checkCount = 0
        while not isChangeMember() and checkCount < 20:
            wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= 20:
            return False
        time.sleep(0.6)
        mouseClick(CHANGE_FORCE_V_STEP3_CLICK_BOX, 0.5, 0.5)  # 点击显示种类
        mouseClick(CHANGE_FORCE_V_STEP4_CLICK_BOX, 0.5, 0.5)  # 点击四星
        mouseClick(CHANGE_FORCE_V_STEP5_CLICK_BOX, 0.5, 0.5)  # 点击冲锋枪
        mouseClick(CHANGE_FORCE_V_STEP6_CLICK_BOX, 1, 1)  # 点击确认
        mouseClick(CHANGE_FORCE_V_STEP7_CLICK_BOX, 0, 0)  # 选择MicroUZI
        checkCount = 0
        while not isFormTeam() and checkCount < 20:
            wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= 20:
            return False
        time.sleep(0.8)
        mouseClick(CHANGE_FORCE_V_STEP8_CLICK_BOX, 0, 0)  # 点击返回

    elif isMicroUZI():
        mouseClick(CHANGE_FORCE_U_STEP1_CLICK_BOX, 0, 0)  # 点击队伍编成
        checkCount = 0
        while not isFormTeam() and checkCount < 20:
            wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= 20:
            return False
        time.sleep(0.8)
        mouseClick(CHANGE_FORCE_U_STEP2_CLICK_BOX, 0.5, 0.5)  # 点击打手
        checkCount = 0
        while not isChangeMember() and checkCount < 20:
            wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= 20:
            return False
        time.sleep(0.6)
        mouseClick(CHANGE_FORCE_U_STEP3_CLICK_BOX, 0.5, 0.5)  # 点击显示种类
        mouseClick(CHANGE_FORCE_U_STEP4_CLICK_BOX, 0.5, 0.5)  # 点击五星
        mouseClick(CHANGE_FORCE_U_STEP5_CLICK_BOX, 0.5, 0.5)  # 点击冲锋枪
        mouseClick(CHANGE_FORCE_U_STEP6_CLICK_BOX, 1, 1)  # 点击确认
        mouseDrag(CHANGE_FORCE_U_STEP7_CLICK_BOX, 0, -1, 2, 400, 0.001, 0.8)  # 拖动人形菜单
        mouseClick(CHANGE_FORCE_U_STEP8_CLICK_BOX, 0, 0)  # 选择Vector
        checkCount = 0
        while not isFormTeam() and checkCount < 20:
            wait(0.3, 0.4)
            checkCount += 1
        if checkCount >= 20:
            return False
        time.sleep(0.8)
        mouseClick(CHANGE_FORCE_U_STEP9_CLICK_BOX, 0, 0)  # 点击返回
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3, 0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.8)
    scaleMap(MAP_SCALE_BOX, 1, 1)  # 缩放地图_1
    mouseDrag(MAP_DRAG_BOX, 1, 1, 1, 400, 0.001, 1)  # 缩放地图_2
    return True


# 放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(AIRPORT_2_CLICK_BOX, 0, 0)  # 点击左方机场
    checkCount = 0
    while not (isSetTeam() or isSetWETeam()) and checkCount < 20:
        wait(0.3, 0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    if isSetWETeam():
        mouseClick(TEAM_SHIFT_CLICK_BOX, 0, 0)  # 切换普通队伍
    checkCount = 0
    while not isSetTeam() and checkCount < 10:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    mouseClick(TEAM_SET_CLICK_BOX, 0, 0)  # 点击放置队伍
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3, 0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    mouseClick(AIRPORT_1_CLICK_BOX, 0, 0)  # 点击右方机场
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        wait(0.3, 0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    mouseClick(TEAM_SET_CLICK_BOX, 0, 0)  # 点击放置队伍
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3, 0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    return True


# 补给打手
def supply():
    mouseClick(AIRPORT_2_CLICK_BOX, 1, 1)
    mouseClick(AIRPORT_2_CLICK_BOX, 1, 1)
    mouseClick(SUPPLY_CLICK_BOX, 1.5, 1.5)
    return True


# 开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX, 0, 0)
    checkCount = 0
    while not isCombatStart() and checkCount < 20:
        wait(0.4, 0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(2)
    return True


# 计划模式
def planMode():
    print("ACTION: 计划模式")
    mouseClick(AIRPORT_1_CLICK_BOX, 0.8, 1)
    mouseClick(PLAN_MODE_CLICK_BOX, 1, 1.5)
    mouseClick(PLAN_POINT1_CLICK_BOX, 0.5, 0.7)
    mouseClick(PLAN_POINT2_CLICK_BOX, 0.5, 0.7)
    mouseClick(PLAN_START_CLICK_BOX, 0, 0)


# 战役结算
def endCombat():
    print("ACTION: 战役结算")
    mouseClick(END_COMBAT_CLICK_BOX, 5, 6)
    checkCount = 0
    while not is13_4() and checkCount < 100:
        mouseClick(COMBAT_END_CLICK_BOX, 0.2, 0.3)
        checkCount += 1
    if checkCount >= 100:
        return False
    return True


# 重启作战
def restartCombat():
    print("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX, 1, 1.5)
    mouseClick(RESTART_STEP2_CLICK_BOX, 0, 0)
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.4, 0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(1)
    return True


# 拆解
def gotoRetire():
    print("ACTION: 拆解人形")
    mouseClick(GOTO_POWERUP_CLICK_BOX, 5, 6)  # 跳转至工厂界面
    mouseClick(CHOOSE_RETIRE_CLICK_BOX, 1, 1)  # 点击资源回收
    # 回收趟数
    for i in range(4):
        mouseClick(CHOOSE_RETIRE_CHARACTER_CLICK_BOX, 0.3, 0.5)  # 点击选择角色
        if isNonRetire():
            break
        mouseClick(RETIRE_CHARACTER_1_CLICK_BOX, 0.2, 0.3)  # 选六个
        mouseClick(RETIRE_CHARACTER_2_CLICK_BOX, 0.2, 0.3)
        mouseClick(RETIRE_CHARACTER_3_CLICK_BOX, 0.2, 0.3)
        mouseClick(RETIRE_CHARACTER_4_CLICK_BOX, 0.2, 0.3)
        mouseClick(RETIRE_CHARACTER_5_CLICK_BOX, 0.2, 0.3)
        mouseClick(RETIRE_CHARACTER_6_CLICK_BOX, 0.2, 0.3)
        # mouseDrag(RETIRE_DRAG_BOX,0,-1,1,325,0.005,1)#往上拖一行
        mouseClick(CHOOSE_FINISH_RETIRE_CLICK_BOX, 0, 1)
        mouseClick(RETIRE_CLICK_BOX, 1, 1)
        mouseClick(CONFIRM_RETIRE_CLICK_BOX, 2, 3)

    # 强化


def gotoPowerup():
    print("ACTION: 强化人形")
    mouseClick(GOTO_POWERUP_CLICK_BOX, 5, 6)
    mouseClick(CHOOSE_POWERUP_CHARACTER_CLICK_BOX, 1, 2)
    mouseClick(FIRST_CHARACTER_CLICK_BOX, 1, 2)
    mouseClick(CHOOSE_EXP_CHARACTER_CLICK_BOX, 2, 3)
    mouseClick(AUTO_CHOOSE_CLICK_BOX, 1, 2)
    mouseClick(CHOOSE_CONFIRM_CLICK_BOX, 1, 2)
    mouseClick(POWERUP_CLICK_BOX, 3, 4)
    mouseClick(POWERUP_FINISH_CLICK_BOX, 3, 4)


# 跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX, 1, 2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX, 4, 5)


# 跳转至工厂
def gotoFactory():
    print("ACTION: 跳转至工厂")
    mouseClick(NAVIGATE_BAR_CLICK_BOX, 1, 2)
    mouseClick(NAVIGATE_FACTORY_CLICK_BOX, 6, 6)


# 跳转至战斗菜单(暂时不用)
def backToCombatMenu():
    print("ACTION: 跳转至战斗菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX, 1, 2)
    mouseClick(NAVIGATE_COMBAT_CLICK_BOX, 5, 6)


# 返回13-4
def returnToCombat():
    print('ACTION：返回13-4')
    mouseClick(RETURN_COMBAT_CLICK_BOX, 8, 9)


# 重新结束13-4
def resumeCombat():
    if isResumeCombat():
        endCombat()


# 收后勤支援
def takeLSupport():
    print("ACTION: 收派后勤")
    mouseClick(L_SUPPORT_STEP1_CLICK_BOX, 2, 3)
    mouseClick(L_SUPPORT_STEP2_CLICK_BOX, 4, 5)


# 启动游戏
def startGame():
    print("ACTION: 启动游戏")
    sim.start_app('com.sunborn.girlsfrontline.cn')


# 关闭作战断开提醒
def closeTip():
    mouseClick(CLOSE_TIP_CLICK_BOX, 5, 5)


# 关闭游戏
def closeGame():
    sim.stop_app('com.sunborn.girlsfrontline.cn')


# 确认每日第一次登录的公告
def confirmAnnouncement():
    mouseClick(CHECK_INFORMATION_CLICK_BOX, 2, 2)
    mouseClick(CONFIRM_INFORMATION_CLICK_BOX, 2, 2)


# =============================================#
#                                             #
#                 本程序主函数                 #
#                                             #
# =============================================#

# # 创建Logger
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# # 创建Handler
# # 终端Handler
# consoleHandler = logging.StreamHandler()
# consoleHandler.setLevel(logging.DEBUG)  
# # 文件Handler
# currentPath = path.dirname(__file__)
# fileHandler = logging.FileHandler(currentPath+'/log.log', mode='w', encoding='UTF-8')
# fileHandler.setLevel(logging.NOTSET)
# # Formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# consoleHandler.setFormatter(formatter)
# fileHandler.setFormatter(formatter)  
# # 添加到Logger中
# logger.addHandler(consoleHandler)
# logger.addHandler(fileHandler)

if __name__ == "__main__":

    # preface()
    startTime = datetime.datetime.now()
    combatCount = 0
    firstCombat = True  # 启动时会给一队单独补给并重开
    failCount = 0
    combatPause = False

    sim = Android(serialno='127.0.0.1:7555')  # 实例化Android类用于通信

    while True:
        if isInMap():
            print("STATE：进入地图")
            failCount = 0
            if firstCombat:
                firstCombat = False
                if not combatPrepare():
                    closeGame()
                continue
            if not changeForce():
                print("ERROR：更换打手失败")
                closeGame()
                continue
            if not setTeam():
                print("ERROR：队伍放置失败")
                closeGame()
                continue
            if not startCombat():
                print("ERROR：战役启动失败")
                continue
            if not supply():
                print("ERROR：补给打手失败")
                closeGame()
                continue
            planMode()
            checkCount = 0
            while (not isCombatFinished()) and checkCount < 200:  # 计划开始后200s还没打完，一般是出问题了（比方说卡了一下导致流程漏了）
                checkCount += 1
                time.sleep(1)
            if checkCount >= 200:  # 过了200s还没结束，直接关闭窗口重启
                if isResumeCombat():
                    endCombat()
                else:
                    print("ERROR：战斗超时！")
                    closeGame()
                    continue
            if not endCombat():  # 结束战役
                print("ERROR：战役结束失败")
                closeGame()
                continue
            combatCount += 1
            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('已运行：' + str(runtime) + '  13-4轮次：' + str(combatCount))
            # if combatCount%2 == 0:    # 每2轮收一次后勤（可选）
            #     backToMainMenu()
        elif is13_4():
            print("STATE： 13-4界面")
            start13_4()
            failCount = 0
        elif isGotoPowerup():
            print("STATE： 强化提醒界面")
            # firstCombat = True
            gotoRetire()
            # firstCombat = True
            backToMainMenu()
        elif isCombatMenu():
            print("STATE： 战斗菜单")
            combatMenuTo13_4()
            failCount = 0
        elif isCombatPause():
            print("STATE： 战斗中断提醒界面")
            failCount = 0
            closeTip()
        elif isReturnCombat():
            print("STATE： 返回作战界面")
            failCount = 0
            returnToCombat()
            resumeCombat()
            firstCombat = True
        elif isMainMenu():
            print("STATE： 主菜单界面")
            mainMenuToCombatMenu()
            failCount = 0
        elif isLSupport():
            print("STATE： 后勤结束界面")
            takeLSupport()
            failCount = 0
        elif isDesktop():
            print("STATE：模拟器桌面")
            firstCombat = True
            failCount = 0
            startGame()
            continue
        elif isFirstLogin():
            print("STATE：公告确认")
            failCount = 0
            confirmAnnouncement()
            continue
        else:  # 不知道在哪
            print("ERROR： 当前状态未知!")
            failCount += 1
            if failCount == 4:
                mouseClick([0.3, 0.45, 0.4, 0.55], 1, 1)
            if failCount >= 5:
                img = getImage([0, 0, 1, 1])
                img.save("errorRecord/" + str(combatCount) + ".png")
                print(">>> ", datetime.datetime.now(), " 无法确定当前状态,关闭重启！")
                closeGame()
            else:
                time.sleep(5)
