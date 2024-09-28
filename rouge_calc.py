class RougeCalculator:
    def __init__(self):
        pass

    def n_gramas(self, texto, n):
        # Función que devuelve los n-gramas de un texto
        palabras = texto.split()
        n_gramas = [tuple(palabras[i:i+n]) for i in range(len(palabras)-n+1)]
        return n_gramas

    def calcular_precision_recall_f1(self, coincidencias, total_referencia, total_generado):
        # Calcula Precision, Recall y F1 Score dados los valores de coincidencias, total de referencia y total generado
        recall = coincidencias / total_referencia if total_referencia > 0 else 0
        precision = coincidencias / total_generado if total_generado > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0
        return precision, recall, f1_score

    def rouge_n(self, resumen_generado, resumen_referencia, n):
        # Calcula ROUGE-N, devuelve precision, recall y F1 Score
        ngramas_generado = self.n_gramas(resumen_generado, n)
        ngramas_referencia = self.n_gramas(resumen_referencia, n)

        # Contar las coincidencias
        ngramas_coincidentes = set(ngramas_generado) & set(ngramas_referencia)

        # Calcular Precision, Recall y F1
        precision, recall, f1_score = self.calcular_precision_recall_f1(
            len(ngramas_coincidentes), len(ngramas_referencia), len(ngramas_generado)
        )

        return precision, recall, f1_score

    def lcs(self, X, Y):
        # Función para calcular la Longest Common Subsequence (LCS) entre dos secuencias
        m = len(X)
        n = len(Y)
        L = [[0] * (n + 1) for i in range(m + 1)]

        # Construir la tabla L[m+1][n+1] en orden de abajo hacia arriba
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])

        return L[m][n]

    def rouge_l(self, resumen_generado, resumen_referencia):
        # Calcula ROUGE-L, devuelve precision, recall y F1 Score
        palabras_generado = resumen_generado.split()
        palabras_referencia = resumen_referencia.split()

        # Calcular la Longest Common Subsequence (LCS)
        longitud_lcs = self.lcs(palabras_generado, palabras_referencia)

        # Calcular Precision, Recall y F1
        precision, recall, f1_score = self.calcular_precision_recall_f1(
            longitud_lcs, len(palabras_referencia), len(palabras_generado)
        )

        return precision, recall, f1_score

    def calcular_rouge(self, modelos, resumen_referencia):
        # Función que calcula ROUGE-1, ROUGE-2 y ROUGE-L para 'n' modelos y un resumen de referencia
        resultados = {}
        for i, modelo in enumerate(modelos):
            rouge_1_p, rouge_1_r, rouge_1_f1 = self.rouge_n(modelo, resumen_referencia, 1)
            rouge_2_p, rouge_2_r, rouge_2_f1 = self.rouge_n(modelo, resumen_referencia, 2)
            rouge_l_p, rouge_l_r, rouge_l_f1 = self.rouge_l(modelo, resumen_referencia)

            resultados[f'Modelo {i+1}'] = {
                'ROUGE-1': {'Precisión': rouge_1_p, 'Recall': rouge_1_r, 'F1-Score': rouge_1_f1},
                'ROUGE-2': {'Precisión': rouge_2_p, 'Recall': rouge_2_r, 'F1-Score': rouge_2_f1},
                'ROUGE-L': {'Precisión': rouge_l_p, 'Recall': rouge_l_r, 'F1-Score': rouge_l_f1}
            }
        return resultados

    def mejor_modelo_por_metrica_completa(self, resultados, nombres_modelos):
        # Función que identifica el mejor modelo para cada métrica (ROUGE-1, ROUGE-2, ROUGE-L) en base a precisión, recall y F1-Score
        mejores_modelos = {
            'ROUGE-1': {'Precisión': {'modelo': None, 'valor': 0}, 'Recall': {'modelo': None, 'valor': 0}, 'F1-Score': {'modelo': None, 'valor': 0}},
            'ROUGE-2': {'Precisión': {'modelo': None, 'valor': 0}, 'Recall': {'modelo': None, 'valor': 0}, 'F1-Score': {'modelo': None, 'valor': 0}},
            'ROUGE-L': {'Precisión': {'modelo': None, 'valor': 0}, 'Recall': {'modelo': None, 'valor': 0}, 'F1-Score': {'modelo': None, 'valor': 0}},
        }

        for i, (modelo, resultado) in enumerate(resultados.items()):
            for metrica, valores in resultado.items():
                for medida, valor in valores.items():
                    if valor > mejores_modelos[metrica][medida]['valor']:
                        mejores_modelos[metrica][medida] = {'modelo': nombres_modelos[i], 'valor': valor}
        
        return mejores_modelos
