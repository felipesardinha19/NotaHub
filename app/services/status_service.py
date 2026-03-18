class StatusService:

    def definir_status(
        self,
        frequencia: float,
        horas_registradas: float,
        carga_total: float,
        horas_faltadas: float
    ) -> str:

        encerrado = horas_registradas >= carga_total
        horas_max_faltas = carga_total * 0.30

        # 🔴 Reprovado
        if horas_faltadas > horas_max_faltas:
            return "Reprovado por falta (Encerrado)" if encerrado else "Reprovado"

        # 🟡 Limite atingido (não pode mais faltar)
        if horas_faltadas == horas_max_faltas and not encerrado:
            return "Em risco (limite de faltas atingido)"

        # 🟡 Próximo do limite
        if not encerrado and horas_faltadas >= horas_max_faltas * 0.8:
            return "Em risco (próximo do limite)"

        # 🔵 Em andamento
        if not encerrado:
            return "OK - Semestre em andamento"

        # 🟢 Encerrado aprovado
        return "Aprovado (Encerrado)"