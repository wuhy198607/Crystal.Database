from dataclasses import dataclass, field
from typing import List, Optional, Dict

from binary import BinaryReader, BinaryWriter
from enum import Enum
@dataclass
class Point:
    x: int = 0
    y: int = 0
    @staticmethod
    def read_point( f):
        x = BinaryReader.read_int32(f)
        y = BinaryReader.read_int32(f)
        return Point(x, y)
    @staticmethod
    def write_point(f, point):
        BinaryWriter.write_int32(f, point.x)
        BinaryWriter.write_int32(f, point.y)
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