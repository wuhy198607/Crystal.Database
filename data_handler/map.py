from dataclasses import dataclass, field
from typing import List, Optional
from binary import BinaryReader, BinaryWriter
from common import Point

@dataclass
class SafeZoneInfo:
    location: Point = field(default_factory=Point)
    size: int = 0  # 应该是uint16
    start_point: bool = False
    def write(self,f):
        self.location.write(f)
        BinaryWriter.write_uint16(f, self.size)
        BinaryWriter.write_bool(f, self.start_point)


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
    def write(self,f):
        BinaryWriter.write_int32(f, self.map_index)
        self.source.write(f)
        self.destination.write(f)
        BinaryWriter.write_bool(f, self.need_hole)
        BinaryWriter.write_bool(f, self.need_move)
        BinaryWriter.write_int32(f, self.conquest_index)    
        BinaryWriter.write_bool(f, self.show_on_big_map)
        BinaryWriter.write_int32(f, self.icon)
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
    def write(self,f):
        BinaryWriter.write_int32(f, self.monster_index)
        self.location.write(f)
        BinaryWriter.write_uint16(f, self.count)
        BinaryWriter.write_uint16(f, self.spread)
        BinaryWriter.write_uint16(f, self.delay)
        BinaryWriter.write_byte(f, self.direction)
        BinaryWriter.write_string(f, self.route_path)
        BinaryWriter.write_uint16(f, self.random_delay)
        BinaryWriter.write_int32(f, self.respawn_index)
        BinaryWriter.write_bool(f, self.save_respawn_time)
        BinaryWriter.write_uint16(f, self.respawn_ticks)

@dataclass
class MineZone:
    location: Point = field(default_factory=Point)
    size: int = 0
    mine_index: int = 0
    def write(self,f):
        self.location.write(f)
        BinaryWriter.write_int32(f,self.size)
        BinaryWriter.write_byte(f,self.mine_index)

