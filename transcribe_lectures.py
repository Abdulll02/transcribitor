import whisper
import os
import time
from moviepy.editor import VideoFileClip

def create_folders():
    folders = ['input_videos', 'transcripts', 'temp_audio']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f" Создана папка: {folder}")

def check_video_files():
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    video_files = []
    
    for file in os.listdir('input_videos'):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_files.append(file)
    
    return video_files

def extract_audio_from_video(video_path, audio_path):
    # Эта функция извлекает аудио из видео файла   
    
    try:
        print("     Извлекаем аудио...")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(
            audio_path, 
            verbose=False, 
            logger=None,
            bitrate="64k"
        )
        video.close()
        return True
    except Exception as e:
        print(f"     Ошибка извлечения аудио: {e}")
        return False

def transcribe_audio(audio_path, model):
    # Эта функция транскрибирует аудио файл

    try:
        # абсолютный путь для надежности
        abs_path = os.path.abspath(audio_path)
        print(f"     Распознаём речь... ({abs_path})")
        
        result = model.transcribe(
            abs_path,
            language="ru",
            fp16=False,
            task="transcribe"
        )
        return result["text"]
    except Exception as e:
        print(f"     Ошибка транскрибации: {e}")
        return ""

def format_filename(name):
    # Форматирует имя файла для сохранения
    name = os.path.splitext(name)[0]
    name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_'))
    return name.strip()

def main():
    # ОСНОВНАЯ ФУНКЦИЯ ДЛЯ ТРАНСКРИБАЦИИ ВИДЕО

    print("🎯 WHISPER - ТРАНСКРИБАЦИЯ ЛЕКЦИЙ")
    print("=" * 50)
    
    # создаем папки (но это на случай если просто запустить скрипт в пустой среде)
    create_folders()
    
    # проверяем видео файлы
    video_files = check_video_files()
    
    if not video_files:
        print(" В папке 'input_videos' не найдены видео файлы!")
        print("\n Поддерживаемые форматы:")
        print("   - MP4, AVI, MOV, MKV, WMV")
        print("\n Положите ваши видео файлы в папку 'input_videos' и запустите скрипт снова")
        return
    
    print(f" Найдено видео файлов: {len(video_files)}")
    for i, file in enumerate(video_files, 1):
        print(f"   {i}. {file}")
    
    # загружаем модель Whisper
    print("\n Загружаем модель Whisper...")
    
    try:
        model = whisper.load_model("base")
        print("    Модель 'base' успешно загружена!")
    except Exception as e:
        print(f"    Ошибка загрузки модели: {e}")
        return
    
    # обрабатываем каждое видео
    print(f"\n Начинаем обработку {len(video_files)} видео...")
    total_start_time = time.time()
    
    for i, video_file in enumerate(video_files, 1):
        video_path = os.path.join('input_videos', video_file)
        output_filename = f"{format_filename(video_file)}.txt"
        output_path = os.path.join('transcripts', output_filename)
        audio_path = os.path.join('temp_audio', f"audio_{i}.mp3")
        
        print(f"\n{'='*60}")
        print(f" Обрабатываем видео {i}/{len(video_files)}:")
        print(f"    Файл: {video_file}")
        print(f"    Результат: {output_filename}")
        print(f"    Аудио: {audio_path}")
        print(f"{'='*60}")
        
        video_start_time = time.time()
        
        try:
            # 1: Извлекаем аудио в локальную папку
            if not extract_audio_from_video(video_path, audio_path):
                continue
            
            audio_time = time.time() - video_start_time
            print(f"     Аудио извлечено за {audio_time:.1f} сек")
            
            # проверяем что файл создан
            if not os.path.exists(audio_path):
                print(f"     Аудио файл не создан: {audio_path}")
                continue
            
            file_size = os.path.getsize(audio_path)
            print(f"     Размер аудио файла: {file_size / (1024*1024):.1f} МБ")
            
            # 2: Транскрибируем
            text = transcribe_audio(audio_path, model)
            
            if not text:
                print("     Не удалось распознать текст")
                print("     Аудио файл сохранен для отладки:", os.path.abspath(audio_path))
                continue
            
            transcribe_time = time.time() - video_start_time - audio_time
            print(f"     Текст распознан за {transcribe_time:.1f} сек")
            
            # 3: Сохраняем результат
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            total_video_time = time.time() - video_start_time
            print(f"     Файл сохранен: {output_path}")
            print(f"     Статистика:")
            print(f"       - Время обработки: {total_video_time:.1f} сек")
            print(f"       - Символов: {len(text)}")
            print(f"       - Слов: {len(text.split())}")
            
            # превью текста
            preview = text[:300] + "..." if len(text) > 300 else text
            print(f"    👁 Превью: {preview}")
            
        except Exception as e:
            print(f"     Ошибка при обработке видео: {e}")
            print("     Аудио файл сохранен для отладки:", os.path.abspath(audio_path))
        
        # показываем прогресс
        if i < len(video_files):
            elapsed_time = time.time() - total_start_time
            avg_time_per_video = elapsed_time / i
            remaining_videos = len(video_files) - i
            estimated_remaining = avg_time_per_video * remaining_videos
            
            print(f"\n ПРОГРЕСС: {i}/{len(video_files)}")
            print(f"    Примерное время до завершения: {estimated_remaining/60:.1f} мин")
    
    # финальная статистика
    total_time = time.time() - total_start_time
    print(f"\n ВСЕ ВИДЕО ОБРАБОТАНЫ!")
    print(f" ИТОГИ:")
    print(f"   - Обработано видео: {len(video_files)}")
    print(f"   - Общее время: {total_time/60:.1f} минут")
    print(f"   - Тексты сохранены в папке 'transcripts'")
    print(f"   - Аудио файлы сохранены в папке 'temp_audio'")
    
    # показываем список созданных файлов
    print(f"\n Созданные файлы:")
    transcript_files = [f for f in os.listdir('transcripts') if f.endswith('.txt')]
    for file in transcript_files:
        file_path = os.path.join('transcripts', file)
        size_kb = os.path.getsize(file_path) / 1024
        print(f"   - {file} ({size_kb:.1f} КБ)")
    
    # показываем сохраненные аудио файлы
    audio_files = [f for f in os.listdir('temp_audio') if f.endswith('.mp3')]
    if audio_files:
        print(f"\n Сохраненные аудио файлы:")
        for file in audio_files:
            file_path = os.path.join('temp_audio', file)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"   - {file} ({size_mb:.1f} МБ)")

if __name__ == "__main__":
    main()
