from dataclasses import dataclass, field
from typing import List, Optional
from binary import BinaryReader,BinaryWriter
from map import Point
import os
from item import Item
@dataclass
class DragonDropInfo:
    chance: int = 0
    item: Optional[Item] = None
    gold: int = 0
    level: int = 0

@dataclass
class Dragon:
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
    def write(self,f):
        BinaryWriter.write_bool(f, self.enabled)
        BinaryWriter.write_string(f, self.map_file_name)
        BinaryWriter.write_string(f, self.monster_name)
        BinaryWriter.write_string(f, self.body_name)
        self.location.write(f)
        self.drop_area_top.write(f)
        self.drop_area_bottom.write(f)
        BinaryWriter.write_int32(f, self.level)
        BinaryWriter.write_int32(f, self.experience)
        BinaryWriter.write_int32(f, len(self.exps))
        for exp in self.exps:   
            BinaryWriter.write_int64(f, exp)
        
    @staticmethod
    def read(f):
        """读取龙信息"""
        try:
            dragon = Dragon()
            
            # 读取基本信息
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
            
         
            
            return dragon
        except Exception as e:
            print(f"读取龙信息时出错: {str(e)}")
            raise

    
    