from auto13_4_airtest_version import *


# 获取指定区域box的截图
def getImage(sim, box):
    #simData = {'width', 'height', 'density', 'orientation', 'rotation', 'max_x', 'max_y'}
    simData = sim.get_display_info()
    boxData = calibrate(sim, box)
    imgLeft   = int(simData['width'] * boxData[0])
    imgTop    = int(simData['height'] * boxData[1])
    imgRight  = int(simData['width'] * boxData[2])
    imgBottom = int(simData['height'] * boxData[3])
    
    imgBytes = sim.screen_proxy.get_frame()
    imgFullSize = Image.open(BytesIO(imgBytes))
    img = imgFullSize.crop([imgLeft,imgTop,imgRight,imgBottom])
    
    # （弃用）img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom)
    return img

# 将windowsData获取的数据转化为模拟器内部的参数
def calibrate(sim, box):
    height = sim.display_info['height']
    box[1] = ((box[1] * 589) - TOP_WIDTH) / height
    box[3] = ((box[3] * 589) - TOP_WIDTH) / height
    return box

#比较两图片吻合度/置信度，结构相似性比较法（真的好用）
def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) # ground_truth img
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # test img
    (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
    return score > 0.95

#判断是否是主界面
def isMainMenu(sim):
    initImage = cv2.imread(IMAGE_PATH+"main_menu.png")
    capImage  = getImage(sim,MAIN_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/main_menu.png',capImage)
    return imageCompare(initImage,capImage)

def isMicroUZI(sim):
    initImage = cv2.imread(IMAGE_PATH+"microuzi.png")
    capImage  = getImage(sim,FIGURE_DETECT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/microuzi.png',capImage)
    return imageCompare(initImage,capImage)

#判断更换的人形名称
def isVector(sim):
    initImage = cv2.imread(IMAGE_PATH+"ventor.png")
    capImage  = getImage(sim,FIGURE_DETECT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/vector.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否是战斗选择菜单
def isCombatMenu(sim):
    initImage = cv2.imread(IMAGE_PATH+"combat_menu.png")
    capImage  = getImage(sim,COMBAT_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/combat_menu.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否是可以选择13-4的界面
def is13_4(sim):
    initImage = cv2.imread(IMAGE_PATH+"_13_4.png")
    capImage  = getImage(sim,CHOOSE_13_4_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/_13_4.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否进入了13-4地图
def isInMap(sim):
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(sim,MAP_13_4_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/map.png',capImage)
    return imageCompare(initImage,capImage)

#在布置重装的界面
def isSetWETeam(sim):
    initImage = cv2.imread(IMAGE_PATH+"set_we_team.png")
    capImage  = getImage(sim,SET_WE_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/set_we_team.png',capImage)
    return imageCompare(initImage,capImage)

#在队伍编成界面
def isFormTeam(sim):
    initImage = cv2.imread(IMAGE_PATH+"form_team.png")
    capImage  = getImage(sim,FORM_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/form_team.png',capImage)
    return imageCompare(initImage,capImage)

#在人员选择界面
def isChangeMember(sim):
    initImage = cv2.imread(IMAGE_PATH+"change_member.png")
    capImage  = getImage(sim,CHANGE_MEMBER_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/change_member.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否作战正常开启
def isCombatStart(sim):
    initImage = cv2.imread(IMAGE_PATH+"combat_start.png")
    capImage  = getImage(sim,COMBAT_START_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/combat_start.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否是模拟器桌面
def isDesktop(sim):
    initImage = cv2.imread(IMAGE_PATH+"desktop.png")
    capImage  = getImage(sim,DESKTOP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/desktop.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否战役结束
def isCombatFinished(sim):
    initImage = cv2.imread(IMAGE_PATH+"combat_finish.png")
    capImage  = getImage(sim,COMBAT_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/combat_finish.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否需要重新结束战役
def isResumeCombat(sim):
    initImage = cv2.imread(IMAGE_PATH+"resume_combat.png")
    capImage  = getImage(sim,RESUME_COMBAT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/resume_combat.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否有回到作战界面
def isReturnCombat(sim):
    initImage = cv2.imread(IMAGE_PATH+"return_combat.png")
    capImage  = getImage(sim,RETURN_COMBAT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/return_combat.png',capImage)
    return imageCompare(initImage,capImage)

#当不知道在哪时，判断是否有导航栏，有就可以通过导航栏回到作战菜单
def isNavigate(sim):
    initImage = cv2.imread(IMAGE_PATH+"navigate.png")
    capImage  = getImage(sim,NAVIGATE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/navigate.png',capImage)
    return imageCompare(initImage,capImage)

#在队伍放置界面
def isSetTeam(sim):
    initImage = cv2.imread(IMAGE_PATH+"set_team.png")
    capImage  = getImage(sim,SET_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/set_team.png',capImage)
    return imageCompare(initImage,capImage)

#在队伍详情界面
def isTeamInfo(sim):
    initImage = cv2.imread(IMAGE_PATH+"team_info.png")
    capImage  = getImage(sim,TEAM_INFO_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/team_info.png',capImage)
    return imageCompare(initImage,capImage)

#判断是否是提醒强化界面
def isGotoPowerup(sim):
    initImage = cv2.imread(IMAGE_PATH+"goto_powerup.png")
    capImage = getImage(sim,GOTO_POWERUP_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/goto_powerup.png',capImage)
    return imageCompare(initImage,capImage)

#在工厂资源回收界面
def isNonRetire(sim):
    initImage = cv2.imread(IMAGE_PATH+"non_retire.png")
    capImage = getImage(sim,NON_RETIRE_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    cv2.imwrite('./initial_IMG/airtest/non_retire.png',capImage)
    return imageCompare(initImage,capImage)

#=================函数调用区域=================#

#判断是否是每日第一次登录的确认界面
def isFirstLogin(sim):
    initImage = cv2.imread(IMAGE_PATH+"first_login.png")
    capImage  = getImage(sim,FIRST_LOGIN_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    return imageCompare(initImage,capImage)   

#判断是否是委托完成界面
def isLSupport(sim):
    initImage = cv2.imread(IMAGE_PATH+"L_support.png")
    capImage  = getImage(sim,L_SUPPORT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    return imageCompare(initImage,capImage)

#判断是否是战斗中断提示界面
def isCombatPause(sim):
    initImage = cv2.imread(IMAGE_PATH+"combat_pause.png")
    capImage  = getImage(sim,COMBAT_PAUSE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    capImage  = cv2.resize(capImage,(initImage.shape[1],initImage.shape[0]))
    return imageCompare(initImage,capImage)

#=================函数调用区域=================#

### 连接模拟器###
sim = Android(serialno='127.0.0.1:7555')

### 功能测试###
# isCombatFinished(sim)
# isMainMenu(sim)
# isMicroUZI(sim)
# isVector(sim)
# isCombatMenu(sim)
# is13_4(sim)
# isInMap(sim)
# isSetWETeam(sim)
# isFormTeam(sim)
# isChangeMember(sim)
# isCombatStart(sim)
isDesktop(sim)
# isResumeCombat(sim)
# isReturnCombat(sim)
# isNavigate(sim)
# isSetTeam(sim)
# isTeamInfo(sim)
# isGotoPowerup(sim)
# isNonRetire(sim)!!!!
