import json
import os
import numpy as np
import matplotlib.pyplot as plt

pasta = "resultados"
dados = []
iteracoes = []
tempos = []
sucessos = []
h_finais = []


# LER ARQUIVOS
for arquivo in os.listdir(pasta):
    if arquivo.endswith(".json"):
        with open(os.path.join(pasta, arquivo), "r", encoding="utf-8") as f:
            data = json.load(f)

            # pega nível 0 (lista)
            for bloco in data:
                # pega lista "dados"
                for item in bloco["resultados"]:
                    iteracoes.append(item["iteracoes"])
                    tempos.append(item["tempo"])
                    sucessos.append(item["sucesso"])
                    h_finais.append(item["h_final"])


# ESTATÍSTICAS
media_iteracoes = np.mean(iteracoes)
dp_iteracoes = np.std(iteracoes)

media_tempo = np.mean(tempos)
dp_tempo = np.std(tempos)

taxa_sucesso = sum(sucessos) / len(sucessos)

media_h_final = np.mean(h_finais)


# RESULTADO FORMATADO
print("\n===== ANÁLISE EXPERIMENTAL =====\n")

print(f"Média do número de iterações: {media_iteracoes:.2f}")
print(f"Desvio padrão das iterações: {dp_iteracoes:.2f}\n")

print(f"Média do tempo de execução: {media_tempo:.6f} s")
print(f"Desvio padrão do tempo: {dp_tempo:.6f} s\n")

print(f"Taxa de sucesso: {taxa_sucesso * 100:.2f}%")
print(f"Média da função objetivo (h final): {media_h_final:.2f}")


# GRÁFICO 1 - Iterações
plt.figure()
plt.plot(iteracoes, marker='o')
plt.title("Número de Iterações por Execução")
plt.xlabel("Execução")
plt.ylabel("Iterações")
plt.grid()
plt.show()


# GRÁFICO 2 - Tempo
plt.figure()
plt.plot(tempos, marker='o')
plt.title("Tempo de Execução por Execução")
plt.xlabel("Execução")
plt.ylabel("Tempo (s)")
plt.grid()
plt.show()


# GRÁFICO 3 - Taxa de sucesso
sucesso_count = sum(sucessos)
falha_count = len(sucessos) - sucesso_count

plt.figure()
plt.bar(["Sucesso", "Falha"], [sucesso_count, falha_count])
plt.title("Taxa de Sucesso do Algoritmo")
plt.show()
