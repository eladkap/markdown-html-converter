class Utils:
    @staticmethod
    def write_html_file(html_lines: list, html_file: str, title: str):
        with open(html_file, 'w') as writer:
            writer.write('<html>\n')
            writer.write(f'<header><title>{title}</title></header>\n')
            writer.write('<body>\n')
            for html_line in html_lines:
                writer.write(f"{html_line}\n")
            writer.write('</body>\n')
            writer.write('</html>\n')
