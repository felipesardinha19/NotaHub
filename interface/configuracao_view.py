import os
import streamlit as st
import datetime
from app.services.backup_services import (
    exportar_relatorio_csv,
    exportar_relatorio_json,
    backup_database
)

# ==========================
# BACKUP & EXPORTAÇÃO
# ==========================
def render_backup_section(db_path: str, usuario_id: int, materia_repo, frequencia_service):
    st.subheader("💾 Backup e Exportação")
    col1, col2, col3 = st.columns(3)

    # ---------- BACKUP DO BANCO ----------
    with col1:
        if st.button("Gerar Backup (.db)", use_container_width=True):
            caminho = backup_database(db_path)
            if caminho and os.path.exists(caminho):
                with open(caminho, "rb") as f:
                    st.download_button(
                        label="Baixar Backup",
                        data=f,
                        file_name="notahub_backup.db",
                        mime="application/octet-stream",
                        use_container_width=True
                    )
            else:
                st.error("Erro ao gerar backup do banco.")

    # ---------- EXPORTAR CSV ----------
    with col2:
        if st.button("Gerar CSV", use_container_width=True):
            caminho = exportar_relatorio_csv(usuario_id, materia_repo, frequencia_service)
            if caminho and os.path.exists(caminho):
                with open(caminho, "rb") as f:
                    st.download_button(
                        label="Baixar CSV",
                        data=f,
                        file_name="relatorio_notahub.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.error("Erro ao gerar relatório CSV.")

    # ---------- EXPORTAR JSON ----------
    with col3:
        if st.button("Gerar JSON", use_container_width=True):
            caminho = exportar_relatorio_json(usuario_id, materia_repo, frequencia_service)
            if caminho and os.path.exists(caminho):
                with open(caminho, "rb") as f:
                    st.download_button(
                        label="Baixar JSON",
                        data=f,
                        file_name="relatorio_notahub.json",
                        mime="application/json",
                        use_container_width=True
                    )
            else:
                st.error("Erro ao gerar relatório JSON.")

# ==========================
# EXCLUSÃO DE MATÉRIAS
# ==========================
def render_delete_section(materia_repo, usuario_id, db_path: str):
    st.subheader("🗑️ Excluir Matérias")
    if st.session_state.get("materia_deletada"):
        st.success("Matéria deletada com sucesso!")
        del st.session_state["materia_deletada"]
        
    materias = materia_repo.listar(usuario_id)

    if not materias:
        st.info("Nenhuma matéria cadastrada.")
        return

    for materia in materias:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"📘 {materia.nome} ({int(materia.carga_total)}h)")

        with col2:
            if st.button("Excluir", key=f"del_{materia.id}"):
                # 🔐 Backup automático antes de deletar
                try:
                    caminho_backup = backup_database(db_path)
                except Exception as e:
                    st.error(f"Falha ao criar backup. Exclusão cancelada.\n{e}")
                    st.stop()  # Para evitar deletar sem backup

                # 🗑 Deleta a matéria
                materia_repo.deletar(materia.id)

                st.session_state["materia_deletada"] = True
                st.rerun()

        st.divider()

# ==========================
# CADASTRO DO SEMESTRE
# ==========================
def render_semestre_section(semestre_repo, usuario_id):
    st.subheader("📅 Cadastro do Semestre")
    if st.session_state.get("semestre_salvo"):
        st.success("Semestre salvo com sucesso!")
        del st.session_state["semestre_salvo"]
    semestre = semestre_repo.obter_ultimo(usuario_id)

    if semestre:
        try:
            data_inicio_atual = datetime.datetime.strptime(semestre.data_inicio, "%Y-%m-%d").date()
            data_fim_atual = datetime.datetime.strptime(semestre.data_fim, "%Y-%m-%d").date()
        except Exception:
            data_inicio_atual = datetime.date.today()
            data_fim_atual = datetime.date.today()
    else:
        data_inicio_atual = datetime.date.today()
        data_fim_atual = datetime.date.today()

    with st.form("form_semestre"):
        data_inicio = st.date_input("Data de Início", value=data_inicio_atual)
        data_fim = st.date_input("Data de Fim", value=data_fim_atual)

        if st.form_submit_button("Salvar Período"):
            if data_fim <= data_inicio:
                st.error("A data final deve ser maior que a data inicial.")
            else:
                semestre_repo.salvar(
                    usuario_id,
                    data_inicio.strftime("%Y-%m-%d"),
                    data_fim.strftime("%Y-%m-%d")
                )
                st.session_state["semestre_salvo"] = True
                st.rerun()