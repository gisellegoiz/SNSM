#### Instalação do PostGreSQL pelo terminal
vm de instalação: 192.168.1.21

#### instalação:
sudo apt install postgresql postgresql-contrib

#### verificar a instalação:
sudo systemctl status postgresql.service

#### acessando:
sudo -u postgres psql

#### acessar o prompt de comando:
psql

#### para sair do prompt:
\q

#### criar um novo banco de dados:
createdb database

#### criar senha:
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'nova_senha';"

#### reestatar:
sudo systemctl restart postgresql

#### ajustando o arquivo de configuração para acesso com os demais hosts:

$ sudo vi /etc/postgresql/12/main/postgresql.conf
listen_addresses = 'localhost,192.168.1.21,192.168.1.66,192.168.1.78' 
#deve ser alterado substiruindo peer por md5




#### Integração do colab com o PostGreSQL usando ngrok ###

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

#### python code

connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
Aqui, host seria 0.tcp.ngrok.io e port seria 12345 (ou o que o ngrok fornecer).


# Execução de scripts do postgre
Necessario realizar a instalação das bibliotecas 
$ python3 -m pip install psycopg2-binary
$ pip install sqlalchemy
$ pip install pandas



Para execução de algumas biliotecas do sql é necessário especificar o caminho para a execução do script=  exemplo.: /usr/bin/python3 consulta.py

# 5.5.1.4.3. 3) Consultando métricas através do NBI baseado em OSM SOL005
Para coleta de métricas por meio do NBI, deve-se seguir o seguinte formato de URL:

https://<host-ip>:<nbi-port>/osm/nspm/v1/pm_jobs/<project-id>/reports/<network-service-id>

Onde:

<host-ip>: É a máquina onde o OSM está instalado.

<nbi-port>: A porta NBI, ou seja, 9999

<project-id>: Atualmente pode ser qualquer string.

<network-service-id>: É o NS ID obtido após a instanciação do serviço de rede.

Observe que um token deve ser obtido primeiro para consultar uma métrica. Mais informações sobre isso podem ser encontradas na documentação do OSM NBI

Em resposta, você obteria uma lista das métricas VNF disponíveis, por exemplo:

   performanceMetric: osm_cpu_utilization
   performanceValue:
       performanceValue:
           performanceValue: '0.9563615332000001'
           vduName: test_fet7912-2-ubuntuvnf2vdu1-1
           vnfMemberIndex: '2'
       timestamp: 1568977549.065



### 5.5.1.1. Gerenciamento de desempenho VNF

### A próxima etapa é ativar a coleta de métricas em seus VNFDs. Cada métrica a ser coletada do VIM para cada VDU deve ser descrita tanto no nível do VDU ​​quanto no nível do VNF. Por exemplo:

vdu:
   id: hackfest_basic_metrics-VM
  ...  
    monitoring-parameter:
    - id: vnf_cpu_util
      name: vnf_cpu_util
      performance-metric: cpu_utilization
    - id: vnf_memory_util
      name: vnf_memory_util
      performance-metric: average_memory_utilization
    - id: vnf_packets_sent
      name: vnf_packets_sent
      performance-metric: packets_sent
    - id: vnf_packets_received
      name: vnf_packets_received
      performance-metric: packets_received
Como você pode ver, uma lista de “métricas NFVI” é definida primeiro no nível VDU, que contém um ID e o nome da métrica normalizada correspondente (neste caso, cpu_utilizatione average_memory_utilization). Os nomes das métricas normalizadas são: cpu_utilization, average_memory_utilization, disk_read_ops, disk_write_ops, disk_read_bytes, disk_write_bytes, packets_received, packets_sent, packets_out_dropped,packets_in_dropped       



### 5.5.4.3. Exemplo
Obtenha os descritores:

git clone --recursive https://osm.etsi.org/gitlab/vnf-onboarding/osm-packages.git
Integre-os:

cd osm-packages
osm vnfpkg-create autoheal_vnf
osm nspkg-create autoheal_ns
Inicie o NS:

osm ns-create --ns_name heal --nsd_name autoheal_nsd --vim_account <VIM_ACCOUNT_NAME>|<VIM_ACCOUNT_ID>
osm ns-list
osm ns-show heal

