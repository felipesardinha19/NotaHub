import streamlit as st
import sys
from pathlib import Path
import sqlite3
import pandas as pd
import altair as alt

# =========================
# Corrige path do projeto
# =========================

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

# =========================
# Imports da arquitetura
# =========================

from app.database.connection import create_tables
from app.repositories.materia_repository import MateriaRepository
from app.repositories.aula_repository import AulaRepository
from app.services.frequencia_service import FrequenciaService
from app.services.status_service import StatusService
from app.models.materia import Materia

DB_PATH = "data/notahub.db"

# cria conexão real
conn = sqlite3.connect(DB_PATH)

# =========================
# Inicialização do sistema
# =========================

create_tables()

materia_repo = MateriaRepository(conn)
aula_repo = AulaRepository(conn)

frequencia_service = FrequenciaService(materia_repo, aula_repo)
status_service = StatusService()

# =========================
# Configuração da página
# =========================

st.set_page_config(page_title="NotaHub", page_icon="📚")
st.title("📚 NotaHub - Controle de Frequência")

aba1, aba2, aba3, aba4, aba5 = st.tabs(["📘 Cadastrar Matérias", "📝 Registrar Aula", "📊 Relatórios", "📃 Listagem", "🗑️ Deletar Matéria"])

# =========================
# Cadastro de Matéria
# =========================
with aba1:
    st.header("Cadastrar Nova Matéria")

    with st.form("form_materia", clear_on_submit=True):
        nome = st.text_input("Nome da Matéria")
        carga_total = st.number_input("Carga Horária Total", min_value=1)
        aulas_por_semana = st.number_input("Aulas por Semana", min_value=1)
        horas_por_aula = st.number_input("Horas por Aula", min_value=1, max_value=4)
        categoria = st.text_input("Categoria")

        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            materia = Materia(
                id=None,
                nome=nome,
                carga_total=carga_total,
                aulas_por_semana=aulas_por_semana,
                horas_por_aula=horas_por_aula,
                categoria=categoria
            )

            materia_repo.inserir(materia)
            st.success("Matéria cadastrada com sucesso!")

#=========================
#Registrar Aulas
#=========================
with aba2:
    st.header("Registrar presença")
    
    materias = materia_repo.listar()

    if materias:
        materia_selecionada = st.selectbox(
            "Selecione uma Matéria",
            materias,
            format_func=lambda m: m.nome
        )

        data = st.date_input("Data da Aula")
        horas = st.number_input("Tempo de Aula", min_value=1, max_value=4) 
        presente = st.checkbox("Aluno esteve presente")

        if st.button("Registrar"):
            aula_repo.inserir(
                materia_id= materia_selecionada.id,
                data=data,
                horas=horas,
                presente=presente
            )
            st.success("Presença registrada com sucesso")
            st.rerun()
    else:
        st.info("Cadastre uma matéria primeiro")
        st.rerun()

#=========================
#Relatorios
#=========================      
with aba3:
    st.header("Relatório")
    for materia in materias:

            # 🔥 Agora o cálculo vem do service
            resultado = frequencia_service.calcular(materia.id)

            st.subheader(materia.nome)
            st.write(f"Carga Total: {int(materia.carga_total)}h")
            st.write(f"Frequência:{resultado['frequencia']:.2f}%")
            st.write(f"Você ainda pode faltar: {int(resultado['horas_restantes'])}h")

            status = resultado["status"]

                # Status colorido
            if status == "Ok":
                st.success(f"Status: {status}")
            elif status == "Em andamento":
                st.info(f"Status: {status}")
            else:
                st.error(f"Status: {status}")
            
            st.divider()

    st.header("Gráfico de Frequência")

    if materias:
        nomes = []
        frequencias = []

        for materia in materias:
            resultado = frequencia_service.calcular(materia.id)
            nomes.append(materia.nome)
            frequencias.append(resultado["frequencia"])

        df = pd.DataFrame({
            "Materia": nomes,  # sem acento
            "Frequencia": frequencias
        })

        # Gráfico Altair
        chart = alt.Chart(df).mark_bar(color="#4CAF50").encode(
            x=alt.X("Materia:N", sort=None, axis=alt.Axis(labelAngle=-45, title="Matéria")),  
            y=alt.Y("Frequencia:Q", title="Frequência %"),
            tooltip=["Materia", "Frequencia"]
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else: 
        st.info("nenhuma matéria encontrada,")

# =========================
# Listagem com cálculo real
# =========================
with aba4:
    st.header("Matérias Cadastradas")

    materias = materia_repo.listar()

    if not materias:
        st.info("Nenhuma matéria cadastrada ainda.")
    else:
        for materia in materias:

            # 🔥 Agora o cálculo vem do service
            resultado = frequencia_service.calcular(materia.id)

            st.subheader(materia.nome)

# ================
# Deletar matéria
# ================
with aba5:
    st.header("Excluir Matérias")

    materias = materia_repo.listar()

    if not materias:
        st.info("Nenhuma matéria cadastrada.")
    else:
        for materia in materias:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(
                    f"📘 {materia.nome} "
                    f"({materia.carga_total}h) "
                    f"- Frequência: {int(resultado['frequencia'])}%"
                )

            with col2:
                if st.button("🗑️ Excluir", key=f"del_{materia.id}"):
                    materia_repo.deletar(materia.id)
                    st.rerun()

            st.divider()