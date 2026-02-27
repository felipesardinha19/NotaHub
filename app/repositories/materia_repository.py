# app/repositories/materia_repository.py

from app.models.materia import Materia

class MateriaRepository:
    def __init__(self, conn):
        self.conn = conn

    def inserir(self, materia: Materia) -> Materia:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO materias (nome, carga_total, aulas_por_semana, horas_por_aula, categoria)
                VALUES (?, ?, ?, ?, ?)
            """, (
                materia.nome,
                materia.carga_total,
                materia.aulas_por_semana,
                materia.horas_por_aula,
                materia.categoria
            ))
            materia.id = cursor.lastrowid
        return materia

    def listar(self) -> list[Materia]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, nome, carga_total, aulas_por_semana, horas_por_aula, categoria, created_at 
            FROM materias
        """)
        rows = cursor.fetchall()
        return [Materia(*row) for row in rows]

    def buscar_por_id(self, materia_id: int) -> Materia | None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, nome, carga_total, aulas_por_semana, horas_por_aula, categoria, created_at 
            FROM materias 
            WHERE id = ?
        """, (materia_id,))
        row = cursor.fetchone()
        return Materia(*row) if row else None

    def deletar(self, materia_id: int) -> bool:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM materias WHERE id = ?", (materia_id,))
            return cursor.rowcount > 0