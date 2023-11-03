import pdfkit

def generate_pdf(content):
    # Define the options for the PDF generation
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None
    }

    # Generate the HTML content
    html_content = generate_html(content)

    # Generate the PDF using the HTML content
    pdfkit.from_string(html_content, 'output.pdf', options=options)

def generate_html(content):
    # Define the CSS style for the HTML content
    css_style = '''
        <style>
            body {
                font-size: 12px;
                text-align: left;
            }
            .page {
                width: 210mm;
                height: 297mm;
                margin: 0;
                padding: 0;
                page-break-after: always;
            }
            .column {
                width: 70mm;
                height: 297mm;
                float: left;
                padding: 5mm;
            }
            .rectangle {
                width: 60mm;
                height: 10mm;
                border: 1px solid black;
                margin-bottom: 5mm;
            }
        </style>
    '''

    # Generate the HTML content for the PDF
    html_content = '<html><head>{}</head><body>'.format(css_style)
    for i in range(27):
        if i % 3 == 0:
            html_content += '<div class="page">'
        html_content += '''
            <div class="column">
                <div class="rectangle">{}</div>
            </div>
        '''.format(content)
        if i % 3 == 2 or i == 26:
            html_content += '</div>'
    html_content += '</body></html>'

    return html_content

# Test the function
content = 'Sample Content'
generate_pdf(content)
