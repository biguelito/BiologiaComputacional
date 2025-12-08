import numpy as np

# --- CONFIGURAÇÕES DE PONTUAÇÃO ---
MATCH = 1
MISMATCH = -1
GAP = -2

class Node:
    """Representa um nó na árvore guia (UPGMA)."""
    def __init__(self, left=None, right=None, sequences=None, id=None):
        self.left = left       # Filho da esquerda
        self.right = right     # Filho da direita
        self.sequences = sequences # Lista de sequências neste nó (se for folha)
        self.id = id           # Identificador para debug
        
    def is_leaf(self):
        return self.left is None and self.right is None

class MSASolver:
    def __init__(self, sequences, match, mismatch, gap):
        self.match = match
        self.mismatch = mismatch
        self.gap = gap
        self.sequences = sequences
        self.num_seqs = len(sequences)
        self.aligned_sequences = []
        self.distance_matrix = []
        self.upgma_root = None

    # =========================================================================
    # FASE 1 — NW PAR-A-PAR E MATRIZ DE DISTÂNCIAS
    # =========================================================================

    def pairwise_nw(self, seq1, seq2):
        n, m = len(seq1), len(seq2)
        score_matrix = np.zeros((n + 1, m + 1))

        for i in range(n + 1): score_matrix[i][0] = i * self.gap
        for j in range(m + 1): score_matrix[0][j] = j * self.gap

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                match_val = score_matrix[i-1][j-1] + (self.match if seq1[i-1] == seq2[j-1] else self.mismatch)
                delete = score_matrix[i-1][j] + self.gap
                insert = score_matrix[i][j-1] + self.gap
                score_matrix[i][j] = max(match_val, delete, insert)

        align1, align2 = "", ""
        i, j = n, m
        matches = 0

        while i > 0 or j > 0:
            current = score_matrix[i][j]

            if i > 0 and j > 0:
                score_diag = score_matrix[i-1][j-1] + (self.match if seq1[i-1] == seq2[j-1] else self.mismatch)
                if current == score_diag:
                    align1 = seq1[i-1] + align1
                    align2 = seq2[j-1] + align2
                    if seq1[i-1] == seq2[j-1]: matches += 1
                    i -= 1; j -= 1
                    continue

            if i > 0 and current == score_matrix[i-1][j] + self.gap:
                align1 = seq1[i-1] + align1
                align2 = "-" + align2
                i -= 1
            else:
                align1 = "-" + align1
                align2 = seq2[j-1] + align2
                j -= 1

        length = len(align1)
        dist = 1.0 - (matches / length) if length > 0 else 1.0
        return dist

    def compute_distance_matrix(self):
        print("=== Fase 1: Calculando Matriz de Distâncias ===")
        dist_matrix = np.zeros((self.num_seqs, self.num_seqs))

        for i in range(self.num_seqs):
            for j in range(i + 1, self.num_seqs):
                d = self.pairwise_nw(self.sequences[i], self.sequences[j])
                dist_matrix[i][j] = dist_matrix[j][i] = d
                print(f"Dist({i}, {j}) = {d:.3f}")

        return dist_matrix

    # =========================================================================
    # FASE 2 — UPGMA
    # =========================================================================

    def build_guide_tree(self):
        print("\n=== Fase 2: Construindo Árvore Guia (UPGMA) ===")

        clusters = [Node(sequences=[(i, self.sequences[i])], id=i) for i in range(self.num_seqs)]

        d_mat = self.distance_matrix.copy()

        while len(clusters) > 1:
            x, y = -1, -1
            min_dist = float("inf")

            for i in range(len(d_mat)):
                for j in range(i + 1, len(d_mat)):
                    if d_mat[i][j] < min_dist:
                        min_dist = d_mat[i][j]
                        x, y = i, j

            node_a = clusters[x]
            node_b = clusters[y]
            print(f"Fundindo clusters {node_a.id} e {node_b.id}  (Dist: {min_dist:.3f})")

            new_node = Node(left=node_a, right=node_b, id=f"({node_a.id}+{node_b.id})")

            new_dists = []
            for k in range(len(d_mat)):
                if k != x and k != y:
                    new_dists.append((d_mat[x][k] + d_mat[y][k]) / 2)

            # remover x e y
            for idx in sorted([x, y], reverse=True):
                d_mat = np.delete(d_mat, idx, axis=0)
                d_mat = np.delete(d_mat, idx, axis=1)
                clusters.pop(idx)

            # adicionar novo cluster
            new_row = np.array(new_dists + [0])
            d_mat = np.vstack((d_mat, new_row[:-1]))
            d_mat = np.column_stack((d_mat, new_row))

            clusters.append(new_node)

        return clusters[0]

    # =========================================================================
    # FASE 3 — ALINHAMENTO PROGRESSIVO
    # =========================================================================

    def get_column_score(self, col_a, col_b):
        score = 0
        for a in col_a:
            for b in col_b:
                if a == "-" and b == "-":
                    score += 0
                elif a == "-" or b == "-":
                    score += self.gap
                elif a == b:
                    score += self.match
                else:
                    score += self.mismatch
        return score

    def align_profiles(self, profile_a, profile_b):

        ids_a = [id_ for (id_, _) in profile_a]
        ids_b = [id_ for (id_, _) in profile_b]

        seqs_a = [seq for (_, seq) in profile_a]
        seqs_b = [seq for (_, seq) in profile_b]

        n = len(seqs_a[0])
        m = len(seqs_b[0])

        dp = np.zeros((n + 1, m + 1))

        len_a = len(seqs_a)
        len_b = len(seqs_b)

        for i in range(1, n + 1): dp[i][0] = dp[i-1][0] + gap * len_b
        for j in range(1, m + 1): dp[0][j] = dp[0][j-1] + gap * len_a

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                col_a = [s[i-1] for s in seqs_a]
                col_b = [s[j-1] for s in seqs_b]

                score_match = dp[i-1][j-1] + self.get_column_score(col_a, col_b)
                score_del = dp[i-1][j] + self.gap * len_b
                score_ins = dp[i][j-1] + self.gap * len_a

                dp[i][j] = max(score_match, score_del, score_ins)

        aligned_a = [""] * len_a
        aligned_b = [""] * len_b

        i, j = n, m

        while i > 0 or j > 0:
            if i > 0 and j > 0:
                col_a = [s[i-1] for s in seqs_a]
                col_b = [s[j-1] for s in seqs_b]
                diag_score = dp[i-1][j-1] + self.get_column_score(col_a, col_b)

                if dp[i][j] == diag_score:
                    for k in range(len_a): aligned_a[k] = seqs_a[k][i-1] + aligned_a[k]
                    for k in range(len_b): aligned_b[k] = seqs_b[k][j-1] + aligned_b[k]
                    i -= 1; j -= 1
                    continue

            if i > 0 and dp[i][j] == dp[i-1][j] + self.gap * len_b:
                for k in range(len_a): aligned_a[k] = seqs_a[k][i-1] + aligned_a[k]
                for k in range(len_b): aligned_b[k] = "-" + aligned_b[k]
                i -= 1
            else:
                for k in range(len_a): aligned_a[k] = "-" + aligned_a[k]
                for k in range(len_b): aligned_b[k] = seqs_b[k][j-1] + aligned_b[k]
                j -= 1

        new_profile = []

        for id_, seq in zip(ids_a, aligned_a):
            new_profile.append((id_, seq))

        for id_, seq in zip(ids_b, aligned_b):
            new_profile.append((id_, seq))

        return new_profile
    
    def progressive_alignment(self):
        print("\n=== Fase 3: Alinhamento Progressivo ===")
        aligned_sequences = self.traverse_and_align(self.upgma_root)
        return aligned_sequences

    def traverse_and_align(self, node):
        if node.is_leaf():
            return node.sequences

        left_profile = self.traverse_and_align(node.left)
        right_profile = self.traverse_and_align(node.right)

        print(f"Alinhando perfil ({len(left_profile)}) com ({len(right_profile)})...")

        return self.align_profiles(left_profile, right_profile)

    def print_distance_matrix(self):
        print("\n--- MATRIZ DE DISTÂNCIAS ---")
        header = "      " + "  ".join([f"{i:>6}" for i in range(len(self.distance_matrix))])
        print(header)
        
        for i, row in enumerate(self.distance_matrix):
            row_str = "  ".join([f"{val:6.3f}" for val in row])
            print(f"{i:>4}  {row_str}")

        return

    def walk_recursive_guide_tree(self, node, level=0):
        if node is None:
            return
        
        indent = "  " * level
        label = f"Leaf {node.sequences[0][0]}" if node.is_leaf() else f"Node {node.id}"
        print(f"{indent}- {label}")

        if node.left:
            self.walk_recursive_guide_tree(node.left, level + 1)
        if node.right:
            self.walk_recursive_guide_tree(node.right, level + 1)

        return
    
    def print_guide_tree(self):
        print("\n--- ÁRVORE UPGMA ---")
        self.walk_recursive_guide_tree(self.upgma_root)

        return

    def print_aligned_sequences(self):
        print("\n--- ALINHAMENTO MÚLTIPLO DE SEQUÊNCIAS ---")
        for id_orig, seq in self.aligned_sequences:
            print(f"Entrada {id_orig+1}: {seq}")

        return

    def run(self, print_matrix=False, print_upgma=False, print_sequences=True):
        self.distance_matrix = self.compute_distance_matrix()
        if print_matrix:
            self.print_distance_matrix()

        self.upgma_root = self.build_guide_tree()
        if print_upgma:
            self.print_guide_tree()
        
        self.aligned_sequences = self.progressive_alignment()
        if print_sequences:
            self.print_aligned_sequences()

        return

# =========================================================================
# EXECUÇÃO
# =========================================================================

# Exemplo de Sequências (Pequenas para fácil visualização)
# Seq 1 e 2 são parecidas. Seq 3 e 4 são parecidas.
match = 1
mismatch = -1
gap = -2

input_sequences = [
    "ATTGCCATT", 
    "ATGGCCATT", 
    "ATCCAATTT", 
    "ATCTTCTT" 
]

msa = MSASolver(input_sequences, match, mismatch, gap)
msa.run(print_matrix=True, print_upgma=True)