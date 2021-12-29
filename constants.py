import os


# used in decode_image for s3 service
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE_FOLDER = os.path.join(ROOT_DIR, "temp_files")
