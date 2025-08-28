import time
from player import Intro

class Market:
    priceatk    = 50
    pricehp     = 100
    pricecri    = 300
    pricecrimul = 200

    def __init__(self,gold):
        self.gold = gold

    def enter(self):
        print(f'보유 자금 \033[33m{self.gold}$\033[0m')

    def attakitem(self,player):
        print(f'공격력 증가 코인 \033[91m+10Atk\033[0m >> \033[33m{self.priceatk}$\033[0m')
        time.sleep(1)
        mount = int(input('수량 입력 :'))
        time.sleep(1)
        unit_price = type(self).priceatk
        total = unit_price * mount
        print(f'업그레이드시 남은 자금 \033[33m{self.gold}$ > {self.gold - total}$\033[0m ')
        if self.gold < total:
            print('Gold 부족 \n구매불가')
        elif(input('확인시 "확인" 입력\n')=="확인"):
            self.gold -= total
            player.atk = player.atk + 10*mount
            player.gold = self.gold
            type(self).priceatk += mount
        
    def hpitem(self,player):
        print(f'체력 증가 코인 \033[32m+100hp\033[0m >> \033[33m{self.pricehp}$\033[0m')
        time.sleep(1)
        mount = int(input('수량 입력 :'))
        time.sleep(1)
        unit_price = type(self).pricehp
        total = unit_price * mount
        print(f'업그레이드시 남은 자금 \033[33m{self.gold}$ > {self.gold - total}$\033[0m')
        if self.gold < total:
            print('Gold 부족 \n구매불가')
        elif(input('확인시 "확인" 입력\n')=="확인"):
            self.gold -= total
            player.gold = self.gold
            player.max_hp += 100*mount
            player.heal_full()
            type(self).pricehp += mount*2
        
    def criitem(self,player):
        print(f'크리티컬 확률 증가 코인 +1% >> \033[33m{self.pricecri}$\033[0m')
        time.sleep(1)
        mount = int(input('수량 입력 :'))
        time.sleep(1)
        unit_price = type(self).pricecri
        total = unit_price * mount
        print(f'업그레이드시 남은 자금 \033[33m{self.gold}$ > {self.gold - total}$\033[0m ')
        if self.gold < total:
            print('Gold 부족 \n구매불가')
        elif(input('확인시 "확인" 입력\n')=="확인"):
            self.gold -= total
            player.gold = self.gold
            player.critical += 0.01*mount
            type(self).pricecri += mount*3

    def crimulitem(self,player):
        print(f'크리티컬 데미지 증가 코인 +5% >> \033[33m{self.pricecrimul}$\033[0m')
        time.sleep(1)
        mount = int(input('수량 입력 :'))
        time.sleep(1)
        unit_price = type(self).pricecrimul
        total = unit_price * mount
        print(f'업그레이드시 남은 자금 \033[33m{self.gold}$ > {self.gold - total}$\033[0m ')
        if self.gold < total:
            print('Gold 부족 \n구매불가')
        elif(input('확인시 "확인" 입력\n')=="확인"):
            self.gold -= total
            player.gold = self.gold
            player.crimult += 0.05*mount
            type(self).pricecrimul += mount*2

    def money(self,player):
        print(f' 현재 남은 자금 \033[33m{player.gold}$\033[0m')

    def stunitem(self,player):
        print(f'기절 아이템 구매 : \033[33m300$\033[0m/개 ')
        time.sleep(1)
        print(f'현재 기절 아이템 수량 : {player.stunmount}개')
        mount = int(input('수량 입력 :'))
        time.sleep(1)
        print(f'구매시 남은 자금 \033[33m{self.gold}$ > {(self.gold)-300*mount}$ \033[0m')
        if(((self.gold)-300*mount)<0):
            print('Gold 부족 \n구매불가')
        elif(input('확인시 "확인" 입력\n')=="확인"):
            self.gold = self.gold - 300*mount
            player.gold = self.gold
            player.stunmount+=mount
