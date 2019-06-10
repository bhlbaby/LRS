from roomManage import *
from character import *
from player import *


class Sheriff:
    #警长可以将自己的投到别人身上的票数为１.５票
    # 决定发言顺序
    def speak_sort_left(self, player, speaklist):
        speaksortlist = []
        for i in range(len(speaklist)):
            if speaklist[i] == player.ID:
                if i != 0:
                    speaksortlist = speaklist[i - 1::-1] + speaklist[len(speaklist):i - 1:-1]
                else:
                    speaksortlist = speaklist[len(speaklist)::-1]
        return speaksortlist

    def speak_sort_right(self, player, speaklist):
        speaksortlist = []
        for i in range(len(speaklist)):
            if speaklist[i] == player.ID:
                if i != len(speaklist):
                    speaksortlist = speaklist[i + 1::] + speaklist[0:i:]
        return speaksortlist

