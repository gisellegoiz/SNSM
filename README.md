### Instalação do PostGreSQL pelo terminal
vm de instalação: 192.168.1.21

# instalação:
sudo apt install postgresql postgresql-contrib

# verificar a instalação:
sudo systemctl status postgresql.service

#acessando:
sudo -u postgres psql

# acessar o prompt de comando:
psql

# para sair do prompt:
\q

# criar um novo banco de dados:
createdb database

# criar senha:
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'nova_senha';"

# reestatar:
sudo systemctl restart postgresql

# ajustando o arquivo de configuração para acesso com os demais hosts:

$ sudo vi /etc/postgresql/12/main/postgresql.conf
listen_addresses = 'localhost,192.168.1.21,192.168.1.66,192.168.1.78' 
#deve ser alterado substiruindo peer por md5




### Integração do colab com o PostGreSQL usando ngrok ###

Devido ao banco estar instalado localmente, foi necessário utilizar o ngrok para criar uma conexão segura entre o colab e o postgresql.
Para macOS e Linux:
Descompacte o arquivo: Você pode usar um descompressor de arquivos ou o terminal com um comando como:
bash
Copy code
unzip /path/to/ngrok.zip -d /destination/folder
Torne-o executável: No terminal, navegue até o diretório onde o ngrok foi descompactado e torne o binário executável com:
bash
Copy code
chmod +x ngrok
Passo 3: Conectar sua conta
Para conectar o ngrok ao seu serviço online e aumentar os limites de uso:

Obtenha seu authtoken na página do ngrok, normalmente disponível em seu dashboard após o login.
Execute o ngrok com seu token:
bash
Copy code
./ngrok authtoken [Seu Authtoken]
Isso armazenará seu token de autenticação na configuração local do ngrok.
Passo 4: Iniciar um túnel
Para expor uma porta local (por exemplo, a porta 5432 do PostgreSQL):

Abra um terminal e navegue até o diretório onde o ngrok está localizado.
Execute o ngrok para expor a porta 5432:
bash
Copy code
./ngrok tcp 5432
Isso iniciará um túnel apontando para a porta 5432 do seu localhost, e o ngrok exibirá uma URL pública (por exemplo, 0.tcp.ngrok.io:12345) que você pode usar para acessar o serviço através da internet.


Conectar usando o Colab: O ngrok fornecerá um endereço como 0.tcp.ngrok.io:12345. Use este endereço e porta no seu script Colab para substituir localhost e 5432. Por exemplo:

# python code

connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
Aqui, host seria 0.tcp.ngrok.io e port seria 12345 (ou o que o ngrok fornecer).


# Execução de scripts do postgre
Para execução de algumas biliotecas do sql é necessário especificar o caminho para a execução do script=  exemplo.: /usr/bin/python3 consulta.py

