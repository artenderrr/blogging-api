import os
import shutil
from typing import Callable

class FileManager:
    ignored = {".gitkeep"}

    @staticmethod
    def generate_full_file_names(directory: str) -> list[str]:
        full_file_names = []
        for file_name in os.listdir(directory):
            full_file_name = os.path.join(directory, file_name)
            if os.path.isfile(full_file_name) and file_name not in FileManager.ignored:
                full_file_names.append(full_file_name)
        return full_file_names
    
    @staticmethod
    def validate_directories_existence(func: Callable[..., None]) -> Callable[..., None]:
        def wrapper(*args: str, **kwargs: str) -> None:
            directories = args + tuple(kwargs.values())
            for directory in directories:
                if not os.path.exists(directory):
                    raise FileNotFoundError(f"Directory {directory} doesn't exist")
            func(*args, **kwargs)
        return wrapper

    @staticmethod
    @validate_directories_existence
    def transfer_files(source_dir: str, destination_dir: str) -> None:
        for full_file_name in FileManager.generate_full_file_names(source_dir):
            shutil.copy(full_file_name, destination_dir)

    @staticmethod
    @validate_directories_existence
    def clear_directory(directory: str) -> None:
        for full_file_name in FileManager.generate_full_file_names(directory):
            os.remove(full_file_name)

class Backup:
    def __init__(self, *, source_dir: str, backup_dir: str) -> None:
        self.source_dir = source_dir
        self.backup_dir = backup_dir
        self._create()

    def _create(self) -> None:
        FileManager.transfer_files(self.source_dir, self.backup_dir)

    def restore(self) -> None:
        FileManager.transfer_files(self.backup_dir, self.source_dir)
        FileManager.clear_directory(self.backup_dir)