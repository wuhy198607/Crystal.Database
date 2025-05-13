from dataclasses import dataclass, field
from typing import List, Optional, Dict
from binary import BinaryReader,BinaryWriter

@dataclass
class GameShopItem:
    item_index: int = 0
    g_index: int = 0
    gold_price: int = 0
    credit_price: int = 0
    count: int = 1
    class_name: str = ""
    category: str = ""
    stock: int = 0
    i_stock: bool = False
    deal: bool = False
    top_item: bool = False
    date: int = 0  # 使用int存储DateTime.ToBinary
    can_buy_gold: bool = False
    can_buy_credit: bool = False
    def write(self,f):
        BinaryWriter.write_int32(f, self.item_index)
        BinaryWriter.write_int32(f, self.g_index)
        BinaryWriter.write_uint32(f, self.gold_price)
        BinaryWriter.write_uint32(f, self.credit_price)
        BinaryWriter.write_uint16(f, self.count)
        BinaryWriter.write_string(f, self.class_name)
        BinaryWriter.write_string(f, self.category)
        BinaryWriter.write_int32(f, self.stock)
        BinaryWriter.write_bool(f, self.i_stock)
        BinaryWriter.write_bool(f, self.deal)
        BinaryWriter.write_bool(f, self.top_item)   
        BinaryWriter.write_int64(f, self.date)
        BinaryWriter.write_bool(f, self.can_buy_gold)
        BinaryWriter.write_bool(f, self.can_buy_credit) 
    @staticmethod
    def read(f):
        """读取商城物品信息"""
        try:
            item = GameShopItem()
            
            # 读取基本信息
            item.item_index = BinaryReader.read_int32(f)
            print(f"读取物品索引: {item.item_index}")
            
            item.g_index = BinaryReader.read_int32(f)
            print(f"读取商品索引: {item.g_index}")
            
            item.gold_price = BinaryReader.read_uint32(f)
            print(f"读取金币价格: {item.gold_price}")
            
            item.credit_price = BinaryReader.read_uint32(f)
            print(f"读取元宝价格: {item.credit_price}")
            
            item.count = BinaryReader.read_uint16(f)
            print(f"读取数量: {item.count}")
            
            item.class_name = BinaryReader.read_string(f)
            print(f"读取职业: {item.class_name}")
            
            item.category = BinaryReader.read_string(f)
            print(f"读取分类: {item.category}")
            
            item.stock = BinaryReader.read_int32(f)
            print(f"读取库存: {item.stock}")
            
            item.i_stock = BinaryReader.read_bool(f)
            print(f"读取是否限量: {item.i_stock}")
            
            item.deal = BinaryReader.read_bool(f)
            print(f"读取是否特价: {item.deal}")
            
            item.top_item = BinaryReader.read_bool(f)
            print(f"读取是否置顶: {item.top_item}")
            
            item.date = BinaryReader.read_int64(f)
            print(f"读取日期: {item.date}")
            
            item.can_buy_gold = BinaryReader.read_bool(f)
            print(f"读取可否用金币购买: {item.can_buy_gold}")
            
            item.can_buy_credit = BinaryReader.read_bool(f)
            print(f"读取可否用元宝购买: {item.can_buy_credit}")
            
            return item
        except Exception as e:
            print(f"读取商城物品信息时出错: {str(e)}")
            raise 