# INSTRUÇÕES

A pastas contem uma versão do arquivo em .py (Python) e um em .ipynb(Jupyter). Qualquer uma das duas pode ser utilizada.
Ao ser rodado o codigo vai pedir que o nome de um produto seja escrito no terminal, as analytics vão ser geradas de acordo com dados do produto digitado.
Além disso, dois arquivos csv estão presentes aqui também:
dados_brutos.csv e df_limpo.csv
O primeiro contém os dados em seu estado bruto após a extração do API eo segundo contém os dados após o tratamento.
Para a visualização do banco de dados é melhor abrir diretamente os arquivos csv.

# DATASET

O dataset vai variar de acordo com o produto que for pesquisado quando o programa rodar.
De maneira geral, o dataframe vai possuir 50 linhas e mais de 50 colunas. Que precisam ser tratados, são muitas colunas vazias ou com informações pouco relevantes.
Optei por criar um data frame novo, contendo apenas as colunas importantes para a análise.
A eles adicinonei a coluna 'BRAND' com informações obtidas da coluna 'attributes' que contem um dicionario com varias informações sobre os produtos.


# ANÁLISE EXPLORATIVA DOS DADOS

As análises a seguir foram feitas com o dataframe obtido com o termo de pesquisa "cofre"
De mãos nos dados tratados foi possível fazer algumas análises:

Primeiro observar a contagem de produtos por marca

![grafico1](https://github.com/RafaelGuisso/teste_dolado/assets/108840079/07c6e2de-1849-4651-b2be-abe57331617a)


Em seguida uma análise dos preços médios dos produtos para cada marca:

![grafico2](https://github.com/RafaelGuisso/teste_dolado/assets/108840079/2bb68e43-b2be-4c32-a014-54f1d581be5d)

Em seguida foi feita análise de quantos produtos tem frete grátis e frete pago:

![grafico3](https://github.com/RafaelGuisso/teste_dolado/assets/108840079/6147f05f-01c3-40c1-a30f-89885e0b7d3c)

Para auxiliar nessa análise foi feito também o gráfico 4 que contém o preço médio dos produtos com frete grátis e frete pago

![grafico4](https://github.com/RafaelGuisso/teste_dolado/assets/108840079/98819cd0-a90f-4964-9a23-8bf03706ba4e)

Foi possível perceber que quando comparados os preços médios dos produtros com frete pago e grátis, geralmente os produtos com frete grátis são mais caros
De fato, para produtos de ticket médio maior (celular, video game, drone...), o frete costuma ser grátis.

Em seguida foi feito o gráfico 5, que contém um um boxplot comparando o número de parcelas com o preço dos produtos.

![grafico5](https://github.com/RafaelGuisso/teste_dolado/assets/108840079/37db32d5-2fda-4c0c-aeca-2e5597c70c22)

De maneira geral, existe uma relação direta entre o preço do produto e o número de parcelas
Quanto mais caro o produto, maior tende a ser o número de parcelas aceitas para o pagamento

Por ultimo o Gráfico 6 contém a contagem de estoque dos produtos.

![grafico6](https://github.com/RafaelGuisso/teste_dolado/assets/108840079/68da1f20-bbf5-4adc-a4c1-412ae61c169b)


Por algum motivo o valor que parece repetir mais vezes é 1, e os demais valores encontrados geralmente são valores redondos como 100, 500 ou 1000.
Provavelmente indicando que o vendedor coloca um valor inicial de estoque quando anuncia um produto e esse valor não é decrescido quando ocorrem vendas.
De qualquer forma, os valores citados muito provavelmente não refletem os valores reais de estoque.

# CONCLUSÃO

O preço do produto impacta fortemente no número de parcelas aceitas e na probabilidade de o frete ser grátis.
Com isso é possível dizer que em geral um produto barato vai ser parcelado em poucas parcelas e vai ter frete pago.
Enquanto que um produto mais caro vai ter mais parcelas e frete grátis, podemos deduzir que o preço do frete já esta imbutido no preço do produto.
Os valores de estoque geralmente é 1 ou valores redondos como 100, 500, 1000.
Provavelmente indicando que o vendedor coloca um valor inicial de estoque quando anuncia um produto e esse valor não é decrescido quando ocorrem vendas.
Acredito que para evitar que o anúncio da venda caia automáticamente quando o estoque inicial chegue a zero.
Mas, colocar o estoque como 1 pode ser uma tática para gerar um gatilho de escassez falsa e gerar compras por impulso.



