from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

data = [
    ["Nome 1", "Logradouro 1", "Número 1", "Complemento 1"],
    ["Nome 2", "Logradouro 2", "Número 2", "Complemento 2"],
    ["Nome 3", "Logradouro 3", "Número 3", "Complemento 3"],
]

pdf_filename = "MultiColumnAdjustedSpacing.pdf"

doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
elements = []

# Configurar estilos para a tabela
style = [
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('LEADING', (0, 0), (-1, -1), 12),  # Ajuste o espaçamento entre as linhas
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Espaçamento inferior
]

# Crie a tabela e defina os estilos
table = Table(data, colWidths=1.75*inch, rowHeights=0.5*inch)
table.setStyle(TableStyle(style))

elements.append(table)

# Adicione uma quebra de página
elements.append(PageBreak())

doc.build(elements)
