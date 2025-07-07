GlobalPay Selenium
Automação para testes de pagamento com cartões usando Selenium WebDriver no site Heartland Hyfin.

Descrição
Este projeto automatiza a submissão de formulários de pagamento utilizando cartões lidos de um arquivo .txt. Para cada cartão, o script preenche dados no site https://heartland.hyfin.app/5JH8XPHJXUJR/paymentLink, simula o pagamento e captura a resposta do sistema, indicando se o cartão foi aprovado ou reprovado.

Tecnologias
Python 3.x

Selenium WebDriver

WebDriver Manager para Chrome

ChromeDriver

Arquivos CSV e TXT para dados de cartões e BINs

Funcionalidades
Leitura de cartões a partir de um arquivo .txt no formato:
numero|mes|ano|cvv

Consulta de informações adicionais do cartão via arquivo .csv de BINs

Automação do preenchimento do formulário de pagamento via Selenium

Captura de mensagens de erro e status do pagamento

Suporte a múltiplos cartões em sequência

Requisitos
Python 3 instalado

Google Chrome instalado (compatível com o ChromeDriver)

Instalar dependências via pip:

bash
Copiar
Editar
pip install selenium webdriver-manager
Estrutura de arquivos
bash
Copiar
Editar
/globalpay-selenium
│
├── main.py                  # Script principal com a automação Selenium
├── cards.txt                # Arquivo texto com cartões para teste (formato: número|mês|ano|cvv)
├── bins.csv                 # Arquivo CSV contendo dados dos BINs dos cartões
├── README.md                # Este arquivo
Como usar
Configure os arquivos:

cards.txt: Inclua os cartões que deseja testar, cada linha no formato:
numero|mes|ano|cvv
Exemplo:
1234567890123456|07|2025|123

bins.csv: Inclua os dados dos BINs para obter informações adicionais no script.

Execute o script principal:

bash
Copiar
Editar
python main.py
O script vai abrir o navegador Chrome, navegar para o site de pagamento, preencher o formulário com os dados do cartão e imprimir no terminal o status (aprovado, reprovado e mensagens detalhadas).

Observações importantes
O script depende do layout e dos elementos HTML do site, que podem mudar e quebrar a automação.

Certifique-se de que o ChromeDriver está compatível com sua versão do Google Chrome.

O arquivo cards.txt deve estar no caminho configurado ou modifique no script.

Uso responsável: evite testes com cartões reais não autorizados.

Exemplo de saída
plaintext
Copiar
Editar
[ℹ️] BIN Info: VISA Credit 16 digits US BANK
Reprovada ➔ 1234567890123456|07|2025|123|VISA Credit 16 digits US BANK ➔ Invalid card, please try again ➔ @DIDIAC68
