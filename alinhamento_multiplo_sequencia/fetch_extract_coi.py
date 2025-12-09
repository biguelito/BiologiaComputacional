from Bio import Entrez, SeqIO
import os

# Obrigatório pelo NCBI
Entrez.email = "gabrielr.nogueira2000@gmail.com"

# Lista das espécies e o gene COI
species_list = [
    "Canis lupus",
    "Vulpes vulpes",
    "Panthera tigris",
    "Gallus gallus",
    "Falco peregrinus",
    "Alligator mississippiensis",
    "Python regius",
    "Xenopus laevis"
]

gene = "COI"

# Pasta onde os FASTA serão salvos
output_folder = "coi_sequences"
os.makedirs(output_folder, exist_ok=True)


def fetch_coi_sequence(species_name, gene_name="COI"):
    """Busca no NCBI a melhor sequência de COI daquela espécie e baixa em FASTA."""
    print(f"\n🔍 Procurando COI para: {species_name}...")

    # Query no NCBI Nucleotide
    query = f"{species_name}[Organism] AND {gene_name}[Gene] AND mitochondrion[Filter]"

    # 1) Buscar IDs
    search = Entrez.esearch(db="nucleotide", term=query, retmax=5)
    results = Entrez.read(search)
    ids = results.get("IdList", [])

    if not ids:
        print(f"⚠ Nenhuma sequência COI encontrada para {species_name}.")
        return None

    seq_id = ids[0]  # Pega a melhor/mais relevante
    print(f"   ✔ Encontrado ID: {seq_id}")

    # 2) Baixar sequência em fasta
    fetch = Entrez.efetch(db="nucleotide", id=seq_id, rettype="fasta", retmode="text")
    record = SeqIO.read(fetch, "fasta")

    # 3) Salvar arquivo
    filename = f"{output_folder}/{species_name.replace(' ', '_')}_COI.fasta"
    SeqIO.write(record, filename, "fasta")

    print(f"   💾 Salvo em: {filename}")

    return filename


# Baixar todas as sequências
print("=== DOWNLOAD DE SEQUÊNCIAS COI (NCBI) ===")
files = []
for sp in species_list:
    path = fetch_coi_sequence(sp, gene)
    if path:
        files.append(path)

print("\n=== CONCLUÍDO ===")
print("Arquivos baixados:")
for f in files:
    print(" -", f)
