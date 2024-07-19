import streamlit as st
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('briefings.db')
c = conn.cursor()

# Função de autenticação básica (para simplificação)
def autenticar_usuario(usuario, senha):
    return usuario == "admin" and senha == "admin123"

# Verificar se o usuário está logado
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Página de Login
st.title("Login de Admin")

if not st.session_state["logged_in"]:
    with st.form(key='login_form'):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        login_button = st.form_submit_button(label="Login")
        if login_button:
            if autenticar_usuario(usuario, senha):
                st.session_state["logged_in"] = True
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha incorretos")
else:
    st.subheader("Briefings Enviados")
    briefings = c.execute("SELECT * FROM briefings").fetchall()
    
    for briefing in briefings:
        st.write(f"ID: {briefing[0]}")
        st.write(f"Cliente: {briefing[1]}")
        st.write(f"Projeto: {briefing[2]}")
        st.write(f"Tipo de Serviço: {briefing[3]}")
        st.write(f"Objetivo: {briefing[4]}")
        st.write(f"Público Alvo: {briefing[5]}")
        st.write(f"Mensagem: {briefing[6]}")
        st.write(f"Plataforma: {briefing[7]}")
        st.write(f"Data de Entrega: {briefing[8]}")
        st.write(f"Considerações: {briefing[9]}")
        st.write("-" * 20)
