from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from binary import BinaryReader,BinaryWriter
from map import Point

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
class ConquestArcherInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        self.location.write(f)
        BinaryWriter.write_int32(f, self.mob_index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_int32(f, self.repair_cost)

@dataclass
class ConquestGateInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        self.location.write(f)
        BinaryWriter.write_int32(f, self.mob_index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_int32(f, self.repair_cost)


@dataclass
class ConquestWallInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        self.location.write(f)
        BinaryWriter.write_int32(f, self.mob_index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_int32(f, self.repair_cost)


@dataclass
class ConquestSiegeInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    mob_index: int = 0
    name: str = ""
    repair_cost: int = 0
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        self.location.write(f)
        BinaryWriter.write_int32(f, self.mob_index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_int32(f, self.repair_cost)


@dataclass
class ConquestFlagInfo:
    index: int = 0
    location: Point = field(default_factory=Point)
    name: str = ""
    file_name: str = ""
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        self.location.write(f)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_string(f, self.file_name)
    

@dataclass
class Conquest:
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
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_bool(f, self.full_map)
        self.location.write(f)
        BinaryWriter.write_uint16(f, self.size)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_int32(f, self.map_index)
        BinaryWriter.write_int32(f, self.palace_index)
        BinaryWriter.write_int32(f, self.guard_index)
        BinaryWriter.write_int32(f, self.gate_index)
        BinaryWriter.write_int32(f, self.wall_index)
        BinaryWriter.write_int32(f, self.siege_index)
        BinaryWriter.write_int32(f, self.flag_index)
        BinaryWriter.write_int32(f, len(self.conquest_guards))
        for guard in self.conquest_guards:
            guard.write(f)
        BinaryWriter.write_int32(f, len(self.extra_maps))
        for map_index in self.extra_maps:
            BinaryWriter.write_int32(f, map_index)  
        BinaryWriter.write_int32(f, len(self.conquest_gates))
        for gate in self.conquest_gates:
            gate.write(f) 
        BinaryWriter.write_int32(f, len(self.conquest_walls))
        for wall in self.conquest_walls:
            wall.write(f)
        BinaryWriter.write_int32(f, len(self.conquest_sieges))
        for siege in self.conquest_sieges:
            siege.write(f)
        BinaryWriter.write_int32(f, len(self.conquest_flags))
        for flag in self.conquest_flags:
            flag.write(f)
        BinaryWriter.write_byte(f, self.start_hour)
        BinaryWriter.write_int32(f, self.war_length)
        BinaryWriter.write_byte(f, self.type.value)
        BinaryWriter.write_byte(f, self.game.value)
        BinaryWriter.write_bool(f, self.monday) 
        BinaryWriter.write_bool(f, self.tuesday)
        BinaryWriter.write_bool(f, self.wednesday)
        BinaryWriter.write_bool(f, self.thursday)
        BinaryWriter.write_bool(f, self.friday)
        BinaryWriter.write_bool(f, self.saturday)
        BinaryWriter.write_bool(f, self.sunday) 
        self.king_location.write(f)
        BinaryWriter.write_uint16(f, self.king_size)
        BinaryWriter.write_int32(f, self.control_point_index)
        BinaryWriter.write_int32(f, len(self.control_points))
        for point in self.control_points:
            point.write(f)  
        
        
    @staticmethod
    def read(f):
        """读取征服信息"""
        try:
            conquest = Conquest()
            
            # 读取基本信息
            conquest.index = BinaryReader.read_int32(f)
            print(f"读取索引: {conquest.index}")
            
            conquest.full_map = BinaryReader.read_bool(f)
            print(f"读取全地图: {conquest.full_map}")
        
            conquest.location = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取位置: ({conquest.location.x}, {conquest.location.y})")
            
            conquest.size = BinaryReader.read_uint16(f)
            print(f"读取大小: {conquest.size}")
            
            conquest.name = BinaryReader.read_string(f)
            print(f"读取名称: {conquest.name}")
            
            conquest.map_index = BinaryReader.read_int32(f)
            print(f"读取地图索引: {conquest.map_index}")
            
            conquest.palace_index = BinaryReader.read_int32(f)
            print(f"读取宫殿索引: {conquest.palace_index}")
            
            conquest.guard_index = BinaryReader.read_int32(f)
            print(f"读取守卫索引: {conquest.guard_index}")
            
            conquest.gate_index = BinaryReader.read_int32(f)
            print(f"读取城门索引: {conquest.gate_index}")
            
            conquest.wall_index = BinaryReader.read_int32(f)
            print(f"读取城墙索引: {conquest.wall_index}")
            
            conquest.siege_index = BinaryReader.read_int32(f)
            print(f"读取攻城索引: {conquest.siege_index}")
            
            conquest.flag_index = BinaryReader.read_int32(f)
            print(f"读取旗帜索引: {conquest.flag_index}")
            
            # 读取守卫列表
            guard_count = BinaryReader.read_int32(f)
            print(f"读取守卫数量: {guard_count}")
            for i in range(guard_count):
                guard = ConquestArcherInfo()
                guard.index = BinaryReader.read_int32(f)
                guard.location = Point(
                    x=BinaryReader.read_int32(f),
                    y=BinaryReader.read_int32(f)
                )
                guard.mob_index = BinaryReader.read_int32(f)
                guard.name = BinaryReader.read_string(f)
                guard.repair_cost = BinaryReader.read_uint32(f)
                conquest.conquest_guards.append(guard)
            
            # 读取额外地图列表
            map_count = BinaryReader.read_int32(f)
            print(f"读取额外地图数量: {map_count}")
            for i in range(map_count):
                map_index = BinaryReader.read_int32(f)
                conquest.extra_maps.append(map_index)
            
            # 读取城门列表
            gate_count = BinaryReader.read_int32(f)
            print(f"读取城门数量: {gate_count}")
            for i in range(gate_count):
                gate = ConquestGateInfo()
                gate.index = BinaryReader.read_int32(f)
                gate.location = Point(
                    x=BinaryReader.read_int32(f),
                    y=BinaryReader.read_int32(f)
                )
                gate.mob_index = BinaryReader.read_int32(f)
                gate.name = BinaryReader.read_string(f)
                gate.repair_cost = BinaryReader.read_int32(f)
                conquest.conquest_gates.append(gate)
            
            # 读取城墙列表
            wall_count = BinaryReader.read_int32(f)
            print(f"读取城墙数量: {wall_count}")
            for i in range(wall_count):
                wall = ConquestWallInfo()
                wall.index = BinaryReader.read_int32(f)
                wall.location = Point(
                    x=BinaryReader.read_int32(f),
                    y=BinaryReader.read_int32(f)
                )
                wall.mob_index = BinaryReader.read_int32(f)
                wall.name = BinaryReader.read_string(f)
                wall.repair_cost = BinaryReader.read_int32(f)
                conquest.conquest_walls.append(wall)
            
            # 读取攻城列表
            siege_count = BinaryReader.read_int32(f)
            print(f"读取攻城数量: {siege_count}")
            for i in range(siege_count):
                siege = ConquestSiegeInfo()
                siege.index = BinaryReader.read_int32(f)
                siege.location = Point(
                    x=BinaryReader.read_int32(f),
                    y=BinaryReader.read_int32(f)
                )
                siege.mob_index = BinaryReader.read_int32(f)
                siege.name = BinaryReader.read_string(f)
                siege.repair_cost = BinaryReader.read_int32(f)
                conquest.conquest_sieges.append(siege)
            
            # 读取旗帜列表
            flag_count = BinaryReader.read_int32(f)
            print(f"读取旗帜数量: {flag_count}")
            for i in range(flag_count):
                flag = ConquestFlagInfo()
                flag.index = BinaryReader.read_int32(f)
                flag.location = Point(
                    x=BinaryReader.read_int32(f),
                    y=BinaryReader.read_int32(f)
                )
                flag.name = BinaryReader.read_string(f)
                flag.file_name = BinaryReader.read_string(f)
                conquest.conquest_flags.append(flag)
            
            # 读取其他信息
            conquest.start_hour = BinaryReader.read_byte(f)
            print(f"读取开始时间: {conquest.start_hour}")
            
            conquest.war_length = BinaryReader.read_int32(f)
            print(f"读取战争时长: {conquest.war_length}")
            
            conquest.type = ConquestType(BinaryReader.read_byte(f))
            print(f"读取类型: {conquest.type}")
            
            conquest.game = ConquestGame(BinaryReader.read_byte(f))
            print(f"读取游戏模式: {conquest.game}")
            
            conquest.monday = BinaryReader.read_bool(f)
            conquest.tuesday = BinaryReader.read_bool(f)
            conquest.wednesday = BinaryReader.read_bool(f)
            conquest.thursday = BinaryReader.read_bool(f)
            conquest.friday = BinaryReader.read_bool(f)
            conquest.saturday = BinaryReader.read_bool(f)
            conquest.sunday = BinaryReader.read_bool(f)
            print(f"读取星期设置: {conquest.monday}, {conquest.tuesday}, {conquest.wednesday}, {conquest.thursday}, {conquest.friday}, {conquest.saturday}, {conquest.sunday}")
            
            conquest.king_location = Point(
                x=BinaryReader.read_int32(f),
                y=BinaryReader.read_int32(f)
            )
            print(f"读取国王位置: ({conquest.king_location.x}, {conquest.king_location.y})")
            
            conquest.king_size = BinaryReader.read_uint16(f)
            print(f"读取国王区域大小: {conquest.king_size}")
            
            conquest.control_point_index = BinaryReader.read_int32(f)
            print(f"读取控制点索引: {conquest.control_point_index}")
            
            control_point_count = BinaryReader.read_int32(f)
            print(f"读取控制点数量: {control_point_count}")
            for i in range(control_point_count):
                point = ConquestFlagInfo()
                point.index = BinaryReader.read_int32(f)
                point.location = Point(
                    x=BinaryReader.read_int32(f),
                    y=BinaryReader.read_int32(f)
                )
                point.name = BinaryReader.read_string(f)
                point.file_name = BinaryReader.read_string(f)
                conquest.control_points.append(point)
            
            return conquest
        except Exception as e:
            print(f"读取征服信息时出错: {str(e)}")
            raise 