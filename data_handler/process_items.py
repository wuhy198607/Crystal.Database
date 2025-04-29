import json

# 读取原始文件
with open('data/items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 只保留index和name字段
simplified_items = []
for item in items:
    simplified_items.append({
        'index': item.get('index'),
        'name': item.get('name')
    })

# 写入新文件
with open('data/items_s.json', 'w', encoding='utf-8') as f:
    json.dump(simplified_items, f, ensure_ascii=False, indent=2)

print("处理完成！") 