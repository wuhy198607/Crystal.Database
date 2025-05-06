from dataclasses import dataclass, field
from typing import List, Dict
from binary import BinaryReader,BinaryWriter
from enum import Enum
from common import Stats, Stat
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
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_uint16(f, self.image)
        BinaryWriter.write_byte(f, self.ai)
        BinaryWriter.write_byte(f, self.effect)
        BinaryWriter.write_uint16(f, self.level)
        BinaryWriter.write_byte(f, self.view_range)
        BinaryWriter.write_byte(f, self.cool_eye)
        self.stats.write(f)
        BinaryWriter.write_byte(f, self.light)
        BinaryWriter.write_uint16(f, self.attack_speed)
        BinaryWriter.write_uint16(f, self.move_speed)   
        BinaryWriter.write_uint32(f, self.experience)
        BinaryWriter.write_bool(f, self.can_push)
        BinaryWriter.write_bool(f, self.can_tame)
        BinaryWriter.write_bool(f, self.auto_rev)
        BinaryWriter.write_bool(f, self.undead)
        BinaryWriter.write_string(f, self.drop_path)
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