# Projeto de Insights House Rocket

<img src="https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/Logo.png" width=70% height=70% />

## Orientações

O contexto de negócio envolvendo este projeto é fictício. A base de dados foi extraída do [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)

Para visualização do projeto acesse o link:

- [Projeto em Produção com Streamlit e Heroku.](https://analytics-house-rocket-pedro.herokuapp.com/)

## 1.Entendimento do Negócio
House Rocket é uma empresa que atua na compra e venda de imóveis nos EUA. Este projeto foi desenvolvido para auxiliar o time de negócios da empresa.
### 1.1 Problema de Negócio
O time de negócios da empresa recebeu novas metas de desempenho. O time está com dificuldades para cumprir as metas utilizando as ferramentas usuais de trabalho.
### 1.2 Objetivo
Este projeto de insights tem como objetivo auxiliar a tomada de decisão do time de negócios na compra e venda dos imóveis para que as metas possam ser cumpridas.
### 1.3 Demandas de Negócio
Produto de dados solicitado pelo time de negócios:

* Dashboard interativo do portfólio com as informações mais relevantes disponíveis, para que possam ser analisadas e auxiliar na tomada de decisão.

* Respostas para duas questões:
  - 1. Quais são os imóveis que deveríamos comprar?
  - 2. Uma vez o imóvel comprado, qual o melhor momento para vendê-lo, e por qual preço?

## 2.Base de Dados
A base de dados fornecida ao time de dados possui 21613 linhas com as descrições das casas, sendo esses 21 atributos.

Definição dos atributos:

|    Atributos    |                         Significado                          |
| -------------   | ----------------------------------------------------------   |
|       id        |       Numeração única de identificação de cada imóvel        |
|      date       |                    Data da venda da casa                     |
|      price      |    Preço que a casa está sendo vendida pelo proprietário     |
|    bedrooms     |                      Número de quartos                       |
|    bathrooms    | Número de banheiros (0.5 = banheiro em um quarto, mas sem chuveiro) |
|   sqft_living   | Medida (em pés quadrado) do espaço interior dos apartamentos |
|    sqft_lot     |     Medida (em pés quadrado)quadrada do espaço terrestre     |
|     floors      |                 Número de andares do imóvel                  |
|   waterfront    | Variável que indica a presença ou não de vista para água (0 = não e 1 = sim) |
|      view       | Um índice de 0 a 4 que indica a qualidade da vista da propriedade. Varia de 0 a 4, onde: 0 = baixa  4 = alta |
|    condition    | Um índice de 1 a 5 que indica a condição da casa. Varia de 1 a 5, onde: 1 = baixo \|-\| 5 = alta |
|      grade      | Um índice de 1 a 13 que indica a construção e o design do edifício. Varia de 1 a 13, onde: 1-3 = baixo, 7 = médio e 11-13 = alta |
|  sqft_basement  | A metragem quadrada do espaço habitacional interior acima do nível do solo |
|    yr_built     |               Ano de construção de cada imóvel               |
|  yr_renovated   |                Ano de reforma de cada imóvel                 |
|     zipcode     |                         CEP da casa                          |
|       lat       |                           Latitude                           |
|      long       |                          Longitude                           |
| sqft_livining15 | Medida (em pés quadrado) do espaço interno de habitação para os 15 vizinhos mais próximo |
|   sqft_lot15    | Medida (em pés quadrado) dos lotes de terra dos 15 vizinhos mais próximo |

## 3.Premissas do Negócio
1. ID duplicados serão deletados.
2. O nível de construção é considerado bom quando o indicador é superior a 10.
3. A condição do imóvel é considerada boa quando o indicador é maior ou igual a 4.
4. Para definição da compra dos imóvel foram utilizadas duas condições:
   1. O imóvel deve está em boa condição de compra.
   2. O valor de compra do imóvel deve ser menor do que a mediana em relação aos imóveis mais próximos, o CEP foi utilizado como medida de proximidade.
5. Para definição da venda dos imóveis foram utilizadas as seguintes condições:
   1. Se o preço da compra for **maior** do que a mediana da região e sazonalidade. O preço de venda é igual ao preço de compra **+ 10%**.
   2. Se o preço da compra for **menor** do que a mediana da região e sazonalidade. O preço de venda é igual ao preço de compra **+ 30%**.

## 4.Planejamento da Solução
### 4.1 Produto final
* Entrega de um Dashboard interativo que pode ser acessado via navegador, contendo o produto de dados que irá auxiliar o time de negócios na tomada de decisões.

### 4.2 Ferramentas
Ferramentas utilizadas no projeto:
- Jupyter Notebook.
- IDE PyCharm.
- Linguagem Python.

### 4.3 Processo
Etapas para solucionar o problema de negócio:

**1.** Coleta de dados.
**2.** Entendimento do negócio.
**3.** Tratamento e limpeza de dados.
**4.** Exploração de dados.
**5.** Teste de hipóteses do negócio.
**6.** Responder os problemas do negócio.
**7.** Realizar o deploy do produto de dados - Dashboard interativo.

## 5.Resultados da Análise
* Foi realizado um overview dos dados através de um **Histograma** de todas as variáveis para auxiliar a analise prévia e necessidade de criação de novos atributos
![Histograma](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/Histograma_.png)

* Durante a exploração dos dados foi observado a necessidade de criação de **Novas Features** para auxiliar a analise, sendo elas:

| Novas Features | Descrição |
| ----------- | --------- |
| construcao_1955 | Indica se a construcão foi feita antes ou depois de 1955. Para construções a baixo de 1955 o valor é 1, se não o valor é 0.|
| sem_porao | Indica se o imóvel tem porão ou não. Para imóveis com porão o valor é 1 e sem porão o valor é 0. |
| ano_venda | Indica exclusivamente o ano de venda do imóvel. |
| mes | Indica, de forma númeral, cada mês de venda do imóvel |
| estações | Indica as 4 estações do ano, de forma nominal, sendo: primavera entre o mês 3 e 5, verão entre o mês 6 e 8, outono entre o mês 9 e 11, por fim, inverno no mês 12, 1 e 2 |
| boa_condição | Indica a boa condição do imóvel através da coluna condição. Foi definido que um local em boas condições deve ter 4 pontos ou mais na coluna condição, se tiver 3 pontos ou menos, não está em boa condição |
| bom_nivel_construcao | Indica o bom nível de construcão do imóvel através da coluna nivel_construcao. Foi definido que um bom nível de construcão deve ter 10 pontos ou mais na coluna nivel_construcao, se tiver 9 pontos ou menos, não está em um bom nível de construcão |
|reformada | Indica se a construção foi reformada: sendo 1 para foi reformada e 0 para não foi reformada . |

 * **Teste de Hipóteses do Negócio**

| Hipótese | Resultado | Gráfico |
| -------- | --------- | ------- |
| H1: Imóveis que possuem vista para água são pelo menos 30% mais caros, na média. | H1 é verdadeira, pois os imóveis com vista para a água, em média, são 211.76% mais caros. | ![h1](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H1.png) |
| H2: Imóveis com data de construção menor do que 1955, são 50% mais baratos na média. | H2 é falsa, pois os imóveis anteriores a 1955, são em média 1.40% mais caros. | ![h2](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H2.png) |
| H3: Imóveis sem porão possuem área total (sqrt_lot) 50% maiores do que imóveis com 	porões, na média. | H3 é falsa, pois os imóveis sem porão são, em média, -18.56% maiores do que imóveis com porão. | ![h3](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H3.png) |
| H4: O Crescimento do preço dos imóveis YoY (Year over Year) é de 10%, em média. | H4 é falsa, pois o crescimento dos preços dos imóveis YoY, em média, é de 0.05% | ![h4](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H4.png) |
| H5: Imóveis com 3 banheiros tem um crescimento médio no Preço MoM (Month of Month) de 15%. | H5 é falsa, os imóveis não possuem um crescimento MoM de 15%, pois ele prossui uma variação média no período de 0.96% | ![h5](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H5.png) |
| H6: Imóveis que nunca foram reformados (yr_renovated == 0) são em média 20% mais baratos. | H6 é verdadeira, pois os imóveis que não foram reformados são mais baratos, em média,43.29% | ![h6](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H6.png) |
| H7: Pelo menos 80% dos imóveis com condição 4 e 5 tem níveis de construção 7 ou mais. | H7 é verdadeira, pois 8568% dos imóveis estão em boa condição. Sendo o total de imóveis em boa condição: 7332 e os imóveis com nível de construção 7 ou mais: 6282. | ![h7](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H7.png) |
| H8: Pelo menos 80% dos imóveis com vista para água possuem nível de construção 10 ou mais. | H8 é falsa, pois os imóveis com boa condição representam 36.20%. Sendo o total de imóveis em boa condição: 163 e os imóveis com nível de construção 10 ou mais: 59. | ![h8](https://github.com/PedroBezerra1/house_rocket_insights_project/blob/main/image/H8.png) |

## 6.Resultados Financeiros
Após a realização da exploração de dados, considerando as premissas e as questões de negócio, chegamos ao seguintes resultados financeiros:
### Compra
* Selecionados 3.808 imóveis para serem comprados.
* O valor do aporte para aquisição dos imóveis selecionados é de $ 1.498.319.634,00.
* O valor total de economia ao adquirir os imóveis selecionados é de $ 379.336.737,00.

### Venda
Considerado apenas os 3.808 imóveis selecionados para compra.
* A lucratividade total estimada é de $ 437.402.562,50.

## 7.Conclusão
O Objetivo do projeto foi atingido, a entrega do dashboard interativo e as respostas para as questões de negócio, auxiliaram o time de negócios na tomada de decisões corretas, cumprindo as metas e maximizando a lucratividade da empresa.





Neste projeto será definido:
Número de imóveis aptos a serem comprados;
Indicação de quais imóveis devem ser comprados;
Valor do preço de compra;
Valor do preço de venda;
Melhor período para realizar a venda;
Lucratividade da operação.
