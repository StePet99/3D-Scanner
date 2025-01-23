import os
import pycolmap

# Directory di input e output
input_dir = "images"  # Directory con le immagini
workspace_dir = "pycolmap_workspace"  # Cartella per i file di lavoro
database_path = os.path.join(workspace_dir, "database.db")
sparse_dir = os.path.join(workspace_dir, "sparse")
dense_dir = os.path.join(workspace_dir, "dense")

# Creazione delle directory necessarie
os.makedirs(workspace_dir, exist_ok=True)
os.makedirs(sparse_dir, exist_ok=True)
os.makedirs(dense_dir, exist_ok=True)

# Funzione di supporto per la ricostruzione
def reconstruct(input_dir, database_path, sparse_dir, dense_dir):
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

# Esegui la ricostruzione
reconstruct(input_dir, database_path, sparse_dir, dense_dir)
