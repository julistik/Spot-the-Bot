import requests
import json
from slugify import slugify
import time

# Загрузка идентификаторов
with open('identifiers.json', 'r') as f:
    data = json.load(f)

identifiers = [item['identifier'] for item in data['response']['docs']]

for identifier in identifiers:
    try:
        # Получение метаданных
        metadata_url = f"https://archive.org/metadata/{identifier}"
        response = requests.get(metadata_url)
        metadata = response.json()
        
        # Поиск файлов DjVuTXT
        txt_files = [
            f for f in metadata.get('files', []) 
            if f.get('format') == 'DjVuTXT' 
            and f['name'].lower().endswith('.txt')
        ]

        if not txt_files:
            print(f"❌ Нет TXT: {identifier}")
            continue

        # Скачивание
        txt_file = txt_files[0]
        title = slugify(txt_file['name'].replace('_djvu.txt', ''))
        download_url = f"https://archive.org/download/{identifier}/{txt_file['name']}"
        
        response = requests.get(download_url)
        with open(f"{title}.txt", "wb") as f:
            f.write(response.content)
        
        print(f"✅ Скачано: {title}.txt")

    except Exception as e:
        print(f"⚠️ Ошибка: {str(e)}")
    
    time.sleep(3)
