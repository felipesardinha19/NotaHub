import sqlite3
from pathlib import Path

"""O que isso faz?
__file__ → arquivo atual
.resolve() → pega o caminho absoluto
.parent → sobe pastas
Vai até a raiz do projeto
Entra na pasta data
Cria/usa o arquivo notahub.db
Isso evita usar caminho fixo tipo "../data/notahub.db".
É mais profissional."""

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "notahub.db"


"""Por que isso é importante?
O SQLite por padrão NÃO ativa foreign key.
Sem isso, você poderia:
Criar aula com materia_id inexistente
Quebrar integridade
Esse comando força o banco a respeitar relacionamentos.
Isso é coisa de sistema sério."""
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        semestre_id INTEGER NOT NULL,
        carga_total REAL NOT NULL CHECK (carga_total > 0),
        aulas_por_semana INTEGER NOT NULL CHECK (aulas_por_semana > 0),
        horas_por_aula INTEGER NOT NULL CHECK (horas_por_aula BETWEEN 1 AND 4),
        categoria TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        """)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS aulas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        materia_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        semestre_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        horas INTEGER NOT NULL CHECK (horas BETWEEN 1 and 4),
        presente INTEGER NOT NULL CHECK (presente IN (0,1)),
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE)
        """)
    
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            dt_criacao TEXT NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS semestre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    """)
    
    """Bloquear a exclusão da matéria se existirem aulas vinculadas."""
    conn.commit()
    conn.close()