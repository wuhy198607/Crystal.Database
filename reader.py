import struct

class BinaryReader:
    @staticmethod
    def read_int32(f):
        """读取32位整数"""
        try:
            data = f.read(4)
            return struct.unpack('<i', data)[0]
        except Exception as e:
            print(f"读取int32时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_int16(f):
        """读取16位整数"""
        try:
            data = f.read(2)
            return struct.unpack('<h', data)[0]
        except Exception as e:
            print(f"读取int16时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_uint16(f):
        """读取16位无符号整数"""
        try:
            data = f.read(2)
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
            return struct.unpack('<Q', data)[0]
        except Exception as e:
            print(f"读取uint64时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_uint32(f):
        """读取32位无符号整数"""
        try:
            data = f.read(4)
            return struct.unpack('<I', data)[0]
        except Exception as e:
            print(f"读取uint32时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_byte(f):
        """读取字节"""
        try:
            data = f.read(1)
            return struct.unpack('<B', data)[0]
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
            return struct.unpack('<?', data)[0]
        except Exception as e:
            print(f"读取bool时出错: {str(e)}")
            if 'data' in locals():
                print(f"原始数据: {' '.join(f'{b:02x}' for b in data)}")
            raise

    @staticmethod
    def read_string(f):
        """读取字符串"""
        try:
            length = BinaryReader.read_int32(f)
            if length <= 0:
                return ""
            data = f.read(length)
            return data.decode('utf-8')
        except Exception as e:
            print(f"读取string时出错: {str(e)}")
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