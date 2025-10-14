import streamlit as st
from algorithm import needleman_wunsch as nw
import numpy as np
import pandas as pd

st.title("Alinhamento global")
st.markdown("Com needleman-wunsch")

s1 = st.text_input("S1", max_chars=100)
s2 = st.text_input("S2", max_chars=100)

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    match = st.number_input("Match", value=1)
with row1_col2:
    mismatch = st.number_input("Mismatch", value=-1)
with row1_col3:
    gap = st.number_input("Gap", value=-2)

if st.button("Alinhar"):
    matrix = nw.needleman_wunsch(s1, s2, match, mismatch, gap)
    matrix_np = np.array(matrix)
    columns_s2 = [f"{i}: {letter}" for i, letter in enumerate(" " + s2)] 
    rows_s1 = [f"{i}: {letter}" for i, letter in enumerate(" " + s1)] 
    df = pd.DataFrame(matrix_np, columns=columns_s2, index=rows_s1)
    st.dataframe(df)

    new_s1, new_s2 = nw.backtracking(s1, s2, matrix, match, mismatch, gap)
    st.markdown(new_s1)
    st.markdown(new_s2)