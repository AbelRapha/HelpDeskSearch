import pandas as pd
import streamlit as st
import sqlite3 as db

#Alterando o Favicoin
st.set_page_config(page_title='Help Desk Search', page_icon = 'static/images/help-desk.png',)

st.write(""" # HelpDeskSearch """)
st.write("## Busque o chamado através de seu Ticket ou Categoria similar")

# Importando a base de dados do governo
@st.cache
def load_dataset(categoria, data_inicio,data_fim, resolvido):
    conn = db.connect('help_desk_database')
    if categoria.isnumeric():
        if resolvido == "todos":
            dados = pd.read_sql(f'''SELECT * FROM chamados
                                    WHERE Ticker like "{categoria}%"
                                    AND "Data Abertura" >= "{data_inicio}" 
                                    AND "Data Abertura" <= "{data_fim}"
                                    ''',conn)
        else:
            dados = pd.read_sql(f'''SELECT * FROM chamados
                                    WHERE Ticker like "{categoria}%"
                                    AND "Data Abertura" >= "{data_inicio}" 
                                    AND "Data Abertura" <= "{data_fim}"
                                    AND Resolvido == "{resolvido}" ''',conn)
    else:
        if resolvido == "todos":
            dados = pd.read_sql(f'''SELECT * FROM chamados
                                    WHERE Categoria like "%{categoria}%"
                                    AND "Data Abertura" >= "{data_inicio}" 
                                    AND "Data Abertura" <= "{data_fim}"
                                    ''',conn)
        else:
            dados = pd.read_sql(f'''SELECT * FROM chamados
                                    WHERE Categoria like "%{categoria}%"
                                    AND "Data Abertura" >= "{data_inicio}" 
                                    AND "Data Abertura" <= "{data_fim}"
                                    AND Resolvido == "{resolvido}" ''',conn)
    return dados

#Criando sidebar
resolvidos = st.sidebar.selectbox(
    "Chamado Resolvido?",
    ("sim","não","todos")
)
data_inicio = st.sidebar.date_input('Selecione a primeira data de abertura do chamado')
data_fim = st.sidebar.date_input('Selecione a segunda data de abertura do chamado')

#Pegando input da pesquisa
frase_busca = st.text_input(" Digite aqui o nome da categoria ou similar", key="name")
frase_busca = frase_busca.replace(" ","%")

#Pegando resultado de busca
if frase_busca:
    dados = load_dataset(frase_busca,data_inicio,data_fim,resolvidos)

    #Mostrando
    st.dataframe(dados[['Categoria','Ticker']],5000,250)
    #Cards
    col1,col2,col3 = st.columns(3)
    col1.metric("Quantidade de chamados filtrados", f"{len(dados.index)}")
    col2.metric("Quantidade de Chamados em Aberto",f"{dados['Data Fechamento'].isna().sum()}", "Chamados")
    col3.metric("Quantidade de Chamados Fechados", f"{dados['Data Fechamento'].notna().sum()}", 'Chamados')
    #Graficos
    grafico1,grafico2 = st.columns(2)
    grafico1.text("Categorias Buscadas")
    grafico1.bar_chart(dados['Categoria'].value_counts())
    grafico2.text("NPS")
    grafico2.bar_chart(dados['Satisfação'].value_counts())


