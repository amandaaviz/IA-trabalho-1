# Trabalho Prático - Inteligência Artificial

## Tema

Hill Climbing aplicado ao problema das 8 rainhas

## Integrantes

* Karen Souza Santos
* Anda Aviz Pina

## Como executar

1. Rodar requirements: 

pip install -r requirements.txt

2. API:

Iniciar a API
uvicorn api:app --reload


3. N8N:

3.1 Baixar n8n: 

npm install n8n -g

3.2 Executar no terminal: 

n8n start

3.3 Acessar: 

O n8n ficará disponível em:
http://localhost:5678

3.4 Baixar o arquivo "Hill Climbing Correto.json" , importar no n8n e Executar


Enviar requisição com:
{
  "num_execucoes": 15,
  "max_iter": 1000,
  "variante": "restart"
}


4. Baixar os 15 JSONs gerados e Salvar todos na pasta: 
resultados/


5. Rodar análise:

python analise.py