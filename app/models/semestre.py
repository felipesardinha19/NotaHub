from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class Semestre:
    data_inicio: date
    data_fim: date
    id: Optional[int] = None
    usuario_id: Optional[int] = None