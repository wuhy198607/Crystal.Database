from dataclasses import dataclass, field
from typing import List, Optional, Dict
from binary import BinaryReader,BinaryWriter

@dataclass
class RespawnTickOption:
    user_count: int = 1
    delay_loss: float = 1.0
    def write(self,f):
        BinaryWriter.write_int32(f, self.user_count)
        BinaryWriter.write_float(f, self.delay_loss)
    

@dataclass
class RespawnTimer:
    base_spawn_rate: int = 20  # 基础刷新率（分钟）
    current_tick_counter: int = 0  # 当前刷新计数器
    last_tick: int = 0  # 上次刷新时间
    last_user_count: int = 0  # 上次用户数量
    current_delay: int = 0  # 当前延迟
    respawn_options: List[RespawnTickOption] = field(default_factory=list)
    def write(self,f):
        BinaryWriter.write_byte(f, self.base_spawn_rate)
        BinaryWriter.write_uint64(f, self.current_tick_counter)
        BinaryWriter.write_uint64(f, self.last_tick)
        BinaryWriter.write_int32(f, self.last_user_count)
        BinaryWriter.write_int32(f, self.current_delay)
        BinaryWriter.write_int32(f, len(self.respawn_options))
        for option in self.respawn_options:
            option.write(f)
        
    @staticmethod
    def read(f):
        """读取刷新计时器信息"""
        try:
            respawn = RespawnTimer()
            
            # 读取基本信息
            print(f"\n开始读取刷新计时器信息，当前位置: {f.tell()}")
            respawn.base_spawn_rate = BinaryReader.read_byte(f)
            print(f"读取基础刷新率: {respawn.base_spawn_rate}")
            
            respawn.current_tick_counter = BinaryReader.read_uint64(f)
            print(f"读取当前刷新计数器: {respawn.current_tick_counter}")
            
            # 读取刷新选项列表
            option_count = BinaryReader.read_int32(f)
            print(f"读取刷新选项数量: {option_count}")
            
            for i in range(option_count):
                option = RespawnTickOption()
                option.user_count = BinaryReader.read_int32(f)
                option.delay_loss = BinaryReader.read_float(f)
                respawn.respawn_options.append(option)
                print(f"读取刷新选项 {i+1}/{option_count}:")
                print(f"  用户数量: {option.user_count}")
                print(f"  延迟损失: {option.delay_loss}")
            
            # 计算当前延迟
            respawn.current_delay = int(round(respawn.base_spawn_rate * 60000))
            print(f"计算当前延迟: {respawn.current_delay}")
            
            return respawn
        except Exception as e:
            print(f"读取刷新计时器信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise 