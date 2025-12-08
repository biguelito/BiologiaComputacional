import streamlit as st
from algorithm import needleman_wunsch as nw  # Assumindo que seu 'algorithm.py' está no mesmo diretório
import numpy as np
import pandas as pd

# --- Configuração da Página ---
# Define o título da aba do navegador e um ícone
st.set_page_config(page_title="Alinhamento Global", page_icon="🧬", layout="wide")

# --- Título Principal ---
st.title("🧬 Alinhamento Global de Sequências")
st.markdown("Implementação do algoritmo **Needleman-Wunsch** para encontrar o alinhamento ótimo.")

# --- Barra Lateral (Sidebar) para Inputs ---
st.sidebar.header("Parâmetros de Entrada")

# Inputs das sequências
s1 = st.sidebar.text_input("Sequência 1 (S1)", max_chars=100, value="GGCGCA")
s2 = st.sidebar.text_input("Sequência 2 (S2)", max_chars=100, value="AGCCCCTG")

# Inputs das pontuações
st.sidebar.subheader("Valores de Pontuação")
match_value = st.sidebar.number_input("Match", value=1)
mismatch_value = st.sidebar.number_input("Mismatch", value=-1)
gap_value = st.sidebar.number_input("Gap", value=-2)

# Botão para executar o alinhamento
if st.sidebar.button("Alinhar Sequências"):

    # --- Área de Resultados (Página Principal) ---
    st.header("Resultados do Alinhamento")

    # Verifica se as sequências não estão vazias
    if s1 and s2:
        # --- 1. Cálculos ---
        # (Mantém a mesma lógica de antes)
        matrix = nw.needleman_wunsch(s1, s2, match_value, mismatch_value, gap_value)
        matrix_np = np.array(matrix)
        
        # Labels para o DataFrame da matriz
        columns_s2 = [f"{i}: {letter}" for i, letter in enumerate(" " + s2)] 
        rows_s1 = [f"{i}: {letter}" for i, letter in enumerate(" " + s1)] 
        df = pd.DataFrame(matrix_np, columns=columns_s2, index=rows_s1)

        # Backtracking
        new_s1, new_s2 = nw.backtracking(s1, s2, matrix, match_value, mismatch_value, gap_value)
        scores = nw.match_list(new_s1, new_s2, match_value, mismatch_value, gap_value)

        # DataFrame do alinhamento final
        new_s_results = np.array([list(new_s1), list(new_s2), scores])
        df_new_s = pd.DataFrame(new_s_results, columns=range(len(new_s1)), index=["S1 Alinhada", "S2 Alinhada", "Scores"])

        # --- 2. Exibição dos Resultados ---

        # Exibe o Score Final usando st.metric para destaque
        st.metric(label="Score Final do Alinhamento", value=f"{matrix[len(s1)][len(s2)]:0.0f}")
        
        st.markdown("---")

        # Exibe as sequências alinhadas em um bloco de código para manter o monoespaçamento
        st.subheader("Sequências Alinhadas")
        alignment_str = f"S1: {new_s1}\nS2: {new_s2}"
        st.code(alignment_str, language='text')
        
        # Exibe o DataFrame do alinhamento detalhado
        st.subheader("Alinhamento Detalhado (Posição por Posição)")
        st.dataframe(df_new_s)
        
        st.markdown("---")

        # Coloca a matriz de DP (que é grande) dentro de um expander
        with st.expander("Visualizar Matriz de Programação Dinâmica (DP)"):
            st.dataframe(df)

    else:
        st.error("Por favor, insira ambas as sequências (S1 e S2) para alinhar.")