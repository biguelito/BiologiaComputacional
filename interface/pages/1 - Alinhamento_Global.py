import streamlit as st
from algorithm import needleman_wunsch as nw

st.title("Alinhamento global")
st.markdown("Com needleman-wunsch")

s1 = st.text_input("S1", max_chars=100)
s2 = st.text_input("S2", max_chars=100)

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    match = st.number_input("Match", value=0)
with row1_col2:
    mismatch = st.number_input("Mismatch", value=0)
with row1_col3:
    gap = st.number_input("Gap", value=0)

if st.button("Alinhar"):
    matrix = nw.needleman_wunsch(s1, s2, match, mismatch, gap)
    print(matrix)