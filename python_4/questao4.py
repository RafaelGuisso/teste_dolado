import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import ast
import seaborn as sns

# Criei uma função que pode ser utilizada para pesquisar qualquer produto desejado no Mercado Livre

def obter_resultados_busca(termo_pesquisa):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo_pesquisa}"
    response = requests.get(url)
    return response.json()

def salvar_resultados_em_csv(resultados, termo_pesquisa, nome_arquivo):
    dataframe = pd.json_normalize(resultados['results'])
    dataframe['Termo_Pesquisa'] = termo_pesquisa 
    dataframe.to_csv(nome_arquivo, index=False, encoding='utf-8')

if __name__ == "__main__":
    termo_de_pesquisa = input("Digite o termo de pesquisa: ")
    resultados = obter_resultados_busca(termo_de_pesquisa)

    print("Resposta completa da API:")
    print(pd.json_normalize(resultados['results']).to_string(index=False)) 

    salvar_resultados_em_csv(resultados, termo_de_pesquisa, 'dados_brutos.csv')
    print("Dados brutos salvos em 'dados_brutos.csv'.")


df = pd.read_csv('dados_brutos.csv')

# A ideia inicial foi de puxar o data frame do API e salvar no formato CSV para permitir uma melhor visualização dos dados
# A visualização foi dos dados foi necessária para que fosse possivel pensar qual direção era melhor seguir

# De maneira geral o dataset é composto de 50 produtos (valor default da API) e possui MUITAS colunas, várias delas vazias ou com informações pouco relevantes
# Minha ideia inicial era de remover algumas dessas colunas, mas depois de alguns testes ficou claro que era melhor criar um dataframe novo contendo apenas oque era relevante

colunas_importantes = ['id', 'title', 'condition', 'price', 'original_price', 'available_quantity', 'attributes', 'shipping.free_shipping', 
                       'seller.nickname', 'shipping.logistic_type', 'installments.quantity', 'installments.amount', 'installments.rate']

try:
    df_novo = df[colunas_importantes].copy()
    print("DataFrame 'df_novo' criado com sucesso.")
except KeyError as e:
    print(f"Algumas colunas não existem no DataFrame original: {str(e)}")
    print("Criando DataFrame 'df_novo' sem essas colunas.")
    colunas_importantes = [
        'id', 'title', 'condition', 'price', 'original_price',
        'available_quantity', 'attributes', 'shipping.free_shipping',
        'seller.nickname', 'shipping.logistic_type'
    ]
    df_novo = df[colunas_importantes].copy()

if df_novo.empty:
    print("O DataFrame 'df_novo' está vazio.")

# Coloquei um try/except porque algumas pesquisas como "carro" não vão apresentar as colunas referentes a parcelamento
# Mesmo sem essas colunas eu quero que o dataframe seja criado e posteriormente analisado

# Após analisar com maior cuidado a coluna "attributes" percebi que ela contém informações potencialmente importantes
# Mas que essas informações variam de produto para produto
# Se eu fosse fazer uma análise mais aprofundada de um produto especifico, eu poderia pegar tamanho, cor, infantil ou adulto, modelo masculino ou feminino, etc...
# Para fazer uma análise mais geral, decidi pegar um atributo que parece existir em todos produtos que eu pesquisei: BRAND

print(df_novo['attributes'].dtype)

# Como o tipo da variavel de 'attributes' deu object, tenho que transformar em string para utiliza-la

df_novo['attributes'] = df_novo['attributes'].astype(str)
df_novo['attributes'] = df_novo['attributes'].apply(ast.literal_eval)

# Função para extrair o 'value_name' quando 'id' é igual a 'BRAND'
def extrair_brand(attributes):
    for attribute in attributes:
        if attribute['id'] == 'BRAND':
            return attribute['value_name']
    return None

# Aplicar a função à coluna 'attributes' para criar uma nova coluna 'brand'
df_novo['brand'] = df_novo['attributes'].apply(extrair_brand)

df_limpo = df_novo.drop(columns=["attributes"])
print(df_limpo)
df_limpo.to_csv('df_limpo.csv', index=False, encoding='utf-8')

# Agora que os dados estão tratados, tenho que pensar que tipo de análise é possível fazer com os dados obtidos.

brand = df_limpo['brand']
contagem = df_limpo['brand'].value_counts()


df_prices = pd.DataFrame({'brand': contagem.index, 'contagem': contagem.values})


average_prices = df_prices.groupby('brand')['contagem'].mean()
average_prices = average_prices.sort_values(ascending=True)

# Plotar um gráfico de barras para a média de contagem por marca
plt.figure(figsize=(10, 6))
bar_plot = average_prices.plot(kind='barh', edgecolor='black', color=['lightblue'])
plt.xlabel('Contagem')
plt.ylabel('Marca')
plt.title('Gráfico 1 - Contagem por Marca')
plt.grid(axis='x')

# Fazendo o Gráfico 2

for container in bar_plot.containers:
    bar_plot.bar_label(container, label_type='edge', color='black', fontsize=9)

plt.show()

brand = df_limpo['brand']
price = df_limpo['price']

