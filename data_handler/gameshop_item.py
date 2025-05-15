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
    def compare(self,other: 'GameShopItem'):
        if self.item_index != other.item_index:
            return False
        if self.g_index != other.g_index:
            return False
        if self.gold_price != other.gold_price:
            return False
        if self.credit_price != other.credit_price:
            return False
        if self.count != other.count:
            return 
        if self.class_name != other.class_name:
            return False
        if self.category != other.category:
            return False
        if self.stock != other.stock:
            return False
        if self.i_stock != other.i_stock:
            return False
        if self.deal != other.deal:
            return False
        if self.top_item != other.top_item:
            return False
        if self.date != other.date:
            return False
        if self.can_buy_gold != other.can_buy_gold:
            return False
        if self.can_buy_credit != other.can_buy_credit:
            return False
        return True
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
            
            item.g_index = BinaryReader.read_int32(f)
            
            item.gold_price = BinaryReader.read_uint32(f)
            
            item.credit_price = BinaryReader.read_uint32(f)
            
            item.count = BinaryReader.read_uint16(f)
            
            item.class_name = BinaryReader.read_string(f)
            
            item.category = BinaryReader.read_string(f)
            
            item.stock = BinaryReader.read_int32(f)
            
            item.i_stock = BinaryReader.read_bool(f)
            
            item.deal = BinaryReader.read_bool(f)
            
            item.top_item = BinaryReader.read_bool(f)
            
            item.date = BinaryReader.read_int64(f)
            
            item.can_buy_gold = BinaryReader.read_bool(f)
            
            item.can_buy_credit = BinaryReader.read_bool(f)
            
            return item
        except Exception as e:
            print(f"读取商城物品信息时出错: {str(e)}")
            raise 