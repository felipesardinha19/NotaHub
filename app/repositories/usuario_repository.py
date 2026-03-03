import sqlite3
from app.models.usuarios import Usuarios


class UsuarioRepository:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def criar(self, usuario: Usuarios) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nome, email, senha_hash, dt_criacao)
                VALUES (?, ?, ?, ?)
            """, (usuario.nome, usuario.email, usuario.senha_hash, usuario.dt_criacao))

            conn.commit()
            return cursor.lastrowid

    def buscar_por_email(self, email: str) -> Usuarios | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email, senha_hash, dt_criacao
                FROM usuarios
                WHERE email = ?
            """, (email,))
            row = cursor.fetchone()

        if row:
            return Usuarios(*row)

        return None

    def listar_todos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email, senha_hash, dt_criacao
                FROM usuarios
            """)
            rows = cursor.fetchall()

        return [
            Usuarios(*row)
            for row in rows
        ]