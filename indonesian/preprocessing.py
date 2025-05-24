import re
import string
from tqdm import tqdm
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

factory = StemmerFactory()
stemmer = factory.create_stemmer()
stem_cache = {}

def cached_stem(word):
    if word not in stem_cache:
        stem_cache[word] = stemmer.stem(word)
    return stem_cache[word]

stop_words = set(stopwords.words('indonesian'))
tokenizer = RegexpTokenizer(r'\w+')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    
    tokens = tokenizer.tokenize(text)
    print(f"Токенов после токенизации: {len(tokens)}")
    
    tokens = [word for word in tokens if word not in stop_words]
    print(f"Токенов после удаления стоп-слов: {len(tokens)}")
    
    # Стемминг с кэшем и прогресс-баром
    tokens = [cached_stem(word) for word in tqdm(tokens, desc="Стемминг")]
    
    return ' '.join(tokens)

# Обработка по частям
chunk_size = 50000

with open("C:/Work/kurs/indonezian_texts/indonesian_corpus.txt", 'rt', encoding='utf-8') as infile:
    with open("C:/Work/kurs/indonezian_texts/done_indonesian_corpus.txt", 'w', encoding='utf-8', buffering=1) as outfile:  # buffering=1 → буферизация по строкам
        chunk_counter = 0
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break
            
            processed = preprocess_text(chunk)
            chunk_counter += 1
            
            if processed.strip():
                outfile.write(processed + ' ')
                outfile.flush()  # Принудительный сброс буфера
                print(f"Чанк {chunk_counter} записан")  # Логирование
                print(f"Обработан чанк {chunk_counter}, размер: {len(processed)} символов")
            
            del chunk, processed  # Освобождение памяти
