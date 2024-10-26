import argparse
import sys

from converter import Converter, ErrorCode

"""
Run:

python main.py --md-file ./md-files/example1.md --html-file C:/md-html-converter/example1.html

python main.py --md-file ./md-files/example2.md --html-file C:/md-html-converter/example2.html

"""


def main() -> int:
    parser = argparse.ArgumentParser(prog='md-html Converter',
                                     description='Markdown-HTML Converter')
    parser.add_argument('-m', '--md-file', required=True, help='md file path')
    parser.add_argument('-t', '--html-file', required=True, help='html file path')
    args = parser.parse_args()

    md_file = args.md_file
    html_file = args.html_file

    error_code = Converter.convert_md_to_html(md_file, html_file)

    if error_code == ErrorCode.SUCCESS.value:
        print(f'file {html_file} was created.')

    return error_code


if __name__ == '__main__':
    sys.exit(main())

    # example_num = 2
    # md_file = f'./md-files/example{example_num}.md'
    # html_file = f'C:/md-html-converter/example{example_num}.html'
    # error_code = Converter.convert_md_to_html(md_file, html_file)
