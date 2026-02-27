class StatusService:

    def definir_status(
        self,
        frequencia: float,
        horas_registradas: float,
        carga_total: float,
        horas_restantes: float
    ) -> str:

        # 🔹 1️⃣ Se ainda não terminou o semestre
        if horas_registradas < carga_total:
            return "Em andamento"

        # 🔹 2️⃣ Se terminou, agora sim decide aprovação
        if frequencia >= 70:
            return "Ok"
        else:
            return "Reprovado"