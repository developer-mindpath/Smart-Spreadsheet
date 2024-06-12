from enum import Enum


class ContentTypeEnum(str, Enum):
    TEXT = "text"
    IMAGE_FILE = "image_file"
    IMAGE_URL = "image_url"
