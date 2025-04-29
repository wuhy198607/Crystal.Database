from dataclasses import dataclass, field
from typing import List, Dict
from reader import BinaryReader
from enum import Enum
class Stat(Enum):
    MinAC = 0
    MaxAC = 1
    MinMAC = 2
    MaxMAC = 3
    MinDC = 4
    MaxDC = 5
    MinMC = 6
    MaxMC = 7
    MinSC = 8
    MaxSC = 9
    Accuracy = 10
    Agility = 11
    HP = 12
    MP = 13
    AttackSpeed = 14
    Luck = 15
    BagWeight = 16
    HandWeight = 17
    WearWeight = 18
    Reflect = 19
    Strong = 20
    Holy = 21
    Freezing = 22
    PoisonAttack = 23
    MagicResist = 30
    PoisonResist = 31
    HealthRecovery = 32
    SpellRecovery = 33
    PoisonRecovery = 34
    CriticalRate = 35
    CriticalDamage = 36
    MaxACRatePercent = 40
    MaxMACRatePercent = 41
    MaxDCRatePercent = 42
    MaxMCRatePercent = 43
    MaxSCRatePercent = 44
    AttackSpeedRatePercent = 45
    HPRatePercent = 46
    MPRatePercent = 47
    HPDrainRatePercent = 48
    ExpRatePercent = 100
    ItemDropRatePercent = 101
    GoldDropRatePercent = 102
    MineRatePercent = 103
    GemRatePercent = 104
    FishRatePercent = 105
    CraftRatePercent = 106
    SkillGainMultiplier = 107
    AttackBonus = 108
    LoverExpRatePercent = 120
    MentorDamageRatePercent = 121
    MentorExpRatePercent = 123
    DamageReductionPercent = 124
    EnergyShieldPercent = 125
    EnergyShieldHPGain = 126
    ManaPenaltyPercent = 127
    TeleportManaPenaltyPercent = 128
    Hero = 129
    Unknown = 255
@dataclass
class Stats:
    values: Dict[Stat, int] = None

    def __post_init__(self):
        if self.values is None:
            self.values = {stat: 0 for stat in Stat}

    def __getitem__(self, key):
        return self.values.get(key, 0)

    def __setitem__(self, key, value):
        if value == 0:
            if key in self.values:
                del self.values[key]
            return
        self.values[key] = value

    def add(self, stats):
        for stat, value in stats.values.items():
            self[stat] += value

    def clear(self):
        self.values.clear()

    def __eq__(self, other):
        if not isinstance(other, Stats):
            return False
        if len(self.values) != len(other.values):
            return False
        for stat, value in self.values.items():
            if other[stat] != value:
                return False
        return True
@dataclass
class DropInfo:
    chance: int = 0
    gold: int = 0
    type: int = 0
    quest_required: bool = False
@dataclass
class Monster:
    index: int = 0
    name: str = ""
    image: int = 0
    ai: int = 0
    effect: int = 0
    level: int = 0
    view_range: int = 7
    cool_eye: int = 0
    stats: Stats = None
    drops: List[DropInfo] = field(default_factory=list)
    can_tame: bool = True
    can_push: bool = True
    auto_rev: bool = True
    undead: bool = False
    has_spawn_script: bool = False
    has_die_script: bool = False
    attack_speed: int = 2500
    move_speed: int = 1800
    experience: int = 0
    light: int = 0
    drop_path: str = ""
    @staticmethod
    def read_stats(f):
        """读取状态信息"""
        try:
            stats = Stats()
            count = BinaryReader.read_int32(f)
            for _ in range(count):
                # 先读取数据
                stat_value = BinaryReader.read_byte(f)
                value = BinaryReader.read_int32(f)
                
                # 检查枚举值是否存在
                try:
                    stat = Stat(stat_value)
                    # 只有在枚举值存在时才赋值
                    stats[stat] = value
                except ValueError:
                    # 如果枚举值不存在，跳过这个属性
                    continue
            return stats
        except Exception as e:
            print(f"读取状态信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise   
    @staticmethod
    def read(f):
        """读取怪物信息"""
        try:
            monster = Monster()
            
            # 读取基本信息
            print(f"\n开始读取怪物信息，当前位置: {f.tell()}")
            monster.index = BinaryReader.read_int32(f)
            print(f"读取怪物索引: {monster.index}")
            
            monster.name = BinaryReader.read_string(f)
            print(f"读取怪物名称: {monster.name}")
            
            monster.image = BinaryReader.read_uint16(f)
            print(f"读取怪物图像: {monster.image}")
            
            monster.ai = BinaryReader.read_byte(f)
            print(f"读取怪物AI: {monster.ai}")
            
            monster.effect = BinaryReader.read_byte(f)
            print(f"读取怪物效果: {monster.effect}")

            monster.level = BinaryReader.read_uint16(f)
            print(f"读取怪物等级: {monster.level}")

            monster.view_range = BinaryReader.read_byte(f)
            print(f"读取视野范围: {monster.view_range}")
            
            monster.cool_eye = BinaryReader.read_byte(f)
            print(f"读取冷却时间: {monster.cool_eye}")

            # 读取完整的状态信息
            monster.stats = Monster.read_stats(f)

            monster.light = BinaryReader.read_byte(f)
            print(f"读取光照设置: {monster.light}")
            
            monster.attack_speed = BinaryReader.read_uint16(f)
            print(f"读取攻击速度: {monster.attack_speed}")
            
            monster.move_speed = BinaryReader.read_uint16(f)
            print(f"读取移动速度: {monster.move_speed}")
            
            monster.experience = BinaryReader.read_uint32(f)
            print(f"读取经验值: {monster.experience}")

            # 直接读取布尔值，不使用位运算
            monster.can_push = BinaryReader.read_bool(f)
            print(f"读取可推动: {monster.can_push}")
            
            monster.can_tame = BinaryReader.read_bool(f)
            print(f"读取可驯服: {monster.can_tame}")

            monster.auto_rev = BinaryReader.read_bool(f)
            print(f"读取自动复活: {monster.auto_rev}")
            
            monster.undead = BinaryReader.read_bool(f)
            print(f"读取不死属性: {monster.undead}")

            monster.drop_path = BinaryReader.read_string(f)
            print(f"读取掉落路径: {monster.drop_path}")

            print(f"怪物信息读取完成，当前位置: {f.tell()}")
            return monster
        except Exception as e:
            print(f"读取怪物信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise