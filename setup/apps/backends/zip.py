from zipfile import ZipFile, BadZipFile
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string


def extract_zip_file(file_data):
    try:
        with ZipFile(file_data, 'r') as zip_file:
            data = []
            for file_info in zip_file.infolist():
                if not file_info.is_dir():
                    with zip_file.open(file_info.filename, 'r') as zip_extracted:
                        extracted_file = ContentFile(
                            zip_extracted.read(), file_info.filename)
                        data.append([file_info.filename, extracted_file])
            return data
    except BadZipFile:
        return None
