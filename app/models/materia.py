from dataclasses import dataclass
from datetime import datetime

@dataclass
class Materia:
    id: int | None = None
    nome: str = ""
    carga_total: float = 0
    aulas_por_semana: int = 0
    horas_por_aula: int = 0
    categoria: str = "Teórica"  # <-- adiciona isso
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")