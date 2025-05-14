import struct
import os
import json
import argparse
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import re
from binary import BinaryReader, BinaryWriter
from  map import Map, Point, SafeZoneInfo, MovementInfo, RespawnInfo, MineZone  
from  item import Item,ItemType,ItemGrade,RequiredType,RequiredClass,RequiredGender,ItemSet,BindMode,SpecialItemMode
from  monster import Monster,DropInfo
from  npc import NPC
from quest import Quest, QuestKillTask, QuestFlagTask, QuestItemTask, QuestItemReward, RequiredClass, QuestType
from dragon import Dragon, DragonDropInfo
from magic import Magic, Spell
from gameshop_item import GameShopItem
from conquest import Conquest, ConquestType, ConquestGame, ConquestArcherInfo, ConquestGateInfo, ConquestWallInfo, ConquestSiegeInfo, ConquestFlagInfo
from respawn_timer import RespawnTimer, RespawnTickOption
from common import Stat,Stats

class Settings:
    """设置类，用于定义各种路径"""
    QuestPath = "Quests"  # 任务文件所在目录
    DropPath = "Drops"    # 掉落文件所在目录






class Envir:
    def __init__(self):
        self.version = 0
        self.map_index = 0  
        self.item_index = 0
        self.monster_index = 0
        self.npc_index = 0
        self.quest_index = 0
        self.gameshop_index = 0
        self.conquest_index = 0
        self.respawn_timer_index = 0
        self.custom_version = 0
        self.maps: List[Map] = []
        self.monsters: List[Monster] = []
        self.items: List[Item] = []
        self.npcs: List[NPC] = []
        self.quests: List[Quest] = []
        self.dragons: List[Dragon] = []  # 添加dragon列表
        self.magics: List[Magic] = []  # 添加魔法信息列表
        self.respawn_timers: List[RespawnTimer] = []
        self.conquests: List[Conquest] = []
        self.gameshop_items: List[GameShopItem] = []

    def load_dragon_drops(self, dragon, db_path):
        """加载龙掉落信息"""
        # 清空所有掉落列表
        for level_drops in dragon.drops:
            level_drops.clear()
            
        # 确保掉落文件目录存在
        drop_path = os.path.join(os.path.dirname(db_path), Settings.DropPath)
        if not os.path.exists(drop_path):
            print(f"掉落文件目录不存在: {drop_path}")
            return
            
        file_path = os.path.join(drop_path, "DragonItem.txt")
        if not os.path.exists(file_path):
            print(f"龙掉落文件不存在: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue
                        
                    drop = self.parse_dragon_drop(line)
                    if drop and 0 < drop.level <= len(dragon.drops):
                        dragon.drops[drop.level - 1].append(drop)
                        
            # 对每个等级的掉落列表进行排序
            for level_drops in dragon.drops:
                level_drops.sort(key=lambda d: (d.gold == 0, d.item.type if d.item else 0))
                
        except Exception as e:
            print(f"加载龙掉落信息时出错: {str(e)}")
            raise

    def parse_dragon_drop(self, line):
        """解析龙掉落信息"""
        parts = line.split()
        if len(parts) < 3:
            return None
            
        try:
            drop = DragonDropInfo()
            drop.chance = int(parts[0][2:])  # 跳过前两个字符
            
            if parts[1].lower() == "gold":
                if len(parts) < 4:
                    return None
                drop.gold = int(parts[2])
                drop.level = int(parts[3])
            else:
                drop.item = self.get_item_info(parts[1])
                if not drop.item:
                    return None
                drop.level = int(parts[2])
                
            return drop
        except (ValueError, IndexError):
            return None

    
    def load_quest_info(self, quest, dbpath, clear=False):
        """加载任务详细信息"""
        if clear:
            self.clear_quest_info(quest)
            
        # 确保任务文件目录存在
        quest_path = os.path.join(os.path.dirname(dbpath), Settings.QuestPath)
        if not os.path.exists(quest_path):
            print(f"任务文件目录不存在: {quest_path}")
            return
            
        file_path = os.path.join(quest_path, f"{quest.file_name}.txt")
        if not os.path.exists(file_path):
            print(f"任务文件不存在: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.parse_quest_file(quest, lines)
        except Exception as e:
            print(f"加载任务文件时出错: {str(e)}")
            raise

    def clear_quest_info(self, quest):
        """清除任务信息"""
        quest.description.clear()
        quest.task_description.clear()
        quest.return_description.clear()
        quest.completion_description.clear()
        quest.carry_items.clear()
        quest.kill_tasks.clear()
        quest.item_tasks.clear()
        quest.flag_tasks.clear()
        quest.fixed_rewards.clear()
        quest.select_rewards.clear()
        quest.exp_reward = 0
        quest.gold_reward = 0
        quest.credit_reward = 0

    def parse_quest_file(self,  quest, lines):
        """解析任务文件"""
        description_key = "[@DESCRIPTION]"
        task_key = "[@TASKDESCRIPTION]"
        return_key = "[@RETURNDESCRIPTION]"
        completion_key = "[@COMPLETION]"
        carry_items_key = "[@CARRYITEMS]"
        kill_tasks_key = "[@KILLTASKS]"
        item_tasks_key = "[@ITEMTASKS]"
        flag_tasks_key = "[@FLAGTASKS]"
        fixed_rewards_key = "[@FIXEDREWARDS]"
        select_rewards_key = "[@SELECTREWARDS]"
        exp_reward_key = "[@EXPREWARD]"
        gold_reward_key = "[@GOLDREWARD]"
        credit_reward_key = "[@CREDITREWARD]"
        
        headers = [
            description_key, task_key, completion_key,
            carry_items_key, kill_tasks_key, item_tasks_key, flag_tasks_key,
            fixed_rewards_key, select_rewards_key, exp_reward_key, gold_reward_key, credit_reward_key, return_key
        ]
        
        current_header = 0
        while current_header < len(headers):
            for i in range(len(lines)):
                line = lines[i].strip().upper()
                if line != headers[current_header].upper():
                    continue
                    
                for j in range(i + 1, len(lines)):
                    inner_line = lines[j].strip()
                    if inner_line.startswith('[') or inner_line.startswith('//'):
                        break
                    if not inner_line:
                        continue
                        
                    if line == description_key:
                        quest.description.append(inner_line)
                    elif line == task_key:
                        quest.task_description.append(inner_line)
                    elif line == return_key:
                        quest.return_description.append(inner_line)
                    elif line == completion_key:
                        quest.completion_description.append(inner_line)
                    elif line == carry_items_key:
                        task = self.parse_quest_item(inner_line)
                        if task:
                            quest.carry_items.append(task)
                    elif line == kill_tasks_key:
                        task = self.parse_quest_kill(inner_line)
                        if task:
                            quest.kill_tasks.append(task)
                    elif line == item_tasks_key:
                        task = self.parse_quest_item(inner_line)
                        if task:
                            quest.item_tasks.append(task)
                    elif line == flag_tasks_key:
                        task = self.parse_quest_flag(inner_line)
                        if task:
                            quest.flag_tasks.append(task)
                    elif line == fixed_rewards_key:
                        reward = self.parse_quest_reward(inner_line)
                        if reward:
                            quest.fixed_rewards.append(reward)
                    elif line == select_rewards_key:
                        reward = self.parse_quest_reward(inner_line)
                        if reward:
                            quest.select_rewards.append(reward)
                    elif line == exp_reward_key:
                        quest.exp_reward = int(inner_line)
                    elif line == gold_reward_key:
                        quest.gold_reward = int(inner_line)
                    elif line == credit_reward_key:
                        quest.credit_reward = int(inner_line)
                        
            current_header += 1

    def parse_quest_item(self, line):
        """解析任务物品"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        count = 1
        if len(parts) > 1:
            count = int(parts[1])
            
        message = ""
        match = re.search(r'"([^"]*)"', line)
        if match:
            message = match.group(1)
            
        item_info = self.get_item_info(parts[0])
        if not item_info:
            # 尝试查找性别特定的物品
            item_info = self.get_item_info(f"{parts[0]}(M)")
            if not item_info:
                item_info = self.get_item_info(f"{parts[0]}(F)")
                
        if not item_info:
            return None
            
        return QuestItemTask(item=item_info, count=count, message=message)

    def parse_quest_kill(self, line):
        """解析击杀任务"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        count = 1
        if len(parts) > 1:
            count = int(parts[1])
            
        message = ""
        match = re.search(r'"([^"]*)"', line)
        if match:
            message = match.group(1)
            
        monster_info = self.get_monster_info(parts[0])
        if not monster_info:
            return None
            
        return QuestKillTask(monster=monster_info, count=count, message=message)

    def parse_quest_flag(self, line):
        """解析标记任务"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        number = int(parts[0])
        if number < 0 or number > 1000:  # 假设最大标记数为1000
            return None
            
        message = ""
        match = re.search(r'"([^"]*)"', line)
        if match:
            message = match.group(1)
            
        return QuestFlagTask(number=number, message=message)

    def parse_quest_reward(self, line):
        """解析任务奖励"""
        if not line:
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        count = 1
        if len(parts) > 1:
            count = int(parts[1])
            
        item_info = self.get_item_info(parts[0])
        if not item_info:
            return None
            
        return QuestItemReward(item=item_info, count=count)
    @staticmethod
    def load(db_path):
        
        """加载数据库文件"""
        if not os.path.exists(db_path):
            print(f"数据库文件不存在: {db_path}")
            return None

        try:
            envir =  Envir()
            with open(db_path, 'rb') as f:
                # 读取版本信息
                envir.version = BinaryReader.read_int32(f)
                envir.custom_version = BinaryReader.read_int32(f)
                
                print(f"\n=== 数据库信息 ===")
                print(f"数据库版本: {envir.version}")
                print(f"自定义版本: {envir.custom_version}")

                print("\n=== 索引信息 ===")
                # 读取索引
                envir.map_index = BinaryReader.read_int32(f)
                envir.item_index = BinaryReader.read_int32(f)
                envir.monster_index = BinaryReader.read_int32(f)
                envir.npc_index = BinaryReader.read_int32(f)
                envir.quest_index = BinaryReader.read_int32(f)
                
                print(f"地图索引: {envir.map_index}")
                print(f"物品索引: {envir.item_index}")
                print(f"怪物索引: {envir.monster_index}")
                print(f"NPC索引: {envir.npc_index}")
                print(f"任务索引: {envir.quest_index}")
                
                # 根据版本读取额外索引
                envir.gameshop_index = BinaryReader.read_int32(f)
                envir.conquest_index = BinaryReader.read_int32(f)
                envir.respawn_timer_index = BinaryReader.read_int32(f)
                
                print(f"商店索引: {envir.gameshop_index}")
                    
                print(f"征服索引: {envir.conquest_index}")
                
                print(f"重生索引: {envir.respawn_timer_index}")

                print("\n=== 地图信息 ===")
                # 读取地图信息
                map_count = BinaryReader.read_int32(f)
                print(f"地图总数: {map_count}")
                
                
                for i in range(map_count):
                    try:
                        map_info = Map.read(f)
                        envir.maps.append(map_info)
                        print(f"\n地图 {i+1}/{map_count}:")
                        print(f"  索引: {map_info.index}")
                        print(f"  文件名: {map_info.filename}")
                        print(f"  标题: {map_info.title}")
                        print(f"  小地图: {map_info.mini_map}")
                        print(f"  大地图: {map_info.big_map}")
                        print(f"  安全区域数量: {len(map_info.safe_zones)}")
                        print(f"  重生点数量: {len(map_info.respawns)}")
                        print(f"  移动点数量: {len(map_info.movements)}")
                        print(f"  矿区数量: {len(map_info.mine_zones)}")
                    except Exception as e:
                        print(f"读取地图 {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== 物品信息 ===")
                # 读取物品信息（全量读取）
                item_count = BinaryReader.read_int32(f)
                print(f"物品总数: {item_count}")
                
                for i in range(item_count):
                    try:
                        item_info = Item.read(f)
                        envir.items.append(item_info)
                        print(f"  索引: {item_info.index}")
                        print(f"  名称: {item_info.name}")
                        print(f"  类型: {item_info.type}")
                        print(f"  等级: {item_info.grade}")
                        print(f"  价格: {item_info.price}")
                        print(f"  耐久: {item_info.durability}")
                        print(f"  堆叠: {item_info.stack_size}")
                    except Exception as e:
                        print(f"读取物品 {i+1} 时出错: {str(e)}")
                        continue
                
                print("\n=== 怪物信息 ===")
                # 读取怪物信息（全量读取）
                monster_count = BinaryReader.read_int32(f)
                print(f"怪物总数: {monster_count}")
                
                for i in range(monster_count):
                    try:
                        monster_info = Monster.read(f)
                        envir.monsters.append(monster_info)
                        print(f"\n怪物 {i+1}/{monster_count}:")
                        print(f"  索引: {monster_info.index}")
                        print(f"  名称: {monster_info.name}")
                        print(f"  等级: {monster_info.level}")
                        print(f"  掉落物数量: {len(monster_info.drops)}")
                        print(f"  攻击速度: {monster_info.attack_speed}")
                        print(f"  移动速度: {monster_info.move_speed}")
                        print(f"  经验值: {monster_info.experience}")
                    except Exception as e:
                        print(f"读取怪物 {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== NPC信息 ===")
                # 读取NPC信息
                npc_count = BinaryReader.read_int32(f)
                print(f"NPC总数: {npc_count}")
                
                for i in range(npc_count):
                    try:
                        npc_info = NPC.read(f)
                        envir.npcs.append(npc_info)
                        print(f"\nNPC {i+1}/{npc_count}:")
                        print(f"  索引: {npc_info.index}")
                        print(f"  名称: {npc_info.name}")
                        print(f"  文件名: {npc_info.file_name}")
                        print(f"  地图索引: {npc_info.map_index}")
                        print(f"  位置: ({npc_info.location.x}, {npc_info.location.y})")
                        print(f"  收集任务数量: {len(npc_info.collect_quest_indexes)}")
                        print(f"  完成任务数量: {len(npc_info.finish_quest_indexes)}")
                    except Exception as e:
                        print(f"读取NPC {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== 任务信息 ===")
                # 读取任务信息
                quest_count = BinaryReader.read_int32(f)
                print(f"任务总数: {quest_count}")
                
                for i in range(quest_count):
                    try:
                        quest_info = Quest.read(f)
                        envir.load_quest_info(quest_info,db_path)
                        envir.quests.append(quest_info)
                        print(f"\n任务 {i+1}/{quest_count}:")
                        print(f"  索引: {quest_info.index}")
                        print(f"  名称: {quest_info.name}")
                        print(f"  组: {quest_info.group}")
                        print(f"  类型: {quest_info.type}")
                        print(f"  最低等级: {quest_info.required_min_level}")
                        print(f"  最高等级: {quest_info.required_max_level}")
                        print(f"  前置任务: {quest_info.required_quest}")
                        print(f"  职业要求: {quest_info.required_class}")
                        print(f"  击杀任务数量: {len(quest_info.kill_tasks)}")
                        print(f"  物品任务数量: {len(quest_info.item_tasks)}")
                        print(f"  标记任务数量: {len(quest_info.flag_tasks)}")
                        print(f"  固定奖励数量: {len(quest_info.fixed_rewards)}")
                        print(f"  可选奖励数量: {len(quest_info.select_rewards)}")
                    except Exception as e:
                        print(f"读取任务 {i+1} 时出错: {str(e)}")
                        continue

                print("\n=== 龙信息 ===")
                # 读取龙信息
                try:
                    dragon_info = Dragon.read(f)
                    # 加载掉落信息
                    envir.load_dragon_drops(dragon_info,db_path)
                    envir.dragons.append(dragon_info)
                    print(f"\n龙信息:")
                    print(f"  启用状态: {dragon_info.enabled}")
                    print(f"  地图文件名: {dragon_info.map_file_name}")
                    print(f"  怪物名称: {dragon_info.monster_name}")
                    print(f"  身体名称: {dragon_info.body_name}")
                    print(f"  位置: ({dragon_info.location.x}, {dragon_info.location.y})")
                    print(f"  掉落区域: ({dragon_info.drop_area_top.x}, {dragon_info.drop_area_top.y}) - ({dragon_info.drop_area_bottom.x}, {dragon_info.drop_area_bottom.y})")
                    for j, exp in enumerate(dragon_info.exps):
                        print(f"  等级 {j+1} 经验值: {exp}")
                    for j, level_drops in enumerate(dragon_info.drops):
                        print(f"  等级 {j+1} 掉落数量: {len(level_drops)}")
                except Exception as e:
                    print(f"读取龙信息时出错: {str(e)}")
                    # 移除continue语句

              
                
                print("\n=== 魔法信息 ===")
                # 读取魔法数量
                magic_count = BinaryReader.read_int32(f)
                print(f"魔法数量: {magic_count}")
                
                # 读取魔法信息
                envir.magics = []
                for i in range(magic_count):
                    try:
                        magic_info = Magic.read(f)
                        envir.magics.append(magic_info)
                        print(f"\n魔法信息 {i+1}/{magic_count}:")
                        print(f"  名称: {magic_info.name}")
                        print(f"  类型: {magic_info.spell}")
                        print(f"  基础消耗: {magic_info.base_cost}")
                        print(f"  等级消耗: {magic_info.level_cost}")
                        print(f"  图标: {magic_info.icon}")
                        print(f"  等级1: {magic_info.level1}")
                        print(f"  等级2: {magic_info.level2}")
                        print(f"  等级3: {magic_info.level3}")
                        print(f"  需求1: {magic_info.need1}")
                        print(f"  需求2: {magic_info.need2}")
                        print(f"  需求3: {magic_info.need3}")
                        print(f"  基础延迟: {magic_info.delay_base}")
                        print(f"  延迟减少: {magic_info.delay_reduction}")
                        print(f"  基础力量: {magic_info.power_base}")
                        print(f"  力量奖励: {magic_info.power_bonus}")
                        print(f"  基础魔法力量: {magic_info.mpower_base}")
                        print(f"  魔法力量奖励: {magic_info.mpower_bonus}")
                        print(f"  范围: {magic_info.range}")
                        print(f"  基础倍数: {magic_info.multiplier_base}")
                        print(f"  倍数奖励: {magic_info.multiplier_bonus}")
                    except Exception as e:
                        print(f"读取魔法信息 {i+1} 时出错: {str(e)}")

                print("\n=== 商城信息 ===")
                # 读取商城物品数量
                gameshop_count = BinaryReader.read_int32(f)
                print(f"商城物品数量: {gameshop_count}")
                
                # 读取商城物品信息
                envir.gameshop_items = []
                for i in range(gameshop_count):
                    try:
                        item = GameShopItem.read(f)
                        envir.gameshop_items.append(item)
                        print(f"\n商城物品 {i+1}/{gameshop_count}:")
                        print(f"  物品索引: {item.item_index}")
                        print(f"  商品索引: {item.g_index}")
                        print(f"  金币价格: {item.gold_price}")
                        print(f"  元宝价格: {item.credit_price}")
                        print(f"  数量: {item.count}")
                        print(f"  职业: {item.class_name}")
                        print(f"  分类: {item.category}")
                        print(f"  库存: {item.stock}")
                        print(f"  是否限量: {item.i_stock}")
                        print(f"  是否特价: {item.deal}")
                        print(f"  是否置顶: {item.top_item}")
                        print(f"  可否用金币购买: {item.can_buy_gold}")
                        print(f"  可否用元宝购买: {item.can_buy_credit}")
                    except Exception as e:
                        print(f"读取商城物品 {i+1} 时出错: {str(e)}")

                print("\n=== 数据读取完成 ===")
                print(f"成功加载地图数量: {len(envir.maps)}")
                print(f"成功加载物品数量: {len(envir.items)}")
                print(f"成功加载怪物数量: {len(envir.monsters)}")
                print(f"成功加载NPC数量: {len(envir.npcs)}")
                print(f"成功加载任务数量: {len(envir.quests)}")
                print(f"成功加载龙数量: {len(envir.dragons)}")

                print("\n=== 征服信息 ===")
                # 读取征服信息
                conquest_count = BinaryReader.read_int32(f)
                print(f"征服数量: {conquest_count}")
                
                envir.conquests = []
                for i in range(conquest_count):
                    try:
                        conquest_info = Conquest.read(f)
                        envir.conquests.append(conquest_info)
                        print(f"\n征服信息 {i+1}/{conquest_count}:")
                        print(f"  索引: {conquest_info.index}")
                        print(f"  名称: {conquest_info.name}")
                        print(f"  地图索引: {conquest_info.map_index}")
                        print(f"  宫殿索引: {conquest_info.palace_index}")
                        print(f"  守卫数量: {len(conquest_info.conquest_guards)}")
                        print(f"  城门数量: {len(conquest_info.conquest_gates)}")
                        print(f"  城墙数量: {len(conquest_info.conquest_walls)}")
                        print(f"  攻城数量: {len(conquest_info.conquest_sieges)}")
                        print(f"  旗帜数量: {len(conquest_info.conquest_flags)}")
                        print(f"  控制点数量: {len(conquest_info.control_points)}")
                    except Exception as e:
                        print(f"读取征服信息 {i+1} 时出错: {str(e)}")

                print("\n=== 刷新计时器信息 ===")
                # 读取刷新计时器信息
                try:
                    respawn_timer = RespawnTimer.read(f)
                    envir.respawn_timers.append(respawn_timer)
                    print(f"\n刷新计时器信息:")
                    print(f"  基础刷新率: {respawn_timer.base_spawn_rate}")
                    print(f"  当前刷新计数器: {respawn_timer.current_tick_counter}")
                    print(f"  刷新选项数量: {len(respawn_timer.respawn_options)}")
                    for i, option in enumerate(respawn_timer.respawn_options):
                        print(f"  选项 {i+1}:")
                        print(f"    用户数量: {option.user_count}")
                        print(f"    延迟损失: {option.delay_loss}")
                except Exception as e:
                    print(f"读取刷新计时器信息时出错: {str(e)}")

        except Exception as e:
            print(f"加载数据库时出错: {str(e)}")
            return None

        return envir
    @staticmethod
    def load_json_to_db(json_dir,db_path):
        """从JSON文件保存数据到二进制文件
        
        Args:
            json_dir: JSON文件所在目录路径
        """
        try:
            
            # 从json_dir中读取version.json文件
            envir=Envir.load_json(json_dir)
            with open(db_path, 'wb') as f:
            # 保存到f这个文件中
                 envir.save_db(f)
            return True
            
        except Exception as e:
            print(f"保存数据库时出错: {str(e)}")
            return False
    @staticmethod
    def load_json(json_dir):
        """从JSON文件加载数据
        
        Args:
            json_dir: JSON文件所在目录路径
        """
        envir = Envir()  # 创建新的Envir实例，不需要db_path
        envir._load_version_info(json_dir)
        envir._load_maps(json_dir)
        envir._load_items(json_dir)
        envir._load_monsters(json_dir)
        envir._load_npcs(json_dir)
        envir._load_quests(json_dir)
        envir._load_dragons(json_dir)
        envir._load_magics(json_dir)
        envir._load_gameshop_items(json_dir)
        envir._load_conquests(json_dir)
        envir._load_respawn_timer(json_dir)
        return envir

    def _load_version_info(self, json_dir):
        """加载版本信息
        
        Args:
            json_dir: JSON文件所在目录路径
        """
        version_path = os.path.join(json_dir, 'version.json')
        with open(version_path, 'r', encoding='utf-8') as read_f:
            #从f这个json文件中读取version和custom_version
            version_data = json.load(read_f) 
            self.version = version_data['version']
            self.custom_version = version_data['custom_version']
            self.map_index = version_data['map_index']
            self.item_index = version_data['item_index']
            self.monster_index = version_data['monster_index']
            self.npc_index = version_data['npc_index']
            self.quest_index = version_data['quest_index']
            self.gameshop_index = version_data['gameshop_index']
            self.conquest_index = version_data['conquest_index']
            self.respawn_timer_index = version_data['respawn_timer_index']  
            print(f"version: {self.version}, custom_version: {self.custom_version}")
            print(f"map_index: {self.map_index}, item_index: {self.item_index}, monster_index: {self.monster_index}, npc_index: {self.npc_index}, quest_index: {self.quest_index}, gameshop_index: {self.gameshop_index}, conquest_index: {self.conquest_index}, respawn_timer_index: {self.respawn_timer_index}")
        

    def _load_maps(self, json_dir):
        """加载地图信息"""
        maps_path = os.path.join(json_dir, 'maps.json')
        with open(maps_path, 'r', encoding='utf-8') as read_f:
            map_data = json.load(read_f)
            for map_info in map_data:
                map_obj = Map()
                map_obj.index = map_info['index']
                map_obj.filename = map_info['file_name']
                map_obj.title = map_info['title']
                map_obj.mini_map = map_info['mini_map']
                map_obj.light = map_info['light']
                map_obj.big_map = map_info['big_map']
                # 加载安全区信息
                for sz in map_info['safe_zones']:
                    safe_zone = SafeZoneInfo()
                    safe_zone.location = Point(sz['location']['x'], sz['location']['y'])
                    safe_zone.size = sz['size']
                    safe_zone.start_point = sz['start_point']
                    map_obj.safe_zones.append(safe_zone)
                for r in map_info['respawns']:
                    respawn = RespawnInfo()
                    respawn.monster_index = r['monster_index']
                    respawn.location = Point(r['location']['x'], r['location']['y'])
                    respawn.count = r['count']
                    respawn.spread = r['spread']
                    respawn.delay = r['delay']
                    respawn.direction = r['direction']
                    respawn.route_path = r['route_path']
                    respawn.random_delay = r['random_delay']
                    respawn.respawn_index = r['respawn_index']
                    respawn.save_respawn_time = r['save_respawn_time']
                    respawn.respawn_ticks = r['respawn_ticks']
                    map_obj.respawns.append(respawn)
                for mv in map_info['movements']:
                    movement = MovementInfo()
                    movement.map_index = mv['map_index']
                    movement.map_index = mv['map_index']
                    movement.source = Point(mv['source']['x'], mv['source']['y'])
                    movement.destination = Point(mv['destination']['x'], mv['destination']['y'])
                    movement.need_hole = mv['need_hole']
                    movement.need_move = mv['need_move']
                    movement.conquest_index = mv['conquest_index']
                    movement.show_on_big_map = mv['show_on_big_map']
                    movement.icon = mv['icon']
                    map_obj.movements.append(movement)
                for mz in map_info['mine_zones']:
                    mine_zone = MineZone()
                    mine_zone.location = Point(mz['location']['x'], mz['location']['y'])
                    mine_zone.size = mz['size']
                    mine_zone.mine_index = mz['mine_index']
                    map_obj.mine_zones.append(mine_zone)
                # 加载其他属性
                map_obj.no_teleport = map_info['no_teleport']
                map_obj.no_reconnect = map_info['no_reconnect']
                map_obj.no_reconnect_map = map_info['no_reconnect_map']
                map_obj.no_random = map_info['no_random']
                map_obj.no_escape = map_info['no_escape']
                map_obj.no_recall = map_info['no_recall']
                map_obj.no_drug = map_info['no_drug']
                map_obj.no_position = map_info['no_position']
                map_obj.no_throw_item = map_info['no_throw_item']
                map_obj.no_drop_player = map_info['no_drop_player']
                map_obj.no_drop_monster = map_info['no_drop_monster']
                map_obj.no_names = map_info['no_names']
                map_obj.fight = map_info['fight']
                map_obj.fire = map_info['fire']
                map_obj.fire_damage = map_info['fire_damage']
                map_obj.lightning = map_info['lightning']
                map_obj.lightning_damage = map_info['lightning_damage']
                map_obj.map_dark_light = map_info['map_dark_light']
                map_obj.mine_index = map_info['mine_index']
                map_obj.no_mount = map_info['no_mount']
                map_obj.need_bridle = map_info['need_bridle']
                map_obj.no_fight = map_info['no_fight']
                map_obj.music = map_info['music']
                self.maps.append(map_obj)

    def _load_items(self, json_dir):
        """加载物品信息"""
        items_path = os.path.join(json_dir, 'items.json')
        with open(items_path, 'r', encoding='utf-8') as read_f:
            item_data = json.load(read_f)
            for item_info in item_data:
                item = Item()
                item.index = item_info['index']
                item.name = item_info['name']
                item.type = ItemType[item_info['type']]
                item.grade = ItemGrade[item_info['grade']]
                item.required_type = RequiredType[item_info['required_type']]
                item.required_class = RequiredClass[item_info['required_class']]
                item.required_gender = RequiredGender[item_info['required_gender']]
                item.set = ItemSet[item_info['set']]
                item.shape = item_info['shape']
                item.weight = item_info['weight']
                item.light = item_info['light']
                item.required_amount = item_info['required_amount']
                item.image = item_info['image']
                item.durability = item_info['durability']
                item.stack_size = item_info['stack_size']
                item.price = item_info['price']
                item.start_item = item_info['start_item']
                item.effect = item_info['effect']
                item.need_identify = item_info['need_identify']
                item.show_group_pickup = item_info['show_group_pickup']
                item.global_drop_notify = item_info['global_drop_notify']
                item.class_based = item_info['class_based']
                item.level_based = item_info['level_based']
                item.can_mine = item_info['can_mine']
                item.can_fast_run = item_info['can_fast_run']
                item.can_awakening = item_info['can_awakening']
                item.bind = BindMode[item_info['bind']]
                item.unique = SpecialItemMode[item_info['unique']]
                item.random_stats_id = item_info['random_stats_id']
                item.random_stats = item_info['random_stats']
                item.tool_tip = item_info['tool_tip']
                item.slots = item_info['slots']
                # 加载状态信息
                item.stats = Stats()
                for stat_name, value in item_info['stats'].items():
                    item.stats[Stat[stat_name]] = value
                self.items.append(item)

    def _load_monsters(self, json_dir):
        """加载怪物信息"""
        monsters_path = os.path.join(json_dir, 'monsters.json')
        with open(monsters_path, 'r', encoding='utf-8') as read_f:
            monster_data = json.load(read_f)
            for monster_info in monster_data:
                monster = Monster()
                monster.index = monster_info['index']
                monster.name = monster_info['name']
                monster.image = monster_info['image']
                monster.ai = monster_info['ai']
                monster.effect = monster_info['effect']
                monster.level = monster_info['level']
                monster.view_range = monster_info['view_range']
                monster.cool_eye = monster_info['cool_eye']
                # 加载状态信息
                monster.stats = Stats()
                for stat_name, value in monster_info['stats'].items():
                    monster.stats[Stat[stat_name]] = value
                # 加载掉落信息
                for drop_info in monster_info['drops']:
                    drop = DropInfo()
                    drop.chance = drop_info['chance']
                    drop.gold = drop_info['gold']
                    drop.type = drop_info['type']
                    drop.quest_required = drop_info['quest_required']
                    monster.drops.append(drop)
                monster.can_tame = monster_info['can_tame']
                monster.can_push = monster_info['can_push']
                monster.auto_rev = monster_info['auto_rev']
                monster.undead = monster_info['undead']
                monster.has_spawn_script = monster_info['has_spawn_script']
                monster.has_die_script = monster_info['has_die_script']
                monster.attack_speed = monster_info['attack_speed']
                monster.move_speed = monster_info['move_speed']
                monster.experience = monster_info['experience']
                monster.light = monster_info['light']
                monster.drop_path = monster_info['drop_path']
                self.monsters.append(monster)

   
    def _load_npcs(self, json_dir):
        """加载NPC信息"""
        npcs_path = os.path.join(json_dir, 'npcs.json')
        with open(npcs_path, 'r', encoding='utf-8') as read_f:
            npc_data = json.load(read_f)
            for npc_info in npc_data:
                npc = NPC()
                npc.index = npc_info['index']
                npc.name = npc_info['name']
                npc.file_name = npc_info['file_name']
                npc.map_index = npc_info['map_index']
                npc.location = Point(npc_info['location']['x'], npc_info['location']['y'])
                npc.rate = npc_info['rate']
                npc.image = npc_info['image']
                npc.time_visible = npc_info['time_visible']
                npc.hour_start = npc_info['hour_start']
                npc.minute_start = npc_info['minute_start']
                npc.hour_end = npc_info['hour_end']
                npc.minute_end = npc_info['minute_end']
                npc.min_lev = npc_info['min_lev']
                npc.max_lev = npc_info['max_lev']
                npc.day_of_week = npc_info['day_of_week']
                npc.class_required = npc_info['class_required']
                npc.flag_needed = npc_info['flag_needed']
                npc.conquest = npc_info['conquest']
                npc.show_on_big_map = npc_info['show_on_big_map']
                npc.big_map_icon = npc_info['big_map_icon']
                npc.can_teleport_to = npc_info['can_teleport_to']
                npc.conquest_visible = npc_info['conquest_visible']
                self.npcs.append(npc)
        pass

    def _load_quests(self, json_dir):
        """加载任务信息"""
        quests_path = os.path.join(json_dir, 'quests.json')
        with open(quests_path, 'r', encoding='utf-8') as read_f:
            quest_data = json.load(read_f)
            for quest_info in quest_data:
                quest = Quest()
                quest.index = quest_info['index']
                quest.name = quest_info['name']
                quest.file_name = quest_info['file_name']
                quest.group = quest_info['group']
                quest.required_min_level = quest_info['required_min_level']
                quest.required_max_level = quest_info['required_max_level']
                quest.required_quest = quest_info['required_quest']
                quest.required_class = RequiredClass[quest_info['required_class']]
                quest.type = QuestType[quest_info['type']]
                quest.goto_message = quest_info['goto_message']
                quest.kill_message = quest_info['kill_message']
                quest.item_message = quest_info['item_message']
                quest.flag_message = quest_info['flag_message']
                quest.time_limit_in_seconds = quest_info['time_limit_in_seconds']
                
                
                self.quests.append(quest)
        pass
    def _load_dragons(self, json_dir):
        """加载龙信息"""
        dragons_path = os.path.join(json_dir, 'dragons.json')
        with open(dragons_path, 'r', encoding='utf-8') as read_f:
            dragon_data = json.load(read_f)
            for dragon_info in dragon_data:
                dragon = Dragon()
                dragon.enabled = dragon_info['enabled']
                dragon.map_file_name = dragon_info['map_file_name']
                dragon.monster_name = dragon_info['monster_name']
                dragon.body_name = dragon_info['body_name']
                dragon.location = Point(dragon_info['location']['x'], dragon_info['location']['y'])
                dragon.drop_area_top = Point(dragon_info['drop_area_top']['x'], dragon_info['drop_area_top']['y'])
                dragon.drop_area_bottom = Point(dragon_info['drop_area_bottom']['x'], dragon_info['drop_area_bottom']['y'])
                dragon.exps = dragon_info['exps']
                # 加载掉落信息
                for level_drops in dragon_info['drops']:
                    level_drop_list = []
                    for drop_info in level_drops:
                        drop = DragonDropInfo()
                        drop.chance = drop_info['chance']
                        if drop_info['item']:
                            item_index = drop_info['item']['index']
                            drop.item = next((item for item in self.items if item.index == item_index), None)
                        drop.gold = drop_info['gold']
                        drop.level = drop_info['level']
                        level_drop_list.append(drop)
                    dragon.drops.append(level_drop_list)
                self.dragons.append(dragon)

    def _load_magics(self, json_dir):
        """加载魔法信息"""
        magics_path = os.path.join(json_dir, 'magics.json')
        with open(magics_path, 'r', encoding='utf-8') as read_f:
            magic_data = json.load(read_f)
            for magic_info in magic_data:
                magic = Magic()
                magic.name = magic_info['name']
                magic.spell = Spell[magic_info['spell']]
                magic.base_cost = magic_info['base_cost']
                magic.level_cost = magic_info['level_cost']
                magic.icon = magic_info['icon']
                magic.level1 = magic_info['level1'] 
                magic.level2 = magic_info['level2']
                magic.level3 = magic_info['level3']
                magic.need1 = magic_info['need1']
                magic.need2 = magic_info['need2']
                magic.need3 = magic_info['need3']
                magic.delay_base = magic_info['delay_base']
                magic.delay_reduction = magic_info['delay_reduction']
                magic.power_base = magic_info['power_base']
                magic.power_bonus = magic_info['power_bonus']
                magic.mpower_base = magic_info['mpower_base']
                magic.mpower_bonus = magic_info['mpower_bonus']
                magic.range = magic_info['range']
                magic.multiplier_base = magic_info['multiplier_base']
                magic.multiplier_bonus = magic_info['multiplier_bonus']

                self.magics.append(magic)
        pass

    def _load_gameshop_items(self, json_dir):
        """加载商城物品信息"""
        gameshop_items_path = os.path.join(json_dir, 'gameshop_items.json')
        with open(gameshop_items_path, 'r', encoding='utf-8') as read_f:
            gameshop_items_data = json.load(read_f)
            for gameshop_item_info in gameshop_items_data:
                gameshop_item = GameShopItem()
                gameshop_item.item_index = gameshop_item_info['item_index']
                gameshop_item.g_index = gameshop_item_info['g_index']
                gameshop_item.gold_price = gameshop_item_info['gold_price']
                gameshop_item.credit_price = gameshop_item_info['credit_price']
                gameshop_item.count = gameshop_item_info['count']
                gameshop_item.class_name = gameshop_item_info['class_name']
                gameshop_item.category = gameshop_item_info['category']
                gameshop_item.stock = gameshop_item_info['stock']
                gameshop_item.i_stock = gameshop_item_info['i_stock']
                gameshop_item.deal = gameshop_item_info['deal']
                gameshop_item.top_item = gameshop_item_info['top_item']
                gameshop_item.date = gameshop_item_info['date']
                gameshop_item.can_buy_gold = gameshop_item_info['can_buy_gold'] 
                gameshop_item.can_buy_credit = gameshop_item_info['can_buy_credit']
                self.gameshop_items.append(gameshop_item)
        pass

    def _load_conquests(self, json_dir):
        """加载征服信息"""
        conquests_path = os.path.join(json_dir, 'conquests.json')
        with open(conquests_path, 'r', encoding='utf-8') as read_f:
            conquests_data = json.load(read_f)
            for conquest_info in conquests_data:
                conquest = Conquest()
                conquest.index = conquest_info['index']
                conquest.name = conquest_info['name']
                conquest.map_index = conquest_info['map_index']
                conquest.location = Point(conquest_info['location']['x'], conquest_info['location']['y'])
                conquest.size = conquest_info['size']
                conquest.full_map = conquest_info['full_map']
                conquest.palace_index = conquest_info['palace_index']
                conquest.guard_index = conquest_info['guard_index']
                conquest.gate_index = conquest_info['gate_index']
                conquest.wall_index = conquest_info['wall_index']
                conquest.siege_index = conquest_info['siege_index']
                conquest.flag_index = conquest_info['flag_index']
                conquest.extra_maps = conquest_info['extra_maps']
                for guard_info in conquest_info['conquest_guards']:
                    guard = ConquestArcherInfo()
                    guard.index = guard_info['index']
                    guard.location = Point(guard_info['location']['x'], guard_info['location']['y'])
                    guard.mob_index = guard_info['mob_index']
                    guard.name = guard_info['name']
                    guard.repair_cost = guard_info['repair_cost']
                    conquest.conquest_guards.append(guard)
                for gate_info in conquest_info['conquest_gates']:
                    gate = ConquestGateInfo()
                    gate.index = gate_info['index']
                    gate.location = Point(gate_info['location']['x'], gate_info['location']['y'])
                    gate.mob_index = gate_info['mob_index']
                    gate.name = gate_info['name']
                    gate.repair_cost = gate_info['repair_cost']
                    conquest.conquest_gates.append(gate)
                for wall_info in conquest_info['conquest_walls']:
                    wall = ConquestWallInfo()
                    wall.index = wall_info['index']
                    wall.location = Point(wall_info['location']['x'], wall_info['location']['y'])
                    wall.mob_index = wall_info['mob_index']
                    wall.name = wall_info['name']
                    wall.repair_cost = wall_info['repair_cost']
                    conquest.conquest_walls.append(wall)
                for flag_info in conquest_info['conquest_flags']:
                    flag = ConquestFlagInfo()
                    flag.index = flag_info['index']
                    flag.location = Point(flag_info['location']['x'], flag_info['location']['y'])
                    flag.name = flag_info['name']
                    flag.file_name = flag_info['file_name']
                    conquest.conquest_flags.append(flag)
                for control_point_info in conquest_info['control_points']:
                    control_point = ConquestFlagInfo()
                    control_point.index = control_point_info['index']
                    control_point.location = Point(control_point_info['location']['x'], control_point_info['location']['y'])
                    control_point.name = control_point_info['name']
                    control_point.file_name = control_point_info['file_name']
                    conquest.control_points.append(control_point)
                conquest.start_hour = conquest_info['start_hour']
                conquest.war_length = conquest_info['war_length']
                conquest.type = ConquestType[conquest_info['type']]
                conquest.game = ConquestGame[conquest_info['game']]
                conquest.monday = conquest_info['monday']
                conquest.tuesday = conquest_info['tuesday']
                conquest.wednesday = conquest_info['wednesday']
                conquest.thursday = conquest_info['thursday']
                conquest.friday = conquest_info['friday']
                conquest.saturday = conquest_info['saturday']
                conquest.sunday = conquest_info['sunday']
                conquest.king_location = Point(conquest_info['king_location']['x'], conquest_info['king_location']['y'])
                conquest.king_size = conquest_info['king_size']
                conquest.control_point_index = conquest_info['control_point_index']
                conquest.control_points = conquest_info['control_points']
                
                self.conquests.append(conquest)

    def _load_respawn_timer(self, json_dir):
        """加载刷新计时器信息"""
        respawn_timer_path = os.path.join(json_dir, 'respawn_timers.json')
        with open(respawn_timer_path, 'r', encoding='utf-8') as read_f:
            respawn_timer_data = json.load(read_f)
            for respawn_timer_info in respawn_timer_data:
                respawn_timer = RespawnTimer()
                respawn_timer.base_spawn_rate = respawn_timer_info['base_spawn_rate']
                respawn_timer.current_tick_counter = respawn_timer_info['current_tick_counter']
                respawn_timer.last_tick = respawn_timer_info['last_tick']
                respawn_timer.last_user_count = respawn_timer_info['last_user_count']
                respawn_timer.current_delay = respawn_timer_info['current_delay']
                for respawn_option_info in respawn_timer_info['respawn_options']:
                    respawn_option = RespawnTickOption()
                    respawn_option.user_count = respawn_option_info['user_count']
                    respawn_option.delay_loss = respawn_option_info['delay_loss']
                    respawn_timer.respawn_options.append(respawn_option)
                self.respawn_timers.append(respawn_timer)
        pass

    def save_to_json(self, output_path):
        """保存数据到多个JSON文件，使用UTF-8编码"""
        # 创建输出目录
        os.makedirs(output_path, exist_ok=True)
        
        # 保存版本信息
        version_data = {
            'version': self.version,
            'custom_version': self.custom_version,
            "map_index": self.map_index,
            "item_index": self.item_index,
            "monster_index": self.monster_index,
            "npc_index": self.npc_index,
            "quest_index": self.quest_index,
            "gameshop_index": self.gameshop_index,
            "conquest_index": self.conquest_index,
            "respawn_timer_index": self.respawn_timer_index,
        }
        version_path = os.path.join(output_path, 'version.json')
        with open(version_path, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, ensure_ascii=False, indent=2)

        # 保存地图信息
        maps_data = [
            {
                'index': m.index,
                'file_name': m.filename,
                'title': m.title,
                'mini_map': m.mini_map,
                'light': m.light,
                'big_map': m.big_map,
                'safe_zones': [
                    {
                        'location': {'x': sz.location.x, 'y': sz.location.y},
                        'size': sz.size,
                        'start_point': sz.start_point
                    } for sz in m.safe_zones
                ],
                'respawns': [
                    {
                        'monster_index': r.monster_index,
                        'location': {'x': r.location.x, 'y': r.location.y},
                        'count': r.count,
                        'spread': r.spread,
                        'delay': r.delay,
                        'direction': r.direction,
                        'route_path': r.route_path,
                        'random_delay': r.random_delay,
                        'respawn_index': r.respawn_index,
                        'save_respawn_time': r.save_respawn_time,
                        'respawn_ticks': r.respawn_ticks
                    } for r in m.respawns
                ],
                'movements': [
                    {
                        'map_index': mv.map_index,
                        'source': {'x': mv.source.x, 'y': mv.source.y},
                        'destination': {'x': mv.destination.x, 'y': mv.destination.y},
                        'need_hole': mv.need_hole,
                        'need_move': mv.need_move,
                        'conquest_index': mv.conquest_index,
                        'show_on_big_map': mv.show_on_big_map,
                        'icon': mv.icon
                    } for mv in m.movements
                ],

                'no_teleport': m.no_teleport,
                'no_reconnect': m.no_reconnect,
                'no_reconnect_map': m.no_reconnect_map,
                'no_random': m.no_random,
                'no_escape': m.no_escape,
                'no_recall': m.no_recall,
                'no_drug': m.no_drug,
                'no_position': m.no_position,
                'no_throw_item': m.no_throw_item,
                'no_drop_player': m.no_drop_player,
                'no_drop_monster': m.no_drop_monster,
                'no_names': m.no_names,
                'fight': m.fight,
                'fire': m.fight,
                'fire_damage': m.fire_damage,
                'lightning': m.lightning,
                'lightning_damage': m.lightning_damage,
                'map_dark_light': m.map_dark_light,
                'mine_zones': [
                    {
                        'location': {'x': mz.location.x, 'y': mz.location.y},
                        'size': mz.size,
                        'mine_index': mz.mine_index
                    } for mz in m.mine_zones
                ],
                'mine_index': m.mine_index,
                'no_mount': m.no_mount,
                'need_bridle': m.need_bridle,
                'no_fight': m.no_fight,
                'music': m.music
            } for m in self.maps
        ]
        maps_path = os.path.join(output_path, 'maps.json')
        with open(maps_path, 'w', encoding='utf-8') as f:
            json.dump(maps_data, f, ensure_ascii=False, indent=2)

        # 保存怪物信息
        monsters_data = [
            {
                'index': m.index,
                'name': m.name,
                'image': m.image,
                'ai': m.ai,
                'effect': m.effect,
                'level': m.level,
                'view_range': m.view_range,
                'cool_eye': m.cool_eye,
                'stats': {stat.name: m.stats[stat] for stat in Stat},
                'drops': [
                    {
                        'chance': d.chance,
                        'gold': d.gold,
                        'type': d.type,
                        'quest_required': d.quest_required
                    } for d in m.drops
                ],
                'can_tame': m.can_tame,
                'can_push': m.can_push,
                'auto_rev': m.auto_rev,
                'undead': m.undead,
                'has_spawn_script': m.has_spawn_script,
                'has_die_script': m.has_die_script,
                'attack_speed': m.attack_speed,
                'move_speed': m.move_speed,
                'experience': m.experience,
                'light': m.light,
                'drop_path': m.drop_path
            } for m in self.monsters
        ]
        monsters_path = os.path.join(output_path, 'monsters.json')
        with open(monsters_path, 'w', encoding='utf-8') as f:
            json.dump(monsters_data, f, ensure_ascii=False, indent=2)

        # 保存NPC信息
        npcs_data = [
            {
                'index': n.index,
                'name': n.name,
                'file_name': n.file_name,
                'map_index': n.map_index,
                'location': {'x': n.location.x, 'y': n.location.y},
                'rate': n.rate,
                'image': n.image,
                'time_visible': n.time_visible,
                'hour_start': n.hour_start,
                'minute_start': n.minute_start,
                'hour_end': n.hour_end,
                'minute_end': n.minute_end,
                'min_lev': n.min_lev,
                'max_lev': n.max_lev,
                'day_of_week': n.day_of_week,
                'class_required': n.class_required,
                'flag_needed': n.flag_needed,
                'conquest': n.conquest,
                'show_on_big_map': n.show_on_big_map,
                'big_map_icon': n.big_map_icon,
                'can_teleport_to': n.can_teleport_to,
                'conquest_visible': n.conquest_visible,
                'collect_quest_indexes': n.collect_quest_indexes,
                'finish_quest_indexes': n.finish_quest_indexes
            } for n in self.npcs
        ]
        npcs_path = os.path.join(output_path, 'npcs.json')
        with open(npcs_path, 'w', encoding='utf-8') as f:
            json.dump(npcs_data, f, ensure_ascii=False, indent=2)

        # 保存任务信息
        quests_data = [
            {
                'index': q.index,
                'name': q.name,
                'group': q.group,
                'file_name': q.file_name,
                'required_min_level': q.required_min_level,
                'required_max_level': q.required_max_level,
                'required_quest': q.required_quest,
                'required_class': q.required_class.name,
                'type': q.type.name,
                'goto_message': q.goto_message,
                'kill_message': q.kill_message,
                'item_message': q.item_message,
                'flag_message': q.flag_message,
                'time_limit_in_seconds': q.time_limit_in_seconds,
                'description': q.description,
                'task_description': q.task_description,
                'return_description': q.return_description,
                'completion_description': q.completion_description,
                'carry_items': [
                    {
                        'item': {'index': t.item.index, 'name': t.item.name},
                        'count': t.count,
                        'message': t.message
                    } for t in q.carry_items
                ],
                'kill_tasks': [
                    {
                        'monster': {'index': t.monster.index, 'name': t.monster.name},
                        'count': t.count,
                        'message': t.message
                    } for t in q.kill_tasks
                ],
                'item_tasks': [
                    {
                        'item': {'index': t.item.index, 'name': t.item.name},
                        'count': t.count,
                        'message': t.message
                    } for t in q.item_tasks
                ],
                'flag_tasks': [
                    {
                        'number': t.number,
                        'message': t.message
                    } for t in q.flag_tasks
                ],
                'gold_reward': q.gold_reward,
                'exp_reward': q.exp_reward,
                'credit_reward': q.credit_reward,
                'fixed_rewards': [
                    {
                        'item': {'index': r.item.index, 'name': r.item.name},
                        'count': r.count
                    } for r in q.fixed_rewards
                ],
                'select_rewards': [
                    {
                        'item': {'index': r.item.index, 'name': r.item.name},
                        'count': r.count
                    } for r in q.select_rewards
                ]
            } for q in self.quests
        ]
        quests_path = os.path.join(output_path, 'quests.json')
        with open(quests_path, 'w', encoding='utf-8') as f:
            json.dump(quests_data, f, ensure_ascii=False, indent=2)

        # 保存物品信息
        items_data = [
            {
                'index': i.index,
                'name': i.name,
                'type': i.type.name,
                'grade': i.grade.name,
                'required_type': i.required_type.name,
                'required_class': i.required_class.name,
                'required_gender': i.required_gender.name,
                'set': i.set.name,
                'shape': i.shape,
                'weight': i.weight,
                'light': i.light,
                'required_amount': i.required_amount,
                'image': i.image,
                'durability': i.durability,
                'stack_size': i.stack_size,
                'price': i.price,
                'start_item': i.start_item,
                'effect': i.effect,
                'need_identify': i.need_identify,
                'show_group_pickup': i.show_group_pickup,
                'global_drop_notify': i.global_drop_notify,
                'class_based': i.class_based,
                'level_based': i.level_based,
                'can_mine': i.can_mine,
                'can_fast_run': i.can_fast_run,
                'can_awakening': i.can_awakening,
                'bind': i.bind.name,
                'unique': i.unique.name,
                'random_stats_id': i.random_stats_id,
                'random_stats': i.random_stats,
                'tool_tip': i.tool_tip,
                'slots': i.slots,
                'stats': {stat.name: i.stats[stat] for stat in Stat},
            } for i in self.items
        ]
        items_path = os.path.join(output_path, 'items.json')
        with open(items_path, 'w', encoding='utf-8') as f:
            json.dump(items_data, f, ensure_ascii=False, indent=2)

        # 保存龙信息
        dragons_data = [
            {
                'enabled': d.enabled,
                'map_file_name': d.map_file_name,
                'monster_name': d.monster_name,
                'body_name': d.body_name,
                'location': {'x': d.location.x, 'y': d.location.y},
                'drop_area_top': {'x': d.drop_area_top.x, 'y': d.drop_area_top.y},
                'drop_area_bottom': {'x': d.drop_area_bottom.x, 'y': d.drop_area_bottom.y},
                'exps': d.exps,
                'drops': [
                    [
                        {
                            'chance': drop.chance,
                            'item': {'index': drop.item.index, 'name': drop.item.name} if drop.item else None,
                            'gold': drop.gold,
                            'level': drop.level
                        } for drop in level_drops
                    ] for level_drops in d.drops
                ]
            } for d in self.dragons
        ]
        dragons_path = os.path.join(output_path, 'dragons.json')
        with open(dragons_path, 'w', encoding='utf-8') as f:
            json.dump(dragons_data, f, ensure_ascii=False, indent=2)
        #增加magic信息
        magics_data = [
            {
                'name': m.name,
                'spell': m.spell.name,
                'base_cost': m.base_cost,
                'level_cost': m.level_cost,
                'icon': m.icon,
                'level1': m.level1, 
                'level2': m.level2,
                'level3': m.level3,
                'need1': m.need1,
                'need2': m.need2,
                'need3': m.need3,
                'delay_base': m.delay_base,
                'delay_reduction': m.delay_reduction,
                'power_base': m.power_base,
                'power_bonus': m.power_bonus,
                'mpower_base': m.mpower_base,
                'mpower_bonus': m.mpower_bonus,
                'range': m.range,
                'multiplier_base': m.multiplier_base,   
                'multiplier_bonus': m.multiplier_bonus,
            } for m in self.magics
        ]
        magics_path = os.path.join(output_path, 'magics.json')
        with open(magics_path, 'w', encoding='utf-8') as f:
            json.dump(magics_data, f, ensure_ascii=False, indent=2) 
        #增加game_shop信息
        game_shop_data = [
            {
                'item_index': g.item_index,
                'g_index': g.g_index,
                'gold_price': g.gold_price,
                'credit_price': g.credit_price,
                'count': g.count,
                'class_name': g.class_name,
                'category': g.category,
                'stock': g.stock,
                'i_stock': g.i_stock,
                'deal': g.deal,
                'top_item': g.top_item,
                'date': g.date,
                'can_buy_gold': g.can_buy_gold,
                'can_buy_credit': g.can_buy_credit,
            }    for g in self.gameshop_items
        ]
        game_shop_path = os.path.join(output_path, 'gameshop_items.json')
        with open(game_shop_path, 'w', encoding='utf-8') as f:
            json.dump(game_shop_data, f, ensure_ascii=False, indent=2)
        # 保存征服信息
        conquests_data = [
            {
                'index': c.index,
                'full_map': c.full_map,
                'location': {'x': c.location.x, 'y': c.location.y},
                'size': c.size,
                'name': c.name,
                'map_index': c.map_index,
                'palace_index': c.palace_index,
                'guard_index': c.guard_index,
                'gate_index': c.gate_index,
                'wall_index': c.wall_index,
                'siege_index': c.siege_index,
                'flag_index': c.flag_index,
                'start_hour': c.start_hour,
                'war_length': c.war_length,
                'type': c.type.name,
                'game': c.game.name,
                'monday': c.monday,
                'tuesday': c.tuesday,
                'wednesday': c.wednesday,
                'thursday': c.thursday,
                'friday': c.friday,
                'saturday': c.saturday,
                'sunday': c.sunday,
                'king_location': {'x': c.king_location.x, 'y': c.king_location.y},
                'king_size': c.king_size,
                'control_point_index': c.control_point_index,
                'extra_maps': c.extra_maps,
                'conquest_guards': [
                    {
                        'index': g.index,
                        'location': {'x': g.location.x, 'y': g.location.y},
                        'mob_index': g.mob_index,
                        'name': g.name,
                        'repair_cost': g.repair_cost
                    } for g in c.conquest_guards
                ],
                'conquest_gates': [
                    {
                        'index': g.index,
                        'location': {'x': g.location.x, 'y': g.location.y},
                        'mob_index': g.mob_index,
                        'name': g.name,
                        'repair_cost': g.repair_cost
                    } for g in c.conquest_gates
                ],
                'conquest_walls': [
                    {
                        'index': w.index,
                        'location': {'x': w.location.x, 'y': w.location.y},
                        'mob_index': w.mob_index,
                        'name': w.name,
                        'repair_cost': w.repair_cost
                    } for w in c.conquest_walls
                ],
                'conquest_sieges': [
                    {
                        'index': s.index,
                        'location': {'x': s.location.x, 'y': s.location.y},
                        'mob_index': s.mob_index,
                        'name': s.name,
                        'repair_cost': s.repair_cost
                    } for s in c.conquest_sieges
                ],
                'conquest_flags': [
                    {
                        'index': f.index,
                        'location': {'x': f.location.x, 'y': f.location.y},
                        'name': f.name,
                        'file_name': f.file_name
                    } for f in c.conquest_flags
                ],
                'control_points': [
                    {
                        'index': p.index,
                        'location': {'x': p.location.x, 'y': p.location.y},
                        'name': p.name,
                        'file_name': p.file_name
                    } for p in c.control_points
                ]
            } for c in self.conquests
        ]
        conquests_path = os.path.join(output_path, 'conquests.json')
        with open(conquests_path, 'w', encoding='utf-8') as f:
            json.dump(conquests_data, f, ensure_ascii=False, indent=2)

        respawn_timers_data = [
            {
                'base_spawn_rate': r.base_spawn_rate,
                'current_tick_counter': r.current_tick_counter,
                'last_tick': r.last_tick,
                'last_user_count': r.last_user_count,   
                'current_delay': r.current_delay,
                'respawn_options': [
                    {
                        'user_count': option.user_count,
                        'delay_loss': option.delay_loss
                    } for option in r.respawn_options
                ]
            } for r in self.respawn_timers  
        ]
        respawn_timers_path = os.path.join(output_path, 'respawn_timers.json')
        with open(respawn_timers_path, 'w', encoding='utf-8') as f:
            json.dump(respawn_timers_data, f, ensure_ascii=False, indent=2) 

    def parse_dragon_drop(self, line):
        """解析龙掉落信息"""
        parts = line.split()
        if len(parts) < 3:
            return None
            
        try:
            drop = DragonDropInfo()
            drop.chance = int(parts[0][2:])  # 跳过前两个字符
            
            if parts[1].lower() == "gold":
                if len(parts) < 4:
                    return None
                drop.gold = int(parts[2])
                drop.level = int(parts[3])
            else:
                drop.item = self.get_item_info(parts[1])
                if not drop.item:
                    return None
                drop.level = int(parts[2])
                
            return drop
        except (ValueError, IndexError):
            return None

    def save_db(self, f):
        """保存环境数据到二进制文件
        
        Args:
            f: 文件对象
        """
        try:
            # 写入版本信息
            BinaryWriter.write_int32(f, self.version)
            BinaryWriter.write_int32(f, self.custom_version)
            
            # 写入索引信息
            BinaryWriter.write_int32(f, self.map_index)
            BinaryWriter.write_int32(f, self.item_index)
            BinaryWriter.write_int32(f, self.monster_index)
            BinaryWriter.write_int32(f, self.npc_index)
            BinaryWriter.write_int32(f, self.quest_index)
            BinaryWriter.write_int32(f, self.gameshop_index)
            BinaryWriter.write_int32(f, self.conquest_index)
            BinaryWriter.write_int32(f, self.respawn_timer_index)
            
            # 写入地图信息
            BinaryWriter.write_int32(f, len(self.maps))
            for map_info in self.maps:
                map_info.write(f)
                
            # 写入物品信息
            BinaryWriter.write_int32(f, len(self.items))
            for item in self.items:
                item.write(f)
                
            # 写入怪物信息
            BinaryWriter.write_int32(f, len(self.monsters))
            for monster in self.monsters:
                monster.write(f)
                
            # 写入NPC信息
            BinaryWriter.write_int32(f, len(self.npcs))
            for npc in self.npcs:
                npc.write(f)
                
            # 写入任务信息
            BinaryWriter.write_int32(f, len(self.quests))
            for quest in self.quests:
                quest.write(f)
                
            # 写入龙信息
            for dragon in self.dragons:
                dragon.write(f)
                
            # 写入魔法信息
            BinaryWriter.write_int32(f, len(self.magics))
            for magic in self.magics:
                magic.write(f)
                
            # 写入商城物品信息
            BinaryWriter.write_int32(f, len(self.gameshop_items))
            for game_shop in self.gameshop_items:
                game_shop.write(f)
                
            # 写入征服信息
            BinaryWriter.write_int32(f, len(self.conquests))
            for conquest in self.conquests:
                conquest.write(f)
                
            # 写入刷新计时器信息
            for respawn_timer in self.respawn_timers:
                respawn_timer.write(f)
                
        except Exception as e:
            print(f"保存数据库时出错: {str(e)}")
            raise


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='处理游戏数据库文件')
    parser.add_argument('--db_path', type=str, default=os.path.join("../Jev", "Server.MirDB.bak"),
                        help='数据库文件路径')
    parser.add_argument('--output', type=str, default='data',
                        help='输出JSON文件的目录')
    parser.add_argument('--option', type=str, default='load',
                        help='load: 加载数据库, save: 保存数据库')
    # 解析命令行参数
    args = parser.parse_args()
    if args.option == 'load':       
        envir = Envir.load(args.db_path)
        if envir:
            print("\n保存解析结果到JSON文件...")
            envir.save_to_json(args.output)
            print("完成!")
    elif args.option == 'save':
        Envir.load_json_to_db( args.output,args.db_path)


if __name__ == "__main__":
    main() 