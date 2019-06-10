from player import Player
from character import *
from Sheriff import *

#游戏开始,所有玩家获取角色
def get_character():
    PlayerList = []
    for i in range(1, 13):
        username = input("请输入第%d个玩家的姓名"%(i))
        PlayerList.append(Player(i, username))
    room = PlayerList[0].CreateRoom()
    for i in range(1, 12):
        PlayerList[i].JoinRoom(room.Room_id)
    room.GiveCharacter()
    for player in room.Players.values():
        print('%d号玩家角色是：%s' % (player.ID, type(player.Character)))
    return room

#天黑玩家角色依次行动

#狼人行动
def wolf_action(room):
    #狼人行动
    NightDeath = []
    input('回车键下一步')
    print('狼人请睁眼')
    input('回车键下一步')
    ID = input('狼人请选择')
    if ID != '':
        ID = int(ID)
        NightDeath.append(ID)
    Wolf.KillPerson(ID, room)
    print('狼人请闭眼')
    return NightDeath

#女巫行动
def witch_action(room,NightDeath):
    print('女巫请睁眼')
    input('回车键下一步')
    print('你有一瓶解药是否要使用(若要使用请输入ID),你有一瓶毒药是否要使用(若要使用请输入ID)')
    if room.JudegeCharacterStatus(Witch) != 0:
        Antidote_Number, Position_Number = room.CheckMedicine()
        choose = ''
        if Antidote_Number != 0:
            if len(NightDeath) != 0:
                for ID in NightDeath:
                    print('%d死了' % ID)
            choose = input("是否要使用解药")
            if choose != '':
                choose = int(choose)
                room.FindCharacter(Witch).Save(choose, room)
                NightDeath.remove(choose)
        if Position_Number != 0 and choose == '':
            choose = input("是否要使用毒药")
            if choose != '':
                choose = int(choose)
                room.FindCharacter(Witch).Poison(choose, room)
                for key in room.Players:
                    if int(key) == choose:
                        room.Players[key].Character.Witch_status = 1
                if choose not in NightDeath:
                    NightDeath.append(choose)
    else:
        print('女巫已死亡请按任意键跳过')
    return NightDeath

#预言家行动
def seer_action(room):
    print("天黑请闭眼")
    print('预言家请睁眼')
    input('回车键下一步')
    print('请选择你需要查验的人')
    if room.JudegeCharacterStatus(Seer) != 0:
        choose = int(input('输入ID:'))
        return Seer.check(choose, room)
    else:
        return '预言家已死亡请按任意键跳过'

#猎人行动
def hunter_action(room,NightDeath,id):
    print('猎人玩家%s请选择是否发动技能,如果发动请输入射杀的玩家ID' % room.Players[id].usename)
    ID = input('玩家id:')
    if ID != '':
        ID = int(ID)
        NightDeath.append(ID)
    Hunter.shoot(ID, room)
    print('ID:%d玩家死亡' % ID)
    return NightDeath

#判断夜晚的死亡情况
def night_death(NightDeath,room):
    if len(NightDeath) == 0:
        print('昨晚是平安夜')
    #否则有人死亡
    else:
        for ID in NightDeath:
            #判断晚上死亡玩家是不是猎人,且猎人如果被女巫毒死无法发动技能
            if type(Character.FindCharacterByPlayerID(ID, room)) == Hunter and room.Players[ID].Character.Witch_status == 0:
                NightDeath=hunter_action(room,NightDeath,ID)
        print('昨晚死亡的是:')
        for ID in NightDeath:
            print(ID,end=' ')
    return NightDeath

#循环遍历玩家是否上警,获取上警玩家列表
def onsheriff(room):
    onslist=[]
    unonslist=[]
    for key in room.Players:
        #遍历所有玩家是否上警,如果上警随意输入信息
        print('玩家%d'%key)
        flag=input("是否上警发言:")
        if flag:
            onslist.append(key)
        else:
            unonslist.append(key)
    return onslist,unonslist

#成为警长
def becomesheriff(player):
    sheriff={}
    sheriff[player]=Sheriff()
    player.Character.Number_Vote=1.5
    print('%d玩家成为警长'%(player.ID))
    return sheriff

#请决定发言顺序
def decidespeaksort(sheriff,players):
    #判断发言顺序
    direction=input('房主请输入发言方向:')
    #获取在场玩家存活的玩家
    for key in sheriff:
        if direction =='警左':
            speaksortlist=sheriff[key].speak_sort_left(key,players)
        elif direction == '警右':
            speaksortlist=sheriff[key].speak_sort_right(key, players)
    return speaksortlist

#循环发言
def speak(speaklist):
    for key in speaklist:
        print('玩家%d请发言' % key)
        input('输入回车结束发言')

