## Consulta de CNPJ
A consulta de situação de CNPJ feita através da API do site [ReceitaWS](https://www.receitaws.com.br/api)  

### Requerimentos
* requests

### Uso
O uso é feito através do preenchimento do arquivo *config.txt* com a lista de CNPJs que deseja consultar separado por linha.  
Depois é só executar o programa e o resultado prévio irá aparecer no shell de execução.

```shell
python consulta.py
```



Após isso é gerado um arquivo *resultado.txt* na qual possui a maioria das informações do cliente.  
O programa faz o tratamento do erro caso aconteça alguma coisa:

* tratamento de `429 - too_many_requests`  e um descanso para poder continuar.
* tratamento de `504 - gateway_timeout` quando não acha o CNPJ na API.
* ou se a internet cair.
* um "erro" é não encontrar o CNPJ e é mostrado no arquivo e prévio.


### TODO
- [ ] Escrever os **Testes**

- [ ] Implementar talvez um front para melhor visualização.
- [x] Implementar um cache em algum banco para melhorar a performance de multiplas consultas
- [x] buscar no cache primeiro **sempre**
- [x] caso não encontre procurar definitivamente na *"receita"*
- [x] verificar se a ultima consulta tem 30 dias de duração se possuir algum registo ou então 
