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
    def check_newline(line: str, html_lines: list) -> bool:
        newline_pat = re.compile(r"^[ ]*\n")
        if newline_pat.match(line):
            html_lines.append('<br>')
            return True
        return False

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
    def check_headers(md_line: str, html_lines: list) -> bool:
        for header_size in range(4, 0, -1):
            header = Converter.check_header(md_line, header_size)
            if header:
                html_lines.append(f'<h{header_size}>{header}</h{header_size}>')
                return True
        return False

    @staticmethod
    def check_style(md_line: str, html_lines: list):
        term_pat = re.compile(r"(\S+)")

        bold_pat = re.compile(r"^\*\*([\w]+)\*\*$")
        italic_pat = re.compile(r"^\*([\w]+)\*$")
        for term in term_pat.findall(md_line):
            m = bold_pat.search(term)
            if m:
                html_lines.append(f'<b>{m.group(1)}</b>')
                continue
            m = italic_pat.search(term)
            if m:
                html_lines.append(f'<i>{m.group(1)}</i>')
                continue
            html_lines.append(term)

    @staticmethod
    def check_regular_line(md_line, html_lines: list):
        html_lines.append(md_line)

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
            if Converter.check_newline(md_line, html_lines):
                continue
            if Converter.check_headers(md_line, html_lines):
                continue
            if Converter.check_style(md_line, html_lines):
                continue
            # Converter.check_regular_line(md_line, html_lines)

        Utils.write_html_file(html_lines, html_file, title='TITLE')

        return ErrorCode.SUCCESS.value
