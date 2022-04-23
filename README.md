# House Rockets Analise de Dados

O conjunto de dados que representam o contexto está disponível na plataforma do Kaggle.
Esse é o link: https://www.kaggle.com/harlfoxem/housesalesprediction

## 1. Questão de negócio
A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita.  Entretanto, O time do negócio não consegue tomar boas decisões de compra sem analisar os dados e o portfólio é muito grande levaria muito tempo para fazer o trabalho manualmente. Logo, o objetivo foi encontrar as melhores oportunidades de compra de imóveis do portfólio da House Rocket através de uma análise com Python. Para isso, foi necessário responder duas questões:
#### 1. Quais são os imóveis que a House Rocket deveria comprar?
#### 2. Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço ?

## 2. Premissas
- Imóveis que deveriam ser comprados => imóveis com valor menor que a mediana da região, condição >=3 e nota >= 8.
- Mehor época do ano para vender => Quando o mercado está aquecido, ou seja, a média de preços está maior.
- Região e época do ano são fatores determinantes no preço.


## 3. Planejamento
- Primeira Questão:
	 - Agrupar os imóveis por região( zipcode ).
	 - Dentro de cada região, encontrar a mediana do preço do imóvel.
 	- Sugerir os imóveis que estão abaixo do preço mediano da região, estejam em boas condições e com nota alta.
- Segunda Questão:
	 - Agrupar os imóveis por mês e calcular a média de preço para saber a melhor época para vender
 	- Depois, para descobrir um bom preço de venda, agrupar os imóveis por região( zipcode ) e época do ano (mês).
	 - Dentro de cada região e época do ano, encontrar a mediana do preço.
	 - Condições de venda:
		1. Se o preço da compra for maior que a mediana da região + época, o preço da venda será igual ao preço da compra + 10%
		2. Se o preço da compra for menor que a mediana da região + época, o preço da venda será igual ao preço da compra + 30%


## Insights
O coeficiente de Pearson, mede o grau de correlação através do cálculo de direção positiva ou negativa. Este coeficiente, normalmente representado por ρ assume apenas valores entre -1 e 1. Como podemos interpretar os valores que ρ pode assumir?
- ρ = 0,9 a 1 (positivo ou negativo): correlação muito forte;
- ρ = 0,7 a 09 (positivo ou negativo): correlação forte;
- ρ = 0,5 a 0,7 (positivo ou negativo): correlação moderada;
- ρ = 0,3 a 0,5 (positivo ou negativo): correlação fraca;
- ρ = 0 a 0,3 (positivo ou negativo): não possui correlação.

De acordo com o coeficiente, os fatores que mais influenciam no PREÇO da casa são: 
- 1º. Square Foot Living area (área de convívio da casa) - 0.702079 (Forte)
- 2º. Nota - 0.667509 (Moderada)
- 3º. Square Foot Above (área de vivência acima do nível do chão) - 0.605611 (Moderado)


## 5. Resultado Financeiro
Se a empresa seguir a recomendação, comprar e revender os imóveis pelos preços sugeridos, o faturmaneto previsto será de U$ 425.699.441


## 6. Conclusão
Foram criados dois arquivos (Best_Houses.csv; Best_Houses_and_Prices.csv) com as recomendações de imóveis, um com recomendações de compra e outro com recomendações de compra + preço de venda. Além disso, um app foi criado a partir do Streamlit e Heroku para permitir uma visualização de dados interativa e instantânea. Esse é o link: https://analytics-house-rocket-web.herokuapp.com/	
