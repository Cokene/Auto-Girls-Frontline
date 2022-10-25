import os
import time
import random
import cv2
import numpy as np

# 返回邻域在10内的随机整数
def rd(n):
    return random.randint(n - 5, n + 5)

# 构造滑动adb shell
def build_shell_swipe(a1, b1, a2, b2):
    return 'adb shell input swipe {} {} {} {}'.format(rd(a1), rd(b1), rd(a2), rd(b2))

# 测试截屏中包含期待的图片
def test_match(template, match):
    result = cv2.matchTemplate(match, template, cv2.TM_CCOEFF_NORMED)
    similarity = cv2.minMaxLoc(result)[1]
    # print(similarity)
    if similarity < 0.8:
        return False
    else:
        return True

# 判断图片相似性
def classify_gray_hist(cur_cropImg, tar_cropImg, size=(256,256)):
    img1 = cv2.resize(cur_cropImg, size)
    img2 = cv2.resize(tar_cropImg, size)
    hist1 = cv2.calcHist([img1], [0], None, [256], [0.0,255.0])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0.0,255.0])

    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree += (1 - abs(hist1[i]-hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree += 1
    degree /= len(hist1)
    
    return degree

def classify_aHash(cur_cropImg, tar_cropImg):
    img1 = cv2.resize(cur_cropImg, (16,16))
    img2 = cv2.resize(tar_cropImg, (16,16)) 
    hash1 = getHash(img1) 
    hash2 = getHash(img2) 
    
    return Hamming_distance(hash1,hash2)

def getHash(image): 
    avreage = np.mean(image) 
    hash = [] 
    for i in range(image.shape[0]): 
        for j in range(image.shape[1]): 
            if image[i,j] > avreage: 
                hash.append(1) 
            else: 
                hash.append(0) 
    return hash

def Hamming_distance(hash1,hash2): 
    num = 0
    for index in range(len(hash1)): 
        if hash1[index] != hash2[index]: 
            num += 1
    return num

# 获取手机屏幕截图
def get_screen():
    s1 = ' adb shell /system/bin/screencap -p /sdcard/shot.png '
    s2 = ' adb pull /sdcard/shot.png '
    os.system(s1)
    time.sleep(0.2)
    os.system(s2)
    template = cv2.imread('shot.png')
    return template

# 链接模拟器
def prepare():
    os.system("adb connect 127.0.0.1:7555")
    os.system("adb devices")

def changeHKorM4(fix_count):
    #点击空白屏幕#
    x0 = 400
    y0 = 450
    # 点击左下角机场
    x00 = 798
    y00 = 770
    # 队伍编成
    x01 = 387
    y01 = 944
    # 返回作战
    x02 = 168
    y02 = 77

    ## 更换HK416 ##
    # 点击五号位
    x1 = 1460
    y1 = 540
    # # 点击HK416
    x2 = 436
    y2 = 395
    # 一键修复
    x3 = 1156
    y3 = 962
    x4 = 1458
    y4 = 829

    ## 更换SOPMOD2 ##
    # 点击SOPMOD2
    x5 = 436
    y5 = 395

    # 用于标记人形替换
    chg = fix_count

    os.system("adb shell input tap {} {}".format(rd(x00), rd(y00)))
    time.sleep(1.5)
    if fix_count != 0 and fix_count % 5 == 0:
        os.system("adb shell input tap {} {}".format(rd(x3), rd(y3)))
        time.sleep(1)
        os.system("adb shell input tap {} {}".format(rd(x4), rd(y4)))
        time.sleep(1)
    os.system("adb shell input tap {} {}".format(rd(x01), rd(y01)))
    time.sleep(2.5)
    os.system("adb shell input tap {} {}".format(rd(x1), rd(y1)))
    time.sleep(1.5)
    if chg % 2 == 1:
        os.system("adb shell input tap {} {}".format(rd(x5), rd(y5)))
        time.sleep(1.2)
    elif chg != 0 and chg % 2 == 0:
        os.system("adb shell input tap {} {}".format(rd(x2), rd(y2)))
        time.sleep(1.2)
    elif chg == 0:
        os.system("adb shell input tap {} {}".format(rd(x2), rd(y2)))
        time.sleep(1.2)
    os.system("adb shell input tap {} {}".format(rd(x02), rd(y02)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x0), rd(y0)))
    time.sleep(2.5)

def clear():
    # 转到工厂
    x01 = 319
    y01 = 87
    x02 = 632
    y02 = 352
    # 回收拆解
    x03 = 152
    y03 = 620
    # 选择角色
    x04 = 500
    y04 = 317
    # 点击拆解人形
    x1 = 170
    y1 = 383
    x2 = 435
    y2 = y1
    x3 = 684
    y3 = y1
    x4 = 967
    y4 = y1
    x5 = 1255
    y5 = y1
    x6 = 1505
    y6 = y1
    x7 = x1
    y7 = 797
    x8 = x2
    y8 = y7
    x9 = x3
    y9 = y7
    x10 = x4
    y10 = y7
    # 确定
    x05 = 1782
    y05 = 969
    # 拆解
    x06 = 1720
    y06 = 907
    x07 = 1172
    y07 = 945

    os.system("adb shell input tap {} {}".format(rd(x01), rd(y01)))
    time.sleep(1)
    os.system("adb shell input tap {} {}".format(rd(x02), rd(y02)))
    time.sleep(2)
    os.system("adb shell input tap {} {}".format(rd(x03), rd(y03)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x04), rd(y04)))
    time.sleep(1)
    os.system("adb shell input tap {} {}".format(rd(x1), rd(y1)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x2), rd(y2)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x3), rd(y3)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x4), rd(y4)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x5), rd(y5)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x6), rd(y6)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x7), rd(y7)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x8), rd(y8)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x9), rd(y9)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x10), rd(y10)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x05), rd(y05)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x06), rd(y06)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x07), rd(y07)))
    time.sleep(0.5)

