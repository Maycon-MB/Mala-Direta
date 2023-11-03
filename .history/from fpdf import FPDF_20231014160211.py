from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(items):
    # Cria um objeto SimpleDocTemplate e define o tamanho da página como letter
    doc = SimpleDocTemplate("output.pdf", pagesize=letter)

    # Obtém um objeto StyleSheet com os estilos de texto pré-definidos
    styles = getSampleStyleSheet()

    # Inicializa uma lista vazia para armazenar os parágrafos
    story = []

    # Divide os itens em sublistas com no máximo 9 itens em cada
    sublists = [items[i:i+9] for i in range(0, len(items), 9)]

    # Para cada sublista de itens
    for sublist in sublists:
        # Inicializa uma lista vazia para armazenar os parágrafos da coluna atual
        column_items = []

        # Para cada item na sublista
        for item in sublist:
            # Cria um objeto Paragraph com o estilo de texto adequado e adiciona à lista de parágrafos da coluna
            column_items.append(Paragraph(item, styles["Normal"]))

        # Adiciona a lista de parágrafos da coluna ao documento
        story.append(column_items)

        # Ad
