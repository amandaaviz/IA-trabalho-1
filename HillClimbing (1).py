import random
import time
import csv
import json
import statistics
import pandas as pd
import matplotlib.pyplot as plt

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
    houve_otimo_local = False
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
            houve_otimo_local = True
            break

        iteracoes += 1

        # Critérios de parada
        if h_atual == 0:
            break

        if mov_laterais >= max_laterais:
            break

    return estado, h_atual, iteracoes, mov_laterais, houve_otimo_local

# ---------------------------
# Random Restart
# ---------------------------
def hill_climbing_restart(max_iter=1000, max_restarts=50):
    melhor_global = None
    melhor_h_global = float('inf')

    total_iteracoes = 0
    total_restarts = 0
    total_laterais = 0
    houve_otimo_local = False

    for _ in range(max_restarts):
        estado, h, it, laterais, otimo_local = hill_climbing(max_iter)

        total_iteracoes += it
        total_laterais += laterais
        total_restarts += 1

        if otimo_local:
            houve_otimo_local = True

        if h < melhor_h_global:
            melhor_global = estado
            melhor_h_global = h

        if melhor_h_global == 0:
            break

    return (
        melhor_global,
        melhor_h_global,
        total_iteracoes,
        total_laterais,
        houve_otimo_local,
        total_restarts
    )

# ---------------------------
# Execução experimental
# ---------------------------
def executar_experimentos(num_execucoes=15):
    resultados = []

    for i in range(num_execucoes):
        inicio = time.time()

        estado_inicial = gerar_estado_aleatorio()
        estado_final, h_final, iteracoes, laterais, otimo_local, total_restarts = hill_climbing_restart()

        fim = time.time()

        resultados.append({
            "execucao": i + 1,
            "estado_inicial": estado_inicial,
            "estado_final": estado_final,
            "h_final": h_final,
            "iteracoes": iteracoes,
            "tempo": fim - inicio,
            "sucesso": h_final == 0,
            "movimentos_laterais": laterais,
            "houve_otimo_local": otimo_local,
            "reinicios": total_restarts
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
# Melhores soluções
# ---------------------------
def melhores_solucoes(resultados):
    ordenado = sorted(resultados, key=lambda x: x["h_final"])
    top5 = []

    vistos = set()

    for r in ordenado:
        estado = tuple(r["estado_final"])

        if estado not in vistos:
            top5.append(r)
            vistos.add(estado)

        if len(top5) == 5:
            break

    return top5

def gerar_grafico():
    df = pd.read_csv("resultados.csv")

    plt.figure(figsize=(10,5))
    plt.bar(df["execucao"], df["iteracoes"])

    plt.xlabel("Execução")
    plt.ylabel("Número de Iterações")
    plt.title("Número de Iterações por Execução")
    
    plt.savefig("grafico_iteracoes.png")
    plt.show()
    plt.close()

    print("\nGráfico salvo como grafico_iteracoes.png")

def gerar_tabela():
    df = pd.read_csv("resultados.csv")

    df_resumo = df[["execucao", "iteracoes", "tempo", "h_final", "sucesso", "movimentos_laterais", "houve_otimo_local", "reinicios"]]

    df_resumo.to_csv("tabela_resultados.csv", index=False)

    print("\nTABELA DE RESULTADOS\n")
    print(df_resumo.to_string(index=False))

    print("\nTabela salva como tabela_resultados.csv")
# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    resultados = executar_experimentos(15)

    salvar_csv(resultados)
    salvar_json(resultados)
    analisar_resultados(resultados)

    top5 = melhores_solucoes(resultados)

    print("\nTOP 5 SOLUÇÕES")

    for i, s in enumerate(top5, 1):
        print(f"{i}: {s}")

    gerar_tabela()
    gerar_grafico()

    print("\nExecução finalizada.")