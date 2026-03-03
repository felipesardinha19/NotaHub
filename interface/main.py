import streamlit as st
from datetime import date, datetime
import sys
from pathlib import Path
import sqlite3
import pandas as pd
import altair as alt

# =========================
# Ajuste de PATH
# =========================
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

# =========================
# Imports do Projeto
# =========================
from app.database.connection import create_tables
from app.repositories.materia_repository import MateriaRepository
from app.repositories.aula_repository import AulaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.frequencia_service import FrequenciaService
from app.services.status_service import StatusService
from app.services.auth_service import AuthService
from app.models.materia import Materia
from app.repositories.semestre_repository import SemestreRepository
from app.services.backup_services import (
    backup_database,
    exportar_relatorio_csv,
    exportar_relatorio_json
)
from interface.configuracao_view import (
    render_backup_section,
    render_delete_section,
    render_semestre_section 
)

# =========================
# Configurações iniciais
# =========================
st.set_page_config(page_title="NotaHub", page_icon="📚")
DB_PATH = "data/notahub.db"

# =========================
# INIT DATABASE & SERVICES
# =========================
def init_database():
    create_tables()

def init_services():
    materia_repo = MateriaRepository(DB_PATH)
    aula_repo = AulaRepository(DB_PATH)
    usuario_repo = UsuarioRepository(DB_PATH)
    semestre_repo = SemestreRepository(DB_PATH)

    frequencia_service = FrequenciaService(materia_repo, aula_repo)
    status_service = StatusService()
    auth_service = AuthService(usuario_repo)

    return materia_repo, aula_repo, frequencia_service, status_service, auth_service, usuario_repo, semestre_repo

