import os
from enum import Enum


class ErrorCode(Enum):
    SUCCESS = 0
    FILE_NOT_EXIST = 1
    BAD_MD_SYNTAX = 2


class Converter:
    @staticmethod
    def convert_md_to_html(md_file: str, html_file: str) -> int:
        if not os.path.exists(md_file):
            return ErrorCode.FILE_NOT_EXIST.value

        md_lines = []
        with open(md_file, 'r') as reader:
            md_lines = reader.readlines()

        for md_line in md_lines:
            pass

        return ErrorCode.SUCCESS.value
