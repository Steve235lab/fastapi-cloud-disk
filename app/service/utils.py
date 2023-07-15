import os


class UtilService:
    @staticmethod
    def get_storage_path() -> str:
        return os.getenv("STORAGE_PATH")
