import os

from CarRental.s3_storage import MediaStorage, StaticStorage
from credential import project_env


class S3:
    def __init__(self, is_media=True):

        self.media_storage = MediaStorage() if is_media else StaticStorage()

    def __call__(self, directory, file, *args, **kwargs):
        try:
            if not file:
                raise "File not Found"
            file_path = os.path.join('{directory}/{env}'.format(env=project_env, directory=directory), file.name)
            self.media_storage.save(file_path, file)
            return file_path

        except Exception as e:
            raise e


