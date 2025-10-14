from nw_test import run_test
from nw_stress_test import execute_test
from nw_global_alignment import align_sequences
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Alinhamento global com needleman-wunsch',
        description="""Executa o alinhamento global utilizando a abordagem de programacao dinamica de needleman-wunsch.
            Sendo possivel rodar o algoritmo de mais de um modo
        """)
    parser.add_argument("--min", type=int, help="Numero minimo para o tamanho da cadeia", default=10)
    parser.add_argument("--max", type=int, help="Numero maximo para o tamanho da cadeia", default=20)
    parser.add_argument("--rep", type=int, help="Numero de repeticoes para o teste de stress", default=100)
    parser.add_argument("--s1", type=str, help="Sequencia S1")
    parser.add_argument("--s2", type=str, help="Sequencia S2")
    parser.add_argument("--path", action="store_true", help="Descreve, linha por linha, o caminho do backtracking")
    parser.add_argument("--mode", type=str,
        choices= ["t", "s", "g"],
        help="""
            't' para um teste com 2 cadeias aleatorias, de tamanho args min e max.\n
            's' para executar o algortimo 100 vezes com 2 cadeias aleatorias, de tamanho args min e max.\n
            'g' para comparar 2 cadeias, args s1 e s2
        """)
    args = parser.parse_args()
    
    if (args.mode == "t"):
        run_test(args.min, args.max, args.path)
    elif (args.mode == "s"):
        execute_test(args.rep, args.min, args.max)
    elif (args.mode == "g"):
        align_sequences(args.s1, args.s2, args.path)
    else:
        print("Escolha um dos modos validos")