from dataclasses import dataclass, field
from typing import List, Optional, Dict

from binary import BinaryReader, BinaryWriter
from enum import Enum
from common import Stats, Stat, RequiredClass
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
    RedFlower = 4
    Smash = 5
    HwanDevil = 6
    Purity = 7
    FiveString = 8
    Mundane = 9
    NokChi = 10
    TaoProtect = 11
    Mir = 12
    Bone = 13
    Bug = 14
    WhiteGold = 15
    WhiteGoldH = 16
    RedJade = 17
    RedJadeH = 18
    Nephrite = 19
    NephriteH = 20
    Whisker1 = 21
    Whisker2 = 22
    Whisker3 = 23
    Whisker4 = 24
    Whisker5 = 25
    Hyeolryong = 26
    Monitor = 27
    Oppressive = 28
    Paeok = 29
    Sulgwan = 30
    BlueFrost = 31
    DarkGhost = 38
    BlueFrostH = 39

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
    is_tooltip: bool = False
    tool_tip: str = ""
    slots: int = 0
    stats: Stats = None
    def compare(self, other: 'Item') -> bool:
        """比较两个物品信息是否一致"""
        if self.index != other.index:
            return False
        if self.name != other.name:
            return False    
        if self.type != other.type:
            return False
        if self.grade != other.grade:
            return False
        if self.required_type != other.required_type:
            return False
        if self.required_class != other.required_class:
            return False
        if self.required_gender != other.required_gender:
            return False
        if self.set != other.set:
            return False    
        if self.shape != other.shape:
            return False
        if self.weight != other.weight:
            return False
        if self.light != other.light:
            return False
        if self.required_amount != other.required_amount:
            return False
        if self.image != other.image:
            return False
        if self.durability != other.durability:
            return False
        if self.stack_size != other.stack_size:
            return False
        if self.price != other.price:
            return False
        if self.start_item != other.start_item:
            return False
        if self.effect != other.effect:
            return False
        if self.need_identify != other.need_identify:
            return False
        if self.show_group_pickup != other.show_group_pickup:
            return False
        if self.class_based != other.class_based:
            return False
        if self.level_based != other.level_based:
            return False
        if self.can_mine != other.can_mine:
            return False
        if self.global_drop_notify != other.global_drop_notify:
            return False
        if self.bind != other.bind:
            return False
        if self.unique != other.unique:
            return False
        if self.random_stats_id != other.random_stats_id:
            return False
        if self.tool_tip != other.tool_tip:
            return False
        if self.slots != other.slots:
            return False
        if self.stats != other.stats:
            return False
        return True
            
            
            

    def write(self, f):
        """写入物品信息"""
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_byte(f,  self.type.value)
        BinaryWriter.write_byte(f, self.grade.value )
        BinaryWriter.write_byte(f, self.required_type.value)
        BinaryWriter.write_byte(f, self.required_class.value)
        BinaryWriter.write_byte(f, self.required_gender.value)
        BinaryWriter.write_byte(f, self.set.value)
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
        BinaryWriter.write_int16(f, self.bind.value)
        BinaryWriter.write_int16(f, self.unique.value)
        BinaryWriter.write_byte(f, self.random_stats_id)
        BinaryWriter.write_bool(f, self.can_fast_run)
        BinaryWriter.write_bool(f, self.can_awakening)
        BinaryWriter.write_byte(f, self.slots)
        self.write_stats(f)
        if(self.is_tooltip):
            BinaryWriter.write_bool(f, True)
            BinaryWriter.write_string(f, self.tool_tip)
        else:
            BinaryWriter.write_bool(f, False)
        
    def write_stats(self, f):
        """写入状态信息"""
        BinaryWriter.write_int32(f, len(self.stats.values))
        for stat in self.stats.values:
            BinaryWriter.write_byte(f, stat.value)
            BinaryWriter.write_int32(f, self.stats[stat])

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
            raise
    @staticmethod
    def read(f):
        """读取物品信息"""
        try:
            item_info = Item()
            
            # 读取基本信息
            item_info.index = BinaryReader.read_int32(f)
            item_info.name = BinaryReader.read_string(f)
            
            # 读取枚举值，如果值不匹配则设置为默认值
            try:
                item_info.type = ItemType(BinaryReader.read_byte(f))
            except ValueError:
                item_info.type = ItemType.Nothing
                
            try:
                item_info.grade = ItemGrade(BinaryReader.read_byte(f))
            except ValueError:
                item_info.grade = ItemGrade.None_
                
            try:
                item_info.required_type = RequiredType(BinaryReader.read_byte(f))
            except ValueError:
                item_info.required_type = RequiredType.Level
                
            # 直接读取原始值，因为可能是位掩码组合
            item_info.required_class = RequiredClass(BinaryReader.read_byte(f))

            try:
                item_info.required_gender = RequiredGender(BinaryReader.read_byte(f))
            except ValueError:
                item_info.required_gender = RequiredGender.None_
                
            try:
                item_info.set = ItemSet(BinaryReader.read_byte(f))
            except ValueError:
                item_info.set = ItemSet.None_
                
            item_info.shape = BinaryReader.read_int16(f)
            
            item_info.weight = BinaryReader.read_byte(f)
            
            item_info.light = BinaryReader.read_byte(f)
            
            item_info.required_amount = BinaryReader.read_byte(f)
            
            item_info.image = BinaryReader.read_uint16(f)
            
            item_info.durability = BinaryReader.read_uint16(f)

            item_info.stack_size = BinaryReader.read_uint16(f)

            item_info.price = BinaryReader.read_uint32(f)


            item_info.start_item = BinaryReader.read_bool(f)


            item_info.effect = BinaryReader.read_byte(f)


            # 读取布尔值组合字节
            bools = BinaryReader.read_byte(f)
            item_info.need_identify = (bools & 0x01) == 0x01
            item_info.show_group_pickup = (bools & 0x02) == 0x02
            item_info.class_based = (bools & 0x04) == 0x04
            item_info.level_based = (bools & 0x08) == 0x08
            item_info.can_mine = (bools & 0x10) == 0x10
            item_info.global_drop_notify = (bools & 0x20) == 0x20


            try:
                item_info.bind = BindMode(BinaryReader.read_int16(f))
            except ValueError:
                item_info.bind = BindMode.None_


            try:
                item_info.unique = SpecialItemMode(BinaryReader.read_int16(f))
            except ValueError:
                item_info.unique = SpecialItemMode.None_

            item_info.random_stats_id = BinaryReader.read_byte(f)
            
            item_info.can_fast_run = BinaryReader.read_bool(f)
            
            item_info.can_awakening = BinaryReader.read_bool(f)

            item_info.slots = BinaryReader.read_byte(f)

            new_stats = Item.read_stats(f)
            item_info.stats = new_stats

            item_info.is_tooltip = BinaryReader.read_bool(f)
            if item_info.is_tooltip:
                item_info.tool_tip = BinaryReader.read_string(f)
            return item_info
        except Exception as e:
            print(f"读取物品信息时出错: {str(e)}")
            raise