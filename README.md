## Consulta de CNPJ
A consulta de situação de CNPJ feita através da API do site [ReceitaWS](https://www.receitaws.com.br/api)  

### Requerimentos
1. Pipev
2. Requests

### Uso
O uso é feito através do preenchimento do arquivo *config.txt* com a lista de CNPJs que deseja consultar separado por linha.  
Depois é só executar o programa e o resultado prévio irá aparecer no shell de execução.
  
Após isso é gerado um arquivo *resultado.txt* na qual possui a Razão Social e a Situação na receita, caso ocorra um erro é mostrado
o CNPJ que ocorreu. 

### TODO

Implementar talvez um front para melhor visualização.
