import sqlite3
from app.models.semestre import Semestre
from datetime import date


class SemestreRepository:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def salvar(self, usuario_id: int, data_inicio: str, data_fim: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id 
                FROM semestre 
                WHERE usuario_id = ?
                LIMIT 1
            """, (usuario_id,))

            exists = cursor.fetchone()

            if exists:
                cursor.execute("""
                    UPDATE semestre 
                    SET data_inicio = ?, data_fim = ?
                    WHERE id = ?
                """, (data_inicio, data_fim, exists[0]))
            else:
                cursor.execute("""
                    INSERT INTO semestre (usuario_id, data_inicio, data_fim)
                    VALUES (?, ?, ?)
                """, (usuario_id, data_inicio, data_fim))

            conn.commit()

    def listar(self, usuario_id: int) -> list[Semestre]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, data_inicio, data_fim
                FROM semestre
                WHERE usuario_id = ?
                ORDER BY data_inicio ASC
            """, (usuario_id,))
            rows = cursor.fetchall()

        return [
            Semestre(
                id=r[0],
                usuario_id=r[1],
                data_inicio=r[2],
                data_fim=r[3]
            )
            for r in rows
        ]

    def obter_ultimo(self, usuario_id: int) -> Semestre | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, data_inicio, data_fim
                FROM semestre
                WHERE usuario_id = ?
                ORDER BY id DESC
                LIMIT 1
            """, (usuario_id,))
            row = cursor.fetchone()

        return (
            Semestre(
                id=row[0],
                usuario_id=row[1],
                data_inicio=row[2],
                data_fim=row[3]
            )
            if row else None
        )

    def obter_ativo(self, usuario_id: int) -> Semestre | None:
        hoje = date.today()

        for s in self.listar(usuario_id):
            inicio = date.fromisoformat(s.data_inicio)
            fim = date.fromisoformat(s.data_fim)
            if inicio <= hoje <= fim:
                return s

        return None