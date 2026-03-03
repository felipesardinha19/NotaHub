import streamlit as st
from app.services.auth_service import autenticar


def render_login(usuario_repo):

    st.title("🔐 Login - NotaHub")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = autenticar(usuario_repo, email, senha)

        if usuario:
            st.session_state.usuario_logado = usuario
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Email ou senha inválidos.")