from player import Player
from character import *
from Sheriff import *

def main():
    PlayerList = []
    for i in range(1, 13):
        username = input("请输入第%d个玩家的姓名"%(i))
        PlayerList.append(Player(i, username))
    room = PlayerList[0].CreateRoom()
    for i in range(1, 12):
        print(PlayerList[i].JoinRoom(room.Room_id))
    room.GiveCharacter()
    for player in room.Players.values():
        print('%d号玩家角色是：%s' % (player.ID, type(player.Character)))
    while True:
        Result = room.JudgeWin()
        if Result is not None:
            print(Result)
            break
        NightDeath = []
        print("天黑请闭眼")
        input('回车键下一步')
        print('狼人请睁眼')
        input('回车键下一步')
        ID = input('狼人请选择')
        if ID != '':
            ID = int(ID)
            NightDeath.append(ID)
        Wolf.KillPerson(ID, room)
        print('狼人请闭眼')
        input('回车键下一步')
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
                choose = input("输入是否要使用解药")
                if choose != '':
                    choose = int(choose)
                    room.FindCharacter(Witch).Save(choose, room)
                    NightDeath.remove(choose)
            if Position_Number != 0 and choose == '':
                choose = input("输入是否要使用毒药")
                if choose != '':
                    choose = int(choose)
                    room.FindCharacter(Witch).Poison(choose, room)
                    for key in room.Players:
                        if int(key) == choose:
                            room.Players[key].Character.Witch_status = 1
                    NightDeath.append(choose)
        else:
            print('女巫已死亡请按任意键跳过')
        print('预言家请睁眼')
        input('回车键下一步')
        print('请选择你需要查验的人')
        if room.JudegeCharacterStatus(Seer) != 0:
            choose = int(input('输入ID'))
            print(Seer.check(choose, room))
        else:
            print('预言家已死亡请按任意键跳过')
        Result = room.JudgeWin()
        if Result is not None:
            print(Result)
            break
        DayDeath = []
        if len(NightDeath) == 0:
            print('昨晚是平安夜')
        else:
            print('昨晚死亡的是')
            for ID in NightDeath:
                print(ID)
            for id in NightDeath:
                if type(Character.FindCharacterByPlayerID(id, room)) == Hunter and room.Players[
                    id].Character.Witch_status == 0:
                    print('猎人玩家%s请选择是否发动技能,如果发动请输入射杀的玩家ID' % room.Players[id].usename)
                    ID = input('玩家id')
                    if ID != '':
                        ID = int(ID)
                        NightDeath.append(ID)
                    Hunter.shoot(ID, room)
                    print('ID:%d玩家死亡' % ID)
        print('现在开始发言')
        players = room.GetAllLive()
        print(players)
        for key in players:
            print('玩家%d请发言' % key)
            input('输入回车结束发言')
        print('请开始投票')
        input('回车下一步')
        for key in players:
            if type(Character.FindCharacterByPlayerID(key, room)) == Idiot and room.FindCharacter(Idiot).skill_status==1:
                print("无法投票")
            print('玩家%d请投票' % key)
            ID = input('输入ID选择要投票的玩家:')
            if ID != '':
                ID = int(ID)
                Character.Vote(ID, room)
        VotePlayer = room.CalVote()
        VotePlayer.Character.Life = 0
        DayDeath.append(VotePlayer.ID)
        room.ClearVoteNumber()
        for id in DayDeath:
            if type(Character.FindCharacterByPlayerID(id, room)) == Hunter:
                print('猎人玩家%s请选择是否发动技能,如果发动请输入射杀的玩家ID'%room.Players[id].usename)
                ID = input('玩家id')
                if ID != '':
                    ID=int(ID)
                    DayDeath.append(ID)
                Hunter.shoot(ID, room)
            elif type(Character.FindCharacterByPlayerID(id, room)) == Idiot and room.FindCharacter(Idiot).skill_status==0:
                # 判断淘汰的是否是白痴玩家
                print("白痴玩家%s发动技能,您可遗留在场上发言,但是没有投票权"%room.Players[id].usename)
                room.FindCharacter(Idiot).Draw(id,room)
                DayDeath.remove(id)
        for id in DayDeath:
            input('玩家%d请留遗言,按回车键结束'%id)


if __name__ == '__main__':
    main()
