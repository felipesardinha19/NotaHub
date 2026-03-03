import os
import csv
import json
import sqlite3
from datetime import datetime


# ===============================
# 1️⃣ Backup completo do banco (.db)
# ===============================
def backup_database(db_path: str) -> str:
    """
    Cria backup do banco SQLite e retorna o caminho do arquivo gerado.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Banco de dados não encontrado: {db_path}")

    # Conexão com o banco original
    conn = sqlite3.connect(db_path)

    # Nome do arquivo de backup
    backup_dir = "data/backups"
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"notahub_backup_{timestamp}.db")

    # Cria conexão para o backup
    backup_conn = sqlite3.connect(backup_path)

    # 🔑 Aqui é que você precisa chamar backup no objeto connection
    conn.backup(backup_conn)

    backup_conn.close()
    conn.close()

    return backup_path


# ===============================
# 2️⃣ Exportar relatório em CSV
# ===============================
def exportar_relatorio_csv(usuario_id, materia_repo, frequencia_service, pasta_backup="backups") -> str:
    os.makedirs(pasta_backup, exist_ok=True)

    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(pasta_backup, f"relatorio_notahub_{data}.csv")

    materias = materia_repo.listar(usuario_id)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Materia",
            "Carga Total (h)",
            "Frequencia (%)",
            "Horas Presenca (h)",
            "Horas Faltadas (h)",
            "Horas Restantes (h)"
        ])

        for materia in materias:
            resultado = frequencia_service.calcular(materia.id, usuario_id)

            if not resultado:
                continue

            writer.writerow([
                materia.nome,
                materia.carga_total,
                round(resultado["frequencia"], 2),
                resultado["horas_presentes"],
                resultado["horas_faltadas"],
                resultado["horas_restantes"]
            ])

    return caminho


# ===============================
# 3️⃣ Backup técnico em JSON
# ===============================
def exportar_relatorio_json(usuario_id, materia_repo, frequencia_service, pasta_backup="backups") -> str:
    os.makedirs(pasta_backup, exist_ok=True)

    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(pasta_backup, f"relatorio_notahub_{data}.json")

    materias = materia_repo.listar(usuario_id)
    dados = []

    for materia in materias:
        resultado = frequencia_service.calcular(materia.id, usuario_id)

        if not resultado:
            continue

        dados.append({
            "materia": materia.nome,
            "carga_total": materia.carga_total,
            "frequencia": round(resultado["frequencia"], 2),
            "horas_presenca": resultado["horas_presentes"],
            "horas_faltadas": resultado["horas_faltadas"],
            "horas_restantes": resultado["horas_restantes"]
        })

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    return caminho