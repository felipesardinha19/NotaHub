import pytest
from app.services.status_service import StatusService

# Fixture para instanciar StatusService
@pytest.fixture
def status_service():
    return StatusService()

def test_status_ok(status_service):
    resultado = status_service.definir_status(80, 10)
    assert resultado == "Ok"

def test_status_risco(status_service):
    resultado = status_service.definir_status(72, 10)
    assert resultado == "Risco"

def test_status_reprovado_por_frequencia(status_service):
    resultado = status_service.definir_status(60, 10)
    assert resultado == "Reprovado"

def test_status_reprovado_por_horas(status_service):
    resultado = status_service.definir_status(80, 0)
    assert resultado == "Reprovado"