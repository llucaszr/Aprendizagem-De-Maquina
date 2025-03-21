import random
import pandas as pd

frutas = ["maçã", "banana", "laranja", "uva", "maçã", "melão", "mamão", "banana"]

# Cria um conjunto (set) para remover as frutas repetidas
conjunto_frutas = set(frutas)

# Cria o arquivo minhas_frutas.txt e grava as frutas com quantidades aleatórias
with open("minhas_frutas.txt", "w") as arquivo:
  for fruta in conjunto_frutas:
    quantidade = random.randint(0, 100)
    arquivo.write(f"{fruta},{quantidade}\n")

# Dicionário para armazenar as frutas e suas quantidades
frutas_quantidades = {}

# Abre o arquivo para ler o conteúdo
with open("minhas_frutas.txt", "r") as arquivo:
  for linha in arquivo:
    fruta, quantidade = linha.strip().split(",")
    quantidade = int(quantidade)
    if fruta in frutas_quantidades:
      frutas_quantidades[fruta] += quantidade
    else:
      frutas_quantidades[fruta] = quantidade

# Cria uma lista de dicionários para criar o DataFrame
dados_frutas = []
for fruta, quantidade in frutas_quantidades.items():
  dados_frutas.append({"Fruta": fruta, "Quantidade": quantidade})

# Cria o DataFrame
df = pd.DataFrame(dados_frutas)

# Exibir o DataFrame
df