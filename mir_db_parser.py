import struct
import os
import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import re

class Settings:
    """设置类，用于定义各种路径"""
    QuestPath = "Quests"  # 任务文件所在目录
    DropPath = "Drops"    # 掉落文件所在目录

class Monster(Enum):
    # 这里需要添加所有怪物类型的枚举值
    pass

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
class Point:
    x: int = 0
    y: int = 0

@dataclass
class MovementInfo:
    map_index: int = 0
    source: Point = field(default_factory=Point)
    destination: Point = field(default_factory=Point)
    need_hole: bool = False
    need_move: bool = False
    conquest_index: int = 0
    show_on_big_map: bool = False
    icon: int = 0

@dataclass
class RespawnInfo:
    monster_index: int = 0
    location: Point = field(default_factory=Point)
    count: int = 0  # 应该是uint16
    spread: int = 0  # 应该是uint16
    delay: int = 0   # 应该是uint16
    direction: int = 0  # 应该是byte
    route_path: str = ""
    random_delay: int = 0  # 应该是uint16
    respawn_index: int = 0
    save_respawn_time: bool = False
    respawn_ticks: int = 0  # 应该是uint16

@dataclass
class NPCInfo:
    index: int = 0
    file_name: str = ""
    name: str = ""
    map_index: int = 0
    location: Point = field(default_factory=Point)
    rate: int = 100
    image: int = 0
    time_visible: bool = False
    hour_start: int = 0
    minute_start: int = 0
    hour_end: int = 0
    minute_end: int = 1
    min_lev: int = 0
    max_lev: int = 0
    day_of_week: str = ""
    class_required: str = ""
    sabuk: bool = False
    flag_needed: int = 0
    conquest: int = 0
    show_on_big_map: bool = False
    big_map_icon: int = 0
    can_teleport_to: bool = False
    conquest_visible: bool = True
    collect_quest_indexes: List[int] = field(default_factory=list)
    finish_quest_indexes: List[int] = field(default_factory=list)

@dataclass
class MineZone:
    location: Point = field(default_factory=Point)
    size: int = 0
    mine_index: int = 0

@dataclass
class SafeZoneInfo:
    info: Optional['MapInfo'] = None
    location: Point = field(default_factory=Point)
    size: int = 0  # 应该是uint16
    start_point: bool = False

@dataclass
class MapInfo:
    def __init__(self):
        self.index = 0
        self.filename = ""
        self.title = ""
        self.mini_map = 0
        self.big_map = 0
        self.music = 0
        self.light = 0
        self.map_dark_light = 0
        self.mine_index = 0
        self.gt_index = 0
        
        self.no_teleport = False
        self.no_reconnect = False
        self.no_random = False
        self.no_escape = False
        self.no_recall = False
        self.no_drug = False
        self.no_position = False
        self.no_fight = False
        self.no_throw_item = False
        self.no_drop_player = False
        self.no_drop_monster = False
        self.no_names = False
        self.no_mount = False
        self.need_bridle = False
        self.fight = False
        self.need_hole = False
        self.fire = False
        self.lightning = False
        self.no_town_teleport = False
        self.no_reincarnation = False
        self.gt = False
        
        self.no_reconnect_map = ""
        self.fire_damage = 0
        self.lightning_damage = 0
        
        self.safe_zones = []
        self.movements = []
        self.respawns = []
        self.npcs = []
        self.mine_zones = []
        self.active_coords = []
        self.weather_particles = 0

    def validate(self):
        """验证地图信息的有效性"""
        if self.index < 0:
            raise ValueError(f"无效的地图索引: {self.index}")
        if not self.filename:
            raise ValueError("地图文件名不能为空")
        if not self.title:
            raise ValueError("地图标题不能为空")
        if self.mini_map < 0:
            raise ValueError(f"无效的小地图索引: {self.mini_map}")
        if self.big_map < 0:
            raise ValueError(f"无效的大地图索引: {self.big_map}")
        if self.light < 0 or self.light > 4:
            raise ValueError(f"无效的光照设置: {self.light}")
        if self.fire_damage < 0:
            raise ValueError(f"无效的火焰伤害: {self.fire_damage}")
        if self.lightning_damage < 0:
            raise ValueError(f"无效的闪电伤害: {self.lightning_damage}")
        if self.map_dark_light < 0:
            raise ValueError(f"无效的地图暗光设置: {self.map_dark_light}")
        if self.mine_index < 0:
            raise ValueError(f"无效的矿区索引: {self.mine_index}")
        if self.music < 0:
            raise ValueError(f"无效的音乐索引: {self.music}")
        if self.weather_particles < 0 or self.weather_particles > 3:
            raise ValueError(f"无效的天气设置: {self.weather_particles}")
        if self.gt_index < 0:
            raise ValueError(f"无效的GT索引: {self.gt_index}")

