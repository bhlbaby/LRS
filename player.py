from roomManage import *
from character import *
from Sheriff import *


class Player():
    __Room_id = ""
    __Character = None
    __Sheriff=None

    def __init__(self, ID, usename):
        self.__ID = ID
        self.__usename = usename

    # 创建房间
    def CreateRoom(self):
        # 调用Room类,创建房间并输入房间总人数
        room = Room(self)
        self.__Room_id = room.Room_id
        # room.AssignmentPlate(self)
        return room

    # 加入房间
    def JoinRoom(self, Room_ID):
        try:
            room = Room.Rooms[Room_ID]
        except Exception:
            return "无该房间号"
        if len(room.Players) == 12:
            return "房间已满无法加入"
        else:
            # 加入房间将玩家信息存入Players字典
            # room.AssignmentPlate(self)
            room.Players[self.ID]=self
            self.__Room_id=Room_ID
            return "加入成功"

    # def get_character(self, character):
    #     self.__Character = character

    @property
    def ID(self):
        return self.__ID

    @property
    def usename(self):
        return self.__usename

    @usename.setter
    def usename(self,value):
        self.__usename=value

    @property
    def Room_id(self):
        return self.__Room_id

    @property
    def Character(self):
        return self.__Character

    @Character.setter
    def Character(self, value):
        self.__Character = value

    # @property
    # def Sheriff(self):
    #     return self.__Sheriff
    #
    # @Sheriff.setter
    # def Sheriff(self, value):
    #     self.__Sheriff = value



if __name__ == "__main__":
    #测试代码
    p1=Player(1,"A")#玩家1
    p2=Player(2,"B")#玩家2
    room=p1.CreateRoom()#玩家1创建房间
    p2.JoinRoom(room.Room_id)#玩家2加入房间
    print(room.Players)
    print(room.GiveCharacter())
    print(room.JudegeCharacterStatus(Seer))
    print(room.CheckMedicine())
    for key in room.Players.values():
        if type(key.Character)=='Seer':
            print(type(key.Character))
            print(key.Character)




