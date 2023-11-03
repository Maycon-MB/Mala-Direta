from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def create_pdf(data):
    # Create a PDF document with the specified page size
    doc = SimpleDocTemplate("output.pdf", pagesize=letter)

    # Create a table with 27 items per page divided into 3 columns of 9 items each
    table_data = []
    for i in range(0, len(data), 9):
        row = data[i:i+9]
        table_data.append(row)

    # Create the table
    table = Table(table_data, colWidths=60, rowHeights=30)

    # Apply the formatting to the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the document
    doc.build([table])