@dataclass
class MonsterInfo:
    index: int = 0
    name: str = ""
    image: int = 0
    ai: int = 0
    effect: int = 0
    level: int = 0
    view_range: int = 7
    cool_eye: int = 0
    stats: Stats = None
    drops: List[DropInfo] = None
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

    def __post_init__(self):
        if self.stats is None:
            self.stats = Stats()
        if self.drops is None:
            self.drops = []

    def read_from_file(self, f, version, custom_version):
        self.index = self.read_int32(f)
        self.name = self.read_string(f)
        self.image = self.read_uint16(f)
        self.ai = self.read_byte(f)
        self.effect = self.read_byte(f)

        if version < 62:
            self.level = self.read_byte(f)
        else:
            self.level = self.read_uint16(f)

        self.view_range = self.read_byte(f)
        self.cool_eye = self.read_byte(f)

        if version > 84:
            # 读取完整的状态信息
            for stat in Stat:
                self.stats[stat] = self.read_int32(f)
        else:
            # 旧版本的状态信息读取
            self.stats[Stat.HP] = self.read_uint32(f)
            
            if version < 62:
                self.stats[Stat.MinAC] = self.read_byte(f)
                self.stats[Stat.MaxAC] = self.read_byte(f)
                self.stats[Stat.MinMAC] = self.read_byte(f)
                self.stats[Stat.MaxMAC] = self.read_byte(f)
                self.stats[Stat.MinDC] = self.read_byte(f)
                self.stats[Stat.MaxDC] = self.read_byte(f)
                self.stats[Stat.MinMC] = self.read_byte(f)
                self.stats[Stat.MaxMC] = self.read_byte(f)
                self.stats[Stat.MinSC] = self.read_byte(f)
                self.stats[Stat.MaxSC] = self.read_byte(f)
            else:
                self.stats[Stat.MinAC] = self.read_uint16(f)
                self.stats[Stat.MaxAC] = self.read_uint16(f)
                self.stats[Stat.MinMAC] = self.read_uint16(f)
                self.stats[Stat.MaxMAC] = self.read_uint16(f)
                self.stats[Stat.MinDC] = self.read_uint16(f)
                self.stats[Stat.MaxDC] = self.read_uint16(f)
                self.stats[Stat.MinMC] = self.read_uint16(f)
                self.stats[Stat.MaxMC] = self.read_uint16(f)
                self.stats[Stat.MinSC] = self.read_uint16(f)
                self.stats[Stat.MaxSC] = self.read_uint16(f)

            if version <= 84:
                self.stats[Stat.Accuracy] = self.read_byte(f)
                self.stats[Stat.Agility] = self.read_byte(f)

        self.light = self.read_byte(f)
        self.attack_speed = self.read_uint16(f)
        self.move_speed = self.read_uint16(f)
        self.experience = self.read_uint32(f)

        self.can_push = self.read_bool(f)
        self.can_tame = self.read_bool(f)

        if version >= 18:
            self.auto_rev = self.read_bool(f)
            self.undead = self.read_bool(f)

        if version >= 89:
            self.drop_path = self.read_string(f)

        return self

class ItemType(Enum):
    Nothing = 0
    Weapon = 1
    Armour = 2
    Helmet = 3
    Necklace = 4
    Bracelet = 5
    Ring = 6
    Amulet = 7
    Belt = 8
    Boots = 9
    Stone = 10
    Torch = 11
    Potion = 12
    Ore = 13
    Meat = 14
    CraftingMaterial = 15
    Scroll = 16
    Gem = 17
    Mount = 18
    Book = 19
    Script = 20
    Reins = 21
    Bells = 22
    Saddle = 23
    Ribbon = 24
    Mask = 25
    Food = 26
    Hook = 27
    Float = 28
    Bait = 29
    Finder = 30
    Reel = 31
    Fish = 32
    Quest = 33
    Awakening = 34
    Pets = 35
    Transform = 36
    Deco = 37

class ItemGrade(Enum):
    None_ = 0
    Common = 1
    Rare = 2
    Legendary = 3
    Mythical = 4

class RequiredType(Enum):
    Level = 0
    MaxAC = 1
    MaxMAC = 2
    MaxDC = 3
    MaxMC = 4
    MaxSC = 5
    MaxLevel = 6
    MinAC = 7
    MinMAC = 8
    MinDC = 9
    MinMC = 10
    MinSC = 11

class RequiredClass(Enum):
    None_ = 0
    Warrior = 1
    Wizard = 2
    Taoist = 3
    Assassin = 4
    Archer = 5

class RequiredGender(Enum):
    None_ = 0
    Male = 1
    Female = 2

class ItemSet(Enum):
    None_ = 0
    Spirit = 1
    Recall = 2
    RedOrchid = 3
    RedFlame = 4
    WhiteGold = 5
    WhiteGoldH = 6
    WhiteGoldL = 7
    WhiteGoldW = 8
    WhiteGoldM = 9
    WhiteGoldT = 10
    WhiteGoldA = 11
    WhiteGoldI = 12
    WhiteGoldS = 13
    WhiteGoldC = 14
    WhiteGoldB = 15
    WhiteGoldD = 16
    WhiteGoldE = 17
    WhiteGoldF = 18
    WhiteGoldG = 19
    WhiteGoldJ = 20
    WhiteGoldK = 21
    WhiteGoldN = 22
    WhiteGoldO = 23
    WhiteGoldP = 24
    WhiteGoldQ = 25
    WhiteGoldR = 26
    WhiteGoldU = 27
    WhiteGoldV = 28
    WhiteGoldX = 29
    WhiteGoldY = 30
    WhiteGoldZ = 31

class BindMode(Enum):
    None_ = 0
    DontDrop = 1
    DontDeathDrop = 2
    DontStore = 4
    DontTrade = 8
    DontRepair = 16
    DontSell = 32
    DontDropRare = 64
    BreakOnDeath = 128
    BindOnEquip = 256
    NoWeddingRing = 4096

