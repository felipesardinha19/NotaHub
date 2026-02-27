from app.models.aula import Aula


class AulaRepository:

    def __init__(self, conn):
        self.conn = conn

    # CREATE
    def inserir(self, materia_id: int, data: str, horas: int, presente: int) -> None:
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO aulas (materia_id, data, horas, presente)
            VALUES (?, ?, ?, ?)
        """, (materia_id, data, horas, presente))

        self.conn.commit()

    # READ ALL BY MATERIA
    def listar_por_materia(self, materia_id: int) -> list[Aula]:
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM aulas
            WHERE materia_id = ?
            ORDER BY data ASC
        """, (materia_id,))

        rows = cursor.fetchall()

        return [Aula(*row) for row in rows]

    # DELETE
    def deletar(self, aula_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM aulas WHERE id = ?", (aula_id,))
        self.conn.commit()