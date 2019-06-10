class Character():
    __Vote_Number = 0
    __Witch_status=0
    __Number_Vote=1

    @staticmethod
    def FindCharacterByPlayerID(PlayerID, room):
        return room.Players[PlayerID].Character

    def __init__(self):
        self.__Life = 1

    def Vote(self,PlayerID, room):
        character = room.Players[PlayerID].Character
        character.Vote_Number += self.Number_Vote

    def FindPlayerID(self, room):
        players = room.Players
        for key in players:
            if players[key].Character == self:
                return key

    @property
    def Vote_Number(self):
        return self.__Vote_Number

    @Vote_Number.setter
    def Vote_Number(self, value):
        self.__Vote_Number = value

    @property
    def Witch_status(self):
        return self.__Witch_status

    @Witch_status.setter
    def Witch_status(self, value):
        self.__Witch_status = value

    @property
    def Life(self):
        return self.__Life

    @Life.setter
    def Life(self, value):
        self.__Life = value

    @property
    def Number_Vote(self):
        return self.__Number_Vote

    @Number_Vote.setter
    def Number_Vote(self,value):
        self.__Number_Vote=value

class Village(Character):
    name = "village"

    def __init__(self):
        super().__init__()

class Wolf(Character):
    name = "wolf"

    def __init__(self):
        super().__init__()

    @staticmethod
    def KillPerson(PlayerID, room):
        if PlayerID == "":
            pass
        else:
            Character.FindCharacterByPlayerID(PlayerID, room).Life = 0

    def FindFriends(self, room):
        FriendID = []
        players = room.Players
        for key in players:
            if type(players[key].Character) == Wolf:
                if key != self.FindPlayerID(room):
                    FriendID.append(key)
        return FriendID

class Hunter(Character):
    name = "hunter"

    def __init__(self):
        super().__init__()
        self.hunt = 1

    @staticmethod
    def shoot(PlayerID, room):
        Character.FindCharacterByPlayerID(PlayerID, room).Life = 0

class Witch(Character):
    name = "witch"

    def __init__(self):
        super().__init__()
        self.antidote_number = 1
        self.posison_number = 1

    def Save(self, PlayerID, room):
        players = room.Players
        players[PlayerID].Character.Life = 1
        self.antidote_number = 0

    def Poison(self, PlayerID, room):
        players = room.Players
        players[PlayerID].Character.Life = 0
        self.posison_number = 0
        print("毒人成功")

    def ReturnMedicineStatus(self):
        return self.antidote_number,self.posison_number

class Idiot(Character):
    name = "idiot"

    def __init__(self):
        super().__init__()
        self.skill_status=0

    def Draw(self,playerID,room):
        room.Players[playerID].Character.Life=1
        self.skill_status = 1
        self.Number_Vote=0

class Seer(Character):
    name = "seer"

    def __init__(self):
        super().__init__()

    @staticmethod
    def check(PlayerID, room):
        players = room.Players
        Type = type(players[PlayerID].Character)
        for temp in God:
            if temp == Type:
                return "Good"
        for temp in Good:
            if temp==Type:
                return "Good"
        for temp in Bad:
            if temp == Type:
                return "Bad"


God = [Seer, Witch, Hunter, Idiot]
Good = [Village]
Bad = [Wolf]