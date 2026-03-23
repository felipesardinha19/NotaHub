import sqlite3
from app.models.materia import Materia
from typing import List, Optional


class MateriaRepository:

    def __init__(self, db_path: str):
        self.db_path = db_path


    def inserir(self, materia: Materia) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO materias 
                (nome, usuario_id, semestre_id, carga_total, aulas_por_semana, horas_por_aula, categoria)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    materia.nome,
                    materia.usuario_id,
                    materia.semestre_id,  
                    materia.carga_total,
                    materia.aulas_por_semana,
                    materia.horas_por_aula,
                    materia.categoria
                )
            )
            conn.commit()


    def listar_por_semestre(self, usuario_id: int, semestre_id: int) -> List[Materia]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, nome, usuario_id, semestre_id, carga_total, aulas_por_semana,
                    horas_por_aula, categoria, created_at
                FROM materias
                WHERE usuario_id = ? AND semestre_id = ?
                """,
                (usuario_id, semestre_id)
            )
            rows = cursor.fetchall()

        return [
            Materia(
                id=row[0],
                nome=row[1],
                usuario_id=row[2],
                semestre_id=row[3], 
                carga_total=row[4],
                aulas_por_semana=row[5],
                horas_por_aula=row[6],
                categoria=row[7],
                created_at=row[8]
            )
            for row in rows
        ]


    def buscar_por_id(self, usuario_id: int, materia_id: int) -> Optional[Materia]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, nome, usuario_id, semestre_id, carga_total, aulas_por_semana,
                    horas_por_aula, categoria, created_at
                FROM materias
                WHERE id = ? AND usuario_id = ?
                """,
                (materia_id, usuario_id)
            )
            row = cursor.fetchone()

        if row:
            return Materia(
                id=row[0],
                nome=row[1],
                usuario_id=row[2],
                semestre_id=row[3],  
                carga_total=row[4],
                aulas_por_semana=row[5],
                horas_por_aula=row[6],
                categoria=row[7],
                created_at=row[8]
            )
        return None


    def deletar(self, materia_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materias WHERE id = ?", (materia_id,))
            conn.commit()
            return cursor.rowcount > 0