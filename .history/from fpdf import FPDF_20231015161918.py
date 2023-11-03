class PDF(FPDF):
    def set_line_height(self, height):
        self.ln(height)

def generate_pdf(file_path, data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=9)  # Define o tamanho padrão da fonte como 9

    page_width = pdf.w
    page_height = pdf.h

    # Defina a largura das colunas para preencher toda a largura da página
    item_width = page_width / 3

    item_height = page_height / 9

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            pdf.add_page()

        col = i % 3
        row = (i % 27) // 3
        x = col * item_width
        y = row * item_height + 1

        lines = item.split('\n')
        reduce_spacing = False  # Variável para controlar a redução do espaçamento

        for line in lines:
            if "eleitor[1]" in line or "cep_formatado" in line:  # Verifica os campos que precisam de tamanho diferente
                pdf.set_font("Arial", size=11)  # Define a fonte como Arial com tamanho 11
            else:
                pdf.set_font("Arial", size=9)  # Define a fonte como Arial com tamanho 9

            pdf.set_xy(x, y)
            pdf.multi_cell(item_width, item_height / 3, line, border=0, align="L")  # Alinha o texto à esquerda

            if "eleitor[4]" in line:
                reduce_spacing = True  # Ativa a redução do espaçamento

            if reduce_spacing:
                y += item_height / 3 - 2  # Reduz o espaço vertical para 2 entre as linhas
            else:
                y += item_height / 3 - 5  # Espaçamento padrão de 5 entre as linhas

    pdf.output(file_path)