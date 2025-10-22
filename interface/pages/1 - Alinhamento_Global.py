import streamlit as st
from algorithm import needleman_wunsch as nw
import numpy as np
import pandas as pd

st.title("Alinhamento global")
st.markdown("Com needleman-wunsch")

s1 = st.text_input("S1", max_chars=100, value="GGCGCA")
s2 = st.text_input("S2", max_chars=100, value="AGCCCCTG")

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    match_value = st.number_input("Match", value=1)
with row1_col2:
    mismatch_value = st.number_input("Mismatch", value=-1)
with row1_col3:
    gap_value = st.number_input("Gap", value=-2)

if st.button("Alinhar"):
    matrix = nw.needleman_wunsch(s1, s2, match_value, mismatch_value, gap_value)
    matrix_np = np.array(matrix)
    columns_s2 = [f"{i}: {letter}" for i, letter in enumerate(" " + s2)] 
    rows_s1 = [f"{i}: {letter}" for i, letter in enumerate(" " + s1)] 
    df = pd.DataFrame(matrix_np, columns=columns_s2, index=rows_s1)
    st.dataframe(df)

    new_s1, new_s2 = nw.backtracking(s1, s2, matrix, match_value, mismatch_value, gap_value)
    scores = nw.match_list(new_s1, new_s2, match_value, mismatch_value, gap_value)

    st.markdown(f"Nova S1: {new_s1}")
    st.markdown(f"Nova S2: {new_s2}")
    st.markdown(f"Melhor Score: {matrix[len(s1)][len(s2)]:0.0f}")

    new_s_results = np.array([list(new_s1), list(new_s2), scores])
    df_new_s = pd.DataFrame(new_s_results, columns=range(len(new_s1)), index=["Nova S1", "Nova S2", "Scores"])
    st.dataframe(df_new_s)