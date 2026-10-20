import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="LocaBike - Aluguel de Bicicletas",
    page_icon="🚲",
    layout="wide"
)

if 'reservas' not in st.session_state:
    st.session_state.reservas = []

st.title("🚲 Sistema de Aluguel de Bicicletas")
st.markdown("Bem-vindo, alugue sua bike")

bikes = {
    "Tradicional": {"preco": 10.0, "tipo": "Urbana", "desc": "Ideal para passeios leves na cidade e ciclovias."},
    "Bike trilha": {"preco": 20.0, "tipo": "Trilha", "desc": "Perfeita para terrenos acidentados e estradas de terra."},
    "Bicicleta Elétrica": {"preco": 25.0, "tipo": "Elétrica", "desc": "Mais conforto e menos esforço para trajetos longos."},
}

aba_aluguel, aba_reservas = st.tabs(["🎯 Realizar Aluguel", "📋 Reservas Ativas"])

with aba_aluguel:
    st.header("Escolha sua Bicicleta")
    
    cols = st.columns(4)
    for i, (nome, info) in enumerate(bikes.items()):
        with cols[i]:
            st.subheader(nome)
            st.markdown(f"**Tipo:** {info['tipo']}")
            st.markdown(f"**Preço:** R$ {info['preco']:.2f} / hora")
            st.caption(info['desc'])
            st.markdown("---")

    st.subheader("Formulário de Reserva")
    with st.form("form_reserva"):
        col_nome, col_bike = st.columns(2)
        with col_nome:
            nome_cliente = st.text_input("Seu Nome Completo")
        with col_bike:
            bike_selecionada = st.selectbox("Selecione o Modelo", list(bikes.keys()))
            
        col_data, col_horas = st.columns(2)
        with col_data:
            data_reserva = st.date_input("Data do Aluguel", datetime.date.today())
        with col_horas:
            horas_aluguel = st.number_input("Quantidade de Horas", min_value=1, max_value=24, value=2)
            
        enviar = st.form_submit_button("Confirmar Aluguel 🚀")
        
        if enviar:
            if nome_cliente.strip() == "":
                st.error("Por favor, insira o seu nome antes de confirmar.")
            else:
                preco_hora = bikes[bike_selecionada]["preco"]
                valor_total = preco_hora * horas_aluguel
                
                nova_reserva = {
                    "Cliente": nome_cliente,
                    "Bicicleta": bike_selecionada,
                    "Data": data_reserva.strftime("%d/%m/%Y"),
                    "Horas": horas_aluguel,
                    "Total (R$)": f"R$ {valor_total:.2f}"
                }
                st.session_state.reservas.append(nova_reserva)
                
                st.success(f"Parabéns, {nome_cliente}! Sua {bike_selecionada} foi reservada com sucesso.")

with aba_reservas:
    st.header("Histórico de Reservas desta Sessão")
    if len(st.session_state.reservas) > 0:
        df = pd.DataFrame(st.session_state.reservas)
        st.dataframe(df, use_container_width=True)

        st.metric(label="Total de Reservas Criadas", value=len(st.session_state.reservas))
    else:
        st.info("Nenhuma reserva realizada ainda nesta sessão. Vá até a aba 'Realizar Aluguel' para começar!")
