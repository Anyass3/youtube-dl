from pydantic import BaseSettings
import os
from pathlib import Path


home_dir = str(Path.home())
Path = os.path.join(home_dir, '.__youtube_temp__')

test_path = os.path.abspath('./.env')


class Settings(BaseSettings):
    app_name: str = "Awesome Youtube Downloader"
    api_key: str  # loaded from .env file or from ennvironment variable
    path: str = Path

    class Config:
        # use absolute path instead
        # because deepending on how you run this in production
        # it might not find the file with tha relalive file
        # but there should be no problem if they(the variables) are avilable as environment variables
        env_file = "backend/.env"
