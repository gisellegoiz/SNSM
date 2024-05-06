import psycopg2

try:
    # Conectar ao banco de dados
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1401",
        host="192.168.1.21"
    )

    # Criar um cursor
    cur = conn.cursor()

    # Executar uma consulta SQL
    cur.execute("SELECT * FROM slice_vm1")

    # Buscar os resultados
    rows = cur.fetchall()

    for row in rows:
        print(row)

    # Fechar a conexão
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Erro ao conectar ao PostgreSQL:", e)
