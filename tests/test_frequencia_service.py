from app.services.frequencia_service import FrequenciaService
from app.services.status_service import StatusService

class FakeMateria:
    def __init__(self):
        self.carga_total = 60
        self.horas_por_aula = 2


class FakeMateriaRepo:
    def get_by_id(self, _):
        return FakeMateria()


class FakeAula:
    def __init__(self, horas, presente):
        self.horas = horas
        self.presente = presente


class FakeAulaRepo:
    def listar_por_materia(self, _):
        return [
            FakeAula(2, 1),
            FakeAula(2, 1),
            FakeAula(2, 0)
        ]


def test_calculo_frequencia():
    materia_repo = FakeMateriaRepo()
    aula_repo = FakeAulaRepo()

    service = FrequenciaService(materia_repo, aula_repo)

    resultado = service.calcular(1)

    assert resultado["frequencia"] == 66.67
    assert resultado["horas_presentes"] == 4
    assert resultado["horas_faltadas"] == 2