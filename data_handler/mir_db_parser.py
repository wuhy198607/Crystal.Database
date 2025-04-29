import struct
import os
import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import re
import random
from reader import BinaryReader
from  map import Map, Point, SafeZoneInfo, MovementInfo, RespawnInfo, MineZone
from  item import Item
from  monster import Monster
from  npc import NPC
class Settings:
    """设置类，用于定义各种路径"""
    QuestPath = "Quests"  # 任务文件所在目录
    DropPath = "Drops"    # 掉落文件所在目录


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

class LightSetting(Enum):
    Normal = 0
    Dawn = 1
    Day = 2
    Dusk = 3
    Night = 4

class WeatherSetting(Enum):
    None_ = 0
    Rain = 1
    Snow = 2
    Fog = 3

class Spell(Enum):
    None_ = 0
    FireBall = 1
    Healing = 2
    # ... 其他魔法类型

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



class QuestType(Enum):
    General = 0
    Daily = 1
    Weekly = 2
    Repeatable = 3
    Story = 4
    Achievement = 5
    Tutorial = 6

@dataclass
class QuestItemTask:
    item: 'ItemInfo' = None
    count: int = 0
    message: str = ""

@dataclass
class QuestKillTask:
    monster: 'MonsterInfo' = None
    count: int = 0
    message: str = ""

@dataclass
class QuestFlagTask:
    number: int = 0
    message: str = ""

@dataclass
class QuestItemReward:
    item: 'ItemInfo' = None
    count: int = 0
@dataclass  
class RequiredClass(Enum):
    None_ = 0
    Warrior = 1
    Wizard = 2
    Taoist = 3
    Assassin = 4
    Archer = 5
@dataclass
class QuestInfo:
    index: int = 0
    name: str = ""
    group: str = ""
    file_name: str = ""
    required_min_level: int = 0
    required_max_level: int = 0
    required_quest: int = 0
    required_class: RequiredClass = field(default_factory=lambda: RequiredClass.None_)
    type: QuestType = field(default_factory=lambda: QuestType.General)  
    goto_message: str = ""
    kill_message: str = ""
    item_message: str = ""
    flag_message: str = ""
    time_limit_in_seconds: int = 0
    
    # 任务描述
    description: List[str] = field(default_factory=list)
    task_description: List[str] = field(default_factory=list)
    return_description: List[str] = field(default_factory=list)
    completion_description: List[str] = field(default_factory=list)
    
    # 任务物品
    carry_items: List[QuestItemTask] = field(default_factory=list)
    
    # 任务目标
    kill_tasks: List[QuestKillTask] = field(default_factory=list)
    item_tasks: List[QuestItemTask] = field(default_factory=list)
    flag_tasks: List[QuestFlagTask] = field(default_factory=list)
    
    # 任务奖励
    gold_reward: int = 0
    exp_reward: int = 0
    credit_reward: int = 0
    fixed_rewards: List[QuestItemReward] = field(default_factory=list)
    select_rewards: List[QuestItemReward] = field(default_factory=list)

@dataclass
class DragonDropInfo:
    chance: int = 0
    item: Optional['ItemInfo'] = None
    gold: int = 0
    level: int = 0

