class StatusService:

    def definir_status(
        self,
        frequencia: float,
        horas_registradas: float,
        carga_total: float,
        horas_restantes: float
    ) -> str:

        semestre_em_andamento = horas_registradas < carga_total

        # 🔴 Já não pode mais faltar (limite atingido ou ultrapassado)
        # Se sua regra usa max(0, ...), horas_restantes nunca será negativa,
        # então considerar == 0 resolve.
        if horas_restantes == 0:
            if semestre_em_andamento:
                return "Semestre em andamento: limite de faltas excedido"
            else:
                return "Reprovado"

        # 🟡 Próximo do limite (alerta de 10% da carga total)
        if semestre_em_andamento and horas_restantes <= carga_total * 0.10:
            return "Semestre em andamento: risco de reprovação"

        # 🔵 Semestre ainda em andamento sem risco
        if semestre_em_andamento:
            return "Semestre em andamento"

        # 🟢 Semestre terminou, avalia aprovação final
        if frequencia >= 75:
            return "OK"
        else:
            return "Reprovado"