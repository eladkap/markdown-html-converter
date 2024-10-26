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
        header_pat = re.compile(fr"{hash_tags}\s+([\S ]+)")
        m = header_pat.search(line)
        if m:
            return m.group(1)
        return None

    @staticmethod
    def check_first_header(line: str):
        return Converter.check_header(line, 1)

    @staticmethod
    def check_headers(md_line: str, html_lines: list) -> bool:
        for header_size in range(6, 0, -1):
            header = Converter.check_header(md_line, header_size)
            if header:
                html_lines.append(f'<h{header_size}>{header}</h{header_size}>')
                return True
        return False

    @staticmethod
    def get_single_styled_line(md_line: str):
        bold_pat1 = re.compile(r"^\*\*([\w ]+)\*\*$")
        bold_pat2 = re.compile(r"^__([\w ]+)__$")
        italic_pat1 = re.compile(r"^\*([\w ]+)\*$")
        italic_pat2 = re.compile(r"^_([\w ]+)_$")
        strike_pat = re.compile(r"^~~([\w ]+)~~$")

        m1 = bold_pat1.search(md_line)
        m2 = bold_pat2.search(md_line)
        m3 = italic_pat1.search(md_line)
        m4 = italic_pat2.search(md_line)
        m5 = strike_pat.search(md_line)
        if m1 is not None:
            return f"<b>{m1.group(1)}</b>"
        if m2 is not None:
            return f"<b>{m2.group(1)}</b>"
        if m3 is not None:
            return f"<i>{m3.group(1)}</i>"
        if m4 is not None:
            return f"<i>{m4.group(1)}</i>"
        if m5 is not None:
            return f"<s>{m5.group(1)}</s>"
        return None

    @staticmethod
    def get_styled_line(md_line: str) -> str:
        html_lines = []
        term_pat = re.compile(r"(\S+)")
        bold_pat = re.compile(r"\*\*([\w]+)\*\*")
        italic_pat = re.compile(r"\*([\w]+)\*")
        anchor_pat = re.compile(r"\[(\w+)\]\(([\w\:\/\.]+)\)")

        for term in term_pat.findall(md_line):
            m = anchor_pat.search(term)
            if m:
                html_lines.append(f"<a href='{m.group(2)}'>{m.group(1)}</a>")
                continue

            m = bold_pat.search(term)
            if m:
                html_lines.append(f'<b>{m.group(1)}</b>')
                continue
            m = italic_pat.search(term)
            if m:
                html_lines.append(f'<i>{m.group(1)}</i>')
                continue
            html_lines.append(term)
        if len(html_lines) == 0:
            return None
        return '\n'.join(html_lines)

    @staticmethod
    def check_style(md_line: str, html_lines: list):
        term_pat = re.compile(r"(\S+)")
        bold_pat = re.compile(r"\*\*([\w]+)\*\*")
        italic_pat = re.compile(r"\*([\w]+)\*")
        anchor_pat = re.compile(r"\[(\w+)\]\(([\w\:\/\.]+)\)")

        for term in term_pat.findall(md_line):
            m = anchor_pat.search(term)
            if m:
                html_lines.append(f"<a href='{m.group(2)}'>{m.group(1)}</a>")
                continue

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
    def check_anchor(md_line: str, html_lines: list):
        anchor_pat = re.compile(r"\[(\w+)\]\(([\w\:\/\.]+)\)")
        m = anchor_pat.search(md_line)
        if m:
            html_lines.append(f"<a href='{m.group(2)}'>{m.group(1)}</a>")

    @staticmethod
    def get_unordered_list_item(md_line: str):
        pat = re.compile(r"^\-\s+([\S ]+)")
        m = pat.search(md_line)
        if m:
            line = m.group(1)
            styled_line = Converter.get_styled_line(line)
            return styled_line
        return None

    @staticmethod
    def is_unordered_list_item(md_line: str) -> bool:
        return Converter.get_unordered_list_item(md_line) is not None

    @staticmethod
    def get_ordered_list_item(md_line: str):
        pat = re.compile(r"^[1-9]+\.\s+([\S]+)")
        m = pat.search(md_line)
        if m:
            return m.group(1)
        return None

    @staticmethod
    def is_ordered_list_item(md_line: str) -> bool:
        return Converter.get_ordered_list_item(md_line) is not None

    @staticmethod
    def check_regular_line(md_line, html_lines: list):
        html_lines.append(md_line)

    @staticmethod
    def add_unordered_list(unordered_list: list, html_lines: list):
        if len(unordered_list) == 0:
            return
        html_lines.append('<ul>')
        for item in unordered_list:
            html_lines.append(f'<li>{item}</li>')
        html_lines.append('</ul>')

    @staticmethod
    def add_ordered_list(ordered_list: list, html_lines: list):
        if len(ordered_list) == 0:
            return
        html_lines.append('<ol>')
        for item in ordered_list:
            html_lines.append(f'<li>{item}</li>')
        html_lines.append('</ol>')

    @staticmethod
    def is_code_symbol(md_line: str) -> bool:
        return md_line.startswith("```")

    @staticmethod
    def add_code_lines(code_lines: list, html_lines: list):
        html_lines.append(
            '<p style=\"font-family: consolas; font-size: small; background-color: lightgray; left: 5px; right: 5px;\">')
        for code_line in code_lines:
            html_lines.append(code_line + '<br>')
        html_lines.append('</p>')

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

        unordered_list = []
        ordered_list = []
        html_lines = []

        i = 0
        while i < len(md_lines):
            md_line = md_lines[i]

            if Converter.check_newline(md_line, html_lines):
                i += 1
                continue

            if Converter.check_headers(md_line, html_lines):
                i += 1
                continue

            if Converter.is_code_symbol(md_line):
                code_lines = []
                i += 1
                md_line = md_lines[i]
                while i < len(md_lines) and not Converter.is_code_symbol(md_line):
                    code_lines.append(md_line)
                    i += 1
                    md_line = md_lines[i]
                Converter.add_code_lines(code_lines, html_lines)
                i += 1
                continue

            while i < len(md_lines) and Converter.is_unordered_list_item(md_line):
                list_item = Converter.get_unordered_list_item(md_line)
                if list_item is not None:
                    unordered_list.append(list_item)
                i += 1
                md_line = md_lines[i]
            Converter.add_unordered_list(unordered_list, html_lines)
            unordered_list = []

            while i < len(md_lines) and Converter.is_ordered_list_item(md_line):
                list_item = Converter.get_ordered_list_item(md_line)
                if list_item is not None:
                    ordered_list.append(list_item)
                i += 1
                md_line = md_lines[i]
            Converter.add_ordered_list(ordered_list, html_lines)
            ordered_list = []

            single_styled_line = Converter.get_single_styled_line(md_line)
            if single_styled_line is not None:
                html_lines.append(single_styled_line)
                i += 1
                continue

            html_lines.append(Converter.get_styled_line(md_line))

            i += 1

        Utils.write_html_file(html_lines, html_file, title='TITLE')

        return ErrorCode.SUCCESS.value
