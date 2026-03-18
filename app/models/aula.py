from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Aula:
    usuario_id: int
    materia_id: int
    semestre_id: int
    data: str
    horas: int
    presente: int
    id: int | None = None
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )