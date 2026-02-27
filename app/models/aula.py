from dataclasses import dataclass

@dataclass
class Aula:
    id: int
    materia_id: int
    data: str
    horas: int
    presente: int
    created_at: str