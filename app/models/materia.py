from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Materia:
    id: int | None = None
    nome: str = ""
    usuario_id: int | None = None
    carga_total: float = 0
    aulas_por_semana: int = 0
    horas_por_aula: int = 0
    categoria: str = "Teórica"
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))