from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak, Frame
from reportlab.lib import colors

# Tamanho das etiquetas e folha (exemplo: 2x2 polegadas)
etiqueta_width = 2 * 72  # 2 polegadas
etiqueta_height = 2 * 72  # 2 polegadas
folha_width = 8.5 * 72  # Largura da folha em polegadas
folha_height = 11 * 72  # Altura da folha em polegadas

# Número total de etiquetas por folha
num_etiquetas_por_folha = 27

# Lista de dados de exemplo
dados = [
    {"nome": "João", "endereco": "Rua A, 123"},
    {"nome": "Maria", "endereco": "Avenida B, 456"},
    # Adicione mais dados aqui
]

# Função para gerar o PDF com etiquetas
def gerar_pdf_etiquetas(dados):
    pdf_filename = "etiquetas.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=(folha_width, folha_height))

    elements = []

    for dado in dados:
        nome = dado["nome"]
        endereco = dado["endereco"]
        etiqueta_text = f"Nome: {nome}\nEndereço: {endereco}"

        # Crie um quadro (Frame) para cada etiqueta
        frame = Frame(0, 0, etiqueta_width, etiqueta_height, showBoundary=1, leftPadding=5)
        frame.addFromList([etiqueta_text], doc)

        elements.append(frame)

        if len(elements) % num_etiquetas_por_folha == 0:
            elements.append(PageBreak())

    doc.build(elements)

# Chame a função para gerar o PDF
gerar_pdf_etiquetas(dados)
