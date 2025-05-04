from dataclasses import dataclass, field
from typing import List, Optional, Dict

from binary import BinaryReader, BinaryWriter
from enum import Enum
from common import Stats, Stat
@dataclass
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
@dataclass
class ItemGrade(Enum):
    None_ = 0
    Common = 1
    Rare = 2
    Legendary = 3
    Mythical = 4
@dataclass
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
@dataclass  
class RequiredClass(Enum):
    None_ = 0
    Warrior = 1
    Wizard = 2
    Taoist = 3
    Assassin = 4
    Archer = 5
@dataclass
class RequiredGender(Enum):
    None_ = 0
    Male = 1
    Female = 2
@dataclass
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

@dataclass
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

@dataclass
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
class Item:
    index: int = 0
    name: str = ""
    type: ItemType = field(default_factory=lambda: ItemType.Nothing)
    grade: ItemGrade = field(default_factory=lambda: ItemGrade.None_)
    required_type: RequiredType = field(default_factory=lambda: RequiredType.Level)
    required_class: RequiredClass = field(default_factory=lambda: RequiredClass.None_)
    required_gender: RequiredGender = field(default_factory=lambda: RequiredGender.None_)
    set: ItemSet = field(default_factory=lambda: ItemSet.None_)
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
    bind: BindMode = field(default_factory=lambda: BindMode.None_)
    unique: SpecialItemMode = field(default_factory=lambda: SpecialItemMode.None_)
    random_stats_id: int = 0
    random_stats: Dict = None
    tool_tip: str = ""
    slots: int = 0
    stats: Stats = None
    def write(self, f):
        """写入物品信息"""
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_byte(f, self.type)
        BinaryWriter.write_byte(f, self.grade)
        BinaryWriter.write_byte(f, self.required_type)
        BinaryWriter.write_byte(f, self.required_class)
        BinaryWriter.write_byte(f, self.required_gender)
        BinaryWriter.write_byte(f, self.set)
        BinaryWriter.write_int16(f, self.shape)
        BinaryWriter.write_byte(f, self.weight)
        BinaryWriter.write_byte(f, self.light)
        BinaryWriter.write_byte(f, self.required_amount)
        BinaryWriter.write_uint16(f, self.image)
        BinaryWriter.write_uint16(f, self.durability)
        BinaryWriter.write_uint16(f, self.stack_size)
        BinaryWriter.write_uint32(f, self.price)
        BinaryWriter.write_bool(f, self.start_item)
        BinaryWriter.write_byte(f, self.effect)
        # #         # 读取布尔值组合字节
        #     bools = BinaryReader.read_byte(f)
        #     print(f"读取布尔值组合字节: {bools:02x}")
        #     item_info.need_identify = (bools & 0x01) == 0x01
        #     item_info.show_group_pickup = (bools & 0x02) == 0x02
        #     item_info.class_based = (bools & 0x04) == 0x04
        #     item_info.level_based = (bools & 0x08) == 0x08
        #     item_info.can_mine = (bools & 0x10) == 0x10
        #     item_info.global_drop_notify = (bools & 0x20) == 0x20
        #     print(f"解析布尔值组合: need_identify={item_info.need_identify}, show_group_pickup={item_info.show_group_pickup}, class_based={item_info.class_based}, level_based={item_info.level_based}, can_mine={item_info.can_mine}, global_drop_notify={item_info.global_drop_notify}")
        boolean_byte = 0
        if self.need_identify:
            boolean_byte |= 0x01
        if self.show_group_pickup:
            boolean_byte |= 0x02
        if self.class_based:
            boolean_byte |= 0x04    
        if self.level_based:
            boolean_byte |= 0x08
        if self.can_mine:
            boolean_byte |= 0x10
        if self.global_drop_notify:
            boolean_byte |= 0x20    
        BinaryWriter.write_byte(f, boolean_byte)
        BinaryWriter.write_int16(f, self.bind)
        BinaryWriter.write_int16(f, self.unique)
        BinaryWriter.write_byte(f, self.random_stats_id)
        BinaryWriter.write_bool(f, self.can_fast_run)
        BinaryWriter.write_bool(f, self.can_awakening)
        BinaryWriter.write_byte(f, self.slots)
        self.write_stats(f)
        BinaryWriter.write_bool(f, self.tool_tip)
        
    def write_stats(self, f):
        """写入状态信息"""
        BinaryWriter.write_int32(f, len(self.stats))
        for stat, value in self.stats.items():
            BinaryWriter.write_byte(f, stat.value)
            BinaryWriter.write_int32(f, value)

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
        """读取物品信息"""
        try:
            item_info = Item()
            
            # 读取基本信息
            print(f"\n开始读取物品信息，当前位置: {f.tell()}")
            item_info.index = BinaryReader.read_int32(f)
            print(f"读取物品索引: {item_info.index}")
            
            item_info.name = BinaryReader.read_string(f)
            print(f"读取物品名称: {item_info.name}")
            
            # 读取枚举值，如果值不匹配则设置为默认值
            try:
                item_info.type = ItemType(BinaryReader.read_byte(f))
                print(f"读取物品类型: {item_info.type}")
            except ValueError:
                item_info.type = ItemType.Nothing
                
            try:
                item_info.grade = ItemGrade(BinaryReader.read_byte(f))
                print(f"读取物品等级: {item_info.grade}")
            except ValueError:
                item_info.grade = ItemGrade.None_
                
            try:
                item_info.required_type = RequiredType(BinaryReader.read_byte(f))
                print(f"读取需求类型: {item_info.required_type}")
            except ValueError:
                item_info.required_type = RequiredType.Level
                
            try:
                item_info.required_class = RequiredClass(BinaryReader.read_byte(f))
                print(f"读取需求职业: {item_info.required_class}")
            except ValueError:
                item_info.required_class = RequiredClass.None_
                
            try:
                item_info.required_gender = RequiredGender(BinaryReader.read_byte(f))
                print(f"读取需求性别: {item_info.required_gender}")
            except ValueError:
                item_info.required_gender = RequiredGender.None_
                
            try:
                item_info.set = ItemSet(BinaryReader.read_byte(f))
                print(f"读取物品套装: {item_info.set}")
            except ValueError:
                item_info.set = ItemSet.None_
                
            item_info.shape = BinaryReader.read_int16(f)
            print(f"读取物品形状: {item_info.shape}")
            
            item_info.weight = BinaryReader.read_byte(f)
            print(f"读取物品重量: {item_info.weight}")
            
            item_info.light = BinaryReader.read_byte(f)
            print(f"读取物品光照: {item_info.light}")
            
            item_info.required_amount = BinaryReader.read_byte(f)
            print(f"读取需求数量: {item_info.required_amount}")
            
            item_info.image = BinaryReader.read_uint16(f)
            print(f"读取物品图像: {item_info.image}")
            
            item_info.durability = BinaryReader.read_uint16(f)
            print(f"读取物品耐久: {item_info.durability}")

            item_info.stack_size = BinaryReader.read_uint16(f)
            print(f"读取堆叠大小: {item_info.stack_size}")

            item_info.price = BinaryReader.read_uint32(f)
            print(f"读取物品价格: {item_info.price}")


            item_info.start_item = BinaryReader.read_bool(f)
            print(f"读取起始物品: {item_info.start_item}")


            item_info.effect = BinaryReader.read_byte(f)
            print(f"读取物品效果: {item_info.effect}")


            # 读取布尔值组合字节
            bools = BinaryReader.read_byte(f)
            print(f"读取布尔值组合字节: {bools:02x}")
            item_info.need_identify = (bools & 0x01) == 0x01
            item_info.show_group_pickup = (bools & 0x02) == 0x02
            item_info.class_based = (bools & 0x04) == 0x04
            item_info.level_based = (bools & 0x08) == 0x08
            item_info.can_mine = (bools & 0x10) == 0x10
            item_info.global_drop_notify = (bools & 0x20) == 0x20
            print(f"解析布尔值组合: need_identify={item_info.need_identify}, show_group_pickup={item_info.show_group_pickup}, class_based={item_info.class_based}, level_based={item_info.level_based}, can_mine={item_info.can_mine}, global_drop_notify={item_info.global_drop_notify}")


            try:
                item_info.bind = BindMode(BinaryReader.read_int16(f))
                print(f"读取绑定模式: {item_info.bind}")
            except ValueError:
                item_info.bind = BindMode.None_


            try:
                item_info.unique = SpecialItemMode(BinaryReader.read_int16(f))
                print(f"读取特殊物品模式: {item_info.unique}")
            except ValueError:
                item_info.unique = SpecialItemMode.None_

            item_info.random_stats_id = BinaryReader.read_byte(f)
            print(f"读取随机属性ID: {item_info.random_stats_id}")
            
            item_info.can_fast_run = BinaryReader.read_bool(f)
            print(f"读取可以快速奔跑: {item_info.can_fast_run}")
            
            item_info.can_awakening = BinaryReader.read_bool(f)
            print(f"读取可以觉醒: {item_info.can_awakening}")

            item_info.slots = BinaryReader.read_byte(f)
            print(f"读取插槽数量: {item_info.slots}")

            print("开始读取新版本属性...")
            new_stats = Item.read_stats(f)
            item_info.stats = new_stats

            is_tooltip = BinaryReader.read_bool(f)
            if is_tooltip:
                item_info.tool_tip = BinaryReader.read_string(f)
                print(f"读取工具提示: {item_info.tool_tip}")


            print(f"物品信息读取完成，当前位置: {f.tell()}")
            return item_info
        except Exception as e:
            print(f"读取物品信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise