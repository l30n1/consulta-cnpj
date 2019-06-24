import sqlite3
from datetime import datetime

# time para gravar a data atual


class Banco:

    EXPIRA = 7

    def __init__(self, conexao):
        '''Objeto de conexao com o banco de dados'''
        self.conexao = conexao

    def conecta(self):
        try:
            self.conn = sqlite3.connect(self.conexao)
        except Exception as e:
            raise e

    def desconecta(self):
        try:
            self.conn.close()
        except Exception as e:
            raise e

    def busca(self, comando):
        c = self.conn.cursor()
        data = c.execute(comando)
        return data

    def query(self, comando):
        c = self.conn.cursor()
        try:
            c.execute(comando)
            self.conn.commit()
        except Exception as e:
            raise e

    # melhorar
    def cnpj_exist(self, cnpj):
        dados = self.busca('SELECT cnpj FROM cliente').fetchall()
        for row in dados:
            cnpj_limpo_comp = self.sanitizar(cnpj)
            cnpj_tratado_busca = self.sanitizar(row[0])
            if cnpj_limpo_comp == cnpj_tratado_busca:
                return True
        return False

    def apagar_registro(self, cnpj):
        if self.cnpj_exist(cnpj):
            try:
                self.query(
                    f"DELETE FROM cliente WHERE cnpj = '{self.format(cnpj)}'")
            except Exception as e:
                raise e

    def sanitizar(self, cnpj):
        x = cnpj.replace('.', '').replace('/', '').replace('-',
                                                           '').replace('\n', '').replace(' ', '')
        return x

    def format(self, cnpj):
        return "{}.{}.{}/{}-{}".format(cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])

    def achar_cnpj(self, cnpj):
        if self.cnpj_exist(cnpj):
            data = self.busca(
                f"SELECT * FROM cliente WHERE cnpj = '{self.format(cnpj)}'")
            novo = list(*data)
            colunas = []
            for row in self.busca('PRAGMA table_info(cliente)'):
                colunas.append(row[1])

            meu_dic = dict(zip(colunas, novo))

            if self.validar_data(meu_dic['data_consulta']):
                return meu_dic
            else:
                self.apagar_registro(cnpj)
                return None
        else:
            return None

    def gravar(self, dados):
        c = self.conn.cursor()
        try:
            tempo = datetime.strftime(datetime.today(), "%d/%m/%Y")
            c.execute(f"""
            INSERT INTO cliente VALUES (
                "{dados["cnpj"]}",
                "{dados["tipo"]}",
                "{dados["abertura"]}",
                "{dados["nome"]}",
                "{dados["fantasia"].replace('"','')}",
                "{dados["natureza_juridica"]}",
                "{dados["logradouro"]}",
                "{dados["numero"]}",
                "{dados["complemento"]}",
                "{dados["cep"]}",
                "{dados["bairro"]}",
                "{dados["municipio"]}",
                "{dados["uf"]}",
                "{dados["email"]}",
                "{dados["telefone"]}",
                "{dados["efr"]}",
                "{dados["situacao"]}",
                "{dados["data_situacao"]}",
                "{dados["motivo_situacao"]}",
                "{dados["situacao_especial"]}",
                "{dados["data_situacao_especial"]}",
                "{dados["capital_social"]}",
                "{tempo}")
                """)
            self.conn.commit()
        except Exception as e:
            raise e

    def validar_data(self, data):
        try:
            dia_consulta = datetime.strptime(data, "%d/%m/%Y")
            hoje = datetime.today()
            diff = hoje - dia_consulta
            if diff.days < self.EXPIRA:
                return True
            else:
                return False
        except ValueError:
            print('data invalida!')
            return True


'''
funcao dando error refatorar

    def validar_cnpj(self, cnpj):
        print(f"TESTE: ----------------------------------------------- -->  {self.cnpj_exist(cnpj)}")
        if self.cnpj_exist(cnpj):
            dados = self.achar_cnpj(cnpj)
            dia_consulta = datetime.strptime(dados['data_consulta'], "%d/%m/%Y")
            hoje = datetime.today()
            diff = hoje - dia_consulta
            if diff.days < self.EXPIRA:
                return True
            else:
                return False
        else:
            return False
'''
