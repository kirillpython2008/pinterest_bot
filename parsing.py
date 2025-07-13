import yt_dlp
from pathlib import Path
import subprocess
import os

def is_ffmpeg_installed() -> bool:
    """Проверяет, установлен ли FFmpeg в системе."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_video(url: str, user_id: str, overwrite: bool = True) -> bool:
    """
    Скачивает видео с Pinterest, используя FFmpeg (если доступен) или запасной вариант.
    При наличии существующего файла перезаписывает его, если overwrite=True.

    Args:
        url (str): Ссылка на видео Pinterest.
        user_id (str): Идентификатор пользователя (для имени файла).
        overwrite (bool): Перезаписывать ли существующий файл. По умолчанию True.

    Returns:
        bool: True - если видео успешно скачано, False - если произошла ошибка.
    """
    # Создаем папку `media`, если её нет
    media_dir = Path("media")
    media_dir.mkdir(exist_ok=True)

    # Итоговый файл (media/media_123.mp4)
    output_file = media_dir / f"media_{user_id}.mp4"

    # Удаляем существующий файл, если требуется перезапись
    if overwrite and output_file.exists():
        output_file.unlink()

    # Настройки yt-dlp
    ydl_opts = {
        "outtmpl": str(output_file.with_suffix(".%(ext)s")),  # Временный файл
        "quiet": True,  # Убрать лишние логи
        "nooverwrites": not overwrite,  # Запретить перезапись, если overwrite=False
    }

    # Если FFmpeg установлен, скачиваем лучшее качество + объединяем аудио и видео
    if is_ffmpeg_installed():
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",  # Конвертируем в MP4
                }
            ],
        })
    else:
        # Без FFmpeg пробуем скачать готовый MP4 (если есть)
        ydl_opts["format"] = "best[ext=mp4]/best"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Если файл сохранился не как .mp4, переименовываем
        if not output_file.exists():
            downloaded_files = list(media_dir.glob(f"media_{user_id}.*"))
            if downloaded_files:
                os.rename(downloaded_files[0], output_file)

        if not output_file.exists():
            return False

        return True

    except Exception:
        # Удаляем временные файлы
        for temp_file in media_dir.glob(f"media_{user_id}.*"):
            if temp_file.exists():
                temp_file.unlink()
        return False
