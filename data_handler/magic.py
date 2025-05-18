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
    def compare(self,other: 'Magic'):
        if self.name != other.name:
            return False
        if self.spell != other.spell:
            return False
        if self.base_cost != other.base_cost:
            return False
        if self.level_cost != other.level_cost:
            return False
        if self.icon != other.icon:
            return False
        if self.level1 != other.level1:
            return False
        if self.level2 != other.level2:
            return False
        if self.level3 != other.level3:
            return False
        if self.need1 != other.need1:
            return False
        if self.need2 != other.need2:
            return False
        if self.need3 != other.need3:
            return False
        if self.delay_base != other.delay_base:
            return False
        if self.delay_reduction != other.delay_reduction:
            return False
        if self.power_base != other.power_base:
            return False
        if self.power_bonus != other.power_bonus:
            return False
        if self.mpower_base != other.mpower_base:
            return False
        if self.mpower_bonus != other.mpower_bonus:
            return False
        if self.range != other.range:
            return False
        if self.multiplier_base != other.multiplier_base:
            return False
        if self.multiplier_bonus != other.multiplier_bonus:
            return False
        return True
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
            magic.name = BinaryReader.read_string(f)

            try:
                magic.spell = Spell(BinaryReader.read_byte(f))
                
            except ValueError:
                magic.spell = Spell.None_
                
            magic.base_cost = BinaryReader.read_byte(f)
            
            magic.level_cost = BinaryReader.read_byte(f)
            
            magic.icon = BinaryReader.read_byte(f)
            
            magic.level1 = BinaryReader.read_byte(f)
            
            magic.level2 = BinaryReader.read_byte(f)
            
            magic.level3 = BinaryReader.read_byte(f)
            
            magic.need1 = BinaryReader.read_uint16(f)

            magic.need2 = BinaryReader.read_uint16(f)
            
            magic.need3 = BinaryReader.read_uint16(f)
            
            magic.delay_base = BinaryReader.read_uint32(f)
            
            magic.delay_reduction = BinaryReader.read_uint32(f)
            
            magic.power_base = BinaryReader.read_uint16(f)
            
            magic.power_bonus = BinaryReader.read_uint16(f)
            
            magic.mpower_base = BinaryReader.read_uint16(f)
            
            magic.mpower_bonus = BinaryReader.read_uint16(f)
            
            magic.range = BinaryReader.read_byte(f)

            magic.multiplier_base = BinaryReader.read_float(f)
            
            magic.multiplier_bonus = BinaryReader.read_float(f)
            
            return magic
        except Exception as e:
            print(f"读取魔法信息时出错: {str(e)}")
            raise 