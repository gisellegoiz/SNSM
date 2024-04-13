# SNSM

### Integração do colab com o PostGreSQL local foi necessario utilizar o ngrok

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
