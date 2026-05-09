# Transcribitor — скрипт для транскрибации видео с помощью Whisper

Кратко: этот проект извлекает аудио из видео (`input_videos/`), распознаёт речь с помощью модели Whisper и сохраняет результаты в `transcripts/`.

**Важно:** для корректной работы требуется установленный ffmpeg (см. раздел "FFmpeg").

---

## Быстрый старт

1. Клонируйте репозиторий и перейдите в папку проекта.
2. Создайте и активируйте виртуальное окружение (Windows, cmd.exe):

```cmd
python -m venv venv
venv\Scripts\activate
```

3. Установите зависимости:

```cmd
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Если вы уже устанавливали `openai-whisper` вручную из GitHub, можно просто установить оставшиеся пакеты:

```cmd
pip install moviepy==1.0.3
```

4. Положите видео в папку `input_videos/` и запустите скрипт:

```cmd
python transcribe_lectures.py
```

Результаты .txt появятся в `transcripts/`, аудио — в `temp_audio/`.

---

## FFmpeg (обязательно для moviepy)

`moviepy` использует `ffmpeg` для чтения и записи медиа. Без установленного `ffmpeg` извлечение аудио не сработает.

Рекомендованные способы установки на Windows:

- Через Chocolatey (требуются права администратора):

```cmd
choco install ffmpeg -y
```

- Через Scoop:

```cmd
scoop install ffmpeg
```

- Ручная загрузка: скачайте сборку (например с https://www.gyan.dev/ffmpeg/builds/), распакуйте и добавьте путь к папке `bin` в `PATH`.

Быстрая Python-альтернатива (но лучше установить обычный системный ffmpeg):

```cmd
pip install imageio-ffmpeg
```

Проверка установки:

```cmd
ffmpeg -version
```

---




## Траблшутинг

- Ошибка при установке `openai-whisper` (KeyError '__version__') — причина: сборка пытается получить метаданные версии из git. Решения:
  - Установите `setuptools_scm` и обновите `setuptools`/`wheel`:

    ```cmd
    pip install --upgrade pip setuptools wheel
    pip install setuptools_scm
    ```

  - Или установите Whisper напрямую из GitHub:

    ```cmd
    pip install git+https://github.com/openai/whisper.git@v20231117
    ```

- Если при запуске скрипта `moviepy` выдаёт ошибки при извлечении аудио — убедитесь, что `ffmpeg` в `PATH`.

- Если нужен GPU-ускоренный распознавание, используйте совместимые сборки `torch` и запускайте с `fp16=True` на поддерживаемых устройствах. Для примера у меня видюха rtx 2060super (8GB VRAM) и сборка pytorch с CUDA 11.8 (https://download.pytorch.org/whl/cu118) По умолчанию в `transcribe_lectures.py` используется `fp16=False` для совместимости с CPU,(т.к. у большинства из вас ноутбуки) но и на чистом CPU скрипт все еще отрабатывает за приемлемое кол-во времени, если у вас +- норм железо.

---

## Советы по использованию

- По умолчанию скрипт использует модель `base`. Для более высокой точности можно выбрать `large` (требует гораздо больше оперативной памяти и места на диске).

---

## Структура проекта

- `transcribe_lectures.py` — основной скрипт
- `requirements.txt` — зависимости
- `input_videos/` — папка для исходных видео
- `temp_audio/` — аудиофайлы извлеченные из видео
- `transcripts/` — результирующие тексты

---

Можете накинуть старку если было полезным)
