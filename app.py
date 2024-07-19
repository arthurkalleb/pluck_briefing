# app.py

import streamlit as st
import sqlite3
import hashlib

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('formulario.db')
    return conn

# Função para salvar o formulário
def save_form(nome_projeto, nome_cliente, telefone, email, prazo_entrega, descricao_projeto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO formulários (nome_projeto, nome_cliente, telefone, email, prazo_entrega, descricao_projeto)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome_projeto, nome_cliente, telefone, email, prazo_entrega, descricao_projeto))
    conn.commit()
    conn.close()

# Função de login
def check_login(username, password):
    return username == "admin" and hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256("adminpass".encode()).hexdigest()

# Página principal do formulário
def main():
    st.title("Formulário de Briefing")
    
    with st.form(key='formulario'):
        nome_projeto = st.text_input("Nome do Projeto")
        nome_cliente = st.text_input("Nome do Cliente")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        prazo_entrega = st.text_input("Prazo de Entrega")
        descricao_projeto = st.text_area("Descreva o Projeto")
        
        submit_button = st.form_submit_button(label='Enviar')
        
        if submit_button:
            save_form(nome_projeto, nome_cliente, telefone, email, prazo_entrega, descricao_projeto)
            st.success("Formulário enviado com sucesso!")

    if st.button('Login de Administrador'):
        st.session_state['login'] = False
        st.session_state['page'] = 'login'

# Página de login
def login():
    st.title("Login de Administrador")
    
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type='password')
    
    if st.button('Login'):
        if check_login(username, password):
            st.session_state['login'] = True
            st.session_state['page'] = 'admin'
        else:
            st.error("Usuário ou senha inválidos.")

# Página de administração
def admin_page():
    st.title("Administração dos Formulários")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM formulários')
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        st.write("Dados dos Formulários Enviados:")
        for row in rows:
            st.write(f"ID: {row[0]}, Nome do Projeto: {row[1]}, Nome do Cliente: {row[2]}, Telefone: {row[3]}, Email: {row[4]}, Prazo de Entrega: {row[5]}, Descrição do Projeto: {row[6]}")
    else:
        st.write("Nenhum formulário enviado ainda.")

# Função principal para gerenciar as páginas
def main_page():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'main'

    if st.session_state['page'] == 'main':
        main()
    elif st.session_state['page'] == 'login':
        login()
    elif st.session_state['page'] == 'admin':
        if st.session_state['login']:
            admin_page()
        else:
            st.error("Você precisa estar logado para acessar esta página.")

if __name__ == "__main__":
    main_page()
