# test_db.py
import pytest
import sqlite3
from app.repositories.materia_repository import MateriaRepository
from app.models.materia import Materia

@pytest.fixture
def repo(tmp_path):
    db_file = tmp_path / "test_notahub.db"

    # Cria tabela no banco temporário
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE materias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                carga_total REAL NOT NULL,
                aulas_por_semana INTEGER NOT NULL,
                horas_por_aula INTEGER NOT NULL,
                categoria TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    repository = MateriaRepository(str(db_file))
    yield repository
    # tmp_path é automaticamente limpo pelo pytest

def test_inserir_materia(repo):
    materia = Materia(
        nome="Matemática",
        carga_total=80,
        aulas_por_semana=4,
        horas_por_aula=2,
        categoria="Teórica"
    )

    repo.inserir(materia)

    materias = repo.listar()
    assert len(materias) == 1
    assert materias[0].nome == "Matemática"
    assert materias[0].carga_total == 80

def test_buscar_por_id(repo):
    materia = Materia(
        nome="História",
        carga_total=60,
        aulas_por_semana=2,
        horas_por_aula=2,
        categoria="Teórica"
    )

    repo.inserir(materia)

    materia_id = repo.listar()[0].id
    encontrada = repo.buscar_por_id(materia_id)

    assert encontrada is not None
    assert encontrada.nome == "História"