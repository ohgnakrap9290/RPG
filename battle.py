from player import Intro
import random
import time
import math

class Stage:
    element = ["불", "물", "바람", "흙", "무속성"]
    color = {
        "불": "\033[91m",   
        "물": "\033[94m",   
        "바람": "\033[0m",   
        "흙": "\033[33m", 
        "무속성": "\033[0m",  
    }
    def __init__(self,round,K: int = 1000):
        self.round=round
        print(f'------------------- Stage {self.round} -------------------')
        self.Mthp   = int(320 * (1.18 ** (self.round - 1)))  
        self.Mtatk  = int(70  * (1.12 ** (self.round - 1)))  
        self.critical = min(0.01 + 0.005 * (self.round - 1), 0.25)  
        self.crimult  = min(1.0 + 0.01 * (self.round - 1), 1.80)
        self.Mtjob=random.choice(Stage.element)
        self.K = K

        self.pre = False

    @classmethod
    def for_upgrade(cls, K: int = 1000):
        """강화 UI 전용 Stage 생성자"""
        obj = cls.__new__(cls)
        obj.K = K
        obj.pre = False
        obj.mode = "upgrade"
        obj.round = 0
        obj.Mthp = obj.Mtatk = 0
        obj.critical = obj.crimult = 0.0
        obj.Mtjob = None
        return obj

    def _p_base(self, L: int) -> float:
        p1, p200 = 0.99, 0.10
        r = (p200 / p1) ** (1 / 199)
        L_eff = max(1, L)
        return max(0.0, min(1.0, p1 * (r ** (L_eff - 1))))

    def _prob(self, step: int, L: int) -> float:
        p1 = self._p_base(L)
        if step == 1:
            return p1
        factor = {5: 0.85, 10: 0.65}[step]   # ← 여기 숫자만 조정하면 체감 바뀜
        return max(0.0, min(1.0, p1 * factor))

    # --- [추가] 레벨 스케일: L↑일수록 1.0 → ~3.0 배까지 점진 증가 ---
    def _level_scale(self, L: int) -> float:
        """
        가격에 곱해지는 레벨 스케일 계수.
        - L=0~1 근처: ≈1.0 (초반 부담 적음)
        - L=200 근처: ≈3.0 (후반 자원 소모 증가)
        지수/다항 완만 곡선으로 급격한 인플레 방지.
        """
        if L <= 1:
            return 1.0
        t = (min(L, 200) - 1) / 199  
        return 1.0 + 2.0 * (t ** 1.3)   # 1.0 → 최대 3.0 근처

    # --- 가격 산정: 기존 공식 × 레벨 스케일 ---
    def price(self, step: int, L: int) -> int:
    
        unit = self.K * self._level_scale(L)           # 레벨당 가격
        discount = {1: 1.00, 5: 0.90, 10: 0.80}[step]  # 묶음할인
        return int(round(unit * step * discount))

    def attempt_upgrade(self, player, step: int) -> dict:
        """
        강화 시도. player.gold와 player.job_lv를 직접 업데이트.
        반환: 결과 dict (UI 후처리/로그용)
        """
        if step not in (1, 5, 10):
            raise ValueError("step must be 1, 5 or 10")

        # 플레이어 상태 보정(없으면 기본값 셋업)
        if not hasattr(player, "job_lv"):
            player.job_lv = 0
        if not hasattr(player, "gold"):
            player.gold = 0

        L0 = player.job_lv
        cost = self.price(step, L0)
        p = self._prob(step, L0)

        if player.gold < cost:
            return {
                "ok": False,
                "reason": "gold_shortage",
                "p": p,
                "step": step,
                "cost": cost,
                "level_before": L0,
                "level_after": L0,
                "gained": 0,
                "gold_before": player.gold,
                "gold_after": player.gold,
            }

        # 결제
        gold_before = player.gold
        player.gold -= cost

        # 판정
        ok = (random.random() < p)
        gained = step if ok else 0
        player.job_lv += gained

        return {
            "ok": ok,
            "p": p,
            "step": step,
            "cost": cost,
            "level_before": L0,
            "level_after": player.job_lv,
            "gained": gained,
            "gold_before": gold_before,
            "gold_after": player.gold,
        }

    # ---------- [미리보기] ----------
    def preview(self, player) -> dict:
        """
        현재 레벨 기준 +1/+5/+10의 확률/가격을 한 번에 조회.
        """
        if not hasattr(player, "job_lv"):
            player.job_lv = 0
        L = player.job_lv
        out = {}
        for step in (1, 5, 10):
            out[step] = {
                "p": self._prob(step, L),
                "price": self.price(step, L),
            }
        return out

    # ---------- [UI] ----------
    def jobup(self, player):
        """
        강화 UI (한 번의 입력-시도-출력 흐름)
        - 보유 자금: player.gold
        - 현재 속성 레벨: player.job_lv (기본 0)
        - 메뉴: "1강", "5강", "10강" 또는 숫자 1/5/10
        - '취소' 입력 시 함수 종료
        """
        # 상태 기본값 보정
        if not hasattr(player, "job_lv"):
            player.job_lv = 0

        if not hasattr(player, "gold"):
            player.gold = 0

        # 헤더
        print()
        print(f'현재 속성 LV : {player.job_lv}')
        print(f'보유 자금    : \033[33m{player.gold}\033[0m')
        print(f'"1강"(1LVUP)  ------  "5강"(5LVUP)  ------  "10강"(10LVUP)')
        print()


        # 미리보기
        info = self.preview(player)
        for step in (1, 5, 10):
            p = info[step]["p"]
            pr = info[step]["price"]
            print(f'+{step:<2}  성공확률: {p*100:5.1f}%   가격: \033[33m{pr}\033[0m')

        # 입력
        print()
        choice = input('원하는 강화를 입력하세요 (1/5/10, 취소=엔터 또는 "취소"): ').strip()
        if choice == "" or choice == "취소":
            print("강화를 취소했습니다.")
            return

        # 입력 파싱
        mapping = {"1강":1, "5강":5, "10강":10, "1":1, "5":5, "10":10}
        if choice not in mapping:
            print("잘못된 입력입니다.")
            return
        step = mapping[choice]

        # 시도
        res = self.attempt_upgrade(player, step)

        # 출력
        time.sleep(0.3)
        print()
        if res["reason"] == "gold_shortage" if "reason" in res else False:
            print(f'자금 부족! 필요: \033[33m{res["cost"]}\033[0m, 보유: \033[33m{res["gold_before"]}\033[0m')
            return

        # 성공/실패 공통 로그
        print(f'+{step} 시도 (p={res["p"]*100:.1f}%, 비용 {res["cost"]})')
        if res["ok"]:
            print(f'\033[92m성공!\033[0m  LV {res["level_before"]} → \033[92m{res["level_after"]}\033[0m  (+\033[92m{res["gained"]}\033[0m)')
        else:
            print(f'\033[91m실패...\033[0m  LV {res["level_before"]} → {res["level_after"]} (변화 없음)')
        print(f'잔액: \033[33m{res["gold_after"]}\033[0m')

    def vs(self, attacker_attr, defender_attr, attacker_job_lv: int) -> int:
        base = 10 * (max(0, attacker_job_lv) ** 3)
        chart = {
            ("물","불"): base,
            ("불","바람"): base,
            ("바람","흙"): base,
            ("흙","물"): base
    }
        return chart.get((attacker_attr, defender_attr), 0)

    def monsterinfo(self,player):
        print(f'Monster Info:')
        color = Stage.color[self.Mtjob]
        reset = "\033[0m"     
        time.sleep(1)
        adddamage = self.vs(player.job,self.Mtjob,player.job_lv)
        subdamage = self.vs(self.Mtjob,player.job,self.round** (1/3)/10)
        print(f'속성 : {color}{self.Mtjob}{reset} 추가데미지 : \033[91m+{adddamage}\033[0m 추가피해 : \033[94m-{subdamage}\033[0m')
        time.sleep(1)
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
                    damage =(player.atk*player.crimult)+self.vs(player.job,self.Mtjob,player.job_lv)
                    
                    self.Mthp = self.Mthp - damage
                    print(f'\033[1;31mCRI!! x{round(player.crimult,2)}Atk! \n{damage}ATK!\033[0m')
                    time.sleep(1)
                    
                    
                else:
                    damage =  player.atk +self.vs(player.job,self.Mtjob,player.job_lv)
                    self.Mthp =  self.Mthp - damage
                    print(f'{damage}의 데미지를 입혔습니다!\n')
                    time.sleep(1)
                    
                
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
                        damage = (player.atk*player.crimult)+self.vs(player.job,self.Mtjob,player.job_lv)
                        self.Mthp = self.Mthp - damage
                        print(f'\033[1;31mCRI!! x{player.crimult}Atk! \n{damage}ATK!\033[0m')
                        
                        time.sleep(1)
                        
                    else:
                        damage = player.atk+self.vs(player.job,self.Mtjob,player.job_lv)
                        self.Mthp =  self.Mthp -damage
                        print(f'{damage}의 데미지를 입혔습니다!\n')
                        time.sleep(1)
                        
                        
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
                    damage = (self.Mtatk*self.crimult)+self.vs(self.Mtjob,player.job,self.round** (1/3)/10)
                    player.hp = player.hp -damage
                    print(f'\033[1;31mCRI!! x{round(self.crimult,2)}Atk! \n{damage}ATK!\033[0m')
                    
                else:
                    damage = self.Mtatk+self.vs(self.Mtjob,player.job,self.round** (1/3)/10)
                    player.hp = player.hp - damage
                    print(f'{damage}의 데미지를 입었습니다!\n')
                    time.sleep(1)
                    
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
                        damage = (player.atk*player.crimult)+self.vs(player.job,self.Mtjob,player.job_lv)
                        self.Mthp = self.Mthp - damage
                        print(f'\033[1;31mCRI!! x{player.crimult}Atk! \n{damage}ATK!\033[0m')
                        
                        time.sleep(1)
                        
                    else:
                        damage= player.atk +self.vs(player.job,self.Mtjob,player.job_lv)
                        self.Mthp =  self.Mthp -damage
                        print(f'{damage}의 데미지를 입혔습니다!\n')
                        time.sleep(1)
                        

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
                    damage = (self.Mtatk*self.crimult)+self.vs(self.Mtjob,player.job,self.round** (1/3)/10)
                    player.hp = player.hp - damage
                    print(f'\033[1;31mCRI!! x{self.crimult}Atk! \n{damage}ATK!\033[0m')
                    time.sleep(1)
                    
                else:
                    damage = self.Mtatk+self.vs(self.Mtjob,player.job,self.round** (1/3)/10)
                    player.hp = player.hp - damage
                    print(f'{damage}의 데미지를 입었습니다!\n')
                    time.sleep(1)
                    
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
                    damage = (player.atk*player.crimult)+self.vs(player.job,self.Mtjob,player.job_lv)
                    self.Mthp = self.Mthp - damage
                    print(f'\033[1;31mCRI!! x{player.crimult}Atk! \n{damage}ATK!\033[0m')
                    
                    time.sleep(1)
                    
                else:
                    damage =  player.atk +self.vs(player.job,self.Mtjob,player.job_lv)
                    self.Mthp =  self.Mthp -damage
                    print(f'{damage}의 데미지를 입혔습니다!\n')
                    time.sleep(1)
                    
                
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

            

