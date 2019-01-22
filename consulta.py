import requests
import json
import time

# cnpj = ['05953543000309', '29954518000146']

# api de consulta
base = 'https://www.receitaws.com.br/v1/cnpj/'


cnpj = []

with open('config.txt', 'r') as f:
    for line in f:
        cnpj.append(line.replace('\n', ''))

    print("Arquivo carregado ...")

# input de consultas
total = len(cnpj)
controle = len(cnpj)
# abrir arquivo para persistencia
with open('resultado.txt', 'w') as f:
    for i in cnpj:
        r = requests.get(f'{base}{i}')
        print(f'[{controle}/{total}]', end=" ")
        if r.status_code == requests.codes.ok:
            data = json.loads(r.text)
            print(f"{r.status_code} - {data['nome']}")
            f.write(f"[{controle}/{total}] | cnpj: {data['cnpj']} | situacao: {data['situacao']} | nome: {data['nome']}\n")
        else:
            print("erro!")
        controle -= 1
        if controle != 0:
            time.sleep(20.5)
