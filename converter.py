import os
import re
from enum import Enum

from utils import Utils


class ErrorCode(Enum):
    SUCCESS = 0
    FILE_NOT_EXIST = 1
    BAD_MD_SYNTAX = 2


class Converter:
    @staticmethod
    def is_valid_md(md_file: str) -> bool:
        return True

    @staticmethod
    def check_header(line: str, header_size: int):
        hash_tags = '#' * header_size
        header_pat = re.compile(fr"{hash_tags}\s+([\w]+)")
        m = header_pat.search(line)
        if m:
            return m.group(1)
        return None

    @staticmethod
    def check_first_header(line: str):
        return Converter.check_header(line, 1)

    @staticmethod
    def check_headers(md_line: str, html_lines: list):
        for header_size in range(4, 0, -1):
            header = Converter.check_header(md_line, header_size)
            if header:
                html_lines.append(f'<h{header_size}>{header}</h{header_size}>')
                return

    @staticmethod
    def check_bold_text(md_line: str, html_lines:list):
        bold_pat = re.compile(r"\*\*([\w]+)\*\*")
        for term in bold_pat.findall(md_line):
            html_lines.append(f'<b>{term}</b>\n')

    @staticmethod
    def convert_md_to_html(md_file: str, html_file: str) -> int:
        if not os.path.exists(md_file):
            print(f'Error: file {md_file} not exist')
            return ErrorCode.FILE_NOT_EXIST.value

        md_lines = []
        with open(md_file, 'r') as reader:
            md_lines = reader.readlines()

        if not Converter.is_valid_md(md_file):
            print('Error: invalid .md file')
            return ErrorCode.BAD_MD_SYNTAX.value

        html_lines = []
        for md_line in md_lines:
            Converter.check_headers(md_line, html_lines)
            Converter.check_bold_text(md_line, html_lines)

        Utils.write_html_file(html_lines, html_file, title='TITLE')

        return ErrorCode.SUCCESS.value