# =========================
# AUTENTICAÇÃO (LOGIN/REGISTRO)
# =========================
def render_auth(auth_service):
    st.title("🔐 NotaHub")

    aba_login, aba_registro = st.tabs(["Login", "Criar Conta"])

    # -------- LOGIN --------
    with aba_login:
        with st.form("form_login"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                usuario = auth_service.autenticar(email, senha)
                if usuario:
                    st.session_state["logado"] = True
                    st.session_state["usuario_id"] = usuario.id
                    st.session_state["usuario_nome"] = usuario.nome
                    st.session_state["recarregar"] = True
                    st.stop()  # Para parar a execução e "recarregar" na próxima renderização
                else:
                    st.error("Email ou senha inválidos")

    # -------- REGISTRO --------
    with aba_registro:
        with st.form("form_register"):
            nome = st.text_input("Nome")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Cadastrar"):
                try:
                    auth_service.registrar(nome, email, senha)
                    st.success("Conta criada com sucesso! Faça login.")
                    st.session_state["recarregar"] = True
                    st.stop()  # Para parar a execução e "recarregar" na próxima renderização
                except Exception:
                    st.error("Email já cadastrado.")

# =========================
# LOGOUT
# =========================
def render_logout():
    col1, col2 = st.columns([8,1])
    with col2:
        if st.button("Sair", key="btn_logout"):
            st.session_state.clear()
            st.session_state["recarregar"] = True
            st.rerun()
# =========================
# TELAS DO APP
# =========================
def render_app(materia_repo, aula_repo, frequencia_service,
               semestre_repo, usuario_id, usuario_nome):
    from datetime import date

    # ----------------------------
    # Topo: saudação + logout + data + semestre
    # ----------------------------
    col1, col2, col3 = st.columns([6,3,3])
    with col1:
        st.title(f"📚 NotaHub - Olá, {usuario_nome}")
    
    # Data de hoje
    hoje = date.today()
    with col2:
        st.markdown(f"**Hoje:** {hoje.strftime('%d/%m/%Y')}")
    
    # Semestre obrigatório
    semestre_atual = semestre_repo.obter_ativo(usuario_id)
    if semestre_atual:
        with col2:
            st.markdown(f"**Semestre:** {semestre_atual.data_inicio} até {semestre_atual.data_fim}")
    else:
        st.warning("Você precisa cadastrar o semestre antes de prosseguir.")
        render_semestre_section(semestre_repo, usuario_id)
        return  # Sai do render_app, só renderiza o semestre

    # Coluna 3: botão de logout
    with col3:
        if st.button("Sair", key="btn_logout", use_container_width=True):
            st.session_state.clear()
            st.session_state["recarregar"] = True
            st.rerun()  # Chama a função que já tem o botão com key única # Interrompe a execução para garantir que o usuário cadastre primeiro
    
    abas = st.tabs([
        "📘 Cadastrar",
        "📝 Registrar Aula",
        "📊 Relatórios",
        "📃 Listagem",
        "⚙️ Configurações"
    ])

    # =========================================================
    # 📘 ABA 1 - CADASTRAR MATÉRIA
    # =========================================================
    with abas[0]:
        st.header("Cadastrar Nova Matéria")

        if st.session_state.get("materia_cadastrada"):
            st.success("Matéria cadastrada com sucesso!")
            del st.session_state["materia_cadastrada"]

        with st.form("form_materia", clear_on_submit=True):

            nome = st.text_input("Nome da Matéria")
            carga_total = st.number_input("Carga Horária Total", min_value=1)
            aulas_por_semana = st.number_input("Aulas por Semana", min_value=1)
            horas_por_aula = st.number_input("Horas por Aula", min_value=1, max_value=4, step=1)
            categoria = st.text_input("Categoria")

            submitted = st.form_submit_button("Cadastrar")

            if submitted:
                if not nome.strip():
                    st.error("O nome da matéria é obrigatório.")
                    st.stop()

                materia = Materia(
                    nome=nome.strip(),
                    usuario_id=int(usuario_id),
                    carga_total=float(carga_total),
                    aulas_por_semana=int(aulas_por_semana),
                    horas_por_aula=int(horas_por_aula),
                    categoria=categoria.strip() if categoria else None
                )

                materia_repo.inserir(materia, usuario_id)

                st.session_state["materia_cadastrada"] = True
                st.rerun()

    # =========================================================
    # 📝 ABA 2 - REGISTRAR AULA
    # =========================================================
    with abas[1]:
        st.header("Registrar Aula")

        if st.session_state.get("aula_registrada"):
            st.success("Aula registrada com sucesso!")
            del st.session_state["aula_registrada"]

        materias = materia_repo.listar(usuario_id)

        if not materias:
            st.info("Cadastre uma matéria primeiro.")
        else:
            with st.form("form_aula", clear_on_submit=True):
                # ------------------ SELEÇÃO DE MATÉRIA ------------------
                materia_sel_index = st.selectbox(
                    "Selecione a Matéria",
                    range(len(materias)),
                    format_func=lambda i: materias[i].nome,
                    key="materia_sel_index"
                )
                materia_sel = materias[materia_sel_index]

                # ------------------ CALCULO DE FREQUÊNCIA ------------------
                freq_service = FrequenciaService(materia_repo, aula_repo)
                status = freq_service.calcular(materia_sel.id, usuario_id)

                restante_para_carga = max((materia_sel.carga_total or 0) - status["horas_totais"], 0)

                aviso_area = st.empty()
                if restante_para_carga <= 0:
                    aviso_area.warning(
                        f"Você já registrou todas as horas da matéria {materia_sel.nome} ({materia_sel.carga_total}h)."
                    )
                    st.form_submit_button("Registro Bloqueado", disabled=True)
                else:
                    data = st.date_input("Data", key="data_aula")
                    max_horas = min(4, int(restante_para_carga))
                    horas = st.number_input(
                        "Horas",
                        min_value=1,
                        max_value=max_horas,
                        step=1,
                        key="horas_aula"
                    )
                    status_aula = st.radio(
                        "Status",
                        ["Presente", "Ausente"],
                        horizontal=True,
                        key="status_aula"
                    )

                    submitted = st.form_submit_button("Registrar")
                    if submitted:
                        # Recalcula antes de inserir
                        status = freq_service.calcular(materia_sel.id, usuario_id)
                        restante_para_carga = max((materia_sel.carga_total or 0) - status["horas_totais"], 0)

                        if restante_para_carga <= 0:
                            st.error("Essa matéria já atingiu a carga total.")
                            st.stop()

                        aula_repo.inserir(
                            usuario_id=usuario_id,
                            materia_id=materia_sel.id,
                            data=data,
                            horas=horas,
                            presente=1 if status_aula == "Presente" else 0
                        )

                        st.session_state["aula_registrada"] = True
                        st.rerun()
                        
    # =========================================================
    # 📊 ABA 3 - RELATÓRIOS
    # =========================================================
    with abas[2]:
        st.header("Relatórios")

        materias = materia_repo.listar(usuario_id)

        if not materias:
            st.info("Nenhuma matéria cadastrada.")
        else:
            dados = []

            for materia in materias:
                resultado = frequencia_service.calcular(materia.id, usuario_id)

                st.subheader(materia.nome)
                st.write(f"Carga Total: {int(materia.carga_total or 0)}h")
                st.write(f"Frequência: {int(resultado.get('frequencia') or 0)}%")
                st.write(f"Horas de presença: {int(resultado.get('horas_presentes') or 0)}h")
                st.write(f"Horas já faltadas: {int(resultado.get('horas_faltadas') or 0)}h")
                st.write(f"Você ainda pode faltar: {int(resultado.get('horas_restantes') or 0)}h")

                status = resultado["status"]

                if "Reprovado" in status:
                    st.error(status)
                elif "risco" in status.lower():
                    st.warning(status)
                elif status == "Ok":
                    st.success(status)
                else:
                    st.info(status)

                st.divider()

                dados.append({
                    "Materia": materia.nome,
                    "Frequencia": resultado["frequencia"]
                })

            # ---------- GRÁFICO ----------
            st.header("Gráfico de Frequência")

            df = pd.DataFrame(dados)

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(
                    "Materia:N",
                    sort=None,
                    axis=alt.Axis(labelAngle=-45, title="Matéria")
                ),
                y=alt.Y("Frequencia:Q", title="Frequência %"),
                tooltip=["Materia", "Frequencia"]
            ).properties(
                height=400
            )

            st.altair_chart(chart, use_container_width=True)

    # =========================================================
    # 📃 ABA 4 - LISTAGEM
    # =========================================================
    with abas[3]:
        st.header("Matérias Cadastradas")

        materias = materia_repo.listar(usuario_id)

        if not materias:
            st.info("Nenhuma matéria cadastrada.")
        else:
            for materia in materias:
                st.write(f"📘 {materia.nome} ({materia.carga_total}h)")
                st.divider()

# =========================================================
# ⚙️ ABA 5 - CONFIGURAÇÕES
# =========================================================

    with abas[4]:
        st.header("Configurações")
        render_semestre_section(semestre_repo, usuario_id)
        st.divider()
        
        # ⚠️ Passando DB_PATH corretamente
        render_delete_section(materia_repo, usuario_id, DB_PATH)
        st.divider()

        # 💾 Seção Backup
        render_backup_section(
            DB_PATH,
            usuario_id,
            materia_repo,
            frequencia_service
        )
# =========================
# MAIN
# =========================
def main():
    init_database()
    materia_repo, aula_repo, frequencia_service, status_service, auth_service, usuario_repo,  semestre_repo = init_services()

    if "recarregar" not in st.session_state:
        st.session_state["recarregar"] = False

    if "logado" not in st.session_state:
        st.session_state["logado"] = False

    if not st.session_state["logado"]:
        render_auth(auth_service)
        return

    render_app(
        materia_repo,
        aula_repo,
        frequencia_service,
        semestre_repo,
        st.session_state["usuario_id"],
        st.session_state["usuario_nome"],
    )

if __name__ == "__main__":
    main()