from rouge_calc import RougeCalculator

def main():
    calculadora_rouge = RougeCalculator()

    # Ingresar el resumen de referencia
    resumen_referencia = input("Ingrese el resumen de referencia: ")

    # Ingresar los nombres de los modelos
    nombres_modelos = input("Ingrese los nombres de los modelos a comparar (separados por comas): ")
    nombres_modelos = [nombre.strip() for nombre in nombres_modelos.split(",")]

    # Ingresar los resúmenes para cada modelo
    modelos = []
    for nombre in nombres_modelos:
        resumen_modelo = input(f"Ingrese el resumen generado por {nombre}: ")
        modelos.append(resumen_modelo)

    # Calcular las métricas ROUGE
    resultados = calculadora_rouge.calcular_rouge(modelos, resumen_referencia)

    # Imprimir los resultados de las métricas ROUGE
    for i, (modelo, resultado) in enumerate(resultados.items()):
        print(f"{nombres_modelos[i]}:")
        for metrica, valores in resultado.items():
            print(f"{metrica}:")
            print(f"  Precisión: {valores['Precisión']:.4f}")
            print(f"  Recall: {valores['Recall']:.4f}")
            print(f"  F1-Score: {valores['F1-Score']:.4f}")
        print()

    # Identificar los mejores modelos para cada métrica y medida
    mejores_modelos = calculadora_rouge.mejor_modelo_por_metrica_completa(resultados, nombres_modelos)

    print("Mejores modelos por métrica y medida:")
    for metrica, medidas in mejores_modelos.items():
        for medida, info in medidas.items():
            print(f"{metrica} - {medida}: Mejor modelo = {info['modelo']} con un valor de {info['valor']:.4f}")


if __name__ == "__main__":

    main()