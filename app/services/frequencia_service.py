from app.services.status_service import StatusService


class FrequenciaService:
    def __init__(self, materia_repo, aula_repo):
        self.materia_repo = materia_repo
        self.aula_repo = aula_repo

    def calcular(self, materia_id: int):
        materia = self.materia_repo.buscar_por_id(materia_id)
        aulas = self.aula_repo.listar_por_materia(materia_id)

        horas_presentes = sum(a.horas for a in aulas if a.presente == 1)
        horas_totais = sum(a.horas for a in aulas)
        horas_faltadas = horas_totais - horas_presentes

        if materia.carga_total == 0:
            frequencia = 0
        else:
            frequencia = round((horas_presentes / materia.carga_total) * 100, 2)

        horas_max_faltas = materia.carga_total * 0.30
        horas_restantes_para_reprovar = horas_max_faltas - horas_faltadas

        horas_registradas = horas_totais

        status_service = StatusService()
        status = status_service.definir_status(
            frequencia = frequencia,
            horas_registradas = horas_registradas,
            carga_total= materia.carga_total,
            horas_restantes=horas_restantes_para_reprovar)
                
        return {
            "frequencia": frequencia,
            "horas_presentes": horas_presentes,
            "horas_faltadas": horas_faltadas,
            "horas_restantes": horas_restantes_para_reprovar,
            "status": status
        }