class SpecialItemMode(Enum):
    None_ = 0
    Paralize = 1
    Teleport = 2
    ClearRing = 4
    Protection = 8
    Revival = 16
    Muscle = 32
    Flame = 64
    Healing = 128
    Probe = 256
    Skill = 512
    NoDuraLoss = 1024
    Blink = 2048
    Blessing = 4096
    Curse = 8192
    NoDrop = 16384
    NoDeathDrop = 32768
    NoStore = 65536
    NoTrade = 131072
    NoRepair = 262144
    NoSell = 524288
    NoWeddingRing = 1048576

@dataclass
class ItemInfo:
    index: int = 0
    name: str = ""
    type: ItemType = ItemType.Nothing
    grade: ItemGrade = ItemGrade.None_
    required_type: RequiredType = RequiredType.Level
    required_class: RequiredClass = RequiredClass.None_
    required_gender: RequiredGender = RequiredGender.None_
    set: ItemSet = ItemSet.None_
    shape: int = 0
    weight: int = 0
    light: int = 0
    required_amount: int = 0
    image: int = 0
    durability: int = 0
    stack_size: int = 1
    price: int = 0
    start_item: bool = False
    effect: int = 0
    need_identify: bool = False
    show_group_pickup: bool = False
    global_drop_notify: bool = False
    class_based: bool = False
    level_based: bool = False
    can_mine: bool = False
    can_fast_run: bool = False
    can_awakening: bool = False
    bind: BindMode = BindMode.None_
    unique: SpecialItemMode = SpecialItemMode.None_
    random_stats_id: int = 0
    random_stats: Dict = None
    tool_tip: str = ""
    slots: int = 0
    stats: Stats = None

    def __post_init__(self):
        if self.stats is None:
            self.stats = Stats()
        if self.random_stats is None:
            self.random_stats = {}

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
class QuestInfo:
    index: int = 0
    name: str = ""
    group: str = ""
    file_name: str = ""
    required_min_level: int = 0
    required_max_level: int = 0
    required_quest: int = 0
    required_class: RequiredClass = RequiredClass.None_
    type: QuestType = QuestType.General
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
    exps: List[int] = field(default_factory=lambda: [10000 * (i + 1) for i in range(9)])  # 默认9级经验值
    drops: List[List[DragonDropInfo]] = field(default_factory=lambda: [[] for _ in range(10)])  # 默认10级掉落

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
            dragon.enabled = self.read_bool(f)
            print(f"读取启用状态: {dragon.enabled}")
            
            dragon.map_file_name = self.read_string(f)
            print(f"读取地图文件名: {dragon.map_file_name}")
            
            dragon.monster_name = self.read_string(f)
            print(f"读取怪物名称: {dragon.monster_name}")
            
            dragon.body_name = self.read_string(f)
            print(f"读取身体名称: {dragon.body_name}")
            
            # 读取位置信息
            dragon.location = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取位置: ({dragon.location.x}, {dragon.location.y})")
            
            dragon.drop_area_top = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取掉落区域顶部: ({dragon.drop_area_top.x}, {dragon.drop_area_top.y})")
            
            dragon.drop_area_bottom = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取掉落区域底部: ({dragon.drop_area_bottom.x}, {dragon.drop_area_bottom.y})")
            
            # 读取经验值
            for i in range(len(dragon.exps)):
                dragon.exps[i] = self.read_int64(f)
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

    def read_int64(self, f):
        """读取64位整数"""
        try:
            data = f.read(8)
            print(f"读取int64原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<q', data)[0]
        except Exception as e:
            print(f"读取int64时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

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

    def read_point(self, f):
        x = MirDBParser.read_int32(f)
        y = MirDBParser.read_int32(f)
        return Point(x, y)

    def read_safe_zone(self, f):
        """读取安全区信息"""
        try:
            safe_zone = SafeZoneInfo()
            safe_zone.location = self.read_point(f)
            safe_zone.size = self.read_uint16(f)  # 修正为uint16
            safe_zone.start_point = self.read_bool(f)  # 修正为bool
            return safe_zone
        except Exception as e:
            print(f"读取安全区信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def read_respawn_info(self, f, version, custom_version):
        """读取重生点信息"""
        try:
            respawn = RespawnInfo()
            
            # 基本字段
            respawn.monster_index = self.read_int32(f)
            respawn.location = self.read_point(f)
            respawn.count = self.read_uint16(f)  # 使用uint16
            respawn.spread = self.read_uint16(f)  # 使用uint16
            respawn.delay = self.read_uint16(f)   # 使用uint16
            respawn.direction = self.read_byte(f)  # 使用byte
            respawn.route_path = self.read_string(f)
            
            # 版本相关字段
            if version > 67:
                respawn.random_delay = self.read_uint16(f)  # 使用uint16
                respawn.respawn_index = self.read_int32(f)
                respawn.save_respawn_time = self.read_bool(f)
                respawn.respawn_ticks = self.read_uint16(f)  # 使用uint16
            else:
                # 在版本<=67时，respawn_index由Envir自动分配
                # 这里需要从Envir获取，但目前我们无法访问Envir
                # 暂时设置为0，后续需要修改
                respawn.respawn_index = 0
            
            return respawn
        except Exception as e:
            print(f"读取重生点信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def read_movement_info(self, f):
        """读取移动点信息"""
        try:
            movement = MovementInfo()
            movement.map_index = self.read_int32(f)
            movement.source = self.read_point(f)
            movement.destination = self.read_point(f)
            movement.need_hole = self.read_bool(f)
            movement.need_move = self.read_bool(f)
            
            # 版本相关字段
            if self.version >= 69:
                movement.conquest_index = self.read_int32(f)
                
            if self.version >= 95:
                movement.show_on_big_map = self.read_bool(f)
                movement.icon = self.read_int32(f)
                
            return movement
        except Exception as e:
            print(f"读取移动点信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def read_mine_zone(self, f):
        """读取矿区信息"""
        try:
            mine_zone = MineZone()
            mine_zone.location = self.read_point(f)
            mine_zone.size = self.read_int32(f)
            mine_zone.mine_index = self.read_byte(f)
            return mine_zone
        except Exception as e:
            print(f"读取矿区信息时出错: {str(e)}")
            raise

    def read_map_info(self, f):
        """读取地图信息"""
        try:
            map_info = MapInfo()
            
            # 获取当前文件位置，但不移动指针
            current_pos = f.tell()
            print(f"\n开始读取地图信息:")
            print(f"当前位置: {current_pos}")
            
            # 读取基本信息
            try:
                map_info.index = self.read_int32(f)
                print(f"地图索引: {map_info.index}")
                
                map_info.filename = self.read_string(f)
                print(f"文件名: {map_info.filename}")
                
                map_info.title = self.read_string(f)
                print(f"标题: {map_info.title}")
                
                map_info.mini_map = self.read_uint16(f)
                print(f"小地图: {map_info.mini_map}")
                
                map_info.light = self.read_byte(f)
                print(f"光照设置: {map_info.light}")
                
                map_info.big_map = self.read_uint16(f)
                print(f"大地图: {map_info.big_map}")
            except Exception as e:
                print(f"读取基本信息时出错: {str(e)}")
                print(f"当前文件位置: {f.tell()}")
                raise
            
            # 读取安全区
            try:
                safe_zone_count = self.read_int32(f)
                print(f"\n安全区数量: {safe_zone_count}")
                print(f"读取安全区前位置: {f.tell()}")
                
                for i in range(safe_zone_count):
                    safe_zone = self.read_safe_zone(f)
                    safe_zone.info = map_info
                    map_info.safe_zones.append(safe_zone)
                    print(f"读取安全区 {i+1}/{safe_zone_count} 后位置: {f.tell()}")
            except Exception as e:
                print(f"读取安全区信息时出错: {str(e)}")
                print(f"当前文件位置: {f.tell()}")
                raise
            
            # 读取重生点
            try:
                respawn_count = self.read_int32(f)
                print(f"\n重生点数量: {respawn_count}")
                print(f"读取重生点前位置: {f.tell()}")
                
                for i in range(respawn_count):
                    respawn = self.read_respawn_info(f, self.version, self.custom_version)
                    map_info.respawns.append(respawn)
                    print(f"读取重生点 {i+1}/{respawn_count} 后位置: {f.tell()}")
            except Exception as e:
                print(f"读取重生点信息时出错: {str(e)}")
                print(f"当前文件位置: {f.tell()}")
                raise
            
            # 读取移动点
            try:
                movement_count = self.read_int32(f)
                print(f"\n移动点数量: {movement_count}")
                print(f"读取移动点前位置: {f.tell()}")
                
                for i in range(movement_count):
                    movement = self.read_movement_info(f)
                    map_info.movements.append(movement)
                    print(f"读取移动点 {i+1}/{movement_count} 后位置: {f.tell()}")
            except Exception as e:
                print(f"读取移动点信息时出错: {str(e)}")
                print(f"当前文件位置: {f.tell()}")
                raise
            
            # 读取布尔属性
            try:
                map_info.no_teleport = self.read_bool(f)
                map_info.no_reconnect = self.read_bool(f)
                map_info.no_reconnect_map = self.read_string(f)
                map_info.no_random = self.read_bool(f)
                map_info.no_escape = self.read_bool(f)
                map_info.no_recall = self.read_bool(f)
                map_info.no_drug = self.read_bool(f)
                map_info.no_position = self.read_bool(f)
                map_info.no_throw_item = self.read_bool(f)
                map_info.no_drop_player = self.read_bool(f)
                map_info.no_drop_monster = self.read_bool(f)
                map_info.no_names = self.read_bool(f)
                map_info.fight = self.read_bool(f)
                map_info.fire = self.read_bool(f)
                map_info.fire_damage = self.read_int32(f)
                map_info.lightning = self.read_bool(f)
                map_info.lightning_damage = self.read_int32(f)
                map_info.map_dark_light = self.read_byte(f)
                print("布尔属性读取完成")
            except Exception as e:
                print(f"读取布尔属性时出错: {str(e)}")
                raise
            
            # 读取矿区
            try:
                mine_zone_count = self.read_int32(f)
                print(f"读取矿区数量: {mine_zone_count}")
                if mine_zone_count > 1000:  # 添加合理性检查
                    raise ValueError(f"矿区数量异常: {mine_zone_count}")
                for i in range(mine_zone_count):
                    try:
                        mine_zone = self.read_mine_zone(f)
                        map_info.mine_zones.append(mine_zone)
                        print(f"读取矿区 {i+1}/{mine_zone_count}")
                    except Exception as e:
                        print(f"读取矿区 {i+1} 时出错: {str(e)}")
                        raise
            except Exception as e:
                print(f"读取矿区信息时出错: {str(e)}")
                raise
            
            try:
                map_info.mine_index = self.read_byte(f)
                map_info.no_mount = self.read_bool(f)
                map_info.need_bridle = self.read_bool(f)
                map_info.no_fight = self.read_bool(f)
                map_info.music = self.read_uint16(f)
                print("其他属性读取完成")
            except Exception as e:
                print(f"读取其他属性时出错: {str(e)}")
                raise
            
            # 版本相关的额外属性
            try:
                if self.version >= 78:
                    map_info.no_town_teleport = self.read_bool(f)
                    
                if self.version >= 79:
                    map_info.no_reincarnation = self.read_bool(f)
                    
                if self.version >= 110:
                    map_info.weather_particles = self.read_uint16(f)
                    
                if self.version >= 111:
                    map_info.gt = self.read_bool(f)
                    map_info.gt_index = self.read_byte(f)
                print("版本相关属性读取完成")
            except Exception as e:
                print(f"读取版本相关属性时出错: {str(e)}")
                raise
            
            return map_info
        
        except Exception as e:
            print(f"读取地图信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def validate_map_info(self, map_info):
        if map_info.index < 0:
            raise ValueError(f"无效的地图索引: {map_info.index}")
        if not map_info.filename:
            raise ValueError("地图文件名不能为空")
        if not map_info.title:
            raise ValueError("地图标题不能为空")
        if map_info.mini_map < 0:
            raise ValueError(f"无效的小地图索引: {map_info.mini_map}")
        if map_info.big_map < 0:
            raise ValueError(f"无效的大地图索引: {map_info.big_map}")
        if map_info.light < 0 or map_info.light > 4:
            raise ValueError(f"无效的光照设置: {map_info.light}")
        if map_info.fire_damage < 0:
            raise ValueError(f"无效的火焰伤害: {map_info.fire_damage}")
        if map_info.lightning_damage < 0:
            raise ValueError(f"无效的闪电伤害: {map_info.lightning_damage}")
        if map_info.map_dark_light < 0:
            raise ValueError(f"无效的地图暗光设置: {map_info.map_dark_light}")
        if map_info.mine_index < 0:
            raise ValueError(f"无效的矿区索引: {map_info.mine_index}")
        if map_info.music < 0:
            raise ValueError(f"无效的音乐索引: {map_info.music}")
        if self.version >= 110 and map_info.weather_particles < 0 or map_info.weather_particles > 3:
            raise ValueError(f"无效的天气设置: {map_info.weather_particles}")
        if self.version >= 111 and map_info.gt_index < 0:
            raise ValueError(f"无效的GT索引: {map_info.gt_index}")

    def read_monster_info(self, f):
        """读取怪物信息"""
        try:
            monster = MonsterInfo()
            
            # 读取基本信息
            print(f"\n开始读取怪物信息，当前位置: {f.tell()}")
            monster.index = self.read_int32(f)
            print(f"读取怪物索引: {monster.index}")
            
            monster.name = self.read_string(f)
            print(f"读取怪物名称: {monster.name}")
            
            monster.image = self.read_uint16(f)
            print(f"读取怪物图像: {monster.image}")
            
            monster.ai = self.read_byte(f)
            print(f"读取怪物AI: {monster.ai}")
            
            monster.effect = self.read_byte(f)
            print(f"读取怪物效果: {monster.effect}")

            # 版本相关的等级读取
            if self.version < 62:
                monster.level = self.read_byte(f)
            else:
                monster.level = self.read_uint16(f)
            print(f"读取怪物等级: {monster.level}")

            monster.view_range = self.read_byte(f)
            print(f"读取视野范围: {monster.view_range}")
            
            monster.cool_eye = self.read_byte(f)
            print(f"读取冷却时间: {monster.cool_eye}")

            # 版本相关的状态信息读取
            if self.version > 84:
                # 读取完整的状态信息
                monster.stats = self.read_stats(f)
            else:
                # 旧版本的状态信息读取
                monster.stats = Stats()
                monster.stats[Stat.HP] = self.read_uint32(f)
                
                if self.version < 62:
                    monster.stats[Stat.MinAC] = self.read_byte(f)
                    monster.stats[Stat.MaxAC] = self.read_byte(f)
                    monster.stats[Stat.MinMAC] = self.read_byte(f)
                    monster.stats[Stat.MaxMAC] = self.read_byte(f)
                    monster.stats[Stat.MinDC] = self.read_byte(f)
                    monster.stats[Stat.MaxDC] = self.read_byte(f)
                    monster.stats[Stat.MinMC] = self.read_byte(f)
                    monster.stats[Stat.MaxMC] = self.read_byte(f)
                    monster.stats[Stat.MinSC] = self.read_byte(f)
                    monster.stats[Stat.MaxSC] = self.read_byte(f)
                else:
                    monster.stats[Stat.MinAC] = self.read_uint16(f)
                    monster.stats[Stat.MaxAC] = self.read_uint16(f)
                    monster.stats[Stat.MinMAC] = self.read_uint16(f)
                    monster.stats[Stat.MaxMAC] = self.read_uint16(f)
                    monster.stats[Stat.MinDC] = self.read_uint16(f)
                    monster.stats[Stat.MaxDC] = self.read_uint16(f)
                    monster.stats[Stat.MinMC] = self.read_uint16(f)
                    monster.stats[Stat.MaxMC] = self.read_uint16(f)
                    monster.stats[Stat.MinSC] = self.read_uint16(f)
                    monster.stats[Stat.MaxSC] = self.read_uint16(f)

                if self.version <= 84:
                    monster.stats[Stat.Accuracy] = self.read_byte(f)
                    monster.stats[Stat.Agility] = self.read_byte(f)

            monster.light = self.read_byte(f)
            print(f"读取光照设置: {monster.light}")
            
            monster.attack_speed = self.read_uint16(f)
            print(f"读取攻击速度: {monster.attack_speed}")
            
            monster.move_speed = self.read_uint16(f)
            print(f"读取移动速度: {monster.move_speed}")
            
            monster.experience = self.read_uint32(f)
            print(f"读取经验值: {monster.experience}")

            # 直接读取布尔值，不使用位运算
            monster.can_push = self.read_bool(f)
            print(f"读取可推动: {monster.can_push}")
            
            monster.can_tame = self.read_bool(f)
            print(f"读取可驯服: {monster.can_tame}")

            if self.version >= 18:
                monster.auto_rev = self.read_bool(f)
                print(f"读取自动复活: {monster.auto_rev}")
                
                monster.undead = self.read_bool(f)
                print(f"读取不死属性: {monster.undead}")

            if self.version >= 89:
                monster.drop_path = self.read_string(f)
                print(f"读取掉落路径: {monster.drop_path}")

            print(f"怪物信息读取完成，当前位置: {f.tell()}")
            return monster
        except Exception as e:
            print(f"读取怪物信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    def read_npc_info(self, f):
        """读取NPC信息"""
        try:
            npc = NPCInfo()
            
            # 读取基本信息
            print(f"\n开始读取NPC信息，当前位置: {f.tell()}")
            npc.index = self.read_int32(f)
            print(f"读取NPC索引: {npc.index}")
            
            npc.map_index = self.read_int32(f)
            print(f"读取地图索引: {npc.map_index}")
            
            # 读取任务索引列表
            collect_count = self.read_int32(f)
            print(f"收集任务数量: {collect_count}")
            for i in range(collect_count):
                quest_index = self.read_int32(f)
                npc.collect_quest_indexes.append(quest_index)
                
            finish_count = self.read_int32(f)
            print(f"完成任务数量: {finish_count}")
            for i in range(finish_count):
                quest_index = self.read_int32(f)
                npc.finish_quest_indexes.append(quest_index)
                
            npc.file_name = self.read_string(f)
            print(f"读取文件名: {npc.file_name}")
            
            npc.name = self.read_string(f)
            print(f"读取名称: {npc.name}")
            
            # 读取位置
            x = self.read_int32(f)
            y = self.read_int32(f)
            npc.location = Point(x, y)
            print(f"读取位置: ({x}, {y})")
            
            # 根据版本读取图像ID
            if self.version >= 72:
                npc.image = self.read_uint16(f)
            else:
                npc.image = self.read_byte(f)
            print(f"读取图像ID: {npc.image}")
            
            npc.rate = self.read_uint16(f)
            print(f"读取比率: {npc.rate}")
            
            if self.version >= 64:
                npc.time_visible = self.read_bool(f)
                npc.hour_start = self.read_byte(f)
                npc.minute_start = self.read_byte(f)
                npc.hour_end = self.read_byte(f)
                npc.minute_end = self.read_byte(f)
                npc.min_lev = self.read_int16(f)
                npc.max_lev = self.read_int16(f)
                npc.day_of_week = self.read_string(f)
                npc.class_required = self.read_string(f)
                
                if self.version >= 66:
                    npc.conquest = self.read_int32(f)
                else:
                    npc.sabuk = self.read_bool(f)
                    
                npc.flag_needed = self.read_int32(f)
                
            if self.version > 95:
                npc.show_on_big_map = self.read_bool(f)
                npc.big_map_icon = self.read_int32(f)
                
            if self.version > 96:
                npc.can_teleport_to = self.read_bool(f)
                
            if self.version >= 107:
                npc.conquest_visible = self.read_bool(f)
                
            return npc
        except Exception as e:
            print(f"读取NPC信息时出错: {str(e)}")
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

    def read_item_info(self, f):
        """读取物品信息"""
        try:
            item_info = ItemInfo()
            
            # 读取基本信息
            print(f"\n开始读取物品信息，当前位置: {f.tell()}")
            item_info.index = self.read_int32(f)
            print(f"读取物品索引: {item_info.index}")
            
            item_info.name = self.read_string(f)
            print(f"读取物品名称: {item_info.name}")
            
            # 读取枚举值，如果值不匹配则设置为默认值
            try:
                item_info.type = ItemType(self.read_byte(f))
                print(f"读取物品类型: {item_info.type}")
            except ValueError:
                item_info.type = ItemType.Nothing
                
            try:
                item_info.grade = ItemGrade(self.read_byte(f))
                print(f"读取物品等级: {item_info.grade}")
            except ValueError:
                item_info.grade = ItemGrade.None_
                
            try:
                item_info.required_type = RequiredType(self.read_byte(f))
                print(f"读取需求类型: {item_info.required_type}")
            except ValueError:
                item_info.required_type = RequiredType.Level
                
            try:
                item_info.required_class = RequiredClass(self.read_byte(f))
                print(f"读取需求职业: {item_info.required_class}")
            except ValueError:
                item_info.required_class = RequiredClass.None_
                
            try:
                item_info.required_gender = RequiredGender(self.read_byte(f))
                print(f"读取需求性别: {item_info.required_gender}")
            except ValueError:
                item_info.required_gender = RequiredGender.None_
                
            try:
                item_info.set = ItemSet(self.read_byte(f))
                print(f"读取物品套装: {item_info.set}")
            except ValueError:
                item_info.set = ItemSet.None_
                
            item_info.shape = self.read_int16(f)
            print(f"读取物品形状: {item_info.shape}")
            
            item_info.weight = self.read_byte(f)
            print(f"读取物品重量: {item_info.weight}")
            
            item_info.light = self.read_byte(f)
            print(f"读取物品光照: {item_info.light}")
            
            item_info.required_amount = self.read_byte(f)
            print(f"读取需求数量: {item_info.required_amount}")
            
            item_info.image = self.read_uint16(f)
            print(f"读取物品图像: {item_info.image}")
            
            item_info.durability = self.read_uint16(f)
            print(f"读取物品耐久: {item_info.durability}")

            # 版本相关的堆叠大小读取
            if self.version <= 84:
                item_info.stack_size = self.read_uint32(f)
            else:
                item_info.stack_size = self.read_uint16(f)
            print(f"读取堆叠大小: {item_info.stack_size}")

            item_info.price = self.read_uint32(f)
            print(f"读取物品价格: {item_info.price}")

            # 版本相关的属性读取
            if self.version <= 84:
                print("开始读取旧版本属性...")
                item_info.stats[Stat.MinAC] = self.read_byte(f)
                item_info.stats[Stat.MaxAC] = self.read_byte(f)
                item_info.stats[Stat.MinMAC] = self.read_byte(f)
                item_info.stats[Stat.MaxMAC] = self.read_byte(f)
                item_info.stats[Stat.MinDC] = self.read_byte(f)
                item_info.stats[Stat.MaxDC] = self.read_byte(f)
                item_info.stats[Stat.MinMC] = self.read_byte(f)
                item_info.stats[Stat.MaxMC] = self.read_byte(f)
                item_info.stats[Stat.MinSC] = self.read_byte(f)
                item_info.stats[Stat.MaxSC] = self.read_byte(f)
                item_info.stats[Stat.HP] = self.read_uint16(f)
                item_info.stats[Stat.MP] = self.read_uint16(f)
                item_info.stats[Stat.Accuracy] = self.read_byte(f)
                item_info.stats[Stat.Agility] = self.read_byte(f)
                item_info.stats[Stat.Luck] = self.read_byte(f)
                item_info.stats[Stat.AttackSpeed] = self.read_byte(f)

            item_info.start_item = self.read_bool(f)
            print(f"读取起始物品: {item_info.start_item}")

            if self.version <= 84:
                item_info.stats[Stat.BagWeight] = self.read_byte(f)
                item_info.stats[Stat.HandWeight] = self.read_byte(f)
                item_info.stats[Stat.WearWeight] = self.read_byte(f)

            item_info.effect = self.read_byte(f)
            print(f"读取物品效果: {item_info.effect}")

            if self.version <= 84:
                item_info.stats[Stat.Strong] = self.read_byte(f)
                item_info.stats[Stat.MagicResist] = self.read_byte(f)
                item_info.stats[Stat.PoisonResist] = self.read_byte(f)
                item_info.stats[Stat.HealthRecovery] = self.read_byte(f)
                item_info.stats[Stat.SpellRecovery] = self.read_byte(f)
                item_info.stats[Stat.PoisonRecovery] = self.read_byte(f)
                item_info.stats[Stat.HPRatePercent] = self.read_byte(f)
                item_info.stats[Stat.MPRatePercent] = self.read_byte(f)
                item_info.stats[Stat.CriticalRate] = self.read_byte(f)
                item_info.stats[Stat.CriticalDamage] = self.read_byte(f)

            # 读取布尔值组合字节
            bools = self.read_byte(f)
            print(f"读取布尔值组合字节: {bools:02x}")
            item_info.need_identify = (bools & 0x01) == 0x01
            item_info.show_group_pickup = (bools & 0x02) == 0x02
            item_info.class_based = (bools & 0x04) == 0x04
            item_info.level_based = (bools & 0x08) == 0x08
            item_info.can_mine = (bools & 0x10) == 0x10
            if self.version >= 77:
                item_info.global_drop_notify = (bools & 0x20) == 0x20
            print(f"解析布尔值组合: need_identify={item_info.need_identify}, show_group_pickup={item_info.show_group_pickup}, class_based={item_info.class_based}, level_based={item_info.level_based}, can_mine={item_info.can_mine}, global_drop_notify={item_info.global_drop_notify}")

            if self.version <= 84:
                item_info.stats[Stat.MaxACRatePercent] = self.read_byte(f)
                item_info.stats[Stat.MaxMACRatePercent] = self.read_byte(f)
                item_info.stats[Stat.Holy] = self.read_byte(f)
                item_info.stats[Stat.Freezing] = self.read_byte(f)
                item_info.stats[Stat.PoisonAttack] = self.read_byte(f)

            try:
                item_info.bind = BindMode(self.read_int16(f))
                print(f"读取绑定模式: {item_info.bind}")
            except ValueError:
                item_info.bind = BindMode.None_

            if self.version <= 84:
                item_info.stats[Stat.Reflect] = self.read_byte(f)
                item_info.stats[Stat.HPDrainRatePercent] = self.read_byte(f)

            try:
                item_info.unique = SpecialItemMode(self.read_int16(f))
                print(f"读取特殊物品模式: {item_info.unique}")
            except ValueError:
                item_info.unique = SpecialItemMode.None_

            item_info.random_stats_id = self.read_byte(f)
            print(f"读取随机属性ID: {item_info.random_stats_id}")
            
            item_info.can_fast_run = self.read_bool(f)
            print(f"读取可以快速奔跑: {item_info.can_fast_run}")
            
            item_info.can_awakening = self.read_bool(f)
            print(f"读取可以觉醒: {item_info.can_awakening}")

            if self.version > 83:
                item_info.slots = self.read_byte(f)
                print(f"读取插槽数量: {item_info.slots}")

            if self.version > 84:
                print("开始读取新版本属性...")
                new_stats = self.read_stats(f)
                item_info.stats = new_stats

            is_tooltip = self.read_bool(f)
            if is_tooltip:
                item_info.tool_tip = self.read_string(f)
                print(f"读取工具提示: {item_info.tool_tip}")

            if self.version < 70:
                if item_info.type == ItemType.Ring and item_info.unique != SpecialItemMode.None_:
                    item_info.bind |= BindMode.NoWeddingRing

            print(f"物品信息读取完成，当前位置: {f.tell()}")
            return item_info
        except Exception as e:
            print(f"读取物品信息时出错: {str(e)}")
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
                self.version = self.read_int32(f)
                self.custom_version = self.read_int32(f)
                
                print(f"\n=== 数据库信息 ===")
                print(f"数据库版本: {self.version}")
                print(f"自定义版本: {self.custom_version}")

                # 检查版本兼容性
                if self.version < 60:  # MinVersion = 60
                    print(f"无法加载版本 {self.version} 的数据库。最低支持版本为 60。")
                    return False
                elif self.version > 112:  # Version = 112
                    print(f"无法加载版本 {self.version} 的数据库。最高支持版本为 112。")
                    return False

                print("\n=== 索引信息 ===")
                # 读取索引
                map_index = self.read_int32(f)
                item_index = self.read_int32(f)
                monster_index = self.read_int32(f)
                npc_index = self.read_int32(f)
                quest_index = self.read_int32(f)
                
                print(f"地图索引: {map_index}")
                print(f"物品索引: {item_index}")
                print(f"怪物索引: {monster_index}")
                print(f"NPC索引: {npc_index}")
                print(f"任务索引: {quest_index}")
                
                # 根据版本读取额外索引
                gameshop_index = 0
                conquest_index = 0
                respawn_index = 0
                
                if self.version >= 63:
                    gameshop_index = self.read_int32(f)
                    print(f"商店索引: {gameshop_index}")
                    
                if self.version >= 66:
                    conquest_index = self.read_int32(f)
                    print(f"征服索引: {conquest_index}")
                    
                if self.version >= 68:
                    respawn_index = self.read_int32(f)
                    print(f"重生索引: {respawn_index}")

                print("\n=== 地图信息 ===")
                # 读取地图信息
                map_count = self.read_int32(f)
                print(f"地图总数: {map_count}")
                
                
                for i in range(map_count):
                    try:
                        map_info = self.read_map_info(f)
                        if map_info is None:
                            print(f"跳过地图 {i+1}: 读取失败")
                            continue
                            
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
                item_count = self.read_int32(f)
                print(f"物品总数: {item_count}")
                
                for i in range(item_count):
                    try:
                        print(f"\n物品 {i+1}/{item_count}:")
                        item_info = self.read_item_info(f)
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
                monster_count = self.read_int32(f)
                print(f"怪物总数: {monster_count}")
                
                for i in range(monster_count):
                    try:
                        monster_info = self.read_monster_info(f)
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
                npc_count = self.read_int32(f)
                print(f"NPC总数: {npc_count}")
                
                for i in range(npc_count):
                    try:
                        npc_info = self.read_npc_info(f)
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
                quest_count = self.read_int32(f)
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

                print("\n=== 数据读取完成 ===")
                print(f"成功加载地图数量: {len(self.maps)}")
                print(f"成功加载物品数量: {len(self.items)}")
                print(f"成功加载怪物数量: {len(self.monsters)}")
                print(f"成功加载NPC数量: {len(self.npcs)}")
                print(f"成功加载任务数量: {len(self.quests)}")
                print(f"成功加载龙数量: {len(self.dragons)}")
                
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

    def read_dragon_info(self, f):
        """读取龙信息"""
        try:
            dragon = DragonInfo()
            
            # 读取基本信息
            print(f"\n开始读取龙信息，当前位置: {f.tell()}")
            dragon.enabled = self.read_bool(f)
            print(f"读取启用状态: {dragon.enabled}")
            
            dragon.map_file_name = self.read_string(f)
            print(f"读取地图文件名: {dragon.map_file_name}")
            
            dragon.monster_name = self.read_string(f)
            print(f"读取怪物名称: {dragon.monster_name}")
            
            dragon.body_name = self.read_string(f)
            print(f"读取身体名称: {dragon.body_name}")
            
            # 读取位置信息
            dragon.location = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取位置: ({dragon.location.x}, {dragon.location.y})")
            
            dragon.drop_area_top = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取掉落区域顶部: ({dragon.drop_area_top.x}, {dragon.drop_area_top.y})")
            
            dragon.drop_area_bottom = Point(
                x=self.read_int32(f),
                y=self.read_int32(f)
            )
            print(f"读取掉落区域底部: ({dragon.drop_area_bottom.x}, {dragon.drop_area_bottom.y})")
            
            # 读取经验值
            for i in range(len(dragon.exps)):
                dragon.exps[i] = self.read_int64(f)
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

    def read_int64(self, f):
        """读取64位整数"""
        try:
            data = f.read(8)
            print(f"读取int64原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<q', data)[0]
        except Exception as e:
            print(f"读取int64时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

def main():
    # 使用相对路径
    db_path = os.path.join("Jev", "Server.MirDB")
    parser = MirDBParser(db_path)
    
    if parser.load():
        print("\n保存解析结果到JSON文件...")
        parser.save_to_json('data')
        print("完成!")

if __name__ == "__main__":
    main() 