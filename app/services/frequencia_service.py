# app/services/frequencia_service.py
from app.services.status_service import StatusService

class FrequenciaService:
    def __init__(self, materia_repo, aula_repo):
        self.materia_repo = materia_repo
        self.aula_repo = aula_repo
        self.status_service = StatusService()

    def calcular(self, materia_id: int, usuario_id: int) -> dict:
        materia = self.materia_repo.buscar_por_id(usuario_id, materia_id)
        if not materia:
            return {
                "frequencia": 0,
                "horas_presentes": 0,
                "horas_faltadas": 0,
                "horas_totais": 0,
                "horas_restantes": 0,
                "status": "ERRO"
            }

        # 🔒 Somente aulas desta matéria
        aulas = [a for a in self.aula_repo.listar_por_materia(usuario_id, materia_id)
                 if a.materia_id == materia_id]

        horas_presentes = sum(float(a.horas) for a in aulas if a.presente == 1)
        horas_faltadas = sum(float(a.horas) for a in aulas if a.presente == 0)
        horas_totais = horas_presentes + horas_faltadas

        carga_total = float(materia.carga_total or 0)
        frequencia = int((horas_presentes / carga_total) * 100) if carga_total > 0 else 0

        horas_max_faltas = carga_total * 0.30
        horas_restantes_para_reprovar = max(horas_max_faltas - horas_faltadas, 0)

        # Status correto
        if horas_faltadas > horas_max_faltas:
            status = "Reprovado"
        elif horas_totais >= carga_total:
            status = "Semestre em andamento"
        else:
            status = "OK"

        return {
            "frequencia": frequencia,
            "horas_presentes": horas_presentes,
            "horas_faltadas": horas_faltadas,
            "horas_totais": horas_totais,
            "horas_restantes": horas_restantes_para_reprovar,
            "status": status
        }