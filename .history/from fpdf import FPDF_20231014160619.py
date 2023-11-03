from fpdf import FPDF, HTMLMixin

# Crie uma classe personalizada com suporte a HTML
class MyPDF(FPDF, HTMLMixin):
    pass

# Crie uma instância da classe personalizada
pdf = MyPDF()

# Adicione uma página ao PDF
pdf.add_page()

# Escreva o conteúdo HTML no PDF
html_code = """
<html>
<body>
    <h1>Exemplo de PDF com colunas</h1>
    <div style="column-count: 3;">
        <p>Texto da coluna 1.</p>
        <p>Texto da coluna 2.</p>
        <p>Texto da coluna 3.</p>
        <!-- Adicione mais conteúdo aqui -->
    </div>
</body>
</html>
"""

pdf.write_html(html_code)

# Salve o PDF em um arquivo
pdf_file = "exemplo_multi_coluna.pdf"
pdf.output(pdf_file)
