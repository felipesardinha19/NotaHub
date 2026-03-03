from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

@dataclass
class Usuarios:
    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    senha_hash: str = ""
    dt_criacao: str = field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    )
    