import pdfkit
import re

def markdown_to_html(text):
    """Converts a simple markdown-style text to HTML."""
    text = text.replace('**', '')  # Remove bold markers (not handling actual bold)
    text = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', text)  # Convert markdown headers to h3
    text = text.replace('\n', '<br>')  # Convert newlines to HTML line breaks
    return text

def create_pdf_report(summary, advice, output_path='financial_report.pdf'):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Financial Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #2c3e50; text-align: center; }}
            h2 {{ color: #34495e; }}
            h3 {{ color: #2980b9; }}
            .section {{ margin-bottom: 20px; }}
            ul {{ padding-left: 20px; }}
        </style>
    </head>
    <body>
        <h1>Financial Report</h1>

        <div class="section">
            <h2>Financial Summary</h2>
            {markdown_to_html(summary)}
        </div>

        <div class="section">
            <h2>Personalized Financial Advice</h2>
            {markdown_to_html(advice)}
        </div>
    </body>
    </html>
    """

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
    }

    pdfkit.from_string(html_content, output_path, options=options)
    print(f"PDF report generated: {output_path}")
