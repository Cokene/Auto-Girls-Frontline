from BattleAutoGFL import *
from airtest.core.android import Android


class AutoZeroTwoGFL:
    pass

class AutoFourSixGFL:
    pass

class AutoEightOneNightGFL:
    pass

class AutoTwelveFourExtremeGFL:
    pass

class AutoThirteenFourGFL(BattleAutoGFL):
    def __init__(self):
        super(AutoThirteenFourGFL, self).__init__()
        # 图像状态判断区域 #
        self.CHOOSE_13_4_IMAGE_BOX = [375, 362, 450, 409, '_13_4.png']  # 13-4菜单界面判断区域
        self.FIGURE_VECTOR_IMAGE_BOX = [95, 295, 180, 325, 'vector.png']  # 燃烧弹人形更换检测判断区域
        self.FIGURE_MICROUZI_IMAGE_BOX = [95, 295, 180, 325, 'microuzi.png']  # 燃烧弹人形更换检测判断区域
        self.FIGURE_DETECT_IMAGE_BOX = [95, 295, 180, 325, 'figure_detect.png']  # 燃烧弹人形更换检测判断区域
        self.COMBAT_START_IMAGE_BOX = [600, 445, 727, 481, 'combat_start.png']  # 开启作战判断区域
        self.COMBAT_FINISH_IMAGE_BOX = [330, 227, 439, 323, 'combat_finish.png']  # 战役完成判断区域

        # 控制动作区域 #
        # 从作战选择界面进入13-4战役界面
        self.COMBAT_MISSION_CLICK_BOX = [37, 127, 75, 145]  # 点击作战任务
        self.CHAPTER_DRAG_BOX = [135, 404, 156, 434]  # 向上拖章节选择条
        self.CHAPTER_13_CLICK_BOX = [127, 422, 150, 440]  # 选择第13章
        self.NORMAL_CLICK_BOX = [570, 104, 592, 127]  # 选择普通难度
        self.EPISODE_DRAG_BOX = [300, 169, 600, 198]  # 向下拖小节选择条

        # 开始13-4的战役
        self.EPISODE_4_CLICK_BOX = [375, 369, 450, 398]  # 选择第4节
        self.ENTER_COMBAT_CLICK_BOX = [540, 375, 600, 404]  # 打开作战子页
        self.END_COMBAT_STEP1_CLICK_BOX = [540, 328, 600, 351]  # 终止作战
        self.END_COMBAT_STEP2_CLICK_BOX = [390, 316, 450, 345]  # 确认终止作战

        # 机场位置点
        self.AIRPORT_1_CLICK_BOX = [0, 303, 5, 314]  # 左机场
        self.AIRPORT_2_CLICK_BOX = [365, 244, 378, 259]  # 右机场

        # 更换打手Echelon formation
        self.CHANGE_FORCE_ECHELON_FORMATION_CLICK_BOX = [120, 403, 172, 413]  # 点击梯队编成

        self.CHANGE_FORCE_V_STEP1_CLICK_BOX = [112, 169, 187, 286]  # 点击Vector
        self.CHANGE_FORCE_V_STEP2_CLICK_BOX = [667, 163, 720, 180]  # 点击显示种类
        self.CHANGE_FORCE_V_STEP3_CLICK_BOX = [562, 98, 577, 110]  # 点击四星
        self.CHANGE_FORCE_V_STEP4_CLICK_BOX = [450, 228, 472, 239]  # 点击冲锋枪
        self.CHANGE_FORCE_V_STEP5_CLICK_BOX = [532, 392, 570, 404]  # 点击确认
        self.CHANGE_FORCE_V_STEP6_CLICK_BOX = [142, 122, 195, 163]  # 选择MicroUZI
        self.CHANGE_FORCE_V_STEP7_CLICK_BOX = [52, 20, 75, 39]  # 点击返回

        self.CHANGE_FORCE_U_STEP1_CLICK_BOX = [112, 169, 187, 286]  # 点击MicroUZI
        self.CHANGE_FORCE_U_STEP2_CLICK_BOX = [667, 163, 720, 180]  # 点击显示种类
        self.CHANGE_FORCE_U_STEP3_CLICK_BOX = [450, 98, 472, 110]  # 点击五星
        self.CHANGE_FORCE_U_STEP4_CLICK_BOX = [450, 228, 472, 239]  # 点击冲锋枪
        self.CHANGE_FORCE_U_STEP5_CLICK_BOX = [532, 392, 570, 404]  # 点击确认
        self.CHANGE_FORCE_U_STEP6_CLICK_BOX = [135, 404, 165, 434]  # 拖动人形菜单
        self.CHANGE_FORCE_U_STEP7_CLICK_BOX = [352, 398, 390, 422]  # 选择Vector
        self.CHANGE_FORCE_U_STEP8_CLICK_BOX = [52, 20, 75, 39]  # 点击返回

        # 计划模式
        self.PLAN_POINT1_CLICK_BOX = [312, 243, 324, 256]  # 点击计划点1
        self.PLAN_POINT2_CLICK_BOX = [370, 412, 379, 422]  # 点击计划点2

    # 检测图像所处的状态函数 Image on Status（有限状态机） #
    # 判断是否是可以选择13-4的界面
    def is13_4(self):
        IMAGE_BOX = self.CHOOSE_13_4_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "_13_4.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断更换的人形名称
    def isVector(self):
        IMAGE_BOX = self.FIGURE_VECTOR_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "vector.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    def isMicroUZI(self):
        IMAGE_BOX = self.FIGURE_MICROUZI_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "microuzi.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否作战正常开启
    def isCombatStart(self):
        IMAGE_BOX = self.COMBAT_START_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "combat_start.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否战役结束
    def isCombatFinished(self):
        IMAGE_BOX = self.COMBAT_FINISH_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "combat_finish.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 控制脚本行动逻辑函数 Action on Image #
    # 由战斗菜单跳转至13-4战役界面
    def combatMenu2_13_4SubMenu(self):
        print("ACTION: 前往13-4战役选择界面")
        self.mouseClick(self.COMBAT_MISSION_CLICK_BOX, 1, 2)
        self.mouseDrag(self.CHAPTER_DRAG_BOX, 0, -1, 2, 400, 0.001, 0.8)
        self.mouseClick(self.CHAPTER_13_CLICK_BOX, 1, 2)
        self.mouseClick(self.NORMAL_CLICK_BOX, 1, 2)
        self.mouseDrag(self.EPISODE_DRAG_BOX, 0, 1, 1, 300, 0.001, 1)

    # 开始13-4作战战役
    def start13_4(self):
        print("ACTION: 启动13-4")
        self.mouseClick(self.EPISODE_4_CLICK_BOX, 1, 1)
        self.mouseClick(self.ENTER_COMBAT_CLICK_BOX, 6, 7)

    # 终止13-4作战战役（作战界面）
    def end13_4(self):
        print("ACTION: 终止13-4")
        self.mouseClick(self.EPISODE_4_CLICK_BOX, 2, 3)
        self.mouseClick(self.END_COMBAT_STEP1_CLICK_BOX, 2, 3)
        self.mouseClick(self.END_COMBAT_STEP2_CLICK_BOX, 2, 3)

    # 更换燃烧弹人形
    def changeForce(self):
        print("ACTION: 更换燃烧弹打工人")
        self.mouseClick(self.AIRPORT_1_CLICK_BOX, 0, 0)  # 点击左侧机场
        if not (self.ImagesJudgeLoop(self.SET_TEAM_IMAGE_BOX, 20)
                or self.ImagesJudgeLoop(self.SET_HA_TEAM_IMAGE_BOX, 20)):
            return False
        time.sleep(0.6)
        if self.isSetHATeam():
            self.mouseClick(self.TEAM_SHIFT_CLICK_BOX, 1, 2)  # 切换为普通队伍
            
        # 判断当前人形是否为Vector
        if self.isVector():
            self.mouseClick(self.CHANGE_FORCE_ECHELON_FORMATION_CLICK_BOX, 0, 0)  # 点击队伍编成
            if not self.ImagesJudgeLoop(self.FORM_TEAM_IMAGE_BOX, 20):
                return False
            time.sleep(0.8)
            self.mouseClick(self.CHANGE_FORCE_V_STEP1_CLICK_BOX, 0.5, 0.5)  # 点击打手
            if not self.ImagesJudgeLoop(self.CHANGE_MEMBER_IMAGE_BOX, 20):
                return False
            time.sleep(0.6)
            self.mouseClick(self.CHANGE_FORCE_V_STEP2_CLICK_BOX, 0.5, 0.5)  # 点击显示种类
            self.mouseClick(self.CHANGE_FORCE_V_STEP3_CLICK_BOX, 0.5, 0.5)  # 点击四星
            self.mouseClick(self.CHANGE_FORCE_V_STEP4_CLICK_BOX, 0.5, 0.5)  # 点击冲锋枪
            self.mouseClick(self.CHANGE_FORCE_V_STEP5_CLICK_BOX, 1, 1)  # 点击确认
            self.mouseClick(self.CHANGE_FORCE_V_STEP6_CLICK_BOX, 0, 0)  # 选择MicroUZI
            if not self.ImagesJudgeLoop(self.FORM_TEAM_IMAGE_BOX, 20):
                return False
            time.sleep(0.8)
            self.mouseClick(self.CHANGE_FORCE_V_STEP7_CLICK_BOX, 0, 0)  # 点击返回战役地图
        # 反之则判断为MicroUzi
        elif self.isMicroUZI():
            self.mouseClick(self.CHANGE_FORCE_ECHELON_FORMATION_CLICK_BOX, 0, 0)  # 点击队伍编成
            if not self.ImagesJudgeLoop(self.FORM_TEAM_IMAGE_BOX, 20):
                return False
            time.sleep(0.8)
            self.mouseClick(self.CHANGE_FORCE_U_STEP1_CLICK_BOX, 0.5, 0.5)  # 点击打手
            if not self.ImagesJudgeLoop(self.CHANGE_MEMBER_IMAGE_BOX, 20):
                return False
            time.sleep(0.6)
            self.mouseClick(self.CHANGE_FORCE_U_STEP2_CLICK_BOX, 0.5, 0.5)  # 点击显示种类
            self.mouseClick(self.CHANGE_FORCE_U_STEP3_CLICK_BOX, 0.5, 0.5)  # 点击五星
            self.mouseClick(self.CHANGE_FORCE_U_STEP4_CLICK_BOX, 0.5, 0.5)  # 点击冲锋枪
            self.mouseClick(self.CHANGE_FORCE_U_STEP5_CLICK_BOX, 1, 1)  # 点击确认
            self.mouseDrag(self.CHANGE_FORCE_U_STEP6_CLICK_BOX, 0, -1, 2, 400, 0.001, 0.8)  # 拖动人形菜单
            self.mouseClick(self.CHANGE_FORCE_U_STEP7_CLICK_BOX, 0, 0)  # 选择Vector
            if not self.ImagesJudgeLoop(self.FORM_TEAM_IMAGE_BOX, 20):
                return False
            time.sleep(0.8)
            self.mouseClick(self.CHANGE_FORCE_U_STEP8_CLICK_BOX, 0, 0)  # 点击返回战役地图
        
        if not self.ImagesJudgeLoop(self.IN_MAP_IMAGE_BOX, 20):
            return False
        time.sleep(0.8)
        # self.combatFixedMapLocation()  # 固定住地图位置（目前不需要）
        return True

    # 计划模式
    def planMode(self):
        print("计划模式")
        self.mouseClick(self.AIRPORT_2_CLICK_BOX, 0.8, 1)
        self.mouseClick(self.PLAN_MODE_CLICK_BOX, 1, 1.5)
        self.mouseClick(self.PLAN_POINT1_CLICK_BOX, 0.5, 0.7)
        self.mouseClick(self.PLAN_POINT2_CLICK_BOX, 0.5, 0.7)
        self.mouseClick(self.PLAN_START_CLICK_BOX, 0, 0)

    def run(self):
        # 该部分实现包含的全部操作及判断逻辑
        # self.preface()
        startTime = datetime.datetime.now()
        combatCount = 0
        firstCombat = False  # 启动时会给一队单独补给并重开
        failCount = 0
        # combatPause = False

        while True:
            # 暂停一下好让我发一会儿呆（不是XD
            keys = key_check()
            if 'T' in keys:
                if self.paused:
                    self.paused = False
                    print('取消暂停')
                    time.sleep(1)
                else:
                    self.paused = True
                    print('暂停...')
                    time.sleep(1)
            # 结束脚本进程
            if 'Q' in keys:
                print('终止进程')
                cv2.destroyAllWindows()
                sys.exit()

            if not self.paused:
                # 查看GPU显存占用信息
                self.freeGraphicProcessUnitMemory()
                if self.isInMap():
                    print("STATE：进入地图")
                    failCount = 0
                    if firstCombat:
                        firstCombat = False
                        if not self.combatPrepare():
                            self.closeGame()
                        continue
                    if not self.changeForce():
                        print("ERROR：更换打手失败")
                        self.closeGame()
                        continue
                    if not self.setTeam(self.AIRPORT_1_CLICK_BOX, self.AIRPORT_2_CLICK_BOX):
                        print("ERROR：队伍放置失败")
                        self.closeGame()
                        continue
                    if not self.startCombat(self.COMBAT_START_IMAGE_BOX):
                        print("ERROR：战役启动失败")
                        continue
                    if not self.supply(self.AIRPORT_1_CLICK_BOX):
                        print("ERROR：补给打手失败")
                        self.closeGame()
                        continue
                    self.planMode()
                    # 计划开始后200s还没打完，一般是出问题了
                    # （比方说卡了一下导致流程漏了）
                    checkCount = 0
                    while (not self.isCombatFinished()) and checkCount < 200:
                        checkCount += 1
                        time.sleep(1)
                    if checkCount >= 200:  # 过了200s还没结束，直接关闭窗口重启
                        if self.isResumeCombat():
                            self.endCombat(self.CHOOSE_13_4_IMAGE_BOX)
                            continue
                        else:
                            print("ERROR：战斗超时！")
                            self.closeGame()
                            continue
                    if not self.endCombat(self.CHOOSE_13_4_IMAGE_BOX):  # 结束战役
                        print("ERROR：战役结束失败")
                        self.closeGame()
                        continue
                    combatCount += 1
                    currentTime = datetime.datetime.now()
                    runtime = currentTime - startTime
                    print('已运行：' + str(runtime) + '  13-4轮次：' + str(combatCount))
                    # if combatCount %2 == 0:    #每2轮收一次后勤（可选）
                    #     backToMainMenu()
                elif self.is13_4():
                    print("STATE： 13-4界面")
                    self.start13_4()
                    failCount = 0
                elif self.isGotoPowerup():
                    print("STATE： 强化提醒界面")
                    # firstCombat = True
                    self.gotoRetire()
                    # firstCombat = True
                    self.back2MainMenu()
                elif self.isCombatMenu():
                    print("STATE： 战斗菜单")
                    self.combatMenu2_13_4SubMenu()
                    failCount = 0
                elif self.isCombatPause():
                    print("STATE： 战斗中断提醒界面")
                    failCount = 0
                    self.closeTips()
                elif self.isReturnCombat():
                    print("STATE： 返回作战界面")
                    failCount = 0
                    self.return2Combat()
                    self.resumeCombat(self.CHOOSE_13_4_IMAGE_BOX)
                    firstCombat = True
                elif self.isMainMenu():
                    print("STATE： 主菜单界面")
                    self.mainMenu2CombatMenu()
                    failCount = 0
                elif self.isLSupport():
                    print("STATE： 后勤结束界面")
                    self.takeLSupport()
                    failCount = 0
                elif self.isDesktop():
                    print("STATE：模拟器桌面")
                    firstCombat = True
                    failCount = 0
                    self.startGame()
                    continue
                elif self.isFirstLogin():
                    print("STATE：公告确认")
                    failCount = 0
                    self.confirmAnnouncement()
                    continue
                # 当脚本不知道此时状态在哪时
                else:
                    print("ERROR： 当前状态未知!")
                    failCount += 1
                    if failCount == 4:
                        # 尝试点击游戏画面任意一处位置
                        self.mouseClick(self.SAVE_MODE_CLICK_BOX, 1, 1)
                    if failCount >= 5:
                        # 截取全幅大小图像
                        img = self.getImage([0, 0, 1, 1])
                        # 记录异常发生时当前具体状态信息图像
                        img.save("errorRecord/" + str(datetime.datetime.now()) + str(combatCount) + ".png")
                        print(">>> ", datetime.datetime.now(), " 无法确定当前状态,关闭重启！")
                        self.closeGame()
                    else:
                        time.sleep(5)

class AutoThirteenFourExtremeGFL:
    pass

class AutoLSupportGFL:
    pass

class AutoSCGFL:
    pass


if __name__ == '__main__':
    print("正在启动脚本...")
    auto13_4 = AutoThirteenFourGFL()
    auto13_4.run()

    # auto13_4.saveStatusImage(auto13_4.COMBAT_FINISH_IMAGE_BOX)
    # auto13_4.transback(auto13_4.EPISODE_DRAG_BOX)