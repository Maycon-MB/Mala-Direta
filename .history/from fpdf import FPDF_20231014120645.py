from fpdf import FPDF

# Tamanho das etiquetas e folha (exemplo: 2x2 polegadas)
etiqueta_width = 2  # largura em polegadas
etiqueta_height = 2  # altura em polegadas
folha_width = 8.5  # largura da folha em polegadas
folha_height = 11  # altura da folha em polegadas

# Número total de etiquetas por folha
num_etiquetas_por_folha = 27

# Lista de dados de exemplo
dados = [
    {"nome": "João", "endereco": "Rua A, 123"},
    {"nome": "Maria", "endereco": "Avenida B, 456"},
    # Adicione mais dados aqui
]

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, title, 0, 1, 'C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Função para gerar o PDF com etiquetas
def gerar_pdf_etiquetas(dados):
    pdf = PDF()
    pdf.add_page()

    etiqueta_width_mm = etiqueta_width * 25.4  # Polegadas para milímetros
    etiqueta_height_mm = etiqueta_height * 25.4

    for dado in dados:
        nome = dado["nome"]
        endereco = dado["endereco"]
        etiqueta_text = f"Nome: {nome}\nEndereço: {endereco}"

        # Adicione uma etiqueta
        pdf.set_fill_color(200, 200, 200)  # Cor de fundo
        pdf.rect(pdf.w - etiqueta_width_mm, pdf.h - etiqueta_height_mm, etiqueta_width_mm, etiqueta_height_mm, 'F')
        pdf.set_fill_color(0)  # Redefina a cor de fundo para transparente
        pdf.chapter_body(etiqueta_text)

        if pdf.page_no() % num_etiquetas_por_folha == 0:
            pdf.add_page()

    pdf.output("etiquetas.pdf")

# Chame a função para gerar o PDF
gerar_pdf_etiquetas(dados)
