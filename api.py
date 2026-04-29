from fastapi import FastAPI
import random
import time
import uuid

app = FastAPI()

N = 8

# Estado inicial
def gerar_estado_aleatorio():
    return [random.randint(0, N - 1) for _ in range(N)]


# Função objetivo
def calcular_conflitos(estado):
    conflitos = 0
    for i in range(N):
        for j in range(i + 1, N):
            if estado[i] == estado[j]:
                conflitos += 1
            elif abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    return conflitos


# Vizinhos
def gerar_vizinhos(estado):
    vizinhos = []
    for col in range(N):
        for linha in range(N):
            if estado[col] != linha:
                novo = estado.copy()
                novo[col] = linha
                vizinhos.append(novo)
    return vizinhos


# Hill Climbing
def hill_climbing(max_iter=1000, max_laterais=50):
    max_iter = int(max_iter)
    estado = gerar_estado_aleatorio()
    h_atual = calcular_conflitos(estado)

    iteracoes = 0
    mov_laterais = 0
    houve_otimo_local = False

    while iteracoes < max_iter:
        vizinhos = gerar_vizinhos(estado)

        melhor_vizinho = None
        melhor_h = float('inf')

        for v in vizinhos:
            h = calcular_conflitos(v)
            if h < melhor_h:
                melhor_h = h
                melhor_vizinho = v

        if melhor_h < h_atual:
            estado = melhor_vizinho
            h_atual = melhor_h
            mov_laterais = 0

        elif melhor_h == h_atual:
            estado = melhor_vizinho
            mov_laterais += 1

        else:
            houve_otimo_local = True
            break

        iteracoes += 1

        if h_atual == 0 or mov_laterais >= max_laterais:
            break

    return estado, h_atual, iteracoes, mov_laterais, houve_otimo_local


# Random Restart
def hill_climbing_restart(max_iter=1000, max_restarts=50):
    melhor_global = None
    melhor_h_global = float('inf')

    total_iteracoes = 0
    total_laterais = 0
    total_restarts = 0
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

    return melhor_global, melhor_h_global, total_iteracoes, total_laterais, houve_otimo_local, total_restarts


# EXECUÇÃO ÚNICA
def executar_uma_execucao(execucao_id, max_iter=1000, variante="restart"):
    inicio = time.time()

    estado_inicial = gerar_estado_aleatorio()

    if variante == "restart":
        estado_final, h_final, iteracoes, laterais, otimo_local, reinicios = hill_climbing_restart(max_iter)
    else:
        estado_final, h_final, iteracoes, laterais, otimo_local = hill_climbing(max_iter)
        reinicios = 0

    fim = time.time()

    return {
        "execucao": execucao_id,
        "estado_inicial": estado_inicial,
        "estado_final": estado_final,
        "h_final": h_final,
        "iteracoes": iteracoes,
        "tempo": fim - inicio,
        "sucesso": h_final == 0,
        "movimentos_laterais": laterais,
        "houve_otimo_local": otimo_local,
        "reinicios": reinicios
    }


# ENDPOINT
@app.post("/executar")
def executar(data: dict):
    max_iter = data.get("max_iter", 1000)
    variante = data.get("variante", "restart")
    execucao_id = str(uuid.uuid4())

    resultado = executar_uma_execucao(execucao_id,max_iter, variante)

    return resultado