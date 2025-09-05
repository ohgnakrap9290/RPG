import random
import re
import time
from collections import Counter

ANSI = re.compile(r'\x1b\[[0-9;]*m')

def _clean(text: str) -> str:
    return ANSI.sub('', text)


class Equip:
    def __init__(self):
        self.player_inven = {}
        self.item_table = {
            "C": [
                "\033[0m나무 검\033[0m",
                "\033[0m나무 방패\033[0m",
                "\033[0m천 갑옷\033[0m",
                "\033[0m룬 반지\033[0m"
            ],
            "\033[32mB\033[0m": [
                "\033[32m돌 검\033[0m",
                "\033[32m돌 방패\033[0m",
                "\033[32m사슬 갑옷\033[0m",
                "\033[32m룬 목걸이\033[0m"
            ],
            "\033[33mA\033[0m": [
                "\033[34m강철 검\033[0m",
                "\033[34m강철 방패\033[0m",
                "\033[34m강철 갑옷\033[0m",
                "\033[34m룬 지팡이\033[0m"
            ],
            "\033[35mS\033[0m": [
                "\033[35m심판의 검\033[0m",
                "\033[35m무한의 방패\033[0m",
                "\033[35m천사의 갑옷\033[0m",
                "\033[35m룬 메아리\033[0m"
            ],
            "\033[93mSS\033[0m": [
                "\033[93m신검\033[0m",
                "\033[93m신의 방패\033[0m",
                "\033[93m신의 갑옷\033[0m",
                "\033[93m룬 코어\033[0m"
            ]
        }

        self.chest_rarity = {
            "일반":   {"C":70, "\033[32mB\033[0m":27,  "\033[33mA\033[0m":2.8, "\033[35mS\033[0m":0.19, "\033[93mSS\033[0m":0.01},
            "희귀":     {"C":40, "\033[32mB\033[0m":40,  "\033[33mA\033[0m":15,  "\033[35mS\033[0m":4.5,  "\033[93mSS\033[0m":0.5},
            "에픽":     {"C":10, "\033[32mB\033[0m":35,  "\033[33mA\033[0m":35,  "\033[35mS\033[0m":18,   "\033[93mSS\033[0m":2},
            "레전드":   {"C": 0, "\033[32mB\033[0m":10,  "\033[33mA\033[0m":40,  "\033[35mS\033[0m":40,   "\033[93mSS\033[0m":10},
        }

        self.player_use_equip={}
        
        self.item_meta = {
            "나무 검":   {"stat": "atk", "base": 10,'type' : 0},
            "나무 방패": {"stat": "def", "base": 15,'type' : 1},
            "천 갑옷":   {"stat": "def", "base": 17,'type' : 2},
            "룬 반지":   {"stat": "atk", "base": 1,'type' : 3},

            "돌 검":     {"stat": "atk", "base": 20,'type' : 0},
            "돌 방패":   {"stat": "def", "base": 30,'type' : 1},
            "사슬 갑옷": {"stat": "def", "base": 34,'type' : 2},
            "룬 목걸이": {"stat": "atk", "base": 4,'type' : 3},

            "강철 검":   {"stat": "atk", "base": 30,'type' : 0},
            "강철 방패": {"stat": "def", "base": 45,'type' : 1},
            "강철 갑옷": {"stat": "def", "base": 51,'type' : 2},
            "룬 지팡이": {"stat": "atk", "base": 8,'type' : 3},

            "심판의 검":   {"stat": "atk", "base": 40,'type' : 0},
            "무한의 방패": {"stat": "def", "base": 60,'type' : 1},
            "천사의 갑옷": {"stat": "def", "base": 68,'type' : 2},
            "룬 메아리":   {"stat": "atk", "base": 14,'type' : 3},

            "신검":       {"stat": "atk", "base": 50,'type' : 0},
            "신의 방패":  {"stat": "def", "base": 75,'type' : 1},
            "신의 갑옷":  {"stat": "def", "base": 85,'type' : 2},
            "룬 코어":    {"stat": "atk", "base": 22,'type' : 3},
        }

        self.rarity_mult = {"C": 1.00, "B": 1.3, "A": 1.7, "S": 2, "SS": 3}
    def _as_internal_rarity(self, r: str) -> str:
        r = r.strip().upper()
        mapping = {
            "C":  "C",
            "B":  "\033[32mB\033[0m",
            "A":  "\033[33mA\033[0m",
            "S":  "\033[35mS\033[0m",
            "SS": "\033[93mSS\033[0m",
        }
        return mapping.get(r, r)

    def _rarity_plain(self, r: str) -> str:
        return _clean(r).upper()
    
    def get_item_bonus(self, rarity_key: str, item_name: str):
        plain_r = self._rarity_plain(rarity_key)
        name = _clean(item_name)
        meta = self.item_meta.get(name)
        if not meta:
            return (0, 0)

        #일단 룬은 나중에 하기
        if "룬" in name or meta.get("type") == 3:
            return (0, 0)

        mult = self.rarity_mult.get(plain_r, 1.0)
        val = meta["base"] * mult

        if meta["stat"] == "atk":
            return (val, 0)
        elif meta["stat"] == "def":
            return (0, val)
        return (0, 0)
    
    def recalc_equipped_bonuses(self, player):
        total_atk = 0.0
        total_def = 0.0
        for rarity_key, name in self.player_use_equip.items():
            a, d = self.get_item_bonus(rarity_key, name)
            total_atk += a
            total_def += d

        player.atk_bonus = int(round(total_atk))
        player.def_bonus = int(round(total_def))

    def chest_info(self,player):
        print('일반 > \033[33m300$\033[0m ------ 희귀 > \033[33m700$\033[0m ------ 에픽 > \033[33m1500$\033[0m ------ 레전드 > \033[33m2400$\033[0m')
        print(f'현재 자금 \033[33m{player.gold}$\033[0m')
        probability = {
            "일반":   {"C":70, "\033[32mB\033[0m":27,  "\033[33mA\033[0m":2.8, "\033[35mS\033[0m":0.19, "\033[93mSS\033[0m":0.01},
            "희귀":     {"C":40, "\033[32mB\033[0m":40,  "\033[33mA\033[0m":15,  "\033[35mS\033[0m":4.5,  "\033[93mSS\033[0m":0.5},
            "에픽":     {"C":10, "\033[32mB\033[0m":35,  "\033[33mA\033[0m":35,  "\033[35mS\033[0m":18,   "\033[93mSS\033[0m":2},
            "레전드":   {"C": 0, "\033[32mB\033[0m":10,  "\033[33mA\033[0m":40,  "\033[35mS\033[0m":40,   "\033[93mSS\033[0m":10},
        }
        for chest, rates in probability.items():
            print(f"\n{chest} 상자 확률:")
            for grade, chance in rates.items():
                print(f"  {grade} : {chance}%")

    def equip_add(self, item, rarity, plus=1):
        if rarity not in self.player_inven:
            self.player_inven[rarity] = Counter()
        name = _clean(item)            
        self.player_inven[rarity][name] += plus

    def equip_info(self):
        print('보유 장비 목록 : ')
        for i,j in self.player_inven.items():
            print(f'[{i}]')
            for h,n in j.items():
                print(f'{h} x {n}',end=' ')
            print("")
        print('')
        print('착용 장비 목록 : ')
        for i,j in self.player_use_equip.items():
            print(f'[{i}] : {j}')
        print('')
                
    def type_check(self, sel_name: str) -> bool:
        # sel_name은 _clean()된 내부 이름이어야 함
        sel_meta = self.item_meta.get(sel_name)
        if not sel_meta:
            raise ValueError(f"목록에 없는 아이템입니다: {sel_name}")
        sel_type = sel_meta["type"]

        for equipped_name in self.player_use_equip.values():
            eq_name = _clean(equipped_name)
            eq_meta = self.item_meta.get(eq_name)
            if eq_meta and eq_meta["type"] == sel_type:
                return False
        return True

    def use_equip(self, player):
        # 인벤 출력
        print('보유 장비 목록 : ')
        for r, cnts in self.player_inven.items():
            print(f'[{r}]')
            for name, n in cnts.items():
                print(f'{name} x {n}', end=' ')
            print("\n")

        # 착용 목록 출력
        print('착용 장비 목록 : ')
        if not self.player_use_equip:
            print('착용중인 장비가 없습니다\n')
        else:
            for r, name in self.player_use_equip.items():
                print(f'[{r}] : {name}')

        # 입력 정규화
        selected_equip_rarity = input('착용할 장비의 등급 입력 : \n').strip()
        selected_equip_rarity = self._as_internal_rarity(selected_equip_rarity)

        raw_name = input('착용할 장비의 이름 입력 : \n').strip()
        selected_equip_name = _clean(raw_name)  # ANSI 제거해 내부키와 맞춤

        # 인벤에 해당 등급 바구니 가져오기 (없으면 빈 Counter)
        bucket = self.player_inven.get(selected_equip_rarity, Counter())

        # 안전 검사 1: 보유 여부
        if bucket.get(selected_equip_name, 0) <= 0:
            print('소유중이지 않거나 잘못된 장비입력입니다\n')
            return

        # 안전 검사 2: 타입 중복(슬롯 충돌)
        if not self.type_check(selected_equip_name):
            print('같은 유형의 장비가 이미 착용중입니다\n')
            return

        # 안전 검사 3: 이미 같은 rarity 칸에 같은 이름을 착용했는지(설계상 rarity->name 저장)
        already = self.player_use_equip.get(selected_equip_rarity)
        if already == selected_equip_name:
            print('이미 착용중인 장비입니다\n')
            return

        # 착용 처리: 인벤 1개 차감, 0되면 키 삭제
        bucket[selected_equip_name] -= 1
        if bucket[selected_equip_name] <= 0:
            del bucket[selected_equip_name]
            if not bucket:            # 등급 바구니가 비면 등급키 제거
                del self.player_inven[selected_equip_rarity]

        # 착용 목록 갱신 (설계상 rarity -> name)
        self.player_use_equip[selected_equip_rarity] = selected_equip_name
        print(f'{selected_equip_name}이/가 착용됐습니다!\n')

        self.recalc_equipped_bonuses(player)
        print(f'장비 보너스: ATK +{getattr(player, "atk_bonus", 0)}, DEF +{getattr(player, "def_bonus", 0)}\n')
        self.equip_plus_atk = getattr(player, "atk_bonus", 0)
        self.equip_plus_def = getattr(player, "def_bonus", 0)

    def roll_item(self, player):
        chest_price = {"일반": 300, "희귀": 700, "에픽": 1500, "레전드": 2400}
        time.sleep(0.5)
        chest_type = input('원하는 상자 등급 입력 (일반/희귀/에픽/레전드): ').strip()

        # 1) 유효성 검사
        if chest_type not in self.chest_rarity:
            print(f'알 수 없는 상자 등급입니다: {chest_type}')
            return

        price = chest_price[chest_type]
        if player.gold < price:
            print('Gold 부족')
            return

        # 2) 구매 확인
        print(f"구매 후 남은 금액 : \033[33m{player.gold - price}$\033[0m")
        confirm = input('확인시 \033[91m"확인"\033[0m, 취소시 \033[91m"취소"\033[0m 또는 Enter: ').strip()
        if confirm != "확인":
            print('구매를 취소했습니다.')
            return

        # 3) 결제(실제 차감!)
        player.gold -= price

        # 4) 등급 가챠
        rarity_table = self.chest_rarity[chest_type]   
        rarities = list(rarity_table.keys())
        weights  = list(rarity_table.values())
        rarity   = random.choices(rarities, weights=weights, k=1)[0] 

        # 5) 아이템 가챠
        pool = self.item_table.get(rarity)
        if not pool:
            print('내부 아이템 테이블 오류(등급 미존재).')
            return
        item = random.choice(pool) 

        self.equip_add(item, rarity)

        time.sleep(1)
        print(f'등급: {rarity}')
        time.sleep(1)
        print(f'아이템: {item}')
        time.sleep(0.3)
        clean_item = _clean(item)
        print(f'→ 인벤토리에 "{clean_item}"이(가) 추가되었습니다. (잔액: \033[33m{player.gold}$\033[0m)')
