from dataclasses import dataclass, field
from typing import List, Dict
from binary import BinaryReader
from enum import Enum
from item import Item
from monster import Monster 

class QuestType(Enum):
    General = 0
    Daily = 1
    Weekly = 2
    Repeatable = 3
    Story = 4
    Achievement = 5
    Tutorial = 6

@dataclass
class QuestItemTask:
    item: 'Item' = None
    count: int = 0
    message: str = ""

@dataclass
class QuestKillTask:
    monster: 'Monster' = None
    count: int = 0
    message: str = ""

@dataclass
class QuestFlagTask:
    number: int = 0
    message: str = ""

@dataclass
class QuestItemReward:
    item: 'Item' = None
    count: int = 0
@dataclass  
class RequiredClass(Enum):
    None_ = 0
    Warrior = 1
    Wizard = 2
    Taoist = 3
    Assassin = 4
    Archer = 5
@dataclass
class Quest:
    index: int = 0
    name: str = ""
    group: str = ""
    file_name: str = ""
    required_min_level: int = 0
    required_max_level: int = 0
    required_quest: int = 0
    required_class: RequiredClass = field(default_factory=lambda: RequiredClass.None_)
    type: QuestType = field(default_factory=lambda: QuestType.General)  
    goto_message: str = ""
    kill_message: str = ""
    item_message: str = ""
    flag_message: str = ""
    time_limit_in_seconds: int = 0
    
    # 任务描述
    description: List[str] = field(default_factory=list)
    task_description: List[str] = field(default_factory=list)
    return_description: List[str] = field(default_factory=list)
    completion_description: List[str] = field(default_factory=list)
    
    # 任务物品
    carry_items: List[QuestItemTask] = field(default_factory=list)
    
    # 任务目标
    kill_tasks: List[QuestKillTask] = field(default_factory=list)
    item_tasks: List[QuestItemTask] = field(default_factory=list)
    flag_tasks: List[QuestFlagTask] = field(default_factory=list)
    
    # 任务奖励
    gold_reward: int = 0
    exp_reward: int = 0
    credit_reward: int = 0
    fixed_rewards: List[QuestItemReward] = field(default_factory=list)  
    select_rewards: List[QuestItemReward] = field(default_factory=list)
        
    @staticmethod
    def read(f):
        """读取任务信息"""
        try:
            quest = Quest()
            
            # 读取基本信息
            print(f"\n开始读取任务信息，当前位置: {f.tell()}")
            quest.index = BinaryReader.read_int32(f)
            print(f"读取任务索引: {quest.index}")
            
            quest.name = BinaryReader.read_string(f)
            print(f"读取任务名称: {quest.name}")
            
            quest.group = BinaryReader.read_string(f)
            print(f"读取任务组: {quest.group}")
            
            quest.file_name = BinaryReader.read_string(f)
            print(f"读取文件名: {quest.file_name}")
            
            quest.required_min_level = BinaryReader.read_int32(f)
            print(f"读取最低等级要求: {quest.required_min_level}")
            
            quest.required_max_level = BinaryReader.read_int32(f)
            if quest.required_max_level == 0:
                quest.required_max_level = 65535  # ushort.MaxValue
            print(f"读取最高等级要求: {quest.required_max_level}")
            
            quest.required_quest = BinaryReader.read_int32(f)
            print(f"读取前置任务: {quest.required_quest}")
            
            # 读取职业要求，如果值无效则设置为None
            try:
                required_class_value = BinaryReader.read_byte(f)
                print(f"读取byte原始字节: {required_class_value:02x}")
                quest.required_class = RequiredClass(required_class_value)
            except ValueError:
                print(f"警告: 无效的职业要求值 {required_class_value}，将设置为 None")
                quest.required_class = RequiredClass.None_
            print(f"读取职业要求: {quest.required_class}")
            
            # 读取任务类型，如果值无效则设置为General
            try:
                quest_type_value = BinaryReader.read_byte(f)
                quest.type = QuestType(quest_type_value)
            except ValueError:
                print(f"警告: 无效的任务类型值 {quest_type_value}，将设置为 General")
                quest.type = QuestType.General
            print(f"读取任务类型: {quest.type}")
            
            quest.goto_message = BinaryReader.read_string(f)
            print(f"读取前往消息: {quest.goto_message}")
            
            quest.kill_message = BinaryReader.read_string(f)
            print(f"读取击杀消息: {quest.kill_message}")
            
            quest.item_message = BinaryReader.read_string(f)
            print(f"读取物品消息: {quest.item_message}")
            
            quest.flag_message = BinaryReader.read_string(f)
            print(f"读取标记消息: {quest.flag_message}")
            
        
            quest.time_limit_in_seconds = BinaryReader.read_int32(f)
            print(f"读取时间限制: {quest.time_limit_in_seconds}")
   
            
            return quest
        except Exception as e:
            print(f"读取任务信息时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise
    