def battle():
    #点击空白屏幕#
    x0 = 400
    y0 = 450
    # # 选择梯队
    # x01 = 917
    # y01 = 143
    # 点击左下角机场
    x1 = 798
    y1 = 770
    # 拖尸队
    x2 = 1759
    y2 = 956
    # 点击左上角机场
    x4 = 746
    y4 = 394
    # 狗粮队
    x5 = x2
    y5 = y2
    # 开始作战
    x7 = 1714
    y7 = 984
    # 点击左上角机场
    x8 = x4
    y8 = y4
    # 补给
    x9 = 1774
    y9 = 841
    # 点击左下角机场
    x10 = x1
    y10 = y1
    # 计划模式
    x11 = 179
    y11 = 884
    # 选择路径
    x12 = 906
    y12 = 552
    x13 = 959
    y13 = 549
    # 执行计划
    x14 = 1790
    y14 = 1000
    # 结束回合
    x15 = 1763
    y15 = 992

    os.system("adb shell input tap {} {}".format(rd(x1), rd(y1)))
    time.sleep(1.5)
    # os.system("adb shell input tap {} {}".format(rd(x01), rd(y01)))
    # time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x2), rd(y2)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x4), rd(y4)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x5), rd(y5)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x7), rd(y7)))
    time.sleep(2.5)
    os.system("adb shell input tap {} {}".format(rd(x8), rd(y8)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x8), rd(y8)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x9), rd(y9)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x10), rd(y10)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x11), rd(y11)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x12), rd(y12)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x13), rd(y13)))
    time.sleep(0.1)
    os.system("adb shell input tap {} {}".format(rd(x14), rd(y14)))
    time.sleep(160)
    
    threshold = 24
    while(True):
        os.system('adb shell screencap /sdcard/Pictures/girlsfrontline/test.png')
        # time.sleep(1)
        os.system('adb pull /sdcard/Pictures/girlsfrontline/test.png D:\ProgramData\mumu\Pictures\current')
        # time.sleep(1)
        os.system('adb shell rm /sdcard/Pictures/girlsfrontline/test.png')
        
        curImg = cv2.imread('D:/ProgramData/mumu/Pictures/current/test.png', 0)
        tarImg1 = cv2.imdecode(np.fromfile('C:/Users/aaa/Documents/MuMu共享文件夹/compare1.png', dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
        # tarImg2 = cv2.imread("C:\Users\aaa\Documents\MuMu共享文件夹\compare2.png", 0")
        
        cur_range = curImg.shape
        cur_line = cur_range[0]     # 行1080
        cur_column = cur_range[1]   # 列1920
        
        tar_range = tarImg1.shape
        tar_line = tar_range[0]
        tar_column = tar_range[1]
        
        height = 140    # 截取区域高
        width = 470     # 截取区域宽
        
        cur_cropImg = curImg[cur_line - height:cur_line, cur_column - width:cur_column]
        tar_cropImg = tarImg1[tar_line - height:tar_line, tar_column - width:tar_column]
    
        d = classify_aHash(cur_cropImg, tar_cropImg)
        if d == threshold or d < threshold:
            break
        else:
            continue

    os.system("adb shell input tap {} {}".format(rd(x15), rd(y15)))
    time.sleep(10)
    os.system("adb shell input tap {} {}".format(rd(x0), rd(y0)))
    time.sleep(5)
    os.system("adb shell input tap {} {}".format(rd(x0), rd(y0)))
    time.sleep(0.5)
    os.system("adb shell input tap {} {}".format(rd(x0), rd(y0)))
    time.sleep(5)

def choose12_4e(clr_count):
    # 选择12_4e关卡
    x1 = 1270
    y1 = 980
    # 普通作战
    x2 = 1520
    y2 = 900
    # 跳转进入战役
    x3 = 318
    y3 = 82
    x4 = 214
    y4 = 352
    if clr_count % 2 == 0:
        clear()
        os.system("adb shell input tap {} {}".format(rd(x3), rd(y3)))
        time.sleep(1)
        os.system("adb shell input tap {} {}".format(rd(x4), rd(y4)))
        time.sleep(2.5)
        os.system("adb shell input tap {} {}".format(rd(x1), rd(y1)))
        time.sleep(0.5)
        os.system("adb shell input tap {} {}".format(rd(x2), rd(y2)))
        time.sleep(5)
    else:
        os.system("adb shell input tap {} {}".format(rd(x1), rd(y1)))
        time.sleep(0.5)
        os.system("adb shell input tap {} {}".format(rd(x2), rd(y2)))
        time.sleep(5)




if __name__ == '__main__':
    clr_count = 0
    fix_count = 0
    prepare()
    while 1:
        changeHKorM4(fix_count)
        battle()
        clr_count = clr_count + 1
        fix_count = fix_count + 1
        choose12_4e(clr_count)