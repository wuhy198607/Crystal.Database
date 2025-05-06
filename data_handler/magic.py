from dataclasses import dataclass, field
from typing import List, Optional, Dict
from binary import BinaryReader,BinaryWriter
from enum import Enum

class Spell(Enum):
    None_ = 0
    FireBall = 1
    Healing = 2
    # ... 其他魔法类型

@dataclass
class Magic:
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
    def write(self,f):
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_byte(f, self.spell.value)
        BinaryWriter.write_byte(f, self.base_cost)
        BinaryWriter.write_byte(f, self.level_cost)
        BinaryWriter.write_byte(f, self.icon)
        BinaryWriter.write_byte(f, self.level1)
        BinaryWriter.write_byte(f, self.level2)
        BinaryWriter.write_byte(f, self.level3)
        BinaryWriter.write_uint16(f, self.need1)
        BinaryWriter.write_uint16(f, self.need2)
        BinaryWriter.write_uint16(f, self.need3)    
        BinaryWriter.write_uint32(f, self.delay_base)   
        BinaryWriter.write_uint32(f, self.delay_reduction)
        BinaryWriter.write_uint16(f, self.power_base)
        BinaryWriter.write_uint16(f, self.power_bonus)
        BinaryWriter.write_uint16(f, self.mpower_base)
        BinaryWriter.write_uint16(f, self.mpower_bonus) 
        BinaryWriter.write_byte(f, self.range)
        BinaryWriter.write_float(f, self.multiplier_base)
        BinaryWriter.write_float(f, self.multiplier_bonus)
            

    @staticmethod
    def read(f):
        """读取魔法信息"""
        try:
            magic = Magic()
            
            # 读取基本信息
            print(f"\n开始读取魔法信息，当前位置: {f.tell()}")
            magic.name = BinaryReader.read_string(f)
            print(f"读取魔法名称: {magic.name}")
            
            try:
                magic.spell = Spell(BinaryReader.read_byte(f))
                print(f"读取魔法类型: {magic.spell}")
            except ValueError:
                magic.spell = Spell.None_
                
            magic.base_cost = BinaryReader.read_byte(f)
            print(f"读取基础消耗: {magic.base_cost}")
            
            magic.level_cost = BinaryReader.read_byte(f)
            print(f"读取等级消耗: {magic.level_cost}")
            
            magic.icon = BinaryReader.read_byte(f)
            print(f"读取图标: {magic.icon}")
            
            magic.level1 = BinaryReader.read_byte(f)
            print(f"读取等级1: {magic.level1}")
            
            magic.level2 = BinaryReader.read_byte(f)
            print(f"读取等级2: {magic.level2}")
            
            magic.level3 = BinaryReader.read_byte(f)
            print(f"读取等级3: {magic.level3}")
            
            magic.need1 = BinaryReader.read_uint16(f)
            print(f"读取需求1: {magic.need1}")
            
            magic.need2 = BinaryReader.read_uint16(f)
            print(f"读取需求2: {magic.need2}")
            
            magic.need3 = BinaryReader.read_uint16(f)
            print(f"读取需求3: {magic.need3}")
            
            magic.delay_base = BinaryReader.read_uint32(f)
            print(f"读取基础延迟: {magic.delay_base}")
            
            magic.delay_reduction = BinaryReader.read_uint32(f)
            print(f"读取延迟减少: {magic.delay_reduction}")
            
            magic.power_base = BinaryReader.read_uint16(f)
            print(f"读取基础力量: {magic.power_base}")
            
            magic.power_bonus = BinaryReader.read_uint16(f)
            print(f"读取力量奖励: {magic.power_bonus}")
            
            magic.mpower_base = BinaryReader.read_uint16(f)
            print(f"读取基础魔法力量: {magic.mpower_base}")
            
            magic.mpower_bonus = BinaryReader.read_uint16(f)
            print(f"读取魔法力量奖励: {magic.mpower_bonus}")
            
            magic.range = BinaryReader.read_byte(f)
            print(f"读取范围: {magic.range}")
                
            magic.multiplier_base = BinaryReader.read_float(f)
            print(f"读取基础倍数: {magic.multiplier_base}")
            
            magic.multiplier_bonus = BinaryReader.read_float(f)
            print(f"读取倍数奖励: {magic.multiplier_bonus}")
            
            print(f"魔法信息读取完成，当前位置: {f.tell()}")
            return magic
        except Exception as e:
            print(f"读取魔法信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise 