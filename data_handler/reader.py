import struct

class BinaryReader:
    @staticmethod
    def read_int32(f):
        """读取32位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(4)
            print(f"读取int32原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<i', data)[0]
        except Exception as e:
            print(f"读取int32时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_int16(f):
        """读取16位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(2)
            print(f"读取int16原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<h', data)[0]
        except Exception as e:
            print(f"读取int16时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_uint16(f):
        """读取无符号16位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(2)
            print(f"读取uint16原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<H', data)[0]
        except Exception as e:
            print(f"读取uint16时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise
    @staticmethod
    def read_uint64(f):
        """读取64位无符号整数"""
        try:
            data = f.read(8)
            if len(data) < 8:
                print(f"读取uint64时数据不足8字节: {len(data)}")
                return 0
            return struct.unpack('<Q', data)[0]
        except Exception as e:
            print(f"读取uint64时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            return 0
    @staticmethod
    def read_uint32(f):
        """读取无符号32位整数，使用小端字节序（little-endian）"""
        try:
            data = f.read(4)
            print(f"读取uint32原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<I', data)[0]
        except Exception as e:
            print(f"读取uint32时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_byte(f):
        """读取一个字节"""
        try:
            data = f.read(1)
            print(f"读取byte原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('B', data)[0]
        except Exception as e:
            print(f"读取byte时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_bool(f):
        """读取布尔值"""
        try:
            data = f.read(1)
            print(f"读取bool原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('?', data)[0]
        except Exception as e:
            print(f"读取bool时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_string(f):
        """读取字符串，使用7位编码的长度前缀格式"""
        try:
            # 读取7位编码的字符串长度
            length = 0
            shift = 0
            while True:
                data = f.read(1)
                print(f"读取字符串长度原始字节: {' '.join(f'{b:02x}' for b in data)}")
                b = struct.unpack('B', data)[0]
                length |= (b & 0x7F) << shift
                if (b & 0x80) == 0:
                    break
                shift += 7
            
            if length == 0:
                return ""
            
            # 读取字符串数据
            data = f.read(length)
            print(f"读取字符串数据原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return data.decode('latin1')
            
        except Exception as e:
            print(f"读取字符串时出错: {str(e)}")
            print(f"当前文件位置: {f.tell()}")
            raise

    @staticmethod
    def read_float(f):
        """读取浮点数"""
        try:
            data = f.read(4)
            return struct.unpack('<f', data)[0]
        except Exception as e:
            print(f"读取float时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise 
    @staticmethod
    def read_int64(f):
        """读取64位整数"""
        try:
            data = f.read(8)
            print(f"读取int64原始字节: {' '.join(f'{b:02x}' for b in data)}")
            return struct.unpack('<q', data)[0]
        except Exception as e:
            print(f"读取int64时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise