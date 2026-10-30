# Instruções API
Arquivo de orientação da API

** Pré-requisitos:
- Python instalado - 3.14.7
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

Para instalar, digite o seguinte comando no terminal:
- pip install -r requirements.txt

Agora, crie um arquivo chamado `.env` na raiz da pasta ../api para armazenar as configurações de conexão do banco. 
Dê uma olhada no arquivo `env.example` de como deve ficar o arquivo. O que falta é colocar o nome do banco -` DB_DATABASE `-.

** Arquivo do banco separado, dê uma olhada
no código disponibilizado para criar tabelas e demais itens corretamente, se não estiver igual, irá dar erro. **

Feito isso, inicie a API com `python run.py` para testar se a configuração foi feita com sucesso.

## Configurações MQTT

Seguindo o seguinte caminho de pastas  --> application/configs e selecionar
o arquivo broker_configs.py, irá encontrar o arquivo responsável pela configuração
do MQTT, que serve para "escutar" e receber os dados postados pelo ESP32.

No arquivo contem 3 codigos diferentes de configuração:
- O primeiro é para realizar testes locais, o broker é o Mosquitto Broker, localmente
- O segundo é para o teste com o código disponivel no simulador WOKWI
- O terceiro é o mais importante, é o código que irá receber os dados do ESP32,
o dispositivo físico, fora da simulação.

É possível alternar entre as configurações, mas precisa de atenção em duas coisas:
- Para realizar o teste local, precisa ser feito a instalação e configuração 
do Mosquitto Broker
    - Para simular o envio de dados - como se fosse o esp32 - existe um modelo
    que esta neste projeto, é o arquivo `publisher.py`. Com a API rodando e o Mosquitto Broker aberto,
    abra um novo terminal e execute o arquivo, ele enviará as mensagens e
    deverá aparecer no terminal da API, logo em seguida, o valor será 
    guardado no banco.

- No Wokwi, o codigo disponibilizado entrega apenas 2 argumentos - temperatura e
umidade - mas, para a inserção do banco se faz necessário 3: temperatura, umidade
e indice uv. O código irá funcionar, mas o campo de indice virá como 0.