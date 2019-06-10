import random
from player import *
from character import *

class Room():
    Rooms = {}
    __Players = {}
    __DeadPlayerID = {}

    def __init__(self,HostInstance):
        RandomNumber = random.randint(1000, 9999)
        self.__Room_id = RandomNumber#需要添加到数据库
        self.__Playernumber = 12
        self.__Host_id=HostInstance.ID
        Room.Rooms[RandomNumber] = self
        self.__Players[HostInstance.ID]=HostInstance


    @property
    def Room_id(self):
        return self.__Room_id

    @property
    def Players(self):
        return self.__Players

    @property
    def Playernumber(self):
        return self.__Playernumber

    def __str__(self):
        return "RoomID:" + str(self.__Room_id)+"\n"+"HostID:"+str(self.__Host_id)

    # def AssignmentPlate(self,player):
    #     RoomNumberPlate = [1, 2]
    #     for i in range(0,2):
    #         Randomindex = random.randint(0, 1 - i)
    #         self.__Players[RoomNumberPlate[Randomindex]] = player
    #         del RoomNumberPlate[Randomindex]

    def CalVote(self):
        #计算投票结果
        max = -1
        for player in self.__Players.values():
            if player.Character.Vote_Number >= max:
                max = player.Character.Vote_Number
        SameNumber = 0
        for player in self.__Players.values():
            if player.Character.Vote_Number == max:
                SameNumber += 1
        if SameNumber == 1:
            for player in self.__Players.values():
                if player.Character.Vote_Number == max:
                    return player
        else:
            SameNumberPlayer = []
            for player in self.__Players.values():
                if player.Character.Vote_Number == max:
                    SameNumberPlayer.append(player)
            Length = len(SameNumberPlayer)
            return SameNumberPlayer[random.randint(0,Length-1)]

    def ClearVoteNumber(self):
        #清除所有玩家上一天所投的票数
        for key in self.__Players:
            self.__Players[key].Character.Vote_Number = 0

    def AddPlayer(self, PlayerInstance):
        self.__Players[PlayerInstance.ID] = PlayerInstance

    def GiveCharacter(self):
        #随机分配所有玩家身份
            Characterindex = []
            for i in range(1, 5):
                Characterindex.append(Village())  # 村民
            for i in range(1, 5):
                Characterindex.append(Wolf())  # 狼人
            Characterindex.append(Witch())  # 女巫
            Characterindex.append(Hunter())  # 猎人
            Characterindex.append(Seer())  # 预言家
            Characterindex.append(Idiot())  # 树人
            play = []
            j={}
            for key in self.__Players:
                play.append(self.__Players[key])
            for i in range(0,12):
                RandomNumber = random.randint(0,11-i)
                play[i].Character=Characterindex[RandomNumber]
                j[play[i]]=play[i].Character
                del Characterindex[RandomNumber]
            return j

    def GetAllDeath(self):
        AllDeath = []
        for key in self.__Players:
            if self.__Players[key].Character.Life == 0:
                AllDeath.append(key)
            return AllDeath

    def GetAllLive(self):
        #获取所有在场的玩家
        AllLive = []
        for key in self.__Players:
            if self.__Players[key].Character.Life == 1:
                AllLive.append(key)
        return AllLive

    def JudegeCharacterStatus(self, character):
        for player in self.Players.values():
            if type(player.Character) == character:
                return player.Character.Life

    def CheckMedicine(self):
        for player in self.Players.values():
            if type(player.Character) == Witch:
                return player.Character.ReturnMedicineStatus()

    def FindCharacter(self, character):
        for player in self.Players.values():
            if type(player.Character) == character:
                return player.Character

    def JudgeWin(self):
        BadDeath = 0
        GodDeath = 0
        GoodDeath = 0
        for key in self.Players:
            if self.Players[key].Character.Life == 0:
                for character in God:
                    if type(self.Players[key].Character) == character:
                        GodDeath += 1
                        break
                for character in Good:
                    if type(self.Players[key].Character) == character:
                        GoodDeath += 1
                        break
                for character in Bad:
                    if type(self.Players[key].Character) == character:
                        BadDeath += 1
                        break

        if GodDeath == 4 or GoodDeath == 4:
            return "狼人胜利"
        if BadDeath == 4:
            return "好人胜利"
        else:
            return None
