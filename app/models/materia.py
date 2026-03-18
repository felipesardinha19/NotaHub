from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Materia:
    semestre_id: int
    nome: str
    usuario_id: int
    carga_total: float

    id: int | None = None
    aulas_por_semana: int = 0
    horas_por_aula: int = 0
    categoria: str = "Teórica"
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )