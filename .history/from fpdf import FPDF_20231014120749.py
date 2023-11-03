from fpdf import FPDF

# Tamanho das etiquetas e folha (exemplo: 2x2 polegadas)
etiqueta_width = 2  # largura em polegadas
etiqueta_height = 2  # altura em polegadas
folha_width = 8.5  # largura da folha em polegadas
folha_height = 11  # altura da folha em polegadas

# Número total de etiquetas por folha
num_etiquetas_por_folha = 27

# Lista de dados de exemplo
dados = dados = [
    {"nome": "João Silva", "endereco": "Rua A, 123"},
    {"nome": "Maria Santos", "endereco": "Avenida B, 456"},
    {"nome": "Carlos Pereira", "endereco": "Travessa C, 789"},
    {"nome": "Ana Oliveira", "endereco": "Avenida D, 1011"},
    {"nome": "Pedro Almeida", "endereco": "Rua E, 1314"},
    {"nome": "Lúcia Ferreira", "endereco": "Avenida F, 1516"},
    {"nome": "Ricardo Souza", "endereco": "Rua G, 1718"},
    {"nome": "Juliana Lima", "endereco": "Travessa H, 1920"},
    {"nome": "Fernando Costa", "endereco": "Rua I, 2122"},
    {"nome": "Mariana Vieira", "endereco": "Avenida J, 2324"},
    {"nome": "Luiz Pereira", "endereco": "Travessa K, 2526"},
    {"nome": "Camila Santos", "endereco": "Rua L, 2728"},
    {"nome": "Paulo Carvalho", "endereco": "Avenida M, 2930"},
    {"nome": "Isabel Ribeiro", "endereco": "Travessa N, 3132"},
    {"nome": "Gabriel Martins", "endereco": "Rua O, 3334"},
    {"nome": "Cláudia Silva", "endereco": "Avenida P, 3536"},
    {"nome": "Marcos Lima", "endereco": "Travessa Q, 3738"},
    {"nome": "Helena Souza", "endereco": "Rua R, 3940"},
    {"nome": "Eduardo Vieira", "endereco": "Avenida S, 4142"},
    {"nome": "Aline Almeida", "endereco": "Travessa T, 4344"},
    {"nome": "Gustavo Pereira", "endereco": "Rua U, 4546"},
    {"nome": "Luciana Oliveira", "endereco": "Avenida V, 4748"},
    {"nome": "José Santos", "endereco": "Travessa W, 4950"},
    {"nome": "Elaine Costa", "endereco": "Rua X, 5152"},
    {"nome": "Rafael Silva", "endereco": "Avenida Y, 5354"},
    {"nome": "Simone Martins", "endereco": "Travessa Z, 5556"},
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