df_prices = pd.DataFrame({'brand': brand, 'price': price})
average_prices = df_prices.groupby('brand')['price'].mean()
average_prices = average_prices.sort_values(ascending=False)

plt.figure(figsize=(10, 6))
average_prices.plot(kind='bar', edgecolor='black', color=['lightgreen'])
plt.xlabel('Marca')
plt.ylabel('Preço Médio')
plt.title('Gráfico 2 - Média de Preço por Marca (Ordem Descendente)')
plt.xticks(rotation=90)
plt.grid(axis='y')

plt.show()

# Fazendo o Gráfico 3

contagem_true_false = df_limpo['shipping.free_shipping'].value_counts()
rotulos_personalizados = {True: 'Gratis', False: 'Pago'}
df_limpo['shipping.free_shipping'] = df_limpo['shipping.free_shipping'].map(rotulos_personalizados)


contagem_true_false = df_limpo['shipping.free_shipping'].value_counts()


cores_personalizadas = {'Gratis': 'skyblue', 'Pago': 'lightcoral'}
plt.figure(figsize=(8, 8))
plt.pie(contagem_true_false, labels=contagem_true_false.index, autopct='%1.1f%%', startangle=90, colors=[cores_personalizadas[label] for label in contagem_true_false.index])
plt.title('Tabela 3 - Distribuição de Frete')
plt.show()

# Fazendo o Gráfico 4

media_gratis = 0
media_pago = 0

media_gratis = df_limpo.loc[df_limpo['shipping.free_shipping'] == 'Gratis', 'price'].mean()
media_pago = df_limpo.loc[df_limpo['shipping.free_shipping'] == 'Pago', 'price'].mean()

print("Soma dos itens com frete grátis:", media_gratis)
print("Soma dos itens com frete pago:", media_pago)

categorias = ['Frete Grátis', 'Frete Pago']
medias = [media_gratis, media_pago]

cores_personalizadas = {'Gratis': 'skyblue', 'Pago': 'lightcoral'}
plt.bar(categorias, medias, color=[cores_personalizadas[label] for label in contagem_true_false.index])
plt.ylabel('Média de Preço')
plt.title('Gráfico 4 - Média de Preço por Tipo de Frete')
plt.show()

# A ideia de fazer esses dois últimos gráfico era de análisar se haveria alguma diferença no preço médio dos produtos com frete grátis e pago.
# Foi possível perceber que quando comparados os preços médios dos produtros com frete pago e grátis, geralmente os produtos com frete grátis são mais caros
# De fato, para produtos de ticket médio maior (celular, video game, drone...), o frete costuma ser gratis.

# Gráfico 5

plt.figure(figsize=(12, 8))
sns.boxplot(x='installments.quantity', y='price', data=df_limpo)
plt.title('Gráfico 5 - Boxplot de Preço por Número de Parcelas')
plt.xlabel('Parcelas')
plt.ylabel('Preço')
plt.show()

# Aqui uma análise em boxplot para analizar se existe uma relação entre preço do produto e até quantas parcelas são aceitas
# De maneira geral, existe uma relação direta entre o preço do produto e o número de parcelas
# Quanto mais caro o produto, maior tende a ser o número de parcelas aceitas para o pagamento

# Gráfico 6

contagem_estoque = df_limpo['available_quantity'].value_counts().sort_values(ascending=True)

plt.figure(figsize=(10, 6))
bar_plot = contagem_estoque.plot(kind='barh', edgecolor='black', color=['mediumseagreen'])
plt.xlabel('Frequência')
plt.ylabel('Estoque')
plt.title('Gráfico 6 - Contagem Estoque')
plt.grid(axis='x')

for container in bar_plot.containers:
    bar_plot.bar_label(container, label_type='edge', color='black', fontsize=9)

plt.show()

# Na análise de estoque eu optei por utilizar a frequencia em que certa quantidade de estoque se repetiu
# Por algum motivo o valor que parece repetir mais vezes é 1, e os demais valores encontrados geralmente são valores redondos como 100, 500 ou 1000
# Provavelmente indicando que o vendedor coloca um valor inicial de estoque quando anuncia um produto e esse valor não é decrescido quando ocorrem vendas
# (Acredito que para evitar que o anúncio da venda caia automáticamente quando o estoque inicial chegue a zero)
# De qualquer forma, os valores citados muito provavelmente não refletem os valores reais de estoque 


# Conclusão:
# O preço do produto impacta fortemente no número de parcelas aceitas e na probabilidade de o frete ser grátis.
# Com isso é possível dizer que em geral um produto barato vai ser parcelado em poucas parcelas e vai ter frete pago
# Enquanto que um produto mais caro vai ter mais parcelas e frete grátis, podemos deduzir que o preço do frete já esta imbutido no preço do produto
# Os valores de estoque geralmente é 1 ou valores redondos como 100, 500, 1000
# Provavelmente indicando que o vendedor coloca um valor inicial de estoque quando anuncia um produto e esse valor não é decrescido quando ocorrem vendas
# Acredito que para evitar que o anúncio da venda caia automáticamente quando o estoque inicial chegue a zero
# Mas, colocar o estoque como 1 pode ser uma tática para gerar um gatilho de escassez falsa e gerar compras por impulso

