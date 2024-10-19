import sys

from converter import Converter, ErrorCode

"""
Run:

python main.py C:/md-html-converter/example1.md C:/md-html-converter/example.html

"""


def main() -> int:
    if len(sys.argv) != 3:
        print('Error: please enter .md file as input and .html file as output')
        return 1

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    error_code = Converter.convert_md_to_html(md_file, html_file)

    if error_code == ErrorCode.SUCCESS.value:
        print(f'file {html_file} was created.')

    return error_code


if __name__ == '__main__':
    sys.exit(main())
