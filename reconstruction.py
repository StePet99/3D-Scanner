import os
import pycolmap
import trimesh

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
    mesh_path = os.path.join(dense_dir, "mesh.ply")
    dense_model.poisson_mesher(
        input_path=os.path.join(dense_dir, "fused.ply"),
        output_path=mesh_path,
    )

    print(">> Conversione della mesh in STL...")
    stl_path = os.path.join(dense_dir, "mesh.stl")
    convert_to_stl(mesh_path, stl_path)

    print(">> Processo completato!")
    print("Nuvola di punti densa salvata in:", os.path.join(dense_dir, "fused.ply"))
    print("Mesh 3D salvata in PLY:", mesh_path)
    print("Mesh 3D salvata in STL:", stl_path)


# Funzione per convertire una mesh da PLY a STL
def convert_to_stl(ply_path, stl_path):
    try:
        # Carica la mesh usando trimesh
        mesh = trimesh.load_mesh(ply_path)
        # Salva la mesh in formato STL
        mesh.export(stl_path)
        print(f"Mesh esportata in formato STL: {stl_path}")
    except Exception as e:
        print(f"Errore durante la conversione a STL: {e}")


if __name__ == "__main__":
    # Chiedi all'utente la directory delle immagini
    input_dir = input("Inserisci il percorso della directory con le immagini: ").strip()

    # Verifica che la directory esista
    if not os.path.isdir(input_dir):
        print("Errore: la directory specificata non esiste.")
    else:
        # Avvia il processo di ricostruzione
        reconstruct(input_dir)
