import sqlite3
from app.models.aula import Aula


class AulaRepository:

    def __init__(self, db_path: str):
        self.db_path = db_path

    # CREATE
    def inserir(self, usuario_id: int, materia_id: int, semestre_id: int, data: str, horas: int, presente: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO aulas (usuario_id, materia_id, semestre_id, data, horas, presente)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (usuario_id, materia_id, semestre_id, data, horas, presente))
            conn.commit()

    # SOMA HORAS
    def somar_horas(self, usuario_id: int, materia_id: int, semestre_id: int) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(horas)
                FROM aulas
                WHERE usuario_id = ?
                AND materia_id = ?
                AND semestre_id = ?
            """, (usuario_id, materia_id, semestre_id))
            result = cursor.fetchone()
            return result[0] if result[0] else 0

    # READ
    def listar_por_materia(self, usuario_id: int, materia_id: int, semestre_id: int) -> list[Aula]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, materia_id, semestre_id, data, horas, presente, created_at
                FROM aulas
                WHERE materia_id = ?
                AND usuario_id = ?
                AND semestre_id = ?
                ORDER BY data ASC
            """, (materia_id, usuario_id, semestre_id))
            rows = cursor.fetchall()

        return [
            Aula(
                usuario_id=row[1],
                materia_id=row[2],
                semestre_id=row[3],
                data=row[4],
                horas=int(row[5]),
                presente=row[6],
                id=row[0],
                created_at=row[7]
            )
            for row in rows
        ]
    
    def listar_por_semestre(self, usuario_id: int, semestre_id: int) -> list[Aula]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, materia_id, semestre_id, data, horas, presente
                FROM aulas
                WHERE usuario_id = ? AND semestre_id = ?
                ORDER BY id DESC
            """, (usuario_id, semestre_id))
            rows = cursor.fetchall()
        
        return [
            Aula(
                id=r[0],
                usuario_id=r[1],
                materia_id=r[2],
                semestre_id=r[3],
                data=r[4],
                horas=r[5],
                presente=r[6]
            )
            for r in rows
        ]
    # DELETE
    def deletar_por_materia(self, materia_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM aulas WHERE materia_id = ?", (materia_id,))
            conn.commit()

    def deletar(self, aula_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM aulas WHERE id = ?", (aula_id,))
            conn.commit()