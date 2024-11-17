import requests
import json
import matplotlib.pyplot as plt


def main():

    # URL de la api (HTTPL de donde extraemos la información)
    url = "https://randomuser.me/api/?results=100"
    
    # Devolver las variables de sus respectivas funciones a la principal

    data = extraer_data(url)
    
    generos, paises, edades, registros, año_creacion_cuentas = transformar_datos(data)
    
    max_edad, min_edad, media, rango = estadisticas_descriptivas(edades)

    # Calculos estadisticos con python y visualización de gráficos con matplotlib

    # Participantes totales
    participantes_totales = len(data["results"])

    # Porcentage del genero 1
    porcentage_genero1 = list(generos.values())[0]/participantes_totales*100
    # Porcentage del genero 2
    porcentage_genero2 = list(generos.values())[1]/participantes_totales*100

    print(f"\nParticipantes: {participantes_totales}\n"
    f"\nGenero: {generos}\n"
    f"{porcentage_genero1:.2f}% {list(generos.keys())[0]}, {porcentage_genero2:.2f}% {list(generos.keys())[1]}\n")
    
    #Gráfico de pastel o tarta → distribucion de género

    datos_genero = [porcentage_genero1, porcentage_genero2]
    tipo_genero = [list(generos.keys())[0], list(generos.keys())[1]]
    plt.pie(datos_genero, labels=tipo_genero, autopct="%0.1f%%")
    plt.axis("equal")
    plt.show()

    #Gráfico de barras → cantidad de usuario del pais
    barra_pais = list(paises.keys())
    usuarios_pais = list(paises.values())
    plt.figure(figsize=(10, 6)) 
    plt.bar(barra_pais, usuarios_pais, color='skyblue')
    plt.title("Cantidad de Usuarios por País")
    plt.xlabel("País")
    plt.ylabel("Número de Usuarios")
    plt.xticks(rotation=90)
    plt.show()

    # Gáfico de línea → Evolución de edad
    plt.plot(sorted(año_creacion_cuentas), edades, marker='o')  # 'o' para marcar los puntos
    plt.title("Evolución de Edad vs Año de Creación de Cuenta")
    plt.xlabel("Año de Creación de Cuenta")
    plt.ylabel("Edad")
    plt.show()

    # Print de cálculos estadisticos: Edad más bajo, alto, rango y media

    print(f"Menor edad: {min_edad}\n"
    f"Mayor edad: {max_edad}\n"
    f"Rango de edad: {rango}\n"
    f"Media de edad: {media:.2f}\n")
    
    #Histograma → distribucion de edad con usuarios

    plt.hist(edades)
    plt.title("Distribución de Edad")
    plt.xlabel("Edades")
    plt.ylabel("Número de Usuarios")
    plt.show()

    #Gráfico de dispersión → Distribución de edad por Años Registrado
    plt.figure(figsize=(10, 6))
    plt.scatter(registros, edades, color='b', marker='o')
    plt.title('Gráfico de Dispersión: Edad por Años Registrado')
    plt.xlabel('Años registrados')
    plt.ylabel('Edad')
    plt.grid(True) 
    plt.show()

    # Extraer y guardar al finalizar a un archivo llamado comutación.json
    try:
        guardar_datos(data, "computación.json")
        print("Datos guardados correctamente.")
    except Exception as error:
        print(f"No se ha podido guardar el archivos, {error}") 


def extraer_data(url):

    # Pedir información al servidor
    data = requests.get(url)
    if data.status_code == 200:
        data_extraido = json.loads(data.text)
        return data_extraido
    else:
        return (f"Error {data.status_code}, no se han podido extraer datos")

def transformar_datos(data):

    #Crear lista y dict de las variables que vamos a usar:
    generos = {}
    paises = {}
    edades = []
    registros = []
    año_creacion_cuentas = []
    

    # Extraer variables que vamos a utilizar:
    for result in data["results"]:
        genero = (result["gender"])
        pais = (result["location"]["country"])
        edad = (result["dob"]["age"])
        tiempo_registrado = (result["registered"]["age"])
        año_registrado = (result["registered"]["date"])
        

        # Crear dict de generos y pais separando sus valores: si existe = añade, si no existe=crea nueva key
        if genero in generos:
            generos[genero] += 1
        else:
            generos[genero] = 1
       
       #dict de paises
        if pais in paises:
            paises[pais] += 1
        else:
            paises[pais] = 1
        
        # Añadir variables edad en lista
        edades.append(int(edad))

        # Añadir años que el usuario esta registrado en lista
        registros.append(tiempo_registrado)
        
        # Añadir año en el que el usuario se registró en lista
        año_creacion_cuentas.append(int(año_registrado[:4]))

    # Return de todos los dict y listas que hemos creado
    return generos, paises, edades, registros, año_creacion_cuentas

def estadisticas_descriptivas(edades):

    # Edad más alta
    max_edad = max(edades)

    # Edad más bajo
    min_edad = min(edades)

    # Media de edad
    media = sum(edades) / len(edades)

    # Rango de edad
    rango = max(edades) - min(edades)

    # Return de las variables de edad más alta, baja, media y rango
    return max_edad, min_edad, media, rango

def guardar_datos(data, nombre_json):

    with open(nombre_json, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()
