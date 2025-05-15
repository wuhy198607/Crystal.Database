from dataclasses import dataclass, field
from typing import List, Dict
from binary import BinaryReader,BinaryWriter
from enum import Enum
from item import Item
from monster import Monster 
@dataclass
@dataclass
class QuestType(Enum):
    General = 0
    Daily = 1
    Weekly = 2
    Repeatable = 3
    Story = 4
    Achievement = 5
    Tutorial = 6
    def write(self,f):
        BinaryWriter.write_byte(f, self.value)
@dataclass
class QuestItemTask:
    item: 'Item' = None
    count: int = 0
    message: str = ""
    def compare(self,other: 'QuestItemTask'):
        if self.item != other.item:
            return False
        if self.count != other.count:
            return False
        if self.message != other.message:
            return False
        return True
    def write(self,f):
        self.item.write(f)
        BinaryWriter.write_int32(f, self.count)
        BinaryWriter.write_string(f, self.message)
@dataclass
class QuestKillTask:
    monster: 'Monster' = None
    count: int = 0
    message: str = ""
    def compare(self,other: 'QuestKillTask'):
        if self.monster != other.monster:
            return False
        if self.count != other.count:
            return False
        if self.message != other.message:
            return False
        return True
    def write(self,f):
        self.monster.write(f)
        BinaryWriter.write_int32(f, self.count)
        BinaryWriter.write_string(f, self.message)
@dataclass
class QuestFlagTask:
    number: int = 0
    message: str = ""
    def write(self,f):
        BinaryWriter.write_int32(f, self.number)
        BinaryWriter.write_string(f, self.message)
@dataclass
class QuestItemReward:
    item: 'Item' = None
    count: int = 0
    def write(self,f):
        self.item.write(f)
        BinaryWriter.write_int32(f, self.count)
@dataclass  
class RequiredClass(Enum):
    None_ = 0
    Warrior = 1
    Wizard = 2
    Taoist = 3
    Assassin = 4
    Archer = 5
    def write(self,f):
        BinaryWriter.write_byte(f, self.value)
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
    def compare(self,other: 'Quest'):
        if self.index != other.index:
            return False
        if self.name != other.name:
            return False
        if self.group != other.group:
            return False
        if self.file_name != other.file_name:
            return False
        if self.required_min_level != other.required_min_level:
            return False
        if self.required_max_level != other.required_max_level:
            return False
        if self.required_quest != other.required_quest:
            return False
        if self.required_class != other.required_class:
            return False
        if self.type != other.type:
            return False
        if self.goto_message != other.goto_message:
            return False
        if self.kill_message != other.kill_message:
            return False
        if self.item_message != other.item_message:
            return False
        if self.flag_message != other.flag_message:
            return False
        if self.time_limit_in_seconds != other.time_limit_in_seconds:
            return False
        if len(self.description) != len(other.description):
            return False
        for i, desc in enumerate(self.description):
            if desc != other.description[i]:
                return False
        if len(self.task_description) != len(other.task_description):
            return False
        for i, task in enumerate(self.task_description):
            if task != other.task_description[i]:
                return False
        if len(self.return_description) != len(other.return_description):
            return False
        for i, desc in enumerate(self.return_description):
            if desc != other.return_description[i]:
                return False
        if len(self.completion_description) != len(other.completion_description):
            return False
        for i, desc in enumerate(self.completion_description):
            if desc != other.completion_description[i]:
                return False
        if len(self.carry_items) != len(other.carry_items):
            return False
        for i, item in enumerate(self.carry_items):
            if not item.compare(other.carry_items[i]):
                return False
        if len(self.kill_tasks) != len(other.kill_tasks):
            return False
        for i, task in enumerate(self.kill_tasks):
            if not task.compare(other.kill_tasks[i]):
                return False
        if len(self.item_tasks) != len(other.item_tasks):
            return False
        for i, task in enumerate(self.item_tasks):
            if not task.compare(other.item_tasks[i]):
                return False
        if len(self.flag_tasks) != len(other.flag_tasks):
            return False

        return True
    def write(self,f):
        BinaryWriter.write_int32(f, self.index)
        BinaryWriter.write_string(f, self.name)
        BinaryWriter.write_string(f, self.group)
        BinaryWriter.write_string(f, self.file_name)
        BinaryWriter.write_int32(f, self.required_min_level)    
        BinaryWriter.write_int32(f, self.required_max_level)
        BinaryWriter.write_int32(f, self.required_quest)
        self.required_class.write(f)
        self.type.write(f)
        BinaryWriter.write_string(f, self.goto_message)
        BinaryWriter.write_string(f, self.kill_message)
        BinaryWriter.write_string(f, self.item_message)
        BinaryWriter.write_string(f, self.flag_message)
        BinaryWriter.write_int32(f, self.time_limit_in_seconds)
        
            
        
        
    @staticmethod
    def read(f):
        """读取任务信息"""
        try:
            quest = Quest()
            
            # 读取基本信息
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
            raise
    