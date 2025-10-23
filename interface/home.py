import streamlit as st

# --- Configuração da Página ---
# st.set_page_config deve ser o primeiro comando Streamlit a ser executado
st.set_page_config(
    page_title="Alinhamento Global de Sequências",
    page_icon="🧬"
)

# --- Título e Introdução ---
st.title("Alinhamento Global pelo Algoritmo de Needleman-Wunsch")

st.markdown("""
Esta aplicação demonstra a implementação do algoritmo de Needleman-Wunsch (1970),
um método canônico para realizar o alinhamento global de sequências.
""")

st.markdown("""
Utilize o menu na barra lateral para navegar até a página de alinhamento
e executar a ferramenta.
""")


# --- Fundamentação Teórica ---
st.header("Fundamentos do Alinhamento Global")
st.markdown("""
O alinhamento global busca determinar a correspondência ótima entre duas sequências
(por exemplo, nucleotídeos ou aminoácidos) considerando-as em toda a sua extensão.
O objetivo é maximizar uma pontuação de similaridade, que é calculada com base em
um sistema de pontuação pré-definido, penalizando desalinhamentos (mismatches)
e a introdução de lacunas (gaps).

Este método é fundamental em bioinformática para inferir homologia funcional
ou evolutiva entre sequências.
""")

st.header("O Algoritmo de Needleman-Wunsch")
st.markdown("""
O algoritmo de Needleman-Wunsch resolve o problema do alinhamento global
utilizando **programação dinâmica**. O processo é dividido em duas fases:

1.  **Construção da Matriz de Pontuação (DP)**
2.  **Rastreamento (Backtracking)**
""")

# --- Detalhes do Algoritmo ---
st.subheader("1. Construção da Matriz")
st.markdown("""
Dadas duas sequências, $S_1$ de comprimento $m$ e $S_2$ de comprimento $n$,
uma matriz (ou tabela) $F$ de dimensões $(m+1) \times (n+1)$ é construída.
Cada célula $F(i, j)$ armazena a pontuação máxima do alinhamento
ótimo entre o prefixo $S_1[1..i]$ e o prefixo $S_2[1..j]$.

A matriz é inicializada com as penalidades de gap:
* $F(i, 0) = i \times d$
* $F(0, j) = j \times d$
(Onde $d$ é a penalidade de gap, geralmente um valor negativo).

As demais células são preenchidas com base na seguinte **fórmula de recorrência**:
""")

st.latex(r'''
F(i, j) = \max \begin{cases}
F(i-1, j-1) + S(S_1[i], S_2[j]) & \text{(Match ou Mismatch)} \\
F(i-1, j) + d & \text{(Gap em } S_2 \text{)} \\
F(i, j-1) + d & \text{(Gap em } S_1 \text{)}
\end{cases}
''')

st.markdown("""
Onde $S(a, b)$ é a pontuação para um *match* (se $a = b$) ou *mismatch*
(se $a \neq b$), e $d$ é a penalidade de gap linear.

A pontuação final do alinhamento ótimo é o valor encontrado na célula
$F(m, n)$.
""")

st.subheader("2. Rastreamento (Backtracking)")
st.markdown("""
Após o preenchimento completo da matriz, o alinhamento ótimo é reconstruído.
O processo inicia na célula $F(m, n)$ e traça um caminho de volta à origem
$F(0, 0)$.

A cada passo, o algoritmo verifica qual das três possibilidades na fórmula
de recorrência gerou o valor da célula atual:
* **Movimento Diagonal:** $F(i-1, j-1)$ foi usado. Isso corresponde a um
    *match* ou *mismatch* (ambos $S_1[i]$ e $S_2[j]$ são alinhados).
* **Movimento Vertical:** $F(i-1, j)$ foi usado. Isso corresponde a um
    gap na sequência $S_2$ (alinhando $S_1[i]$ com '$-$' ).
* **Movimento Horizontal:** $F(i, j-1)$ foi usado. Isso corresponde a um
    gap na sequência $S_1$ (alinhando $S_2[j]$ com '$-$' ).

O caminho traçado, lido do início ao fim, revela o alinhamento global.
""")