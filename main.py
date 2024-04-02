from fastapi import FastAPI
from fastapi import HTTPException, status, Response
from models import Cantor
import requests
import json

app = FastAPI()

MUSICAS = {
    1:351595631,
    2:129231818,
    3:2355587775,
    4:2315441485
}
 

cantores ={
    1:{
        "nome": "Shaw mendes",
        "ano_nasc": 1998,
        "genero": "Pop",
        "tempo_carreira": 25,
    },
    2:{
        "nome": "Elvis Presley",
        "ano_nasc": 1935,
        "genero": "Rock",
        "tempo_carreira": 23,
    },
    3:{
        "nome": "Taylor Swift",
        "ano_nasc": 1989,
        "genero": "Country",
        "tempo_carreira": 20,
    },
      4:{
        "nome": "Alok",
        "ano_nasc": 1991,
        "genero": "Eletronica",
        "tempo_carreira": 10,
    }
}

@app.get('/cantores')
async def get_cantores():
    return cantores


@app.get('/cantores_musica')
async def get_cantores():
    request = requests.get("http://10.234.86.72:8000/musicas")
    musicas = json.loads(request.content)
    d4  ={}
    for chave in musicas.keys():
        d1 = musicas[chave]
        d2 = cantores[int(chave)]
        d3 = dict(d1, **d2)
        d4[chave] = d3
    return d4

#get consumindo api do deezer
@app.get('/cantorLink/{cantor_id}')
async def get_cantores_id(cantor_id):
    try:
        cantor_id = int(cantor_id)
        cantor = cantores[cantor_id]
        cantor.update({"id": cantor_id})
        
        url = f'https://deezerdevs-deezer.p.rapidapi.com/track/{MUSICAS[cantor_id]}' 

        print(url)
        
        headers = {
            "X-RapidAPI-Key": "f7f5182486mshc35a209e947abcdp12f459jsna69f73fc791e",
            "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
        }
 
        res = requests.get(url, headers=headers)
 
        data = res.json()
        data_link = data["link"]
        link  = {"link de uma de suas músicas no deezer:": data_link}
        return cantor, link
    except KeyError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Cantor não encontrado.')
    except  ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="So aceito inteiros....")
    
@app.get('/cantores/{cantor_id}')
async def get_cantores_id(cantor_id):
    try:
        cantor_id = int(cantor_id)
        cantor = cantores[cantor_id]
        cantor.update({"id": cantor_id})
        return cantor
    except KeyError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Cantor não encontrado.')
    except  ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="So aceito inteiros....")    

@app.post("/cantores" , status_code=status.HTTP_201_CREATED)
async def post_cantor(cantor:Cantor):
    if cantor.id not in cantores:
        next_id = len(cantores) +1
        cantores[next_id] = cantor
        del cantor.id
        return cantor
    else:
        raise HTTPException (status_code=status.HTTP_409_CONFLICT, detail= f"Já existe um cantor com ID {cantor.id}")
    

@app.put("/cantores/{cantor_id}")
async def put_cantores(cantor_id: int , cantor:Cantor):
    if cantor_id in cantores:
        cantores [cantor_id] = cantor
        cantor.id = cantor_id
        del cantor.id
        return cantor
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Cantor não encontrado.')
    
@app.delete("/cantores/{cantor_id}")
async def delete_cantor(cantor_id : int):
    if cantor_id in cantores:
        del cantores [cantor_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Esse curso não existe")




if __name__ =='__main__':
    import uvicorn
    uvicorn.run("main:app" ,host='0.0.0.0' , port=8000, reload=True)