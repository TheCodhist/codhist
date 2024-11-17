import requests
import json
import pandas as pd

class Person:
    def __init__(self, genero, nombre, apellido, edad, pais, registro):
        self.genero = genero
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.pais = pais
        self.registro = registro
    def __repr__(self):
        return (f"Nombre: {self.nombre} {self.apellido}, Género: {self.genero}, País: {self.pais}, Edad: {self.edad}, Años Registrado: {self.registro}")


def main():

    url = "https://randomuser.me/api/?results=10"
    
    personas = []
    data = extract_data(url)
    for result in data["results"]:
        nombre = (result["name"]["first"])
        apellido = (result["name"]["last"])
        genero = (result["gender"])
        pais = (result["location"]["country"])
        edad = (result["dob"]["age"])
        registro = (result["registered"]["age"])

        persona = Person(genero, nombre, apellido, edad, pais, registro)
        personas.append(persona)
        print(persona.edad)
    
    media, rango = media_y_rango(personas)

    print(f"Media de edad: {media:.2f} Rango de edad: {rango}")
    print(pd.__version__)

    

def extract_data(url):
    data = requests.get(url)
    if data.status_code == 200:
        data_extracted = json.loads(data.text)
        return data_extracted
    else:
        return (f"Error {data.status_code}, no se han podido extraer datos")

def media_y_rango(personas):

    edades = [persona.edad for persona in personas]
    
    media = sum(edades)/len(edades)
    rango = max(edades) - min(edades)
    return media, rango




if __name__ == "__main__":
    main()