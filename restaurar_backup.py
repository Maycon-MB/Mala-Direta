import os
import sys
import psycopg2
import PySimpleGUI as sg

if getattr(sys, 'frozen', False):
    # Se estiver executando como um executável congelado, o ícone está incorporado.
    icon_path = sys._MEIPASS  # Caminho para o diretório temporário com ícones incorporados
    icon_file = os.path.join(icon_path, 'Mala_Direta.ico')
else:
    # Se estiver executando como script, o ícone deve estar no mesmo diretório.
    icon_file = 'Mala_Direta.ico'


sg.theme('DarkTeal12')

class AplicacaoBackup:
    def __init__(self):
        # Configuração da conexão com o banco de dados
        self.config_banco_dados()

        # Definição do layout da interface gráfica
        layout = [
            [sg.Text("Selecione o arquivo de backup:")],
            [sg.InputText(key="CAMINHO_BACKUP", size=(50, 1), ), sg.FileBrowse()],
            [sg.Button("Restaurar Backup", key="RESTAURAR_BACKUP")],
            [sg.Output(size=(60, 10), expand_x=True, expand_y=True)],
        ]

        # Criação da janela
        self.janela = sg.Window("Restauração de Backup PostgreSQL", layout, resizable=True, finalize=True)

    def config_banco_dados(self):
        self.conexao = psycopg2.connect(
            host='roundhouse.proxy.rlwy.net',
            user='postgres',
            password='FbBC5BdfeCaDdEF2aAcb6G2CdeFd366f',
            database='railway',
            port='32589'
        )

    def restaurar_backup(self, caminho_backup):
        try:
            with self.conexao.cursor() as cursor:
                with open(caminho_backup, "r") as arquivo:
                    # Lê o arquivo e executa instruções SQL a partir dos dados
                    for linha in arquivo:
                        dados = linha.strip().split(';')
                        sql = f"INSERT INTO tabela_eleitores VALUES ({', '.join(['%s']*len(dados))})"
                        cursor.execute(sql, dados)

            self.conexao.commit()
            print("Restauração concluída com sucesso!")

        except Exception as e:
            print(f"Erro durante a restauração: {e}")

    def executar(self):
        while True:
            evento, valores = self.janela.read()

            if evento == sg.WIN_CLOSED:
                break

            elif evento == "RESTAURAR_BACKUP":
                caminho_backup = valores["CAMINHO_BACKUP"]
                if caminho_backup:
                    self.restaurar_backup(caminho_backup)
                else:
                    print("Por favor, selecione um arquivo de backup.")

        self.janela.close()

if __name__ == "__main__":
    app = AplicacaoBackup()
    app.executar()
