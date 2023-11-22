from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

individuo = 6       # tam_poblacion
ciudades = 30       
rango_inicial = 1
rango_final = 30
generaciones = 20
p_cruza = 0.7       # Recombinacion
p_mutacion = 0.1    # Mutacion


def generar_individuo():
    ruta = random.sample(range(rango_inicial, rango_final + 1), ciudades)
    return ruta


def calcular_suma_total(ruta):
    suma_total = sum(ruta)
    return suma_total


def generar_nueva_generacion(generacion_actual):
    nueva_poblacion = []

    mejor_individuo = min(generacion_actual, key=calcular_suma_total)
    nueva_poblacion.append(mejor_individuo)

    while len(nueva_poblacion) < individuo - 1:
        n_rec = random.random()
        if n_rec <= p_cruza:
            Padre = random.choice(generacion_actual)
            Madre = random.choice(generacion_actual)
            if Padre != Madre:
                punto_cruza = random.randint(1, ciudades - 1)
                Hijo = Padre[:punto_cruza] + \
                    [ciudad for ciudad in Madre if ciudad not in Padre]
                nueva_poblacion.append(Hijo)
        elif n_rec <= p_mutacion:
            individuo_intercambio = random.choice(generacion_actual)
            individuo_pos_1 = random.randint(0, ciudades - 1)
            individuo_pos_2 = random.randint(0, ciudades - 1)
            individuo_intercambio[individuo_pos_1], individuo_intercambio[
                individuo_pos_2] = individuo_intercambio[individuo_pos_2], individuo_intercambio[individuo_pos_1]

    while len(nueva_poblacion) < individuo:
        nueva_poblacion.append(generar_individuo())

    return nueva_poblacion


primer_generacion = [generar_individuo() for _ in range(individuo)]

for i, lista in enumerate(primer_generacion):
    suma_total = calcular_suma_total(lista)
    print(f"Individuo {
          i + 1}: {lista}, Suma total del recorrido: {suma_total}")

while generaciones > 0:
    nueva_poblacion = generar_nueva_generacion(primer_generacion)
    mejor_individuo = min(nueva_poblacion, key=calcular_suma_total)
    mejor_suma_total = calcular_suma_total(mejor_individuo)

    id_mejor_individuo = nueva_poblacion.index(mejor_individuo)

    print(f"\nEl mejor individuo en la generación {
          generaciones} es el individuo número {id_mejor_individuo + 1}\n")
    print(f"Suma total del recorrido del mejor individuo: {
          mejor_suma_total}\n")

    primer_generacion = nueva_poblacion
    generaciones -= 1

mejor_individuo = min(primer_generacion, key=calcular_suma_total)
mejor_suma_total = calcular_suma_total(mejor_individuo)

id_mejor_individuo = primer_generacion.index(mejor_individuo)

print(f"\nEl mejor individuo en la última generación es el individuo número {
      id_mejor_individuo + 1}\n")
print(f"Suma total del recorrido del mejor individuo: {mejor_suma_total}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    datos_formulario = request.get_json()
    ciudades_form = int(datos_formulario.get('ciudades'))
    poblacion_form = int(datos_formulario.get('poblacion'))
    recombinacion_form = float(datos_formulario.get('recombinacion'))
    mutacion_form = float(datos_formulario.get('mutacion'))
    generaciones_form = int(datos_formulario.get('generaciones'))

    global ciudades, individuo, p_cruza, p_mutacion, generaciones
    ciudades = ciudades_form
    individuo = poblacion_form
    p_cruza = recombinacion_form
    p_mutacion = mutacion_form
    generaciones = generaciones_form

    primera_generacion = [generar_individuo() for _ in range(individuo)]

    while generaciones > 0:
        nueva_poblacion = generar_nueva_generacion(primera_generacion)
        mejor_individuo = min(nueva_poblacion, key=calcular_suma_total)
        mejor_suma_total = calcular_suma_total(mejor_individuo)

        id_mejor_individuo = nueva_poblacion.index(mejor_individuo)

        print(f"\nEl mejor individuo en la generación {
              generaciones} es el individuo número {id_mejor_individuo + 1}\n")
        print(f"Suma total del recorrido del mejor individuo: {
              mejor_suma_total}\n")

        primera_generacion = nueva_poblacion
        generaciones -= 1

    mejor_individuo = min(primera_generacion, key=calcular_suma_total)
    mejor_suma_total = calcular_suma_total(mejor_individuo)

    id_mejor_individuo = primera_generacion.index(mejor_individuo)

    print(f"\nEl mejor individuo en la última generación es el individuo número {
          id_mejor_individuo + 1}\n")
    print(f"Suma total del recorrido del mejor individuo: {mejor_suma_total}\n")

    resultado = {'mensaje': 'Formulario procesado correctamente'}
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
