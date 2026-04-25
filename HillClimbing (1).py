import random
import time
import csv
import json
import statistics

N = 8

# ---------------------------
# Estado inicial
# ---------------------------
def gerar_estado_aleatorio():
    return [random.randint(0, N - 1) for _ in range(N)]

# ---------------------------
# Função objetivo (h)
# ---------------------------
def calcular_conflitos(estado):
    conflitos = 0
    for i in range(N):
        for j in range(i + 1, N):
            if estado[i] == estado[j]:
                conflitos += 1
            elif abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    return conflitos

# ---------------------------
# Vizinhança
# ---------------------------
def gerar_vizinhos(estado):
    vizinhos = []
    for col in range(N):
        for linha in range(N):
            if estado[col] != linha:
                novo = estado.copy()
                novo[col] = linha
                vizinhos.append(novo)
    return vizinhos

# ---------------------------
# Hill Climbing (Steepest Ascent)
# com controle de platô
# ---------------------------
def hill_climbing(max_iter=1000, max_laterais=50):
    estado = gerar_estado_aleatorio()
    h_atual = calcular_conflitos(estado)

    iteracoes = 0
    mov_laterais = 0

    while iteracoes < max_iter:
        vizinhos = gerar_vizinhos(estado)

        melhor_vizinho = None
        melhor_h = float('inf')

        for v in vizinhos:
            h = calcular_conflitos(v)
            if h < melhor_h:
                melhor_h = h
                melhor_vizinho = v

        # Melhorou
        if melhor_h < h_atual:
            estado = melhor_vizinho
            h_atual = melhor_h
            mov_laterais = 0

        # Platô (movimento lateral)
        elif melhor_h == h_atual:
            estado = melhor_vizinho
            mov_laterais += 1

        # Ótimo local
        else:
            break

        iteracoes += 1

        # Critérios de parada
        if h_atual == 0:
            break

        if mov_laterais >= max_laterais:
            break

    return estado, h_atual, iteracoes

# ---------------------------
# Random Restart
# ---------------------------
def hill_climbing_restart(max_iter=1000, max_restarts=50):
    melhor_global = None
    melhor_h_global = float('inf')
    total_iteracoes = 0

    for _ in range(max_restarts):
        estado, h, it = hill_climbing(max_iter)
        total_iteracoes += it

        if h < melhor_h_global:
            melhor_global = estado
            melhor_h_global = h

        if melhor_h_global == 0:
            break

    return melhor_global, melhor_h_global, total_iteracoes

# ---------------------------
# Execução experimental
# ---------------------------
def executar_experimentos(num_execucoes=15):
    resultados = []

    for i in range(num_execucoes):
        inicio = time.time()

        estado_inicial = gerar_estado_aleatorio()
        estado_final, h_final, iteracoes = hill_climbing_restart()

        fim = time.time()

        resultados.append({
            "execucao": i + 1,
            "estado_inicial": estado_inicial,
            "estado_final": estado_final,
            "h_final": h_final,
            "iteracoes": iteracoes,
            "tempo": fim - inicio,
            "sucesso": h_final == 0
        })

    return resultados

# ---------------------------
# Salvar resultados
# ---------------------------
def salvar_csv(resultados, nome="resultados.csv"):
    with open(nome, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

def salvar_json(resultados, nome="resultados.json"):
    with open(nome, "w") as f:
        json.dump(resultados, f, indent=4)

# ---------------------------
# Estatísticas
# ---------------------------
def analisar_resultados(resultados):
    iteracoes = [r["iteracoes"] for r in resultados]
    tempos = [r["tempo"] for r in resultados]
    sucessos = [r["sucesso"] for r in resultados]
    h_vals = [r["h_final"] for r in resultados]

    print("\n--- ANÁLISE ---")
    print("Média iterações:", statistics.mean(iteracoes))
    print("Desvio padrão iterações:", statistics.stdev(iteracoes))
    print("Média tempo:", statistics.mean(tempos))
    print("Desvio padrão tempo:", statistics.stdev(tempos))
    print("Taxa de sucesso:", sum(sucessos) / len(sucessos))
    print("Valor médio de h:", statistics.mean(h_vals))

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    resultados = executar_experimentos(15)
    salvar_csv(resultados)
    salvar_json(resultados)
    analisar_resultados(resultados)

    print("\nExecução finalizada.")