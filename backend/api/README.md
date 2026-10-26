# Instruções API
Arquivo de orientação da API

** Pré-requisitos:
- Python instalado
- ODBC Driver 17 For SQL Server
- SQL Server
- Repositório GitHub clonado e aberto na IDE

Comando para clonar repositório:
`git clone [link repositorio]`

## Inicialização do Projeto
Antes de iniciar a API, é necessário realizar algumas etapas de inicialização de ambiente e instalações de dependências do projeto!

Primeiro, inicie o ambiente virtual:
### Windows - Powershell
- python -m venv venv
- .\venv\Scripts\Activate.ps1

### Windows - CMD
- python -m venv venv
- .\venv\Scripts\activate.bat

Uma pasta `.venv` será criada na raiz da pasta ../api/

Existe um arquivo `requirements.txt` que contém todas as bibliotecas e versões utilizadas.

Para instalar, digite o seguinte comando:
- pip install -r requirements.txt

Agora, crie um arquivo chamado `.env` na raiz da pasta ../api para armazenar as configurações de conexão do banco. 
Dê uma olhada no arquivo `.env.example` de como deve ficar o arquivo. O que falta é colocar o nome do banco -` DB_DATABASE `-.

** Arquivo do banco separado, dê uma olhada
no código disponibilizado para criar tabelas e demais itens corretamente, se não estiver igual, irá dar erro. **

Feito isso, inicie a API com `python run.py`.