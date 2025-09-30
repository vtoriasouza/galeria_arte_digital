import requests
import random
from PIL import Image
from io import BytesIO

def obter_obra_de_arte_aleatoria():
    url_base = "https://collectionapi.metmuseum.org/public/collection/v1/"

    try:
        response = requests.get(url_base + "objects")
        response.raise_for_status()
        data = response.json()
        id_aleatorio = random.choice(data["objectIDs"])
        response_obra = requests.get(url_base + "objects/" + str(id_aleatorio))
        response_obra.raise_for_status()
        obra_data = response_obra.json()
        return obra_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados da API: {e}")
        return None
    
def exibir_obra(url_imagem, titulo, artista):
    try:
        response_imagem = requests.get(url_imagem)
        response_imagem.raise_for_status()
        image_bytes = BytesIO(response_imagem.content)
        img = Image.open(image_bytes)
        img.show()
        print(f"/nObra: {titulo}\nArtista: {artista}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter a imagem: {e}")

if __name__ == "__main__":
    print("Buscando uma obra de arte aleatória do Metropolitan Museum...")
    obra = obter_obra_de_arte_aleatoria()
    
    if obra and "primaryImage" in obra and obra["primaryImage"]:
        url_imagem = obra["primaryImage"]
        titulo = obra.get("title", "Titulo não disponível")
        artista = obra.get("artistDisplayName", "Artista não disponível")
        exibir_obra(url_imagem, titulo, artista)
    else:
        print("Desculpe. Não foi possível encontrar uma obra de arte com imagem.")
