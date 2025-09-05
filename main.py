from player import Intro
from battle import Stage
from market import Market
from equipment import Equip

if __name__ == "__main__":
    name = input('이름을 입력하세요!')
    charctor = Intro(name)
    equip = Equip()
    charctor.intromessage()
    charctor.infointroduce()
    charctor.select_job()
    

    while(1):
        print('\033[36m"전투" ------ "상점" ------ "정보" ------ "속성"\033[0m')
        goTo = input('')
        if(goTo=="전투"):
            stage = Stage(int(input('\033[36mStage number?:\033[0m')))
            stage.monsterinfo(charctor)
            stage.battleintro()
            stage.battlestart(charctor)
            
        elif(goTo=="상점"):
            market = Market(charctor.gold)
            market.enter()
            print('\033[36m"공격력" ------ "체력" ------ "치명타확률" ------ "치명타배수" ------ "아이템" ------ "뒤로가기"\033[0m')
            item = input('')
            if(item=="공격력"):
                market.attakitem(charctor)
            elif(item=="체력"):
                market.hpitem(charctor)
            elif(item=='치명타확률'):
                market.criitem(charctor)
            elif(item=='치명타배수'):
                market.crimulitem(charctor)
            elif(item == "아이템"):
                print('\033[36m"기절아이템" ------ "장비"\033[0m')
                goToitem = input('')
                if(goToitem=="기절아이템"):
                    market.stunitem(charctor)
                elif(goToitem == '장비'):
                    print('\033[36m정보 ------ 장비강화 ------ 상자 ------ 착용\033[0m')
                    goToequip = input('')
                    if(goToequip=="상자"):
                        equip.chest_info(charctor)
                        equip.roll_item(charctor)
                    elif(goToequip=="정보"):
                        equip.equip_info()
                    elif(goToequip=="착용"):
                        equip.use_equip(charctor)
            elif(item=="뒤로가기"):
                pass
        elif(goTo =='정보'):
            charctor.infointroduce()
        elif(goTo=='속성'):
            charctor.jobbase()
            print('변경 ------ 강화 ------ 정보 ------ 뒤로가기')
            goTojob = input('')
            if(goTojob=="변경"):
                charctor.select_job()
            elif(goTojob=="강화"):
                upgrader = Stage.for_upgrade() 
                upgrader.jobup(charctor)
            elif(goTojob=="정보"):
                charctor.jobinfo()
            elif(goTojob=="뒤로가기"):
                pass