@dataclass
class Map:
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
        
        self.safe_zones: List[SafeZoneInfo] = []
        self.movements: List[MovementInfo] = []
        self.respawns: List[RespawnInfo] = []
        self.mine_zones: List[MineZone] = []
        self.weather_particles = 0  
    def write(self, f):
        """写入地图信息"""
        # 写入基本信息
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_string(f, self.filename)
        BinaryWriter.write_string(f, self.title)
        BinaryWriter.write_uint16(f, self.mini_map)
        BinaryWriter.write_byte(f, self.light)
        BinaryWriter.write_uint16(f, self.big_map)

        # 写入安全区
        BinaryWriter.write_int32(f, len(self.safe_zones))
        for safe_zone in self.safe_zones:
            safe_zone.write(f)

        # 写入重生点
        BinaryWriter.write_int32(f, len(self.respawns))
        for respawn in self.respawns:
            respawn.write(f)

        # 写入移动点
        BinaryWriter.write_int32(f, len(self.movements))
        for movement in self.movements:
            movement.write(f)

        # 写入布尔属性
        BinaryWriter.write_bool(f, self.no_teleport)
        BinaryWriter.write_bool(f, self.no_reconnect)
        BinaryWriter.write_string(f, self.no_reconnect_map)
        BinaryWriter.write_bool(f, self.no_random)
        BinaryWriter.write_bool(f, self.no_escape)
        BinaryWriter.write_bool(f, self.no_recall)
        BinaryWriter.write_bool(f, self.no_drug)
        BinaryWriter.write_bool(f, self.no_position)
        BinaryWriter.write_bool(f, self.no_throw_item)
        BinaryWriter.write_bool(f, self.no_drop_player)
        BinaryWriter.write_bool(f, self.no_drop_monster)
        BinaryWriter.write_bool(f, self.no_names)
        BinaryWriter.write_bool(f, self.fight)
        BinaryWriter.write_bool(f, self.fire)
        BinaryWriter.write_int32(f, self.fire_damage)
        BinaryWriter.write_bool(f, self.lightning)
        BinaryWriter.write_int32(f, self.lightning_damage)
        BinaryWriter.write_byte(f, self.map_dark_light)

        # 写入矿区
        BinaryWriter.write_int32(f, len(self.mine_zones))
        for mine_zone in self.mine_zones:
            mine_zone.write(f)

        # 写入其他属性
        BinaryWriter.write_byte(f, self.mine_index)
        BinaryWriter.write_bool(f, self.no_mount)
        BinaryWriter.write_bool(f, self.need_bridle)
        BinaryWriter.write_bool(f, self.no_fight)
        BinaryWriter.write_uint16(f, self.music)

        # 写入版本相关属性
        BinaryWriter.write_bool(f, self.no_town_teleport)
        BinaryWriter.write_bool(f, self.no_reincarnation)
        BinaryWriter.write_uint16(f, self.weather_particles)
        BinaryWriter.write_bool(f, self.gt)
        BinaryWriter.write_byte(f, self.gt_index)

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

    @staticmethod
    def read_safe_zone(f):
        """读取安全区信息"""
        try:
            safe_zone = SafeZoneInfo()
            safe_zone.location = Point.read_point(f)
            safe_zone.size = BinaryReader.read_uint16(f)  # 修正为uint16
            safe_zone.start_point = BinaryReader.read_bool(f)  # 修正为bool
            return safe_zone
        except Exception as e:
            print(f"读取安全区信息时出错: {str(e)}")
            raise
    @staticmethod
    def read_respawn_info( f):
        """读取重生点信息"""
        try:
            respawn = RespawnInfo()
            
            # 基本字段
            respawn.monster_index = BinaryReader.read_int32(f)
            respawn.location = Point.read_point(f)
            respawn.count = BinaryReader.read_uint16(f)  # 使用uint16
            respawn.spread = BinaryReader.read_uint16(f)  # 使用uint16
            respawn.delay = BinaryReader.read_uint16(f)   # 使用uint16
            respawn.direction = BinaryReader.read_byte(f)  # 使用byte
            respawn.route_path = BinaryReader.read_string(f)
            
            # 版本相关字段
            respawn.random_delay = BinaryReader.read_uint16(f)  # 使用uint16
            respawn.respawn_index = BinaryReader.read_int32(f)
            respawn.save_respawn_time = BinaryReader.read_bool(f)
            respawn.respawn_ticks = BinaryReader.read_uint16(f)  # 使用uint16
            
            return respawn
        except Exception as e:
            print(f"读取重生点信息时出错: {str(e)}")
            raise
        
    @staticmethod
    def read_movement_info(f):    
        """读取移动点信息"""
        try:
            movement = MovementInfo()
            movement.map_index = BinaryReader.read_int32(f)
            movement.source = Point.read_point(f)
            movement.destination = Point.read_point(f)
            movement.need_hole = BinaryReader.read_bool(f)
            movement.need_move = BinaryReader.read_bool(f)
            
            # 版本相关字段
            movement.conquest_index = BinaryReader.read_int32(f)
            movement.show_on_big_map = BinaryReader.read_bool(f)
            movement.icon = BinaryReader.read_int32(f)
                
            return movement
        except Exception as e:
            print(f"读取移动点信息时出错: {str(e)}")
            raise
    @staticmethod
    def read_mine_zone( f):
        """读取矿区信息"""
        try:
            mine_zone = MineZone()
            mine_zone.location = Point.read_point(f)
            mine_zone.size = BinaryReader.read_int32(f)
            mine_zone.mine_index = BinaryReader.read_byte(f)
            return mine_zone
        except Exception as e:
            print(f"读取矿区信息时出错: {str(e)}")
            raise
    @staticmethod
    def read(f):
        """读取地图信息"""
        try:
            map_info = Map()
            print(f"\n开始读取地图信息:")
            
            # 读取基本信息
            try:
                map_info.index = BinaryReader.read_int32(f)
                print(f"地图索引: {map_info.index}")
                
                map_info.filename = BinaryReader.read_string(f)
                print(f"文件名: {map_info.filename}")
                
                map_info.title = BinaryReader.read_string(f)
                print(f"标题: {map_info.title}")
                
                map_info.mini_map = BinaryReader.read_uint16(f)
                print(f"小地图: {map_info.mini_map}")
                
                map_info.light = BinaryReader.read_byte(f)
                print(f"光照设置: {map_info.light}")
                
                map_info.big_map = BinaryReader.read_uint16(f)
                print(f"大地图: {map_info.big_map}")
            except Exception as e:
                print(f"读取基本信息时出错: {str(e)}")
                raise
            
            # 读取安全区
            try:
                safe_zone_count = BinaryReader.read_int32(f)
                print(f"\n安全区数量: {safe_zone_count}")
                
                for i in range(safe_zone_count):
                    safe_zone = Map.read_safe_zone(f)
                    map_info.safe_zones.append(safe_zone)
            except Exception as e:
                print(f"读取安全区信息时出错: {str(e)}")
                raise
            
            # 读取重生点
            try:
                respawn_count = BinaryReader.read_int32(f)
                print(f"\n重生点数量: {respawn_count}")
                for i in range(respawn_count):
                    respawn = Map.read_respawn_info(f)
                    map_info.respawns.append(respawn)
            except Exception as e:
                print(f"读取重生点信息时出错: {str(e)}")
                raise
            
            # 读取移动点
            try:
                movement_count = BinaryReader.read_int32(f)
                print(f"\n移动点数量: {movement_count}")
                
                for i in range(movement_count):
                    movement = Map.read_movement_info(f)
                    map_info.movements.append(movement)
            except Exception as e:
                print(f"读取移动点信息时出错: {str(e)}")
                raise
            
            # 读取布尔属性
            try:
                map_info.no_teleport = BinaryReader.read_bool(f)
                map_info.no_reconnect = BinaryReader.read_bool(f)
                map_info.no_reconnect_map = BinaryReader.read_string(f)
                map_info.no_random = BinaryReader.read_bool(f)
                map_info.no_escape = BinaryReader.read_bool(f)
                map_info.no_recall = BinaryReader.read_bool(f)
                map_info.no_drug = BinaryReader.read_bool(f)
                map_info.no_position = BinaryReader.read_bool(f)
                map_info.no_throw_item = BinaryReader.read_bool(f)
                map_info.no_drop_player = BinaryReader.read_bool(f)
                map_info.no_drop_monster = BinaryReader.read_bool(f)
                map_info.no_names = BinaryReader.read_bool(f)
                map_info.fight = BinaryReader.read_bool(f)
                map_info.fire = BinaryReader.read_bool(f)
                map_info.fire_damage = BinaryReader.read_int32(f)
                map_info.lightning = BinaryReader.read_bool(f)
                map_info.lightning_damage = BinaryReader.read_int32(f)
                map_info.map_dark_light = BinaryReader.read_byte(f)
                print("布尔属性读取完成")
            except Exception as e:
                print(f"读取布尔属性时出错: {str(e)}")
                raise
            
            # 读取矿区
            try:
                mine_zone_count = BinaryReader.read_int32(f)
                print(f"读取矿区数量: {mine_zone_count}")
                for i in range(mine_zone_count):
                    try:
                        mine_zone = Map.read_mine_zone(f)
                        map_info.mine_zones.append(mine_zone)
                        print(f"读取矿区 {i+1}/{mine_zone_count}")
                    except Exception as e:
                        print(f"读取矿区 {i+1} 时出错: {str(e)}")
                        raise
            except Exception as e:
                print(f"读取矿区信息时出错: {str(e)}")
                raise
            
            try:
                map_info.mine_index = BinaryReader.read_byte(f)
                map_info.no_mount = BinaryReader.read_bool(f)
                map_info.need_bridle = BinaryReader.read_bool(f)
                map_info.no_fight = BinaryReader.read_bool(f)
                map_info.music = BinaryReader.read_uint16(f)
                print("其他属性读取完成")
            except Exception as e:
                print(f"读取其他属性时出错: {str(e)}")
                raise
            
            # 版本相关的额外属性
            try:
                map_info.no_town_teleport = BinaryReader.read_bool(f)
                    
                map_info.no_reincarnation = BinaryReader.read_bool(f)
                    
                map_info.weather_particles = BinaryReader.read_uint16(f)
                    
                map_info.gt = BinaryReader.read_bool(f)
                map_info.gt_index = BinaryReader.read_byte(f)
                print("版本相关属性读取完成")
            except Exception as e:
                print(f"读取版本相关属性时出错: {str(e)}")
                raise
            
            return map_info
        
        except Exception as e:
            print(f"读取地图信息时出错: {str(e)}")
            raise
