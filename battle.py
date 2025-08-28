from player import Intro
import random
import time

class Stage:
    def __init__(self,round):
        self.round=round
        print(f'------------------- Stage {self.round} -------------------')
        self.Mthp   = int(320 * (1.18 ** (self.round - 1)))  
        self.Mtatk  = int(70  * (1.12 ** (self.round - 1)))  
        self.critical = min(0.01 + 0.005 * (self.round - 1), 0.25)  
        self.crimult  = min(1.0 + 0.01 * (self.round - 1), 1.80)  

        self.pre = False

    def monsterinfo(self):
        print(f'Monster Info:')
        print(f'Atk : \033[91m{int(self.Mtatk)}\033[0m Hp : \033[32m{int(self.Mthp)}\033[0m\nCri : \033[1;31m{round(self.critical,2)}\033[0m CriMul : \033[1;31m{round(self.crimult,2)}\033[0m')

    def battleintro(self):       
        time.sleep(2)
        print('선공 후공 정하기')
        preatklist = [random.randint(0, 1) for _ in range(10)]
        for i in range(10):
            print(preatklist[i],end=' ')
            time.sleep(0.5)
        print('\n')
        time.sleep(3)
        if(preatklist.count(0)<preatklist.count(1)):
            print('Pre-Attack!')
            time.sleep(1)
            self.pre = True
            print('\033[36m----- Battle Start! -----\033[0m')
        else:
            print('Late-Attack!')
            time.sleep(1)
            print('\033[36m----- Battle Start! -----\033[0m')
        
    def alive(self):
        return self.Mthp>0

    def battlestart(self,player):
        while(self.alive() and player.alive()):
            if(self.pre):
                time.sleep(1)
                print(f'{player.name}이/가 공격했습니다!')
                time.sleep(1)
                if(random.random() < player.critical):
                    print(f'\033[1;31mCRI!! x{round(player.crimult,2)}Atk! \n{player.atk*player.crimult}ATK!\033[0m')
                    time.sleep(1)
                    self.Mthp = self.Mthp - (player.atk*player.crimult)
                else:
                    print(f'{player.atk}의 데미지를 입혔습니다!\n')
                    time.sleep(1)
                    self.Mthp =  self.Mthp - player.atk 
                
                print(f'MONSTER 남은 체력: \033[35m{round(self.Mthp,2)}\033[0m\n')
                time.sleep(1)
                if(not self.alive()):
                    print('상대가 쓰려졌다!')
                    time.sleep(1)
                    print('\033[36m----- Battle end! -----\033[0m')
                    time.sleep(3)
                    print(f'Stage {self.round} Success')
                    time.sleep(1)
                    print(f'\033[33m{100*self.round}$ 를 획득했습니다!\033[0m')
                    player.gold = player.gold + self.round*100
                    player.heal_full()
                    break
                if(player.stunmount>0):
                    print(f'\033[94m{player.name}이 기절 아이템을 사용했습니다!\033[0m')
                    time.sleep(1)
                    player.stunmount-=1
                    print(f'{player.name}이/가 공격했습니다!')
                    time.sleep(1)
                    if(random.random() < player.critical):
                        print(f'\033[1;31mCRI!! x{player.crimult}Atk! \n{player.atk*player.crimult}ATK!\033[0m')
                        
                        time.sleep(1)
                        self.Mthp = self.Mthp - (player.atk*player.crimult)
                    else:
                        print(f'{player.atk}의 데미지를 입혔습니다!\n')
                        time.sleep(1)
                        self.Mthp =  self.Mthp - player.atk 
                        
                        print(f'MONSTER 남은 체력: \033[35m{round(self.Mthp,2)}\033[0m\n')
                    if(not self.alive()):
                        print('상대가 쓰려졌다!')
                        time.sleep(1)
                        print('\033[36m----- Battle end! -----\033[0m')
                        time.sleep(3)
                        print(f'Stage {self.round} Success')
                        time.sleep(1)
                        print(f'\033[33m{100*self.round}$ 를 획득했습니다!\033[0m')
                        player.gold = player.gold + self.round*100
                        player.heal_full()
                        break

                print('상대가 공격했습니다!')
                time.sleep(1)
                if(random.random() < self.critical):
                    print(f'\033[1;31mCRI!! x{round(self.crimult,2)}Atk! \n{self.Mtatk*self.crimult}ATK!\033[0m')
                    
                    player.hp = player.hp - (self.Mtatk*self.crimult)
                else:
                    print(f'{self.Mtatk}의 데미지를 입었습니다!\n')
                    time.sleep(1)
                    player.hp = player.hp - self.Mtatk
                print(f'Player 남은 체력: \033[32m{round(player.hp,2)}\033[0m\n')
                if(not player.alive()):
                    print('Defeat...')
                    time.sleep(1)
                    print('\033[36m----- Battle end -----\033[0m')
                    time.sleep(3)
                    print(f'Stage {self.round} Failure')
                    print(f'\033[91m{50*self.round}$ 를 잃었습니다\033[0m')
                    player.gold = player.gold - self.round*50
                    
                    player.heal_full()
                    
                    break
            else:
                if(player.stunmount>0):
                    print(f'\033[94m{player.name}이 기절 아이템을 사용했습니다!\033[0m')
                    time.sleep(1)
                    player.stunmount-=1
                    print(f'{player.name}이/가 공격했습니다!')
                    time.sleep(1)
                    if(random.random() < player.critical):
                        print(f'\033[1;31mCRI!! x{player.crimult}Atk! \n{player.atk*player.crimult}ATK!\033[0m')
                        
                        time.sleep(1)
                        self.Mthp = self.Mthp - (player.atk*player.crimult)
                    else:
                        print(f'{player.atk}의 데미지를 입혔습니다!\n')
                        time.sleep(1)
                        self.Mthp =  self.Mthp - player.atk 

                        print(f'MONSTER 남은 체력: \033[35m{round(self.Mthp,2)}\033[0m\n')
                    if(not self.alive()):
                        print('상대가 쓰려졌다!')
                        time.sleep(1)
                        print('\033[36m----- Battle end! -----\033[0m')
                        time.sleep(3)
                        print(f'Stage {self.round} Success')
                        time.sleep(1)
                        print(f'\033[33m{100*self.round}$ 를 획득했습니다!\033[0m')
                        player.gold = player.gold + self.round*100
                        player.heal_full()
                        break

                print('상대가 공격했습니다!')
                time.sleep(1)
                if(random.random() < self.critical):
                    print(f'\033[1;31mCRI!! x{self.crimult}Atk! \n{self.Mtatk*self.crimult}ATK!\033[0m')
                    time.sleep(1)
                    player.hp = player.hp - (self.Mtatk*self.crimult)
                else:
                    print(f'{self.Mtatk}의 데미지를 입었습니다!\n')
                    time.sleep(1)
                    player.hp = player.hp - self.Mtatk
                print(f'Player 남은 체력: \033[32m{round(player.hp,2)}\033[0m\n')
                if(not player.alive()):
                    print('Defeat...')
                    time.sleep(1)
                    print('\033[36m----- Battle end -----\033[0m')
                    time.sleep(3)
                    print(f'Stage {self.round} Failure')
                    print(f'\033[91m{50*self.round}$ 를 잃었습니다\033[0m')
                    player.gold = player.gold - self.round*50
                    
                    player.heal_full()
                    break
                print(f'{player.name}이/가 공격했습니다!')
                time.sleep(1)
                if(random.random() < player.critical):
                    print(f'\033[1;31mCRI!! x{player.crimult}Atk! \n{player.atk*player.crimult}ATK!\033[0m')
                    
                    time.sleep(1)
                    self.Mthp = self.Mthp - (player.atk*player.crimult)
                else:
                    print(f'{player.atk}의 데미지를 입혔습니다!\n')
                    time.sleep(1)
                    self.Mthp =  self.Mthp - player.atk 
                
                    print(f'MONSTER 남은 체력: \033[35m{round(self.Mthp,2)}\033[0m\n')
                if(not self.alive()):
                    print('상대가 쓰려졌다!')
                    time.sleep(1)
                    print('\033[36m----- Battle end! -----\033[0m')
                    time.sleep(3)
                    print(f'Stage {self.round} Success')
                    time.sleep(1)
                    print(f'\033[33m{100*self.round}$ 를 획득했습니다!\033[0m')
                    player.gold = player.gold + self.round*100
                    player.heal_full()
                    break

            

