# from job import Job
from equipment import Equip

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
        self.pjobatk_fire= 10
        self.pjobatk_water= 10
        self.pjobatk_wind= 10
        self.pjobatk_soil= 10
        self.job_lv=0


    def heal_full(self):
        self.hp = self.max_hp

    def intromessage(self):
        print(f'안녕하세요 {self.name}님!') 
        print(f'\033[36m게임 시작을 입력해주세요.\033[0m')
        input()
        
    def infointroduce(self):
        self.atk+= getattr(self, "atk_bonus", 0)
        self.hp += getattr(self, "def_bonus", 0)*2.5
        print(f'\nInfo\n체력 : \033[32m{self.hp}\033[0m\n공격력 : \033[91m{self.atk}\033[0m\n크리티컬 확률 : \033[1;31m{round(self.critical*100, 1)}%\033[0m  \n크리티컬 배수 : \033[1;31mx{round(self.crimult, 2)}\033[0m')
        print(f'장비 추가 공격력 : \033[91m{getattr(self, "atk_bonus", 0)}\033[0m 장비 추가 방어력 : \033[94m{getattr(self, "def_bonus", 0)}\033[0m')
        
    def alive(self):
        return self.hp>0

    def select_job(self):
        print("\033[91m불\033[0m --- \033[94m물\033[0m ---  바람 --- \033[33m흙\033[0m")
        self.job = (input('속성을 선택하세요!\n'))
        while(self.job not in ['불','물','바람','흙']):
            print('\033[91m네 가지 속성중 하나를 선택하세요.\033[0m')
            self.job = (input('속성을 선택하세요!\n'))
        print(f'{self.job}을 선택하셨습니다!')
        print('\033[36m속성은 추후에 변경할 수 있음\033[0m\n')

    def jobbase(self):
        if(self.job=='불'):
            print(f'현재 가진 속성 : \033[91m불\033[0m')
        elif(self.job=='물'):
            print(f'현재 가진 속성 : \033[94m물\033[0m')
        elif(self.job=='바람'):
            print(f'현재 가진 속성 : 바람')
        elif(self.job=='흙'):
            print(f'현재 가진 속성 : \033[33m흙\033[0m')

    def jobinfo(self):
        dic1={'불':0,'물':1,'바람':2,'흙':3}
        dic1value=dic1[self.job]
        list1=[f'\033[91m불\033[0m 속성 : \n바람 속성 몬스터에게 \033[91m+{self.pjobatk_fire}\033[0m 추가피해 ',f'\033[94m물\033[0m 속성 : \n\033[91m불\033[0m 속성 몬스터에게 \033[91m+{self.pjobatk_water}\033[0m 추가피해',f'바람 속성 : \n\033[33m흙\033[0m 속성 몬스터에게 \033[91m+{self.pjobatk_wind}\033[0m 추가피해',f'\033[33m흙\033[0m 속성 :\n\033[94m물\033[0m 속성 몬스터에게 \033[91m+{self.pjobatk_soil}\033[0m 추가피해 ']
        print(list1[dic1value])
    


