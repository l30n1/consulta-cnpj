import requests
import json
import time
from banco import Banco
from datetime import datetime


def marcarHora():
    hora = datetime.now()
    hora = datetime.strftime(hora, '%H:%M:%S')
    print(hora, end=' ')


# cnpj = ['05953543000309', '29954518000146']

'''
API de consulta
'''
teste = False
if teste:
    base = 'https://www.receitas.com.br/v1/cnpj/'
else:
    base = 'https://www.receitaws.com.br/v1/cnpj/'

cnpj = []

with open('config.txt', 'r') as f:
    for line in f:
        codigo = line.replace('.', '').replace(
            '/', '').replace('-', '').replace('\n', '').replace(' ', '')
        if codigo != '':
            cnpj.append(codigo)

    print("Arquivo carregado ...")

'''
Dict de controle
'''
check = {}
check['total'] = len(cnpj)
check['controle'] = len(cnpj)
check['tentativas'] = 0

'''
Gravação de Persistência
tenta acessar > caso erro outras tentativas são feitas
'''

b = Banco('dbexample.db')
b.conecta()


with open('resultado.txt', 'w') as f:
    for i in cnpj:

        if b.achar_cnpj(i):
            marcarHora()
            data = b.achar_cnpj(i)
            print(
                f"[{check['controle']:02}/{check['total']:02}] - CACHE - {data['data_consulta']} - {data['nome']}")
            f.write(f"[{check['controle']:02}/{check['total']:02}] | cnpj: {data['cnpj']} | situacao: {data['situacao']} | nome: {data['nome']} | endereco: {data['logradouro']}-{data['numero']} | complemento: {data['complemento']} | uf: {data['uf']} | municipio: {data['municipio']} | bairro: {data['bairro']}\n")
            check['controle'] -= 1

        else:
            while not(check['tentativas'] > 4):
                marcarHora()
                try:
                    r = requests.get(f'{base}{i}', timeout=5)
                    print(
                        f"[{check['controle']:02}/{check['total']:02}] - T:{check['tentativas']:02} - R:{r.status_code} - ", end='')
                    if r.status_code == requests.codes.ok:
                        data = json.loads(r.text)
                        b.gravar(data)
                        print(f"{data['nome']}")
                        if data['status'] == 'OK':
                            f.write(f"[{check['controle']:02}/{check['total']:02}] | cnpj: {data['cnpj']} | situacao: {data['situacao']} | nome: {data['nome']} | endereco: {data['logradouro']}-{data['numero']} | complemento: {data['complemento']} | uf: {data['uf']} | municipio: {data['municipio']} | bairro: {data['bairro']}\n")
                        else:
                            print("erro!")
                            f.write(
                                f"[{check['controle']:02}/{check['total']:02}] | cnpj: {i} | situacao: ERRO! | {data['message']}\n")

                        check['controle'] -= 1
                        if check['controle'] != 0:
                            time.sleep(20.5)
                        break

                    if r.status_code == requests.codes.too_many:
                        print('#  muitas requisicoes!')
                        time.sleep(45)

                except requests.ReadTimeout as e:
                    print(f"[{check['controle']:02}/{check['total']:02}] | cnpj: {i} | situacao: CNPJ com erro na API!")
                    f.write(f"[{check['controle']:02}/{check['total']:02}] | cnpj: {i} | situacao: CNPJ com erro na API!")
                    break

                check['tentativas'] += 1
                time.sleep(1)

            if check['tentativas'] == 5:
                print('Erro: Impossivel conectar!')
                f.close()
                raise
            check['tentativas'] = 0
