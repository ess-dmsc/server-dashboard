import time
import urllib.request

def extract_svg(html_content):
    svgs = []
    while '<svg' in html_content:
        start_index = html_content.index('<svg')
        end_index = html_content.index('</svg>') + len('</svg>')
        svg = html_content[start_index:end_index]
        svg = svg.replace('<svg ', '<svg style="background-color:white;" ')
        svg = svg.replace('<br>', '&#10;')
        svg = svg.replace('&var-server', '&#38;var-server')
        svg = svg.replace('&nbsp;', '&#160;')
        svgs.append(svg)
        html_content = html_content[end_index:]
    return svgs

def save_svg(svg_content, filename):
    with open(filename, 'w') as file:
        for svg in svg_content:
            file.write(svg)

def main():

    while True:
        with urllib.request.urlopen('http://localhost:8765/') as response:
            html_content = response.read().decode()

        svg = extract_svg(html_content)
        save_svg(svg, '/ess/ecdc/dashboard/data/instruments.svg')
        time.sleep(10)

if __name__ == "__main__":
    main()
