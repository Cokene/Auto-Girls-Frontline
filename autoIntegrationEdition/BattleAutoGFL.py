import time

from BaseAutoGFL import *

class BattleAutoGFL(BaseAutoGFL):
    # 游戏战斗参数变量
    def __init__(self):
        super(BattleAutoGFL, self).__init__()
        self.firstCombat = False  # 启动时会给一队单独补给并重开

        # 图像状态判断区域 #
        self.COMBAT_MENU_IMAGE_BOX = [37, 375, 90, 434, 'combat_menu.png']  # 战斗菜单界面判断区域
        self.IN_MAP_IMAGE_BOX = [615, 434, 712, 481, 'in_map.png']  # 战役地图判断区域
        self.SET_TEAM_IMAGE_BOX = [637, 404, 690, 422, 'set_team.png']  # 队伍放置判断区域
        self.SET_HA_TEAM_IMAGE_BOX = [90, 127, 150, 151, 'set_ha_team.png']  # 重装队伍队伍放置判断区域
        self.FORM_TEAM_IMAGE_BOX = [210, 186, 285, 257, 'form_team.png']  # 队伍编成判断区域
        self.CHANGE_MEMBER_IMAGE_BOX = [675, 139, 712, 198, 'change_member.png']  # 人员选择判断区域
        self.TEAM_INFO_IMAGE_BOX = [637, 357, 705, 381, 'team_info.png']  # 队伍补给详情页判断区域
        self.GOTO_POWERUP_IMAGE_BOX = [465, 219, 533, 241, 'goto_powerup.png']  # 提醒强化判断区域
        self.GOTO_EQUIPMENT_POWERUP_IMAGE_BOX = [472, 222, 551, 315, 'goto_equipment_powerup.png']  # 提醒装备强化判断区域
        self.COMBAT_PAUSE_IMAGE_BOX = [337, 328, 412, 357, 'combat_pause.png']  # 战斗终止提示判断区域(standby)
        self.RETURN_COMBAT_IMAGE_BOX = [641, 348, 732, 380, 'return_combat.png']  # 回到作战界面判断区域
        self.NON_RETIRE_IMAGE_BOX = [172, 157, 202, 192, 'non_retire.png']  # 人形回收判断区域
        self.NON_EQUIPMENT_RETIRE_IMAGE_BOX = [172, 157, 202, 192, 'non_equipment_retire.png']  # 装备回收判断区域
        self.ANTHROPOMORPHIC_ROBOT_POWERUP_IMAGE_BOX = [410, 197, 483, 335, 'anthropomorphic_robot_powerup.png']  # 人形强化判断区域
        self.EQUIPMENT_POWERUP_IMAGE_BOX = [136, 128, 244, 170, 'equipment_powerup.png']  # 强化装备判断区域
        self.RESUME_COMBAT_IMAGE_BOX = [577, 440, 630, 487, 'resume_combat.png']  # 重新结束战役判断区域（异常处理判断区域）

        # 控制动作区域 #
        # 从主菜单进入作战选择界面
        self.COMBAT_CLICK_BOX = [487, 257, 562, 304]  # 在主菜单点击战斗（无作战进行中情况）
        self.COMBAT_BREAK_CLICK_BOX = [487, 257, 562, 304]  # 在主菜单点击战斗（作战中断情况）

        # 缩小地图，拖动地图
        self.MAP_SCALE_BOX = [75, 80, 150, 110]
        self.MAP_DRAG_BOX = [112, 80, 187, 110]

        # 放置队伍
        self.TEAM_SHIFT_CLICK_BOX = [315, 80, 360, 104]  # 切换成普通梯队
        self.TEAM_SET_CLICK_BOX = [637, 404, 690, 422]  # 放置梯队

        # 开始作战
        self.START_COMBAT_CLICK_BOX = [637, 445, 690, 469]  # 点击开始作战

        # 关闭作战断开提醒
        self.CLOSE_TIP_CLICK_BOX = [337, 328, 412, 357]  # 关闭提醒(deprecated)

        # 结束作战
        self.END_COMBAT_CLICK_BOX = [675, 457, 705, 469]  # 点击结束作战

        # 返回作战
        self.RETURN_COMBAT_CLICK_BOX = [562, 351, 675, 369]  # 返回战役作战界面

        # 计划模式
        self.PLAN_MODE_CLICK_BOX = [30, 416, 75, 428]  # 点击计划模式
        self.PLAN_START_CLICK_BOX = [660, 445, 735, 463]  # 点击执行计划

        # 补给人形
        self.SUPPLY_CLICK_BOX = [637, 363, 705, 375]  # 点击补给

        # 撤退人形
        self.WITHDRAW_STEP1_CLICK_BOX = [540, 410, 585, 422]  # 点击撤退
        self.WITHDRAW_STEP2_CLICK_BOX = [412, 322, 465, 339]  # 确认撤退

        # 重启战役作战
        self.RESTART_STEP1_CLICK_BOX = [165, 16, 195, 45]  # 点击终止作战
        self.RESTART_STEP2_CLICK_BOX = [255, 322, 322, 334]  # 点击重新作战

        # 拆解人形
        self.GOTO_POWERUP_CLICK_BOX = [502, 263, 547, 304]  # 前往强化界面
        self.CHOOSE_RETIRE_CLICK_BOX = [45, 233, 90, 257]  # 选择回收拆解选项
        self.CHOOSE_RETIRE_CHARACTER_CLICK_BOX = [187, 116, 225, 157]  # 选择拆解人形
        self.RETIRE_CHARACTER_1_CLICK_BOX = [90, 139, 105, 175]  # 第一行的第一只人形
        self.RETIRE_CHARACTER_2_CLICK_BOX = [180, 139, 195, 175]  # 第一行的第二只人形
        self.RETIRE_CHARACTER_3_CLICK_BOX = [270, 139, 285, 175]  # 第一行的第三只人形
        self.RETIRE_CHARACTER_4_CLICK_BOX = [360, 139, 375, 175]  # 第一行的第四只人形
        self.RETIRE_CHARACTER_5_CLICK_BOX = [450, 139, 465, 175]  # 第一行的第五只人形
        self.RETIRE_CHARACTER_6_CLICK_BOX = [540, 139, 555, 175]  # 第一行的第六只人形
        self.RETIRE_DRAG_BOX = [300, 316, 450, 316]  # 往上拖一行
        self.CHOOSE_FINISH_RETIRE_CLICK_BOX = [660, 363, 690, 398]  # 完成选择
        self.RETIRE_CLICK_BOX = [630, 416, 675, 434]  # 点击拆解
        self.CONFIRM_RETIRE_CLICK_BOX = [405, 398, 480, 422]  # 确认拆解高星人形

        # 强化人形
        self.CHOOSE_POWERUP_CHARACTER_CLICK_BOX = [150, 198, 225, 257]  # 选择被强化人形
        self.FIRST_CHARACTER_CLICK_BOX = [75, 139, 105, 175]  # 选择第一只人形
        self.CHOOSE_EXP_CHARACTER_CLICK_BOX = [300, 151, 322, 175]  # 选择狗粮
        self.AUTO_CHOOSE_CLICK_BOX = [660, 351, 705, 387]  # 智能选择
        self.CHOOSE_CONFIRM_CLICK_BOX = [660, 351, 705, 387]  # 完成选择
        self.POWERUP_CLICK_BOX = [645, 404, 690, 422]  # 点击强化
        self.POWERUP_FINISH_CLICK_BOX = [345, 339, 405, 351]  # 完成强化

        # 拆解装备(standby)

        # 强化装备
        self.CHOOSE_POWERUP_EQUIPMENT_CLICK_BOX = [159, 235, 220, 310]  # 选择被强化装备
        self.FIRST_EQUIPMENT_CLICK_BOX = [31, 102, 87, 143]  # 选择第一件需要强化装备
        self.CHOOSE_EXP_EQUIPMENT_CLICK_BOX = [300, 150, 340, 180]  # 选择低品质装备
        self.AUTO_CHOOSE_EQUIPMENT_CLICK_BOX = [660, 351, 705, 387]  # 智能选择装备
        self.CHOOSE_CONFIRM_EQUIPMENT_CLICK_BOX = [660, 351, 705, 387]  # 完成选择
        self.POWERUP_EQUIPMENT_CLICK_BOX = [663, 406, 723, 420]  # 点击强化
        self.POWERUP_EQUIPMENT_FINISH_CLICK_BOX = [410, 395, 486, 412]  # 完成强化

        # 跳至主菜单/战斗菜单/工厂菜单
        self.NAVIGATE_BAR_CLICK_BOX = [114, 24, 132, 42]  # 打开导航条
        self.NAVIGATE_BAR_DRAG_BOX = [75, 127, 127, 151]  # 向右拖导航条
        self.NAVIGATE_COMBAT_CLICK_BOX = [73, 127, 94, 144]  # 跳转至作战菜单
        self.NAVIGATE_FACTORY_CLICK_BOX = [280, 128, 300, 147]  # 跳转至工厂菜单
        self.NAVIGATE_MAIN_MENU_CLICK_BOX = [150, 69, 210, 80]  # 跳转至主菜单（返回基地）

    # 模拟Ctrl加滚轮实现的缩放地图功能
    # direct = 0 : 放大    direct = 1 : 缩小    times : 连续缩放次数
    def scaleMap(self, box, direct, times):
        windowData = self.getWindowData()
        width = box[2] - box[0]
        height = box[3] - box[1]
        scaleX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width * random.random())
        scaleY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
        scalePos = (scaleX, scaleY)
        win32api.SetCursorPos(scalePos)
        win32api.keybd_event(0x11, 0, 0, 0)  # 按下Ctrl键
        for i in range(times):
            if direct == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 1)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)
            self.wait(0.5, 0.7)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(1)  # 进程中断1s

    # 检测图像所处的状态函数 Image on Status（有限状态机） #
    # 在工厂资源回收界面
    def isNonRetire(self):
        IMAGE_BOX = self.NON_RETIRE_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "non_retire.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在工厂装备资源回收界面
    def isNonEquipmentRetire(self):
        IMAGE_BOX = self.NON_EQUIPMENT_RETIRE_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "non_equipment_retire.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在工厂强化界面
    def isAnthropomorphicRobotPowerup(self):
        IMAGE_BOX = self.ANTHROPOMORPHIC_ROBOT_POWERUP_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "anthropomorphic_robot_powerup.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在工厂装备强化界面
    def isEquipmentPowerup(self):
        IMAGE_BOX = self.EQUIPMENT_POWERUP_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "equipment_powerup.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否是战斗选择菜单
    def isCombatMenu(self):
        IMAGE_BOX = self.COMBAT_MENU_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "combat_menu.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否进入作战战役地图
    def isInMap(self):
        IMAGE_BOX = self.IN_MAP_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "in_map.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在队伍放置界面
    def isSetTeam(self):
        IMAGE_BOX = self.SET_TEAM_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "set_team.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在布置重装的界面
    def isSetHATeam(self):
        IMAGE_BOX = self.SET_HA_TEAM_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "set_ha_team.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在队伍编成界面
    def isFormTeam(self):
        IMAGE_BOX = self.FORM_TEAM_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "form_team.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在人员选择界面
    def isChangeMember(self):
        IMAGE_BOX = self.CHANGE_MEMBER_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "change_member.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 在队伍详情界面
    def isTeamInfo(self):
        IMAGE_BOX = self.TEAM_INFO_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "team_info.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否是提醒强化界面
    def isGotoPowerup(self):
        IMAGE_BOX = self.GOTO_POWERUP_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "goto_powerup.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否时提醒装备强化界面
    def isGotoEquipmentPowerup(self):
        IMAGE_BOX = self.GOTO_EQUIPMENT_POWERUP_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "goto_equipment_powerup.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否有回到作战界面
    def isReturnCombat(self):
        IMAGE_BOX = self.RETURN_COMBAT_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "return_combat.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断战斗终止提醒界面
    def isCombatPause(self):
        IMAGE_BOX = self.COMBAT_PAUSE_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "combat_pause.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 判断是否需要重新结束战役
    def isResumeCombat(self):
        IMAGE_BOX = self.RESUME_COMBAT_IMAGE_BOX[:4]
        NORM_IMAGE_BOX = self.trans(IMAGE_BOX)
        initImage = cv2.imread(self.IMAGE_PATH + "resume_combat.png")
        capImage = self.getImage(NORM_IMAGE_BOX)
        capImage = cv2.cvtColor(np.asarray(capImage), cv2.COLOR_RGB2BGR)
        return self.imageCompare(initImage, capImage)

    # 控制脚本行动逻辑函数 Action on Image #
    # 主菜单跳转至战斗菜单
    def mainMenu2CombatMenu(self, break_Off=False):
        # 若遇到战斗中断情况
        if break_Off:
            print("ACTION: 前往作战菜单-战斗中断")
            self.mouseClick(self.COMBAT_BREAK_CLICK_BOX, 5, 6)
        else:
            print("ACTION: 前往作战菜单")
            self.mouseClick(self.COMBAT_CLICK_BOX, 2, 3)

    # 战前准备，调整地图（新）
    def combatPrepare(self):
        print("ACTION: 战前整备")
        self.mouseClick(self.MAP_SCALE_BOX, 0.5, 0.6)
        self.scaleMap(self.MAP_SCALE_BOX, 1, 12)  # 拉扯（缩放）12次XD
        # self.mouseDrag(self.MAP_DRAG_BOX, 1, 1, 1, 240, 0.001, 1)  # 该拖拉操作暂时不用
        return True

    # 固定地图位置
    def combatFixedMapLocation(self):
        self.scaleMap(self.MAP_SCALE_BOX, 1, 1)  # 缩放地图
        self.mouseDrag(self.MAP_DRAG_BOX, 1, 1, 1, 400, 0.001, 1)  # 拉扯地图固定位置

    # 更换打手人形
    def changeForce(self):
        pass

    # 放置肝枪队伍
    # CONSTANT_COORD1_BOX指定机场坐标放置的为拖尸人（输出人形）XD
    # CONSTANT_COORD2_BOX指定机场坐标放置的为主力队伍
    def setTeam(self, CONSTANT_COORD1_BOX, CONSTANT_COORD2_BOX):
        print("ACTION: 放置队伍人形")
        self.mouseClick(CONSTANT_COORD1_BOX, 0, 0)  # 选中拖尸人空降机场
        if not (self.ImagesJudgeLoop(self.SET_TEAM_IMAGE_BOX, 20)
                or self.ImagesJudgeLoop(self.SET_HA_TEAM_IMAGE_BOX, 20)):
            return False
        time.sleep(0.4)  # 进程中断0.4s
        if self.isSetHATeam():
            self.mouseClick(self.TEAM_SHIFT_CLICK_BOX, 0, 0)  # 切换为步战梯队
        if not self.ImagesJudgeLoop(self.SET_TEAM_IMAGE_BOX, 10):
            return False
        self.mouseClick(self.TEAM_SET_CLICK_BOX, 0, 0)  # 选中空降需补给队伍
        if not self.ImagesJudgeLoop(self.IN_MAP_IMAGE_BOX, 20):
            return False

        time.sleep(0.4)

        self.mouseClick(CONSTANT_COORD2_BOX, 0, 0)  # 选中主力人形空降机场
        if not self.ImagesJudgeLoop(self.SET_TEAM_IMAGE_BOX, 20):
            return False
        time.sleep(0.4)
        self.mouseClick(self.TEAM_SET_CLICK_BOX, 0, 0)  # 选中空降主力步战队伍
        if not self.ImagesJudgeLoop(self.IN_MAP_IMAGE_BOX, 20):
            return False
        time.sleep(0.4)
        return True

    # 补给打手人形
    def supply(self, CONSTANT_COORD1_BOX):
        print("ACTION: 补给打工人")
        self.mouseClick(CONSTANT_COORD1_BOX, 1, 1)
        self.mouseClick(CONSTANT_COORD1_BOX, 1, 1)
        self.mouseClick(self.SUPPLY_CLICK_BOX, 1.5, 1.5)
        return True

    # 计划模式
    def planMode(self):
        pass

    # 开始战役作战
    def startCombat(self, CONSTANT_IMAGE_BOX):
        print("ACTION: 开始作战行动")
        self.mouseClick(self.START_COMBAT_CLICK_BOX, 0, 0)
        if not self.ImagesJudgeLoop(CONSTANT_IMAGE_BOX, 20):
            return False
        time.sleep(2)
        return True

    # 结束战役作战
    def endCombat(self, CONSTANT_IMAGE_BOX):
        print("ACTION: 战役结算")
        time.sleep(1)
        self.mouseClick(self.END_COMBAT_CLICK_BOX, 5, 6)
        if not self.ImagesJudgeLoop(CONSTANT_IMAGE_BOX, 100):
            return False
        return True

    # 重启战役作战
    def restartCombat(self):
        print("ACTION: 重启作战行动")
        self.mouseClick(self.RESTART_STEP1_CLICK_BOX, 1, 1.5)
        self.mouseClick(self.RESTART_STEP2_CLICK_BOX, 0, 0)
        if not self.ImagesJudgeLoop(self.IN_MAP_IMAGE_BOX, 20):
            return False
        time.sleep(1)
        return True

    # 拆解人形
    def gotoRetire(self):
        print("ACTION: 拆解人形")
        self.mouseClick(self.GOTO_POWERUP_IMAGE_BOX, 5, 6)  # 跳转至工厂界面
        self.mouseClick(self.CHOOSE_RETIRE_CLICK_BOX, 1, 1)  # 点击资源回收
        # 回收趟数
        for i in range(4):
            self.mouseClick(self.CHOOSE_RETIRE_CHARACTER_CLICK_BOX, 0.3, 0.5)  # 点击选择角色
            if self.isNonRetire():
                time.sleep(0.5)
                break
            self.mouseClick(self.RETIRE_CHARACTER_1_CLICK_BOX, 0.2, 0.3)  # 选六个
            self.mouseClick(self.RETIRE_CHARACTER_2_CLICK_BOX, 0.2, 0.3)
            self.mouseClick(self.RETIRE_CHARACTER_3_CLICK_BOX, 0.2, 0.3)
            self.mouseClick(self.RETIRE_CHARACTER_4_CLICK_BOX, 0.2, 0.3)
            self.mouseClick(self.RETIRE_CHARACTER_5_CLICK_BOX, 0.2, 0.3)
            self.mouseClick(self.RETIRE_CHARACTER_6_CLICK_BOX, 0.2, 0.3)
            self.mouseClick(self.CHOOSE_FINISH_RETIRE_CLICK_BOX, 0.5, 1)
            self.mouseClick(self.RETIRE_CLICK_BOX, 1, 1)
            self.mouseClick(self.CONFIRM_RETIRE_CLICK_BOX, 2, 3)

    # 强化人形
    def gotoPowerup(self):
        print("ACTION: 强化人形")
        self.mouseClick(self.GOTO_POWERUP_CLICK_BOX, 5, 6)
        self.mouseClick(self.CHOOSE_POWERUP_CHARACTER_CLICK_BOX, 1, 2)
        self.mouseClick(self.FIRST_CHARACTER_CLICK_BOX, 1, 2)
        self.mouseClick(self.CHOOSE_EXP_CHARACTER_CLICK_BOX, 2, 3)
        self.mouseClick(self.AUTO_CHOOSE_CLICK_BOX, 1, 2)
        self.mouseClick(self.CHOOSE_CONFIRM_CLICK_BOX, 1, 2)
        self.mouseClick(self.POWERUP_CLICK_BOX, 3, 4)
        self.mouseClick(self.POWERUP_FINISH_CLICK_BOX, 3, 4)

    # 分解装备
    def gotoEquipmentRetire(self):
        pass

    # 强化装备
    def gotoEquipmentPowerup(self):
        pass

    # 跳转至主菜单（回主菜单收后勤资源）
    def back2MainMenu(self):
        print("ACTION: 跳转至主菜单")
        self.mouseClick(self.NAVIGATE_BAR_CLICK_BOX, 1, 2)
        self.mouseClick(self.NAVIGATE_MAIN_MENU_CLICK_BOX, 6, 7)

    # 跳转至工厂
    def gotoFactory(self):
        print("ACTION: 跳转至工厂")
        self.mouseClick(self.NAVIGATE_BAR_CLICK_BOX, 1, 2)
        self.mouseClick(self.NAVIGATE_FACTORY_CLICK_BOX, 6, 6)

    # 跳转至战斗菜单
    def back2CombatMenu(self):
        print("ACTION: 跳转至战斗菜单")
        self.mouseClick(self.NAVIGATE_BAR_CLICK_BOX, 1, 2)
        self.mouseClick(self.NAVIGATE_COMBAT_CLICK_BOX, 5, 6)

    # 返回战役
    def return2Combat(self):
        print("ACTION: 返回正在进行的战役")
        self.mouseClick(self.RETURN_COMBAT_CLICK_BOX, 8, 9)

    # 重新进入并结束战役
    def resumeCombat(self, CONSTANT_IMAGE_BOX):
        print("ACTION: 重新进入并结束战役")
        if self.isResumeCombat():
            self.endCombat(CONSTANT_IMAGE_BOX)

    # 关闭作战断开提醒(deprecated)
    def closeTips(self):
        self.mouseClick(self.CLOSE_TIP_CLICK_BOX, 5, 5)


if __name__ == '__main__':
    battleautoGFL = BattleAutoGFL()