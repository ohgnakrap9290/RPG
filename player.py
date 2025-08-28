class Intro:
    def __init__(self,name):
        self.name =name
        self.hp = 600
        self.atk = 60
        self.critical = 0.1
        self.crimult = 2
        self.gold = 1000
        self.max_hp = self.hp
        self.stunmount = 0

    def heal_full(self):
        self.hp = self.max_hp

    def intromessage(self):
        print(f'안녕하세요 {self.name}님!') 
        print(f'\033[36m게임 시작을 입력해주세요.\033[0m')
        input()
        
    def infointroduce(self):
        print(f'\nInfo\n체력 : \033[32m{self.hp}\033[0m\n공격력 : \033[91m{self.atk}\033[0m\n크리티컬 확률 : \033[1;31m{round(self.critical*100, 1)}%\033[0m  \n크리티컬 배수 : \033[1;31mx{round(self.crimult, 2)}\033[0m\n')
        
    def alive(self):
        return self.hp>0

