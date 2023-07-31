import os

from CarRental.s3_storage import MediaStorage, StaticStorage
from credential import project_env


class S3:
    def __init__(self, directory, file, is_media=True):
        if not file:
            raise "File not Found"
        self.file_path = os.path.join(
            '{directory}/{env}'.format(env=project_env, directory=directory),
            file.name
        )
        self.media_storage = MediaStorage() if is_media else StaticStorage()

    def __call__(self, file, *args, **kwargs):
        try:
            self.media_storage.save(self.file_path, self.file_path)
            return self.media_storage.url(self.file_path)

        except Exception as e:
            raise e

