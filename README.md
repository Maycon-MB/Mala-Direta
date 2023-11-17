
# Mala Direta

Mala Direta em Python.
Este é um programa em Python que permite criar etiquetas de endereço para mala direta a partir de um banco de dados de eleitores. O programa é composto por várias funcionalidades, incluindo:

Geração de Etiquetas: O programa gera etiquetas de endereço formatadas a partir dos dados do banco de dados de eleitores.

Filtragem de Eleitores: Você pode aplicar filtros aos eleitores com base em critérios específicos, como idade, cidade, etc., antes de gerar as etiquetas.

Personalização de Etiquetas: As etiquetas de endereço podem ser personalizadas de acordo com suas preferências, incluindo o layout e o estilo do texto.

Exportação para PDF: As etiquetas de endereço são exportadas para um arquivo PDF, pronto para serem impressas.

Interface Gráfica Amigável: O programa possui uma interface gráfica intuitiva que facilita a interação e configuração das opções.

Como Usar
Para usar o programa, siga estas etapas:

Instalação: Certifique-se de que você possui o Python instalado em seu sistema. Você também precisará instalar as dependências necessárias, que estão listadas no arquivo requirements.txt.

Execução: Execute o arquivo main.py para iniciar a interface gráfica do programa.

Tela de Login com Senha
A primeira janela do seu projeto é a tela de login, que solicita uma senha de acesso para permitir a entrada no sistema. Abaixo estão os principais elementos desta tela:

Senha de Acesso: A senha correta para acesso ao sistema é definida como "123" podendo ser alterada obviamente.

Campo de Senha: Um campo de entrada de senha permite que o usuário insira a senha de acesso. A senha é ocultada por padrão, mas o botão "Mostrar / Ocultar" permite ao usuário exibir ou ocultar a senha.

Botão de Entrar: Após inserir a senha correta, o usuário pode pressionar o botão "Entrar" para acessar o sistema.

Verificação de Senha
Há uma função, verificar_senha, que verifica se a senha inserida pelo usuário corresponde à senha correta definida no código.

Layout Principal

O tema da janela é definido como 'DarkTeal12'.
A janela principal é dividida em seis colunas, cada uma contendo campos de entrada e rótulos relacionados às informações do eleitor.
A primeira coluna lida com informações pessoais, como nome e data de nascimento.
A segunda coluna contém informações de endereço, como logradouro, número e complemento.
A terceira coluna é dedicada a informações sobre bairro, cidade e UF.
A quarta coluna aborda informações de contato, incluindo e-mail, telefone e Instagram.
A quinta coluna é para dados adicionais, como zona, seção e local.
A sexta coluna inclui um campo de observações.
No final, há uma seção de botões para "Registrar eleitor", "Exibir Eleitores" e "Fechar".

Janela de Exibição de Eleitores

A segunda janela do seu projeto é dedicada à exibição e gerenciamento de eleitores registrados. Ela permite a visualização dos eleitores cadastrados e oferece funcionalidades como filtragem, impressão e exclusão. Abaixo estão os principais elementos desta janela:

Total de Eleitores: Na parte superior, é exibido o total de eleitores registrados.

Opções de Filtro: A janela oferece opções de filtro, permitindo que você selecione o critério de filtragem, como nome, data de nascimento ou observações, entre outros.

Tabela de Eleitores: A tabela exibe os eleitores registrados com informações detalhadas, incluindo matrícula, nome, data de nascimento, CEP, endereço, informações de contato, zona, seção e local.

Botões de Ação: Existem botões para executar ações específicas, como imprimir os dados, limpar filtros, deletar um eleitor e fechar a janela de exibição.

Seleção de Relatórios: Você pode selecionar diferentes tipos de relatórios, como etiquetas gerais, etiquetas com data de nascimento, relatórios por Instagram, e outros.

Filtros de Pesquisa: Há botões de filtro para facilitar a pesquisa com base em critérios específicos, como nome, logradouro, bairro, e assim por diante.

Janela de Edição de Eleitor

Esta função cria uma janela de edição para um eleitor específico. A janela permite a edição das informações do eleitor, incluindo matrícula, nome, data de nascimento, CEP, endereço, informações de contato, zona, seção, local e outras informações. Abaixo estão os principais elementos desta janela:

Campos de Informações: Cada campo é composto por um rótulo (por exemplo, "Nome:") e um campo de entrada onde o usuário pode editar as informações do eleitor. Os campos de entrada são preenchidos com os dados atuais do eleitor.

Botão de Salvamento: Há um botão "Salvar" que permite ao usuário salvar as alterações feitas nas informações do eleitor.


## Funcionalidades

O projeto possui as seguintes funcionalidades:

1. **Conexão com o Banco de Dados:** O código inclui funções para estabelecer uma conexão com um banco de dados PostgreSQL usando o módulo psycopg2.

2. **Registro de Eleitores:** Há uma função chamada `registrar_eleitor` que permite inserir informações de eleitores em uma tabela do banco de dados.

3. **Exibição de Eleitores:** A função `exibir_eleitores` recupera e exibe os registros de eleitores da tabela, ordenados por nome.

4. **Atualização de Registros:** A função `atualizar_registro` permite atualizar as informações de um eleitor com base no seu ID.

5. **Exclusão de Eleitores:** A função `deletar_porID` possibilita a exclusão de registros de eleitores por ID.

6. **Filtragem de Registros:** Existem várias funções de filtragem, como `filtrar_por_nome`, `filtrar_por_nascimento`, `filtrar_por_cep`, que permitem buscar registros com base em critérios específicos.

7. **Filtragem por Diversos Campos:** Funções para filtrar registros com base em campos como logradouro, número, complemento, bairro, cidade, UF, email, telefone, Instagram, observações, zona, seção e local.

8. **Consulta de CEP:** O projeto inclui funcionalidades para consulta de CEP, permitindo que os usuários insiram um CEP e recuperem automaticamente informações como logradouro, bairro, cidade e UF a partir de um serviço online.

9. **Formatação de Telefone:** A função `formatar_telefone` permite formatar números de telefone em um formato legível, adicionando hífens e espaços.

10. **Formatação de Data de Nascimento:** A função `formatar_nascimento` permite formatar datas de nascimento em um formato legível, adicionando barras.

11. **Limpeza de Campos de Janela:** A função `limpar_campos_janela` facilita a limpeza de campos de entrada em uma interface gráfica, permitindo a redefinição rápida de valores em campos de entrada.

Todas essas funcionalidades ajudam na gestão e busca de informações de eleitores em um banco de dados PostgreSQL, além de fornecer uma ferramenta útil para consulta de CEP e formatação de dados. Certifique-se de explicar cada funcionalidade de forma clara para os usuários que acessarem o README do seu projeto.




## Autores

- [@Maycon-MB](https://github.com/Maycon-MB)

