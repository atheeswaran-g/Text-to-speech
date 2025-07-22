from flask import Flask, request, send_file, render_template_string
import pdfkit
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Text to PDF Converter</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                textarea { width: 100%; height: 300px; }
                button { padding: 10px 20px; margin-top: 10px; }
            </style>
        </head>
        <body>
            <h1>Text to PDF Converter</h1>
            <form action="/convert" method="post">
                <textarea name="text" placeholder="Enter your text here..."></textarea><br>
                <button type="submit">Convert to PDF</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    text = request.form.get('text', '')
    
    if not text:
        return "No text provided", 400
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        <pre>{text}</pre>
    </body>
    </html>
    """
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name
        
        pdfkit.from_string(html_content, pdf_path)
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='converted.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500
    finally:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)