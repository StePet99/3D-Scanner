import os
import pycolmap

# Funzione di supporto per la ricostruzione
def reconstruct(input_dir):
    # Percorsi per i file e le cartelle di output
    database_path = os.path.join(input_dir, "database.db")
    sparse_dir = os.path.join(input_dir, "sparse")
    dense_dir = os.path.join(input_dir, "dense")

    # Creazione delle directory necessarie
    os.makedirs(sparse_dir, exist_ok=True)
    os.makedirs(dense_dir, exist_ok=True)

    print(">> Estrazione delle feature...")
    pycolmap.extract_features(database_path=database_path, image_path=input_dir)

    print(">> Matching delle feature...")
    pycolmap.match_exhaustive(database_path=database_path)

    print(">> Ricostruzione sparsa...")
    sparse_model = pycolmap.Reconstruction()
    sparse_model.mapper(
        database_path=database_path,
        image_path=input_dir,
        output_path=sparse_dir,
    )

    print(">> Ricostruzione densa...")
    dense_model = pycolmap.Reconstruction()
    dense_model.dense_reconstruction(
        image_path=input_dir,
        sparse_model_path=os.path.join(sparse_dir, "0"),
        output_path=dense_dir,
    )

    print(">> Creazione della mesh...")
    dense_model.poisson_mesher(
        input_path=os.path.join(dense_dir, "fused.ply"),
        output_path=os.path.join(dense_dir, "mesh.ply"),
    )

    print(">> Processo completato!")
    print("Nuvola di punti densa salvata in:", os.path.join(dense_dir, "fused.ply"))
    print("Mesh 3D salvata in:", os.path.join(dense_dir, "mesh.ply"))


if __name__ == "__main__":
    # Chiedi all'utente la directory delle immagini
    input_dir = input("Inserisci il percorso della directory con le immagini: ").strip()

    # Verifica che la directory esista
    if not os.path.isdir(input_dir):
        print("Errore: la directory specificata non esiste.")
    else:
        # Avvia il processo di ricostruzione
        reconstruct(input_dir)
