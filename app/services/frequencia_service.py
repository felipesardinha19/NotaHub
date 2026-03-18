from app.services.status_service import StatusService

class FrequenciaService:

    def __init__(self, materia_repo, aula_repo):
        self.materia_repo = materia_repo
        self.aula_repo = aula_repo
        self.status_service = StatusService()

    def calcular(self, materia_id: int, usuario_id: int) -> dict:
        materia = self.materia_repo.buscar_por_id(usuario_id, materia_id)

        if not materia:
            return self._resultado_vazio()

        aulas = self.aula_repo.listar_por_materia(
            usuario_id,
            materia_id,
            materia.semestre_id
        )

        horas_presentes = sum(float(a.horas) for a in aulas if a.presente == 1)
        horas_faltadas = sum(float(a.horas) for a in aulas if a.presente == 0)
        horas_totais = horas_presentes + horas_faltadas

        carga_total = float(materia.carga_total or 0)

        frequencia = (
            int((horas_presentes / carga_total) * 100)
            if carga_total > 0 else 0
        )

        horas_max_faltas = carga_total * 0.30
        horas_restantes = max(horas_max_faltas - horas_faltadas, 0)

        # 🔥 AGORA USANDO O STATUS SERVICE
        status = self.status_service.definir_status(
            frequencia=frequencia,
            horas_registradas=horas_totais,
            carga_total=carga_total,
            horas_faltadas=horas_faltadas
        )

        return {
            "frequencia": frequencia,
            "horas_presentes": horas_presentes,
            "horas_faltadas": horas_faltadas,
            "horas_totais": horas_totais,
            "horas_restantes": horas_restantes,
            "status": status
        }

    def _resultado_vazio(self):
        return {
            "frequencia": 0,
            "horas_presentes": 0,
            "horas_faltadas": 0,
            "horas_totais": 0,
            "horas_restantes": 0,
            "status": "ERRO"
        }