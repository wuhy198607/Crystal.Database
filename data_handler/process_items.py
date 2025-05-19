import json

def process_items():
    # Read the original items.json
    with open('data/items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    # Read the translated items_s.json
    with open('data/items_s.json', 'r', encoding='utf-8') as f:
        translated_items = json.load(f)
    
    # Create a dictionary for quick lookup of translated names
    translated_names = {item['index']: item['name'] for item in translated_items}
    
    # Update the names in the original items
    for item in items:
        if item.get('index') in translated_names:
            item['name'] = translated_names[item['index']]
    
    # Write the updated items back to items.json
    with open('data/items.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    process_items() 