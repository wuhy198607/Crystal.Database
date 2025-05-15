from dataclasses import dataclass, field
from typing import List, Dict
from binary import BinaryReader,BinaryWriter    
from enum import Enum
from common import Point
@dataclass
class NPC:
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
    flag_needed: int = 0
    conquest: int = 0
    show_on_big_map: bool = False
    big_map_icon: int = 0
    can_teleport_to: bool = False
    conquest_visible: bool = True
    collect_quest_indexes: List[int] = field(default_factory=list)
    finish_quest_indexes: List[int] = field(default_factory=list)
    def compare(self,other):
        if self.index != other.index:
            return False
        if self.map_index != other.map_index:
            return False
        if self.collect_quest_indexes != other.collect_quest_indexes:
            return False
        if self.finish_quest_indexes != other.finish_quest_indexes:
            return False
        if self.file_name != other.file_name:
            return False
        if self.name != other.name:
            return False
        if self.location != other.location:
            return False
        if self.image != other.image:
            return False
        if self.rate != other.rate:
            return False    
        if self.time_visible != other.time_visible:
            return False
        if self.hour_start != other.hour_start:
            return False
        if self.minute_start != other.minute_start:
            return False
        if self.hour_end != other.hour_end:
            return False
        if self.minute_end != other.minute_end:
            return False
        if self.min_lev != other.min_lev:
            return False
        if self.max_lev != other.max_lev:
            return False
        if self.day_of_week != other.day_of_week:
            return False
        if self.class_required != other.class_required:
            return False
        if self.flag_needed != other.flag_needed:
            return False
        if self.conquest != other.conquest:
            return False
        if self.show_on_big_map != other.show_on_big_map:
            return False
        if self.big_map_icon != other.big_map_icon:
            return False
        if self.can_teleport_to != other.can_teleport_to:
            return False
        if self.conquest_visible != other.conquest_visible:
            return False
        return True
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_int32(f, self.map_index)
        BinaryWriter.write_int32(f, len(self.collect_quest_indexes))
        for quest_index in self.collect_quest_indexes:
            BinaryWriter.write_int32(f, quest_index)
        BinaryWriter.write_int32(f, len(self.finish_quest_indexes))
        for quest_index in self.finish_quest_indexes:
            BinaryWriter.write_int32(f, quest_index)
        BinaryWriter.write_string(f, self.file_name)
        BinaryWriter.write_string(f, self.name)
        self.location.write(f)
        BinaryWriter.write_uint16(f, self.image)
        BinaryWriter.write_uint16(f, self.rate)
        BinaryWriter.write_bool(f, self.time_visible)
        BinaryWriter.write_byte(f, self.hour_start)
        BinaryWriter.write_byte(f, self.minute_start)
        BinaryWriter.write_byte(f, self.hour_end)
        BinaryWriter.write_byte(f, self.minute_end)
        BinaryWriter.write_int16(f, self.min_lev)
        BinaryWriter.write_int16(f, self.max_lev)
        BinaryWriter.write_string(f, self.day_of_week)
        BinaryWriter.write_string(f, self.class_required)
        BinaryWriter.write_int32(f, self.conquest)
        BinaryWriter.write_int32(f, self.flag_needed)
        BinaryWriter.write_bool(f, self.show_on_big_map)
        BinaryWriter.write_int32(f, self.big_map_icon)
        BinaryWriter.write_bool(f, self.can_teleport_to)
        BinaryWriter.write_bool(f, self.conquest_visible)


    @staticmethod
    def read(f):
        """读取NPC信息"""
        try:
            npc = NPC()
            
            # 读取基本信息
            npc.index = BinaryReader.read_int32(f)
            print(f"读取NPC索引: {npc.index}")
            
            npc.map_index = BinaryReader.read_int32(f)
            print(f"读取地图索引: {npc.map_index}")
            
            # 读取任务索引列表
            collect_count = BinaryReader.read_int32(f)
            print(f"收集任务数量: {collect_count}")
            for i in range(collect_count):
                quest_index = BinaryReader.read_int32(f)
                npc.collect_quest_indexes.append(quest_index)
                
            finish_count = BinaryReader.read_int32(f)
            print(f"完成任务数量: {finish_count}")
            for i in range(finish_count):
                quest_index = BinaryReader.read_int32(f)
                npc.finish_quest_indexes.append(quest_index)
                
            npc.file_name = BinaryReader.read_string(f)
            print(f"读取文件名: {npc.file_name}")
            
            npc.name = BinaryReader.read_string(f)
            print(f"读取名称: {npc.name}")
            
            # 读取位置
            x = BinaryReader.read_int32(f)
            y = BinaryReader.read_int32(f)
            npc.location = Point(x, y)
            print(f"读取位置: ({x}, {y})")
            
            npc.image = BinaryReader.read_uint16(f)
            print(f"读取图像ID: {npc.image}")
            
            npc.rate = BinaryReader.read_uint16(f)
            print(f"读取比率: {npc.rate}")
            
            npc.time_visible = BinaryReader.read_bool(f)
            npc.hour_start = BinaryReader.read_byte(f)
            npc.minute_start = BinaryReader.read_byte(f)
            npc.hour_end = BinaryReader.read_byte(f)
            npc.minute_end = BinaryReader.read_byte(f)
            npc.min_lev = BinaryReader.read_int16(f)
            npc.max_lev = BinaryReader.read_int16(f)
            npc.day_of_week = BinaryReader.read_string(f)
            npc.class_required = BinaryReader.read_string(f)
            
            npc.conquest = BinaryReader.read_int32(f)
                
            npc.flag_needed = BinaryReader.read_int32(f)
                
            npc.show_on_big_map = BinaryReader.read_bool(f)
            npc.big_map_icon = BinaryReader.read_int32(f)
            
            npc.can_teleport_to = BinaryReader.read_bool(f)
                
            npc.conquest_visible = BinaryReader.read_bool(f)
                
            return npc
        except Exception as e:
            print(f"读取NPC信息时出错: {str(e)}")
            raise