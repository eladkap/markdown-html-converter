import sys


def main() -> int:
    if len(sys.argv) != 2:
        print('Error: please enter .md file as input and .html file as output')
        return 1

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    convert_md_to_html(md_file, html_file)


if __name__ == '__main__':
    sys.exit(main())
