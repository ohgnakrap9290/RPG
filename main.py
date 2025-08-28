from player import Intro
from battle import Stage
from market import Market

if __name__ == "__main__":
    name = input('이름을 입력하세요!')
    charctor = Intro(name)
    charctor.intromessage()
    charctor.infointroduce()
    while(1):
        print('\033[36m"battle" ------ "market" ------ "info"\033[0m')
        goTo = input('')
        if(goTo=="battle"):
            stage = Stage(int(input('\033[36mStage number?:\033[0m')))
            stage.monsterinfo()
            stage.battleintro()
            stage.battlestart(charctor)
        elif(goTo=="market"):
            market = Market(charctor.gold)
            market.enter()
            item = input('\033[36m"upatk" ------ "uphp" ------ "upcri" ------ "upcrimul" ------ "stunitem"\n\033[0m')
            if(item=="upatk"):
                market.attakitem(charctor)
            elif(item=="uphp"):
                market.hpitem(charctor)
            elif(item=='upcri'):
                market.criitem(charctor)
            elif(item=='upcrimul'):
                market.crimulitem(charctor)
            elif(item == "stunitem"):
                market.stunitem(charctor)
        elif(goTo =='info'):
            charctor.infointroduce()