#循环投票,获取票数最高的玩家
def vote(room,votelist):
    for key in votelist:
        #如果白痴玩家的技能状态为发动过技能,且还没有死亡,白痴玩家不能投票
        if type(Character.FindCharacterByPlayerID(key,room)) == Idiot and room.FindCharacter(Idiot).skill_status == 1:
            print("您的身份是白痴且技能发动无法投票")
            continue
        print('玩家%d请投票:' % key)
        ID = input('输入ID选择要投票的玩家:')
        if ID != '':
            ID = int(ID)
            room.Players[key].Character.Vote(ID, room)
    VotePlayer = room.CalVote()
    room.ClearVoteNumber()
    return VotePlayer

#白天死亡列表
def day_death(Voteplayer):
    DayDeath=[]
    DayDeath.append(Voteplayer.ID)
    Voteplayer.Character.Life = 0
    return DayDeath

#判断出局的玩家是否有白痴和猎人
def judgeplayerisidiotorhunter(room,DayDeath):
    for id in DayDeath:
        if type(Character.FindCharacterByPlayerID(id, room)) == Hunter:
            #判断淘汰玩家是否是猎人玩家
            print('猎人玩家%s请选择是否发动技能,如果发动请输入射杀的玩家ID' % room.Players[id].usename)
            ID = input('玩家id:')
            if ID != '':
                ID = int(ID)
                DayDeath.append(ID)
            Hunter.shoot(ID, room)
        elif type(Character.FindCharacterByPlayerID(id, room)) == Idiot and room.FindCharacter(Idiot).skill_status == 0:
            # 判断淘汰的是否是白痴玩家
            print("白痴玩家%s发动技能,您可遗留在场上发言,但是没有投票权" % room.Players[id].usename)
            room.FindCharacter(Idiot).Draw(id, room)
            DayDeath.remove(id)
    for id in DayDeath:
        input('玩家%d请留遗言,按回车键结束' % id)
    return DayDeath

# 判断死亡玩是否是警长,如果是警长则移交警徽
def deathpalyerissheriff(sheriff,deathlist,room):
    for ID in deathlist:
        for player in sheriff:
            if player.ID == ID:
                id = input('请输入移交房主的id')
                if id!='':
                    id=int(id)
                    player = room.Players[id]
                    sheriff = becomesheriff(player)
                    return sheriff
                else:
                    print('玩家撕掉警徽')
                    return None
        else:
            return sheriff

#第一天结束之后循环游戏过程
def afterfirstday(room,sheriff):
        NightDeath = wolf_action(room)
        NightDeath = witch_action(room, NightDeath)
        NightDeath = night_death(NightDeath, room)
        if type(NightDeath) == list:
            if sheriff:
                sheriff=deathpalyerissheriff(sheriff, NightDeath, room)
        players = room.GetAllLive()
        if sheriff:
            speaksortlist = decidespeaksort(sheriff, players)
        else:
            speaksortlist = players
        speak(speaksortlist)
        VotePlayer = vote(room, speaksortlist)
        DayDeath = day_death(VotePlayer)
        DayDeath = judgeplayerisidiotorhunter(room, DayDeath)
        if sheriff:
            sheriff = deathpalyerissheriff(sheriff, DayDeath, room)
        if sheriff:
            return sheriff
        else:
            return None

#第一天
def firstday():
    #第一天
    room=get_character()
    print(seer_action(room))
    NightDeath=wolf_action(room)
    NightDeath=witch_action(room,NightDeath)
    #选择上警的玩家
    onslist,unonslist=onsheriff(room)
    if len(onslist)==1:
        sheriff=becomesheriff(room.Players[onslist[0]])
        #上警玩家依次发言
    else:
        speak(onslist)
        #未上警玩家投票选取出警长
        player=vote(room,unonslist)
        #某位玩家成为警长
        sheriff=becomesheriff(player)
    NightDeath=night_death(NightDeath, room)
    if type(NightDeath)==list:
        # 判断死亡玩是否是警长,如果是警长则移交警徽
        speak(NightDeath)
        sheriff=deathpalyerissheriff(sheriff, NightDeath, room)
    #获取在场的所有存活玩家
    players = room.GetAllLive()
    if sheriff:
        speaksortlist=decidespeaksort(sheriff,players)
    else:
        speaksortlist=players
    print(speaksortlist)
    speak(speaksortlist)
    VotePlayer=vote(room,speaksortlist)
    DayDeath=day_death(VotePlayer)
    #判断白天出局玩家是否为警长
    sheriff = deathpalyerissheriff(sheriff, DayDeath, room)
    judgeplayerisidiotorhunter(room, DayDeath)
    # sheriff=deathpalyerissheriff(sheriff, DayDeath, room)
    while True:
        Result = room.JudgeWin()
        if Result is not None:
            print(Result)
            return
        sheriff=afterfirstday(room, sheriff)
        sheriff=sheriff
        Result = room.JudgeWin()
        if Result is not None:
            print(Result)
            return




def main():
    firstday()


if __name__=="__main__":
    main()