@dataclass
class DragonInfo:
    enabled: bool = False
    map_file_name: str = "D2083"
    monster_name: str = "Evil Mir"
    body_name: str = "00"
    location: Point = field(default_factory=Point)
    drop_area_top: Point = field(default_factory=Point)
    drop_area_bottom: Point = field(default_factory=Point)
    level: int = 1
    experience: int = 0
    exps: List[int] = field(default_factory=lambda: [10000 * (i + 1) for i in range(12)])  # 12级经验值
    drops: List[List[DragonDropInfo]] = field(default_factory=lambda: [[] for _ in range(13)])  # 13级掉落

    def __post_init__(self):
        # 设置默认位置
        if self.location.x == 0 and self.location.y == 0:
            self.location = Point(82, 44)
        if self.drop_area_top.x == 0 and self.drop_area_top.y == 0:
            self.drop_area_top = Point(75, 45)
        if self.drop_area_bottom.x == 0 and self.drop_area_bottom.y == 0:
            self.drop_area_bottom = Point(86, 57)

    def read_dragon_info(self, f):
        """读取龙信息"""
        try:
            dragon = DragonInfo()
            
            # 读取基本信息
            print(f"\n开始读取龙信息，当前位置: {f.tell()}")
            dragon.enabled = BinaryReader.read_bool(f)
            print(f"读取启用状态: {dragon.enabled}")
            
            dragon.map_file_name = BinaryReader.read_string(f)
            print(f"读取地图文件名: {dragon.map_file_name}")
            
            dragon.monster_name = BinaryReader.read_string(f)
            print(f"读取怪物名称: {dragon.monster_name}")
            
            dragon.body_name = BinaryReader.read_string(f)
            print(f"读取身体名称: {dragon.body_name}")
            
            # 读取位置信息
            dragon.location = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取位置: ({dragon.location.x}, {dragon.location.y})")
            
            dragon.drop_area_top = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取掉落区域顶部: ({dragon.drop_area_top.x}, {dragon.drop_area_top.y})")
            
            dragon.drop_area_bottom = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取掉落区域底部: ({dragon.drop_area_bottom.x}, {dragon.drop_area_bottom.y})")
            
            # 读取经验值
            for i in range(len(dragon.exps)):
                dragon.exps[i] = BinaryReader.read_int64(f)
                print(f"读取等级 {i+1} 经验值: {dragon.exps[i]}")
            
            # 加载掉落信息
            self.load_dragon_drops(dragon)
            
            return dragon
        except Exception as e:
            print(f"读取龙信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def load_dragon_drops(self, dragon):
        """加载龙掉落信息"""
        # 清空所有掉落列表
        for level_drops in dragon.drops:
            level_drops.clear()
            
        # 确保掉落文件目录存在
        drop_path = os.path.join(os.path.dirname(self.db_path), Settings.DropPath)
        if not os.path.exists(drop_path):
            print(f"掉落文件目录不存在: {drop_path}")
            return
            
        file_path = os.path.join(drop_path, "DragonItem.txt")
        if not os.path.exists(file_path):
            print(f"龙掉落文件不存在: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue
                        
                    drop = self.parse_dragon_drop(line)
                    if drop and 0 < drop.level <= len(dragon.drops):
                        dragon.drops[drop.level - 1].append(drop)
                        
            # 对每个等级的掉落列表进行排序
            for level_drops in dragon.drops:
                level_drops.sort(key=lambda d: (d.gold == 0, d.item.type if d.item else 0))
                
        except Exception as e:
            print(f"加载龙掉落信息时出错: {str(e)}")
            raise

    def parse_dragon_drop(self, line):
        """解析龙掉落信息"""
        parts = line.split()
        if len(parts) < 3:
            return None
            
        try:
            drop = DragonDropInfo()
            drop.chance = int(parts[0][2:])  # 跳过前两个字符
            
            if parts[1].lower() == "gold":
                if len(parts) < 4:
                    return None
                drop.gold = int(parts[2])
                drop.level = int(parts[3])
            else:
                drop.item = self.get_item_info(parts[1])
                if not drop.item:
                    return None
                drop.level = int(parts[2])
                
            return drop
        except (ValueError, IndexError):
            return None


@dataclass
class MagicInfo:
    name: str = ""
    spell: Spell = Spell.None_
    base_cost: int = 0
    level_cost: int = 0
    icon: int = 0
    level1: int = 0
    level2: int = 0
    level3: int = 0
    need1: int = 0
    need2: int = 0
    need3: int = 0
    delay_base: int = 1800
    delay_reduction: int = 0
    power_base: int = 0
    power_bonus: int = 0
    mpower_base: int = 0
    mpower_bonus: int = 0
    range: int = 9
    multiplier_base: float = 1.0
    multiplier_bonus: float = 0.0

@dataclass
class UserMagic:
    spell: Spell = Spell.None_
    info: Optional[MagicInfo] = None
    level: int = 0
    key: int = 0
    experience: int = 0
    is_temp_spell: bool = False
    cast_time: int = 0

    def get_magic_info(self, spell: Spell) -> Optional[MagicInfo]:
        for info in self.magic_info_list:
            if info.spell == spell:
                return info
        return None

    def create_client_magic(self):
        if not self.info:
            return None
        return {
            'name': self.info.name,
            'spell': self.info.spell,
            'base_cost': self.info.base_cost,
            'level_cost': self.info.level_cost,
            'icon': self.info.icon,
            'level1': self.info.level1,
            'level2': self.info.level2,
            'level3': self.info.level3,
            'need1': self.info.need1,
            'need2': self.info.need2,
            'need3': self.info.need3,
            'level': self.level,
            'key': self.key,
            'experience': self.experience,
            'is_temp_spell': self.is_temp_spell,
            'delay': self.get_delay(),
            'range': self.info.range,
            'cast_time': self.cast_time
        }

    def get_delay(self) -> int:
        if not self.info:
            return 0
        return self.info.delay_base - (self.level * self.info.delay_reduction)

    def get_power(self) -> int:
        if not self.info:
            return 0
        return int(round((self.mpower() / 4.0) * (self.level + 1) + self.def_power()))

    def mpower(self) -> int:
        if not self.info:
            return 0
        if self.info.mpower_bonus > 0:
            return random.randint(self.info.mpower_base, self.info.mpower_bonus + self.info.mpower_base)
        return self.info.mpower_base

    def def_power(self) -> int:
        if not self.info:
            return 0
        if self.info.power_bonus > 0:
            return random.randint(self.info.power_base, self.info.power_bonus + self.info.power_base)
        return self.info.power_base

    def get_multiplier(self) -> float:
        if not self.info:
            return 0.0
        return self.info.multiplier_base + (self.level * self.info.multiplier_bonus)

    def get_damage(self, damage_base: int) -> int:
        return int((damage_base + self.get_power()) * self.get_multiplier())

class MirDBParser:
    def __init__(self, db_path):
        self.db_path = db_path
        self.version = 0
        self.custom_version = 0
        self.maps = []
        self.monsters = []
        self.items = []
        self.npcs = []
        self.quests = []
        self.dragons = []  # 添加dragon列表
        self.magics = []  # 添加魔法信息列表

    @staticmethod
    def read_int32(f):
        """读取32位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(4)
            print(f"读取int32原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<i', data)[0]
        except Exception as e:
            print(f"读取int32时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_int16(f):
        """读取16位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(2)
            print(f"读取int16原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<h', data)[0]
        except Exception as e:
            print(f"读取int16时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_uint16(f):
        """读取无符号16位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(2)
            print(f"读取uint16原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<H', data)[0]
        except Exception as e:
            print(f"读取uint16时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise
    @staticmethod
    def read_uint64(f):
        """读取64位无符号整数"""
        try:
            data = f.read(8)
            if len(data) < 8:
                print(f"读取uint64时数据不足8字节: {len(data)}")
                return 0
            return struct.unpack('<Q', data)[0]
        except Exception as e:
            print(f"读取uint64时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            return 0
    @staticmethod
    def read_uint32(f):
        """读取无符号32位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(4)
            print(f"读取uint32原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<I', data)[0]
        except Exception as e:
            print(f"读取uint32时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_byte(f):
        """读取一个字节"""
        try:
            data = f.read(1)
            print(f"读取byte原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('B', data)[0]
        except Exception as e:
            print(f"读取byte时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_bool(f):
        """读取布尔值"""
        try:
            data = f.read(1)
            print(f"读取bool原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('?', data)[0]
        except Exception as e:
            print(f"读取bool时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_string(f):
        """读取字符串，使用7位编码的长度前缀格式"""
        try:
            # 读取7位编码的字符串长度
            length = 0
            shift = 0
            while True:
                data = f.read(1)
                print(f"读取字符串长度原始字节: {' '.join(f'{b:02x}' for b in data)}")
                b = struct.unpack('B', data)[0]
                length |= (b & 0x7F) << shift
                if (b & 0x80) == 0:
                    break
                shift += 7
            
            if length == 0:
                return ""
            
            # 读取字符串数据
            data = f.read(length)
            print(f"读取字符串数据原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return data.decode('latin1')
            
        except Exception as e:
            print(f"读取字符串时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    


    

    def read_stats(self, f):
        """读取状态信息"""
        try:
            stats = Stats()
            count = self.read_int32(f)
            for _ in range(count):
                # 先读取数据
                stat_value = self.read_byte(f)
                value = self.read_int32(f)
                
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


    def read_quest_info(self, f):
        """读取任务信息"""
        try:
            quest = QuestInfo()
            
            # 读取基本信息
            print(f"\n开始读取任务信息，当前位置: {f.tell()}")
            quest.index = self.read_int32(f)
            print(f"读取任务索引: {quest.index}")
            
            quest.name = self.read_string(f)
            print(f"读取任务名称: {quest.name}")
            
            quest.group = self.read_string(f)
            print(f"读取任务组: {quest.group}")
            
            quest.file_name = self.read_string(f)
            print(f"读取文件名: {quest.file_name}")
            
            quest.required_min_level = self.read_int32(f)
            print(f"读取最低等级要求: {quest.required_min_level}")
            
            quest.required_max_level = self.read_int32(f)
            if quest.required_max_level == 0:
                quest.required_max_level = 65535  # ushort.MaxValue
            print(f"读取最高等级要求: {quest.required_max_level}")
            
            quest.required_quest = self.read_int32(f)
            print(f"读取前置任务: {quest.required_quest}")
            
            # 读取职业要求，如果值无效则设置为None
            try:
                required_class_value = self.read_byte(f)
                print(f"读取byte原始字节: {required_class_value:02x}")
                quest.required_class = RequiredClass(required_class_value)
            except ValueError:
                print(f"警告: 无效的职业要求值 {required_class_value}，将设置为 None")
                quest.required_class = RequiredClass.None_
            print(f"读取职业要求: {quest.required_class}")
            
            # 读取任务类型，如果值无效则设置为General
            try:
                quest_type_value = self.read_byte(f)
                quest.type = QuestType(quest_type_value)
            except ValueError:
                print(f"警告: 无效的任务类型值 {quest_type_value}，将设置为 General")
                quest.type = QuestType.General
            print(f"读取任务类型: {quest.type}")
            
            quest.goto_message = self.read_string(f)
            print(f"读取前往消息: {quest.goto_message}")
            
            quest.kill_message = self.read_string(f)
            print(f"读取击杀消息: {quest.kill_message}")
            
            quest.item_message = self.read_string(f)
            print(f"读取物品消息: {quest.item_message}")
            
            quest.flag_message = self.read_string(f)
            print(f"读取标记消息: {quest.flag_message}")
            
            if self.version > 90:
                quest.time_limit_in_seconds = self.read_int32(f)
                print(f"读取时间限制: {quest.time_limit_in_seconds}")
            
            # 加载任务详细信息
            self.load_quest_info(quest)
            
            return quest
        except Exception as e:
            print(f"读取任务信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def load_quest_info(self, quest, clear=False):
        """加载任务详细信息"""
        if clear:
            self.clear_quest_info(quest)
            
        # 确保任务文件目录存在
        quest_path = os.path.join(os.path.dirname(self.db_path), Settings.QuestPath)
        if not os.path.exists(quest_path):
            print(f"任务文件目录不存在: {quest_path}")
            return
            
        file_path = os.path.join(quest_path, f"{quest.file_name}.txt")
        if not os.path.exists(file_path):
            print(f"任务文件不存在: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.parse_quest_file(quest, lines)
        except Exception as e:
            print(f"加载任务文件时出错: {str(e)}")
            raise

    def clear_quest_info(self, quest):
        """清除任务信息"""
        quest.description.clear()
        quest.task_description.clear()
        quest.return_description.clear()
        quest.completion_description.clear()
        quest.carry_items.clear()
        quest.kill_tasks.clear()
        quest.item_tasks.clear()
        quest.flag_tasks.clear()
        quest.fixed_rewards.clear()
        quest.select_rewards.clear()
        quest.exp_reward = 0
        quest.gold_reward = 0
        quest.credit_reward = 0

    def parse_quest_file(self, quest, lines):
        """解析任务文件"""
        description_key = "[@DESCRIPTION]"
        task_key = "[@TASKDESCRIPTION]"
        return_key = "[@RETURNDESCRIPTION]"
        completion_key = "[@COMPLETION]"
        carry_items_key = "[@CARRYITEMS]"
        kill_tasks_key = "[@KILLTASKS]"
        item_tasks_key = "[@ITEMTASKS]"
        flag_tasks_key = "[@FLAGTASKS]"
        fixed_rewards_key = "[@FIXEDREWARDS]"
        select_rewards_key = "[@SELECTREWARDS]"
        exp_reward_key = "[@EXPREWARD]"
        gold_reward_key = "[@GOLDREWARD]"
        credit_reward_key = "[@CREDITREWARD]"
        
        headers = [
            description_key, task_key, completion_key,
            carry_items_key, kill_tasks_key, item_tasks_key, flag_tasks_key,
            fixed_rewards_key, select_rewards_key, exp_reward_key, gold_reward_key, credit_reward_key, return_key
        ]
        
        current_header = 0
        while current_header < len(headers):
            for i in range(len(lines)):
                line = lines[i].strip().upper()
                if line != headers[current_header].upper():
                    continue
                    
                for j in range(i + 1, len(lines)):
                    inner_line = lines[j].strip()
                    if inner_line.startswith('[') or inner_line.startswith('//'):
                        break
                    if not inner_line:
                        continue
                        
                    if line == description_key:
                        quest.description.append(inner_line)
                    elif line == task_key:
                        quest.task_description.append(inner_line)
                    elif line == return_key:
                        quest.return_description.append(inner_line)
                    elif line == completion_key:
                        quest.completion_description.append(inner_line)
                    elif line == carry_items_key:
                        task = self.parse_quest_item(inner_line)
                        if task:
                            quest.carry_items.append(task)
                    elif line == kill_tasks_key:
                        task = self.parse_quest_kill(inner_line)
                        if task:
                            quest.kill_tasks.append(task)
                    elif line == item_tasks_key:
                        task = self.parse_quest_item(inner_line)
                        if task:
                            quest.item_tasks.append(task)
                    elif line == flag_tasks_key:
                        task = self.parse_quest_flag(inner_line)
                        if task:
                            quest.flag_tasks.append(task)
                    elif line == fixed_rewards_key:
                        reward = self.parse_quest_reward(inner_line)
                        if reward:
                            quest.fixed_rewards.append(reward)
                    elif line == select_rewards_key:
                        reward = self.parse_quest_reward(inner_line)
                        if reward:
                            quest.select_rewards.append(reward)
                    elif line == exp_reward_key:
                        quest.exp_reward = int(inner_line)
                    elif line == gold_reward_key:
                        quest.gold_reward = int(inner_line)
                    elif line == credit_reward_key:
                        quest.credit_reward = int(inner_line)
                        
            current_header += 1

    def parse_quest_item(self, line):
        """解析任务物品"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        count = 1
        if len(parts) > 1:
            count = int(parts[1])
            
        message = ""
        match = re.search(r'"([^"]*)"', line)
        if match:
            message = match.group(1)
            
        item_info = self.get_item_info(parts[0])
        if not item_info:
            # 尝试查找性别特定的物品
            item_info = self.get_item_info(f"{parts[0]}(M)")
            if not item_info:
                item_info = self.get_item_info(f"{parts[0]}(F)")
                
        if not item_info:
            return None
            
        return QuestItemTask(item=item_info, count=count, message=message)

    def parse_quest_kill(self, line):
        """解析击杀任务"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        count = 1
        if len(parts) > 1:
            count = int(parts[1])
            
        message = ""
        match = re.search(r'"([^"]*)"', line)
        if match:
            message = match.group(1)
            
        monster_info = self.get_monster_info(parts[0])
        if not monster_info:
            return None
            
        return QuestKillTask(monster=monster_info, count=count, message=message)

    def parse_quest_flag(self, line):
        """解析标记任务"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        number = int(parts[0])
        if number < 0 or number > 1000:  # 假设最大标记数为1000
            return None
            
        message = ""
        match = re.search(r'"([^"]*)"', line)
        if match:
            message = match.group(1)
            
        return QuestFlagTask(number=number, message=message)

    def parse_quest_reward(self, line):
        """解析任务奖励"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        count = 1
        if len(parts) > 1:
            count = int(parts[1])
            
        item_info = self.get_item_info(parts[0])
        if not item_info:
            return None
            
        return QuestItemReward(item=item_info, count=count)

    def load(self):
        """加载数据库文件"""
        if not os.path.exists(self.db_path):
            print(f"数据库文件不存在: {self.db_path}")
            return False

        try:
            with open(self.db_path, 'rb') as f:
                # 读取版本信息
                self.version = BinaryReader.read_int32(f)
                self.custom_version = BinaryReader.read_int32(f)
                
                print(f"\n=== 数据库信息 ===")
                print(f"数据库版本: {self.version}")
                print(f"自定义版本: {self.custom_version}")

                print("\n=== 索引信息 ===")
                # 读取索引
                map_index = BinaryReader.read_int32(f)
                item_index = BinaryReader.read_int32(f)
                monster_index = BinaryReader.read_int32(f)
                npc_index = BinaryReader.read_int32(f)
                quest_index = BinaryReader.read_int32(f)
                
                print(f"地图索引: {map_index}")
                print(f"物品索引: {item_index}")
                print(f"怪物索引: {monster_index}")
                print(f"NPC索引: {npc_index}")
                print(f"任务索引: {quest_index}")
                
                # 根据版本读取额外索引
                gameshop_index = 0
                conquest_index = 0
                respawn_index = 0
                
                gameshop_index = BinaryReader.read_int32(f)
                print(f"商店索引: {gameshop_index}")
                    
                conquest_index = BinaryReader.read_int32(f)
                print(f"征服索引: {conquest_index}")
                
                respawn_index = BinaryReader.read_int32(f)
                print(f"重生索引: {respawn_index}")

                print("\n=== 地图信息 ===")
                # 读取地图信息
                map_count = BinaryReader.read_int32(f)
                print(f"地图总数: {map_count}")
                
                
                for i in range(map_count):
                    try:
                        map_info = Map.read(f)
                        self.maps.append(map_info)
                        print(f"\n地图 {i+1}/{map_count}:")
                        print(f"  索引: {map_info.index}")
                        print(f"  文件名: {map_info.filename}")
                        print(f"  标题: {map_info.title}")
                        print(f"  小地图: {map_info.mini_map}")
                        print(f"  大地图: {map_info.big_map}")
                        print(f"  安全区域数量: {len(map_info.safe_zones)}")
                        print(f"  重生点数量: {len(map_info.respawns)}")
                        print(f"  移动点数量: {len(map_info.movements)}")
                        print(f"  矿区数量: {len(map_info.mine_zones)}")
                    except Exception as e:
                        print(f"读取地图 {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== 物品信息 ===")
                # 读取物品信息（全量读取）
                item_count = BinaryReader.read_int32(f)
                print(f"物品总数: {item_count}")
                
                for i in range(item_count):
                    try:
                        item_info = Item.read(f)
                        self.items.append(item_info)
                        print(f"  索引: {item_info.index}")
                        print(f"  名称: {item_info.name}")
                        print(f"  类型: {item_info.type}")
                        print(f"  等级: {item_info.grade}")
                        print(f"  价格: {item_info.price}")
                        print(f"  耐久: {item_info.durability}")
                        print(f"  堆叠: {item_info.stack_size}")
                    except Exception as e:
                        print(f"读取物品 {i+1} 时出错: {str(e)}")
                        continue
                
                print("\n=== 怪物信息 ===")
                # 读取怪物信息（全量读取）
                monster_count = BinaryReader.read_int32(f)
                print(f"怪物总数: {monster_count}")
                
                for i in range(monster_count):
                    try:
                        monster_info = Monster.read(f)
                        self.monsters.append(monster_info)
                        print(f"\n怪物 {i+1}/{monster_count}:")
                        print(f"  索引: {monster_info.index}")
                        print(f"  名称: {monster_info.name}")
                        print(f"  等级: {monster_info.level}")
                        print(f"  掉落物数量: {len(monster_info.drops)}")
                        print(f"  攻击速度: {monster_info.attack_speed}")
                        print(f"  移动速度: {monster_info.move_speed}")
                        print(f"  经验值: {monster_info.experience}")
                    except Exception as e:
                        print(f"读取怪物 {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== NPC信息 ===")
                # 读取NPC信息
                npc_count = BinaryReader.read_int32(f)
                print(f"NPC总数: {npc_count}")
                
                for i in range(npc_count):
                    try:
                        npc_info = NPC.read(f)
                        self.npcs.append(npc_info)
                        print(f"\nNPC {i+1}/{npc_count}:")
                        print(f"  索引: {npc_info.index}")
                        print(f"  名称: {npc_info.name}")
                        print(f"  文件名: {npc_info.file_name}")
                        print(f"  地图索引: {npc_info.map_index}")
                        print(f"  位置: ({npc_info.location.x}, {npc_info.location.y})")
                        print(f"  收集任务数量: {len(npc_info.collect_quest_indexes)}")
                        print(f"  完成任务数量: {len(npc_info.finish_quest_indexes)}")
                    except Exception as e:
                        print(f"读取NPC {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== 任务信息 ===")
                # 读取任务信息
                quest_count = BinaryReader.read_int32(f)
                print(f"任务总数: {quest_count}")
                
                for i in range(quest_count):
                    try:
                        quest_info = self.read_quest_info(f)
                        self.quests.append(quest_info)
                        print(f"\n任务 {i+1}/{quest_count}:")
                        print(f"  索引: {quest_info.index}")
                        print(f"  名称: {quest_info.name}")
                        print(f"  组: {quest_info.group}")
                        print(f"  类型: {quest_info.type}")
                        print(f"  最低等级: {quest_info.required_min_level}")
                        print(f"  最高等级: {quest_info.required_max_level}")
                        print(f"  前置任务: {quest_info.required_quest}")
                        print(f"  职业要求: {quest_info.required_class}")
                        print(f"  击杀任务数量: {len(quest_info.kill_tasks)}")
                        print(f"  物品任务数量: {len(quest_info.item_tasks)}")
                        print(f"  标记任务数量: {len(quest_info.flag_tasks)}")
                        print(f"  固定奖励数量: {len(quest_info.fixed_rewards)}")
                        print(f"  可选奖励数量: {len(quest_info.select_rewards)}")
                    except Exception as e:
                        print(f"读取任务 {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== 龙信息 ===")
                # 读取龙信息
                try:
                    dragon_info = self.read_dragon_info(f)
                    self.dragons.append(dragon_info)
                    print(f"\n龙信息:")
                    print(f"  启用状态: {dragon_info.enabled}")
                    print(f"  地图文件名: {dragon_info.map_file_name}")
                    print(f"  怪物名称: {dragon_info.monster_name}")
                    print(f"  身体名称: {dragon_info.body_name}")
                    print(f"  位置: ({dragon_info.location.x}, {dragon_info.location.y})")
                    print(f"  掉落区域: ({dragon_info.drop_area_top.x}, {dragon_info.drop_area_top.y}) - ({dragon_info.drop_area_bottom.x}, {dragon_info.drop_area_bottom.y})")
                    print(f"  等级: {dragon_info.level}")
                    print(f"  经验值: {dragon_info.experience}")
                    for j, exp in enumerate(dragon_info.exps):
                        print(f"  等级 {j+1} 经验值: {exp}")
                    for j, level_drops in enumerate(dragon_info.drops):
                        print(f"  等级 {j+1} 掉落数量: {len(level_drops)}")
                except Exception as e:
                    print(f"读取龙信息时出错: {str(e)}")
                    # 移除continue语句

              
                
                print("\n=== 魔法信息 ===")
                # 读取魔法数量
                magic_count = BinaryReader.read_int32(f)
                print(f"魔法数量: {magic_count}")
                
                # 读取魔法信息
                self.magics = []
                for i in range(magic_count):
                    try:
                        magic_info = self.read_magic_info(f)
                        self.magics.append(magic_info)
                        print(f"\n魔法信息 {i+1}/{magic_count}:")
                        print(f"  名称: {magic_info.name}")
                        print(f"  类型: {magic_info.spell}")
                        print(f"  基础消耗: {magic_info.base_cost}")
                        print(f"  等级消耗: {magic_info.level_cost}")
                        print(f"  图标: {magic_info.icon}")
                        print(f"  等级1: {magic_info.level1}")
                        print(f"  等级2: {magic_info.level2}")
                        print(f"  等级3: {magic_info.level3}")
                        print(f"  需求1: {magic_info.need1}")
                        print(f"  需求2: {magic_info.need2}")
                        print(f"  需求3: {magic_info.need3}")
                        print(f"  基础延迟: {magic_info.delay_base}")
                        print(f"  延迟减少: {magic_info.delay_reduction}")
                        print(f"  基础力量: {magic_info.power_base}")
                        print(f"  力量奖励: {magic_info.power_bonus}")
                        print(f"  基础魔法力量: {magic_info.mpower_base}")
                        print(f"  魔法力量奖励: {magic_info.mpower_bonus}")
                        print(f"  范围: {magic_info.range}")
                        print(f"  基础倍数: {magic_info.multiplier_base}")
                        print(f"  倍数奖励: {magic_info.multiplier_bonus}")
                    except Exception as e:
                        print(f"读取魔法信息 {i+1} 时出错: {str(e)}")

                print("\n=== 商城信息 ===")
                # 读取商城物品数量
                gameshop_count = BinaryReader.read_int32(f)
                print(f"商城物品数量: {gameshop_count}")
                
                # 读取商城物品信息
                self.gameshop_items = []
                for i in range(gameshop_count):
                    try:
                        item = GameShopItem()
                        item.item_index = BinaryReader.read_int32(f)
                        item.g_index = BinaryReader.read_int32(f)
                        item.gold_price = BinaryReader.read_uint32(f)
                        item.credit_price = BinaryReader.read_uint32(f)
                        if self.version <= 84:
                            item.count = BinaryReader.read_uint32(f)
                        else:
                            item.count = BinaryReader.read_uint16(f)
                        item.class_name = BinaryReader.read_string(f)
                        item.category = BinaryReader.read_string(f)
                        item.stock = BinaryReader.read_int32(f)
                        item.i_stock = BinaryReader.read_bool(f)
                        item.deal = BinaryReader.read_bool(f)
                        item.top_item = BinaryReader.read_bool(f)
                        item.date = BinaryReader.read_int64(f)
                        if self.version > 105:
                            item.can_buy_gold = BinaryReader.read_bool(f)
                            item.can_buy_credit = BinaryReader.read_bool(f)
                        
                        self.gameshop_items.append(item)
                        print(f"\n商城物品 {i+1}/{gameshop_count}:")
                        print(f"  物品索引: {item.item_index}")
                        print(f"  商品索引: {item.g_index}")
                        print(f"  金币价格: {item.gold_price}")
                        print(f"  元宝价格: {item.credit_price}")
                        print(f"  数量: {item.count}")
                        print(f"  职业: {item.class_name}")
                        print(f"  分类: {item.category}")
                        print(f"  库存: {item.stock}")
                        print(f"  是否限量: {item.i_stock}")
                        print(f"  是否特价: {item.deal}")
                        print(f"  是否置顶: {item.top_item}")
                        print(f"  可否用金币购买: {item.can_buy_gold}")
                        print(f"  可否用元宝购买: {item.can_buy_credit}")
                    except Exception as e:
                        print(f"读取商城物品 {i+1} 时出错: {str(e)}")

                print("\n=== 数据读取完成 ===")
                print(f"成功加载地图数量: {len(self.maps)}")
                print(f"成功加载物品数量: {len(self.items)}")
                print(f"成功加载怪物数量: {len(self.monsters)}")
                print(f"成功加载NPC数量: {len(self.npcs)}")
                print(f"成功加载任务数量: {len(self.quests)}")
                print(f"成功加载龙数量: {len(self.dragons)}")

                print("\n=== 征服信息 ===")
                # 读取征服信息
                conquest_count = BinaryReader.read_int32(f)
                print(f"征服数量: {conquest_count}")
                
                self.conquests = []
                for i in range(conquest_count):
                    try:
                        conquest_info = self.read_conquest_info(f)
                        self.conquests.append(conquest_info)
                        print(f"\n征服信息 {i+1}/{conquest_count}:")
                        print(f"  索引: {conquest_info.index}")
                        print(f"  名称: {conquest_info.name}")
                        print(f"  地图索引: {conquest_info.map_index}")
                        print(f"  宫殿索引: {conquest_info.palace_index}")
                        print(f"  守卫数量: {len(conquest_info.conquest_guards)}")
                        print(f"  城门数量: {len(conquest_info.conquest_gates)}")
                        print(f"  城墙数量: {len(conquest_info.conquest_walls)}")
                        print(f"  攻城数量: {len(conquest_info.conquest_sieges)}")
                        print(f"  旗帜数量: {len(conquest_info.conquest_flags)}")
                        print(f"  控制点数量: {len(conquest_info.control_points)}")
                    except Exception as e:
                        print(f"读取征服信息 {i+1} 时出错: {str(e)}")

                print("\n=== 刷新计时器信息 ===")
                # 读取刷新计时器信息
                try:
                    respawn_timer = self.read_respawn_timer(f)
                    self.respawn_timer = respawn_timer
                    print(f"\n刷新计时器信息:")
                    print(f"  基础刷新率: {respawn_timer.base_spawn_rate}")
                    print(f"  当前刷新计数器: {respawn_timer.current_tick_counter}")
                    print(f"  刷新选项数量: {len(respawn_timer.respawn_options)}")
                    for i, option in enumerate(respawn_timer.respawn_options):
                        print(f"  选项 {i+1}:")
                        print(f"    用户数量: {option.user_count}")
                        print(f"    延迟损失: {option.delay_loss}")
                except Exception as e:
                    print(f"读取刷新计时器信息时出错: {str(e)}")

        except Exception as e:
            print(f"加载数据库时出错: {str(e)}")
            return False

        return True

    def save_to_json(self, output_path):
        """保存数据到多个JSON文件，使用UTF-8编码"""
        # 创建输出目录
        os.makedirs(output_path, exist_ok=True)
        
        # 保存版本信息
        version_data = {
            'version': self.version,
            'custom_version': self.custom_version
        }
        version_path = os.path.join(output_path, 'version.json')
        with open(version_path, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, ensure_ascii=False, indent=2)

        # 保存地图信息
        maps_data = [
            {
                'index': m.index,
                'file_name': m.filename,
                'title': m.title,
                'mini_map': m.mini_map,
                'light': m.light,
                'big_map': m.big_map,
                'safe_zones': [
                    {
                        'location': {'x': sz.location.x, 'y': sz.location.y},
                        'size': sz.size,
                        'start_point': sz.start_point
                    } for sz in m.safe_zones
                ],
                'no_teleport': m.no_teleport,
                'no_reconnect': m.no_reconnect,
                'no_reconnect_map': m.no_reconnect_map,
                'no_random': m.no_random,
                'no_escape': m.no_escape,
                'no_recall': m.no_recall,
                'no_drug': m.no_drug,
                'no_position': m.no_position,
                'no_throw_item': m.no_throw_item,
                'no_drop_player': m.no_drop_monster,
                'no_drop_monster': m.no_drop_monster,
                'no_names': m.no_names,
                'fight': m.fight,
                'fire': m.fight,
                'fire_damage': m.fire_damage,
                'lightning': m.lightning,
                'lightning_damage': m.lightning_damage,
                'map_dark_light': m.map_dark_light,
                'mine_index': m.mine_index,
                'no_mount': m.no_mount,
                'need_bridle': m.need_bridle,
                'no_fight': m.no_fight,
                'music': m.music
            } for m in self.maps
        ]
        maps_path = os.path.join(output_path, 'maps.json')
        with open(maps_path, 'w', encoding='utf-8') as f:
            json.dump(maps_data, f, ensure_ascii=False, indent=2)

        # 保存怪物信息
        monsters_data = [
            {
                'index': m.index,
                'name': m.name,
                'image': m.image,
                'ai': m.ai,
                'effect': m.effect,
                'level': m.level,
                'view_range': m.view_range,
                'cool_eye': m.cool_eye,
                'stats': {stat.name: m.stats[stat] for stat in Stat},
                'drops': [
                    {
                        'chance': d.chance,
                        'gold': d.gold,
                        'type': d.type,
                        'quest_required': d.quest_required
                    } for d in m.drops
                ],
                'can_tame': m.can_tame,
                'can_push': m.can_push,
                'auto_rev': m.auto_rev,
                'undead': m.undead,
                'has_spawn_script': m.has_spawn_script,
                'has_die_script': m.has_die_script,
                'attack_speed': m.attack_speed,
                'move_speed': m.move_speed,
                'experience': m.experience,
                'light': m.light,
                'drop_path': m.drop_path
            } for m in self.monsters
        ]
        monsters_path = os.path.join(output_path, 'monsters.json')
        with open(monsters_path, 'w', encoding='utf-8') as f:
            json.dump(monsters_data, f, ensure_ascii=False, indent=2)

        # 保存NPC信息
        npcs_data = [
            {
                'index': n.index,
                'name': n.name,
                'file_name': n.file_name,
                'map_index': n.map_index,
                'location': {'x': n.location.x, 'y': n.location.y},
                'rate': n.rate,
                'image': n.image,
                'time_visible': n.time_visible,
                'hour_start': n.hour_start,
                'minute_start': n.minute_start,
                'hour_end': n.hour_end,
                'minute_end': n.minute_end,
                'min_lev': n.min_lev,
                'max_lev': n.max_lev,
                'day_of_week': n.day_of_week,
                'class_required': n.class_required,
                'sabuk': n.sabuk,
                'flag_needed': n.flag_needed,
                'conquest': n.conquest,
                'show_on_big_map': n.show_on_big_map,
                'big_map_icon': n.big_map_icon,
                'can_teleport_to': n.can_teleport_to,
                'conquest_visible': n.conquest_visible,
                'collect_quest_indexes': n.collect_quest_indexes,
                'finish_quest_indexes': n.finish_quest_indexes
            } for n in self.npcs
        ]
        npcs_path = os.path.join(output_path, 'npcs.json')
        with open(npcs_path, 'w', encoding='utf-8') as f:
            json.dump(npcs_data, f, ensure_ascii=False, indent=2)

        # 保存任务信息
        quests_data = [
            {
                'index': q.index,
                'name': q.name,
                'group': q.group,
                'file_name': q.file_name,
                'required_min_level': q.required_min_level,
                'required_max_level': q.required_max_level,
                'required_quest': q.required_quest,
                'required_class': q.required_class.name,
                'type': q.type.name,
                'goto_message': q.goto_message,
                'kill_message': q.kill_message,
                'item_message': q.item_message,
                'flag_message': q.flag_message,
                'time_limit_in_seconds': q.time_limit_in_seconds,
                'description': q.description,
                'task_description': q.task_description,
                'return_description': q.return_description,
                'completion_description': q.completion_description,
                'carry_items': [
                    {
                        'item': {'index': t.item.index, 'name': t.item.name},
                        'count': t.count,
                        'message': t.message
                    } for t in q.carry_items
                ],
                'kill_tasks': [
                    {
                        'monster': {'index': t.monster.index, 'name': t.monster.name},
                        'count': t.count,
                        'message': t.message
                    } for t in q.kill_tasks
                ],
                'item_tasks': [
                    {
                        'item': {'index': t.item.index, 'name': t.item.name},
                        'count': t.count,
                        'message': t.message
                    } for t in q.item_tasks
                ],
                'flag_tasks': [
                    {
                        'number': t.number,
                        'message': t.message
                    } for t in q.flag_tasks
                ],
                'gold_reward': q.gold_reward,
                'exp_reward': q.exp_reward,
                'credit_reward': q.credit_reward,
                'fixed_rewards': [
                    {
                        'item': {'index': r.item.index, 'name': r.item.name},
                        'count': r.count
                    } for r in q.fixed_rewards
                ],
                'select_rewards': [
                    {
                        'item': {'index': r.item.index, 'name': r.item.name},
                        'count': r.count
                    } for r in q.select_rewards
                ]
            } for q in self.quests
        ]
        quests_path = os.path.join(output_path, 'quests.json')
        with open(quests_path, 'w', encoding='utf-8') as f:
            json.dump(quests_data, f, ensure_ascii=False, indent=2)

        # 保存物品信息
        items_data = [
            {
                'index': i.index,
                'name': i.name,
                'type': i.type.name,
                'grade': i.grade.name,
                'required_type': i.required_type.name,
                'required_class': i.required_class.name,
                'required_gender': i.required_gender.name,
                'set': i.set.name,
                'shape': i.shape,
                'weight': i.weight,
                'light': i.light,
                'required_amount': i.required_amount,
                'image': i.image,
                'durability': i.durability,
                'stack_size': i.stack_size,
                'price': i.price,
                'start_item': i.start_item,
                'effect': i.effect,
                'need_identify': i.need_identify,
                'show_group_pickup': i.show_group_pickup,
                'global_drop_notify': i.global_drop_notify,
                'class_based': i.class_based,
                'level_based': i.level_based,
                'can_mine': i.can_mine,
                'can_fast_run': i.can_fast_run,
                'can_awakening': i.can_awakening,
                'bind': i.bind.name,
                'unique': i.unique.name,
                'random_stats_id': i.random_stats_id,
                'random_stats': i.random_stats,
                'tool_tip': i.tool_tip,
                'slots': i.slots,
                'stats': {stat.name: i.stats[stat] for stat in Stat}
            } for i in self.items
        ]
        items_path = os.path.join(output_path, 'items.json')
        with open(items_path, 'w', encoding='utf-8') as f:
            json.dump(items_data, f, ensure_ascii=False, indent=2)

        # 保存龙信息
        dragons_data = [
            {
                'enabled': d.enabled,
                'map_file_name': d.map_file_name,
                'monster_name': d.monster_name,
                'body_name': d.body_name,
                'location': {'x': d.location.x, 'y': d.location.y},
                'drop_area_top': {'x': d.drop_area_top.x, 'y': d.drop_area_top.y},
                'drop_area_bottom': {'x': d.drop_area_bottom.x, 'y': d.drop_area_bottom.y},
                'level': d.level,
                'experience': d.experience,
                'exps': d.exps,
                'drops': [
                    [
                        {
                            'chance': drop.chance,
                            'item': {'index': drop.item.index, 'name': drop.item.name} if drop.item else None,
                            'gold': drop.gold,
                            'level': drop.level
                        } for drop in level_drops
                    ] for level_drops in d.drops
                ]
            } for d in self.dragons
        ]
        dragons_path = os.path.join(output_path, 'dragons.json')
        with open(dragons_path, 'w', encoding='utf-8') as f:
            json.dump(dragons_data, f, ensure_ascii=False, indent=2)

        # 保存征服信息
        conquests_data = [
            {
                'index': c.index,
                'full_map': c.full_map,
                'location': {'x': c.location.x, 'y': c.location.y},
                'size': c.size,
                'name': c.name,
                'map_index': c.map_index,
                'palace_index': c.palace_index,
                'guard_index': c.guard_index,
                'gate_index': c.gate_index,
                'wall_index': c.wall_index,
                'siege_index': c.siege_index,
                'flag_index': c.flag_index,
                'start_hour': c.start_hour,
                'war_length': c.war_length,
                'type': c.type.name,
                'game': c.game.name,
                'monday': c.monday,
                'tuesday': c.tuesday,
                'wednesday': c.wednesday,
                'thursday': c.thursday,
                'friday': c.friday,
                'saturday': c.saturday,
                'sunday': c.sunday,
                'king_location': {'x': c.king_location.x, 'y': c.king_location.y},
                'king_size': c.king_size,
                'control_point_index': c.control_point_index,
                'extra_maps': c.extra_maps,
                'conquest_guards': [
                    {
                        'index': g.index,
                        'location': {'x': g.location.x, 'y': g.location.y},
                        'mob_index': g.mob_index,
                        'name': g.name,
                        'repair_cost': g.repair_cost
                    } for g in c.conquest_guards
                ],
                'conquest_gates': [
                    {
                        'index': g.index,
                        'location': {'x': g.location.x, 'y': g.location.y},
                        'mob_index': g.mob_index,
                        'name': g.name,
                        'repair_cost': g.repair_cost
                    } for g in c.conquest_gates
                ],
                'conquest_walls': [
                    {
                        'index': w.index,
                        'location': {'x': w.location.x, 'y': w.location.y},
                        'mob_index': w.mob_index,
                        'name': w.name,
                        'repair_cost': w.repair_cost
                    } for w in c.conquest_walls
                ],
                'conquest_sieges': [
                    {
                        'index': s.index,
                        'location': {'x': s.location.x, 'y': s.location.y},
                        'mob_index': s.mob_index,
                        'name': s.name,
                        'repair_cost': s.repair_cost
                    } for s in c.conquest_sieges
                ],
                'conquest_flags': [
                    {
                        'index': f.index,
                        'location': {'x': f.location.x, 'y': f.location.y},
                        'name': f.name,
                        'file_name': f.file_name
                    } for f in c.conquest_flags
                ],
                'control_points': [
                    {
                        'index': p.index,
                        'location': {'x': p.location.x, 'y': p.location.y},
                        'name': p.name,
                        'file_name': p.file_name
                    } for p in c.control_points
                ]
            } for c in self.conquests
        ]
        conquests_path = os.path.join(output_path, 'conquests.json')
        with open(conquests_path, 'w', encoding='utf-8') as f:
            json.dump(conquests_data, f, ensure_ascii=False, indent=2)

        # 保存刷新计时器信息
        if hasattr(self, 'respawn_timer') and self.respawn_timer:
            respawn_timer_data = {
                'base_spawn_rate': self.respawn_timer.base_spawn_rate,
                'current_tick_counter': self.respawn_timer.current_tick_counter,
                'last_tick': self.respawn_timer.last_tick,
                'last_user_count': self.respawn_timer.last_user_count,
                'current_delay': self.respawn_timer.current_delay,
                'respawn_options': [
                    {
                        'user_count': option.user_count,
                        'delay_loss': option.delay_loss
                    } for option in self.respawn_timer.respawn_options
                ]
            }
            respawn_timer_path = os.path.join(output_path, 'respawn_timer.json')
            with open(respawn_timer_path, 'w', encoding='utf-8') as f:
                json.dump(respawn_timer_data, f, ensure_ascii=False, indent=2)

    def read_dragon_info(self, f):
        """读取龙信息"""
        try:
            dragon = DragonInfo()
            
            # 读取基本信息
            print(f"\n开始读取龙信息，当前位置: {f.tell()}")
            dragon.enabled = BinaryReader.read_bool(f)
            print(f"读取启用状态: {dragon.enabled}")
            
            dragon.map_file_name = BinaryReader.read_string(f)
            print(f"读取地图文件名: {dragon.map_file_name}")
            
            dragon.monster_name = BinaryReader.read_string(f)
            print(f"读取怪物名称: {dragon.monster_name}")
            
            dragon.body_name = BinaryReader.read_string(f)
            print(f"读取身体名称: {dragon.body_name}")
            
            # 读取位置信息
            dragon.location = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取位置: ({dragon.location.x}, {dragon.location.y})")
            
            dragon.drop_area_top = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取掉落区域顶部: ({dragon.drop_area_top.x}, {dragon.drop_area_top.y})")
            
            dragon.drop_area_bottom = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取掉落区域底部: ({dragon.drop_area_bottom.x}, {dragon.drop_area_bottom.y})")
            
            # 读取经验值
            for i in range(len(dragon.exps)):
                dragon.exps[i] = BinaryReader.read_int64(f)
                print(f"读取等级 {i+1} 经验值: {dragon.exps[i]}")
            
            # 加载掉落信息
            self.load_dragon_drops(dragon)
            
            return dragon
        except Exception as e:
            print(f"读取龙信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def load_dragon_drops(self, dragon):
        """加载龙掉落信息"""
        # 清空所有掉落列表
        for level_drops in dragon.drops:
            level_drops.clear()
            
        # 确保掉落文件目录存在
        drop_path = os.path.join(os.path.dirname(self.db_path), Settings.DropPath)
        if not os.path.exists(drop_path):
            print(f"掉落文件目录不存在: {drop_path}")
            return
            
        file_path = os.path.join(drop_path, "DragonItem.txt")
        if not os.path.exists(file_path):
            print(f"龙掉落文件不存在: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue
                        
                    drop = self.parse_dragon_drop(line)
                    if drop and 0 < drop.level <= len(dragon.drops):
                        dragon.drops[drop.level - 1].append(drop)
                        
            # 对每个等级的掉落列表进行排序
            for level_drops in dragon.drops:
                level_drops.sort(key=lambda d: (d.gold == 0, d.item.type if d.item else 0))
                
        except Exception as e:
            print(f"加载龙掉落信息时出错: {str(e)}")
            raise

    def parse_dragon_drop(self, line):
        """解析龙掉落信息"""
        parts = line.split()
        if len(parts) < 3:
            return None
            
        try:
            drop = DragonDropInfo()
            drop.chance = int(parts[0][2:])  # 跳过前两个字符
            
            if parts[1].lower() == "gold":
                if len(parts) < 4:
                    return None
                drop.gold = int(parts[2])
                drop.level = int(parts[3])
            else:
                drop.item = self.get_item_info(parts[1])
                if not drop.item:
                    return None
                drop.level = int(parts[2])
                
            return drop
        except (ValueError, IndexError):
            return None


    def read_magic_info(self, f):
        """读取魔法信息"""
        magic = MagicInfo()
        
        # 读取基本信息
        magic.name = self.read_string(f)
        try:
            magic.spell = Spell(self.read_byte(f))
        except ValueError:
            magic.spell = Spell.None_  # 如果值不在枚举中，设置为None
        magic.base_cost = self.read_byte(f)
        magic.level_cost = self.read_byte(f)
        magic.icon = self.read_byte(f)
        magic.level1 = self.read_byte(f)
        magic.level2 = self.read_byte(f)
        magic.level3 = self.read_byte(f)
        magic.need1 = self.read_uint16(f)
        magic.need2 = self.read_uint16(f)
        magic.need3 = self.read_uint16(f)
        magic.delay_base = self.read_uint32(f)
        magic.delay_reduction = self.read_uint32(f)
        magic.power_base = self.read_uint16(f)
        magic.power_bonus = self.read_uint16(f)
        magic.mpower_base = self.read_uint16(f)
        magic.mpower_bonus = self.read_uint16(f)
        
        # 版本相关的读取
        if self.version > 66:
            magic.range = self.read_byte(f)
        if self.version > 70:
            magic.multiplier_base = self.read_float(f)
            magic.multiplier_bonus = self.read_float(f)
            
        return magic

    def read_float(self, f):
        """读取单精度浮点数，对应C#的ReadSingle"""
        try:
            data = f.read(4)
            if len(data) != 4:
                raise ValueError("读取float时数据长度不足4字节")
            return struct.unpack('<f', data)[0]  # 使用小端序，对应C#的BinaryReader
        except Exception as e:
            print(f"读取float时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            return 0.0  # 出错时返回0.0，避免浮点数错误

    def read_conquest_info(self, f):
        """读取征服信息"""
        try:
            conquest = ConquestInfo()
            
            # 读取基本信息
            print(f"\n开始读取征服信息，当前位置: {f.tell()}")
            conquest.index = self.read_int32(f)
            print(f"读取索引: {conquest.index}")
            
            if self.version > 73:
                conquest.full_map = self.read_bool(f)
                print(f"读取全地图: {conquest.full_map}")
            
            conquest.location = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取位置: ({conquest.location.x}, {conquest.location.y})")
            
            conquest.size = self.read_uint16(f)
            print(f"读取大小: {conquest.size}")
            
            conquest.name = self.read_string(f)
            print(f"读取名称: {conquest.name}")
            
            conquest.map_index = self.read_int32(f)
            print(f"读取地图索引: {conquest.map_index}")
            
            conquest.palace_index = self.read_int32(f)
            print(f"读取宫殿索引: {conquest.palace_index}")
            
            conquest.guard_index = self.read_int32(f)
            print(f"读取守卫索引: {conquest.guard_index}")
            
            conquest.gate_index = self.read_int32(f)
            print(f"读取城门索引: {conquest.gate_index}")
            
            conquest.wall_index = self.read_int32(f)
            print(f"读取城墙索引: {conquest.wall_index}")
            
            conquest.siege_index = self.read_int32(f)
            print(f"读取攻城索引: {conquest.siege_index}")
            
            if self.version > 72:
                conquest.flag_index = self.read_int32(f)
                print(f"读取旗帜索引: {conquest.flag_index}")
            
            # 读取守卫列表
            guard_count = self.read_int32(f)
            print(f"读取守卫数量: {guard_count}")
            for i in range(guard_count):
                guard = ConquestArcherInfo()
                guard.index = self.read_int32(f)
                guard.location = Point(
                    x=self.read_int32(f),
                    y=self.read_int32(f)
                )
                guard.mob_index = self.read_int32(f)
                guard.name = self.read_string(f)
                guard.repair_cost = self.read_uint32(f)
                conquest.conquest_guards.append(guard)
            
            # 读取额外地图列表
            map_count = self.read_int32(f)
            print(f"读取额外地图数量: {map_count}")
            for i in range(map_count):
                map_index = self.read_int32(f)
                conquest.extra_maps.append(map_index)
            
            # 读取城门列表
            gate_count = self.read_int32(f)
            print(f"读取城门数量: {gate_count}")
            for i in range(gate_count):
                gate = ConquestGateInfo()
                gate.index = self.read_int32(f)
                gate.location = Point(
                    x=self.read_int32(f),
                    y=self.read_int32(f)
                )
                gate.mob_index = self.read_int32(f)
                gate.name = self.read_string(f)
                if self.version <= 84:
                    gate.repair_cost = self.read_uint32(f)
                else:
                    gate.repair_cost = self.read_int32(f)
                conquest.conquest_gates.append(gate)
            
            # 读取城墙列表
            wall_count = self.read_int32(f)
            print(f"读取城墙数量: {wall_count}")
            for i in range(wall_count):
                wall = ConquestWallInfo()
                wall.index = self.read_int32(f)
                wall.location = Point(
                    x=self.read_int32(f),
                    y=self.read_int32(f)
                )
                wall.mob_index = self.read_int32(f)
                wall.name = self.read_string(f)
                if self.version <= 84:
                    wall.repair_cost = self.read_uint32(f)
                else:
                    wall.repair_cost = self.read_int32(f)
                conquest.conquest_walls.append(wall)
            
            # 读取攻城列表
            siege_count = self.read_int32(f)
            print(f"读取攻城数量: {siege_count}")
            for i in range(siege_count):
                siege = ConquestSiegeInfo()
                siege.index = self.read_int32(f)
                siege.location = Point(
                    x=self.read_int32(f),
                    y=self.read_int32(f)
                )
                siege.mob_index = self.read_int32(f)
                siege.name = self.read_string(f)
                if self.version <= 84:
                    siege.repair_cost = self.read_uint32(f)
                else:
                    siege.repair_cost = self.read_int32(f)
                conquest.conquest_sieges.append(siege)
            
            # 读取旗帜列表
            if self.version > 72:
                flag_count = self.read_int32(f)
                print(f"读取旗帜数量: {flag_count}")
                for i in range(flag_count):
                    flag = ConquestFlagInfo()
                    flag.index = self.read_int32(f)
                    flag.location = Point(
                        x=self.read_int32(f),
                        y=self.read_int32(f)
                    )
                    flag.name = self.read_string(f)
                    flag.file_name = self.read_string(f)
                    conquest.conquest_flags.append(flag)
            
            # 读取其他信息
            conquest.start_hour = self.read_byte(f)
            print(f"读取开始时间: {conquest.start_hour}")
            
            conquest.war_length = self.read_int32(f)
            print(f"读取战争时长: {conquest.war_length}")
            
            conquest.type = ConquestType(self.read_byte(f))
            print(f"读取类型: {conquest.type}")
            
            conquest.game = ConquestGame(self.read_byte(f))
            print(f"读取游戏模式: {conquest.game}")
            
            conquest.monday = self.read_bool(f)
            conquest.tuesday = self.read_bool(f)
            conquest.wednesday = self.read_bool(f)
            conquest.thursday = self.read_bool(f)
            conquest.friday = self.read_bool(f)
            conquest.saturday = self.read_bool(f)
            conquest.sunday = self.read_bool(f)
            print(f"读取星期设置: {conquest.monday}, {conquest.tuesday}, {conquest.wednesday}, {conquest.thursday}, {conquest.friday}, {conquest.saturday}, {conquest.sunday}")
            
            conquest.king_location = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取国王位置: ({conquest.king_location.x}, {conquest.king_location.y})")
            
            conquest.king_size = self.read_uint16(f)
            print(f"读取国王区域大小: {conquest.king_size}")
            
            if self.version > 74:
                conquest.control_point_index = self.read_int32(f)
                print(f"读取控制点索引: {conquest.control_point_index}")
                
                control_point_count = self.read_int32(f)
                print(f"读取控制点数量: {control_point_count}")
                for i in range(control_point_count):
                    point = ConquestFlagInfo()
                    point.index = self.read_int32(f)
                    point.location = Point(
                        x=self.read_int32(f),
                        y=self.read_int32(f)
                    )
                    point.name = self.read_string(f)
                    point.file_name = self.read_string(f)
                    conquest.control_points.append(point)
            
            return conquest
        except Exception as e:
            print(f"读取征服信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def read_respawn_timer(self, f):
        """读取刷新计时器信息"""
        try:
            respawn = RespawnTimer()
            
            # 读取基本信息
            print(f"\n开始读取刷新计时器信息，当前位置: {f.tell()}")
            respawn.base_spawn_rate = self.read_byte(f)
            print(f"读取基础刷新率: {respawn.base_spawn_rate}")
            
            respawn.current_tick_counter = self.read_uint64(f)
            print(f"读取当前刷新计数器: {respawn.current_tick_counter}")
            
            # 读取刷新选项列表
            option_count = self.read_int32(f)
            print(f"读取刷新选项数量: {option_count}")
            
            for i in range(option_count):
                option = RespawnTickOption()
                option.user_count = self.read_int32(f)
                option.delay_loss = self.read_float(f)
                respawn.respawn_options.append(option)
                print(f"读取刷新选项 {i+1}/{option_count}:")
                print(f"  用户数量: {option.user_count}")
                print(f"  延迟损失: {option.delay_loss}")
            
            # 计算当前延迟
            respawn.current_delay = int(round(respawn.base_spawn_rate * 60000))
            print(f"计算当前延迟: {respawn.current_delay}")
            
            return respawn
        except Exception as e:
            print(f"读取刷新计时器信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

@dataclass
class GameShopItem:
    item_index: int = 0
    g_index: int = 0
    gold_price: int = 0
    credit_price: int = 0
    count: int = 1
    class_name: str = ""
    category: str = ""
    stock: int = 0
    i_stock: bool = False
    deal: bool = False
    top_item: bool = False
    date: int = 0  # 使用int存储DateTime.ToBinary
    can_buy_gold: bool = False
    can_buy_credit: bool = False

@dataclass
class ConquestArcherInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0

@dataclass
class ConquestGateInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0

@dataclass
class ConquestWallInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0

@dataclass
class ConquestSiegeInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0

@dataclass
class ConquestFlagInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    name: str = ""
    file_name: str = ""

class ConquestType(Enum):
    Request = 0
    AutoWar = 1
    Forced = 2

class ConquestGame(Enum):
    CapturePalace = 0  # 占领宫殿模式
    KingOfHill = 1    # 山丘之王模式
    Random = 2        # 随机模式
    Classic = 3       # 经典模式
    ControlPoints = 4 # 控制点模式

@dataclass
class ConquestInfo:
    index: int = 0
    full_map: bool = False
    location: Point = field(default_factory=Point)
    size: int = 0
    name: str = ""
    map_index: int = 0
    palace_index: int = 0
    guard_index: int = 0
    gate_index: int = 0
    wall_index: int = 0
    siege_index: int = 0
    flag_index: int = 0
    start_hour: int = 0
    war_length: int = 60
    type: ConquestType = ConquestType.Request
    game: ConquestGame = ConquestGame.CapturePalace
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
    saturday: bool = False
    sunday: bool = False
    king_location: Point = field(default_factory=Point)
    king_size: int = 0
    control_point_index: int = 0
    
    extra_maps: List[int] = field(default_factory=list)
    conquest_guards: List[ConquestArcherInfo] = field(default_factory=list)
    conquest_gates: List[ConquestGateInfo] = field(default_factory=list)
    conquest_walls: List[ConquestWallInfo] = field(default_factory=list)
    conquest_sieges: List[ConquestSiegeInfo] = field(default_factory=list)
    conquest_flags: List[ConquestFlagInfo] = field(default_factory=list)
    control_points: List[ConquestFlagInfo] = field(default_factory=list)

@dataclass
class RespawnTickOption:
    user_count: int = 1
    delay_loss: float = 1.0

@dataclass
class RespawnTimer:
    base_spawn_rate: int = 20  # 基础刷新率（分钟）
    current_tick_counter: int = 0  # 当前刷新计数器
    last_tick: int = 0  # 上次刷新时间
    last_user_count: int = 0  # 上次用户数量
    current_delay: int = 0  # 当前延迟
    respawn_options: List[RespawnTickOption] = field(default_factory=list)

 

def main():
    # 使用相对路径
    db_path = os.path.join("../Jev", "Server.MirDB")
    parser = MirDBParser(db_path)
    
    if parser.load():
        print("\n保存解析结果到JSON文件...")
        parser.save_to_json('data')
        print("完成!")

if __name__ == "__main__":
    main() 