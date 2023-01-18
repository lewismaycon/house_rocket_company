# House Rocket Company
###### [Visualizar projeto](https://lewismaycon-house-rocket-company-house-rocket-pf-tgejra.streamlit.app/)

## 1.0 Contexto do Negócio
A House Rocket Company¹ é uma empresa do setor imobiliário que atua principalmente na compra e venda de imóveis, lucrando com a valorização de tais aquisições entre esses períodos.

Pensando em expandir a sua área de atuação, a companhia, que vem recentemente elevando o seu investimento no estado de Washington, decidiu olhar para um condado específico da região, o King County (Condado de King).

Para tomar suas decisões quanto aos potenciais investimentos que possivelmente serão feitos em tal região, a equipe de negócios da empresa optou por contratar um serviço de análise de dados para que tivesse suas decisões orientadas à dados visando concluir se realmente compensaria para o grupo empregar capital nesta área e qual seria a melhor maneira de o fazer.

Foi com esse contexto em mente que o presente projeto foi desenvolvido.
######  ¹ A House Rocket, assim como toda a situação problema, é fictícia, sendo criada apenas para ajudar no contexto de análise de dados do projeto.

## 2.0 Questões do Negócios
Aqui estão as perguntas que o time de negócio da House Rocket pediu para que o time de dados respondesse.

**2.1** Quais são os imóveis que a House Rocket deveria comprar e por qual preço?

**2.2** Uma vez comprados os imóveis, qual o melhor momento para vendê-los e por qual preço?

## 3.0 Dados
A base de dados utilizada no projeto foi retirada do site da [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). A seguir, está uma breve descrição de deste:
|     COLUNA    | DESCRIÇÃO                                                              |
|:-------------:|------------------------------------------------------------------------|
| id            | Identificador único de cada imóvel                                     |
| date          | Data da venda                                                          |
| price         | Preço que foi vendido                                                  |
| bedrooms      | Quantidade de quartos                                                  |
| bathrooms     | Quantidade de banheiros                                                |
| sqft_living   | Área da sala de estar em metros quadrados                              |
| sqft_lot      | Área do lote em metros quadrados                                       |
| floors        | Quantidade de pisos/andares                                            |
| waterfront    | Identificador que informa se o imóvel tem ou não vista para água       |
| view          | Vista do imóvel medida em índice                                       |
| condition     | Condição do imóvel medida em índice                                    |
| grade         | Nota dada ao imóvel baseada no sistema de classificação de King County |
| sqft_above    | Área além do porão medida em metros quadrados                          |
| sqft_basement | Área do porão medida em metros quadrados                               |
| yr_built      | Ano de construção                                                      |
| yr_renovated  | Ano da última reforma feita                                            |
| zipcode       | Código postal                                                          |
| lat           | Latitude                                                               |
| long          | Longitude                                                              |
| sqft_living15 | Área da sala de estar para os quinze vizinhos mais próximos            |
| sqft_lot15    | Área da sala de estar para os quinze vizinhos mais próximos            |

## 4.0 Premissas
**4.1** Para calcular a melhor temporada de venda e o aumento aproximado dos preços do imóveis foi utilizado apenas o histórico presente no dados coletados, que abrange o período de maio de 2014 à maio de 2015. Logo, é possível que os resultados obtidos fossem diferentes caso o período de fosse maior ou menor.

**4.2** Um banheiro completo foi considerado como possuindo uma pia, um vaso sanitário, um choveiro e uma banheira; banheiros que possuem valor igual a 0,75 (¾) foram considerados com uma pia, um vaso sanitário e um choveiro ou uma banheira; e banheiros com valor igual a 0,5 (½) foram considerados banheiros sem choveiro e sem banheira.

**4.3** Um piso com valor igual a 0,5 foi considerado um piso mezanino - “plataforma elevada construída entre o piso e o teto de um edifício ou instalações”².

**4.4** As condições dos imóveis, que variam entre 1 e 5, foram considerados, respectivamente, como “muito ruim”, “ruim”, “média”, “boa” e “muito boa”.

**4.5** Imóveis com o valor de ‘yr_renovated’ igual a 0 foram considerados que não fizeram nenhuma reforma.

**4.6** O imóvel que possui, segundo a base de dados, 33 quartos foi alterado para 3, sendo então considerado um erro de digitação.
###### ² Definição da Mimura Comercial e Serviços Ltda., empresa de engenharia civil.

## 5.0 Planejamento da Solução
**5.1 Produto Final**

Neste ponto, considera-se as respostas para as perguntas feitas e a forma de entregá-las como o produto final, o material criado pelo time de dados para o time de negócio. Assim sendo, o modelo entregável escolhido foi um dashboard com as visualizações necessárias - disponível no link logo ao início deste documento.

**5.2 Ferramentas**
- Python 3.0
- Jupyter Notebook
- Pycharm
- Git e Github
- Streamlit Cloud
- Estatística descritiva

**5.3 Processo**

Aqui estão as formas escolhidas para responder as duas questões solicitadas.

**5.3.1** Quais são os imóveis que a House Rocket deveria comprar e por qual preço?

Para definir que um imóvel está em um bom preço para ser comprado, é necessário ter um preço base para que esse seja comparado. O cálculo escolhido para obter tal valor foi a mediana pois esta, diferente da média, não é afetada por possíveis outliers. Logo, havia uma ponto central onde os preço poderiam ser classificados acima ou abaixo da mesma.

Entretanto, há diversos fatores que podem afetar os preços dos imóveis como a presença ou ausência de porão ou a região onde estão localizados, por exemplo. Dessa forma, técnicas de estatística descritiva e alguma bibliotecas no Python - pandas, numpy, ploty, seaborn, sweetviz e matplotlib - foram utilizadas para definir possíveis filtros que formassem melhor agora não mais uma, mas diversas medianas.

Isto posto, as colunas escolhidas como filtros foram “grade”, “zipcode” e “waterfront”, ou seja, as medianas dos preço foram formadas conforme a região do imóvel, a sua nota de avaliação e o fato de ter ou não vista para água. Em seguida, foram criados quatro possíveis classificações para cada imóvel, sendo estas baseadas também nas condições do mesmo, como visto a seguir:
|    STATUS    |                           DESCRIÇÃO                          |
|:------------:|:------------------------------------------------------------:|
| 1 compra A   | O preço está abaixo da mediana e a condição é 5              |
| 2 compra B   | O preço está abaixo da mediana e a condição é 4              |
| 3 neutro     | O preço está abaixo da mediana e a condição é 3              |
| 4 não compra | O preço está acima da mediana ou a condição está abaixo de 3 |

A classificação “3 neutro” indica que, embora esteja em um bom preço, o imóvel pode necessitar de uma reforma, assim, caberá a equipe de negócios avaliar se esses casos compensariam para a empresa.

Por fim, para representar ainda melhor o potencial de retorno de cada imóvel, foi criada uma coluna “upside” que representa a diferença entre o preço e a mediana, medido em porcentagem. Ou seja, se um imóvel possui 20% de upside, por exemplo, isto significa que seu preço está 20% descolado da mediana, neste caso, para baixo - percentuais negativos significam que está deslocado para cima. Segue um exemplo de como está representada a tabela de compras no dashboard:
|     id     |    data    |  preco | regiao | classificacao | vista_agua | condicao | preco_mediano |   status   | upside |
|:----------:|:----------:|:------:|:------:|:-------------:|:----------:|:--------:|:-------------:|:----------:|:------:|
| 5111400086 | 2014-05-12 | 110000 |  98038 |       6       |      0     |     5    |     222000    | 1 compra A | 50,45% |

**5.3.2** Uma vez comprados os imóveis, qual o melhor momento para vendê-los e por qual preço?

O primeiro passo tomado para definir os preços e o momento de venda foi calcular qual seria a melhor temporada de vendas. Assim, as datas foram agrupadas nas quatros estações do ano conforme o clima dos EUA e foi concluído que a estação mais apropriada é a primavera. Diante disso, também foram calculados os potenciais de valorização para os imóveis dependendo do período em que foi comprado e considerando que este seria vendido na próxima primavera.
| TEMPORADA DA COMPRA | TAXA ESPERADA |
|:-------------------:|:-------------:|
|       Inverno       |     6,50%     |
|        Outono       |     4,00%     |
|        Verão        |     1,00%     |
|      Primavera      |     0,00%     |

Em seguida, a coluna “upside” foi atualizada juntando agora o desconto na compra com o potencial de valorização. Esse, então, seria o potencial mínimo de retorno para cada imóvel. Exemplificando: um imóvel foi comprado com 20% de upside; por ter sido comprado no inverno, este tem um potencial de valorização de aproximadamente 6,50%; logo, a taxa mínima de lucro esperada para este caso é 21,30%.

Dessa forma, têm-se que a primavera é o melhor momento para vender os imóveis e que os preços de vendas serão representados pelo preço de compra acrescido do upside. E, ainda, é importante frisar que esse seria o potencial mínimo, de forma que há espaço para um ganho maior através de estratégias vindas das equipes de negócios e marketing/vendas. Segue um exemplo de como está representada a tabela de vendas  no dashboard:
|     id     | temporada |   status   | preço de compra | preço de venda | upside |  lucro |
|:----------:|:---------:|:----------:|:---------------:|:--------------:|:------:|:------:|
| 5111400086 | primavera | 1 compra A |      110000     |     222000     | 55,45% | 112000 |

## 6.0 Principais Insights
**6.1** Os imóveis com vista para água são cerca de 212% mais caros, na média.

![](/img/6.1.png)

**6.2** A avaliação dos imóveis construídos nas últimas três décadas encontra-se em média cerca de 19% acima da avaliação dos imóveis construídos entre 1900 e 1959, enquanto que há um crescimento médio de 4,7% por década entre as décadas de 1940 e 1990.

![](/img/6.2.png)

**6.3** Para os imóveis construídos após a década de 1960, a condição diminui em média cerca de 4% por década.

![](/img/6.3.png)

**6.4** Para imóveis que possuem entre 1 e 8 quartos, o preço aumenta em média cerca de 20% conforme aumenta-se a quantidade de quartos.

![](/img/6.4.png)

## 7.0 Resultados Financeiros
**7.1 Geral:** aqui temos uma média para todos os imóveis indicados para compra, separados pelo status. Para o status “compra A” a média de retorno do valor investido é de 14,16%, ou um lucro de R$72.943,52 por imóvel, enquanto que o status “compra B” possui 15,58% e R$77.234,78.
|  status  | upside |   lucro  | quantidade |
|:--------:|:------:|:--------:|:----------:|
| compra A | 14,16% | 72943,52 |     468    |
| compra B | 15,58% | 77234,78 |    2562    |

**7.2 Primeira situação:** caso sejam comprados os 100 imóveis com os maiores upsides da classe “compra A”.
|    DESCRIÇÃO   |       VALOR      |
|:--------------:|:----------------:|
| total comprado | R$ 42.406.468,00 |
| total vendido  | R$ 59.602.194,61 |
| lucro total    | R$ 17.195.726,61 |
| lucro médio    |    R$ 171.957,26 |
| upside médio   |      29,26%      |

**7.3 Segunda situação:** caso sejam comprados os 100 imóveis com os maiores upsides da classe “compra B”.
|    DESCRIÇÃO   |       VALOR      |
|:--------------:|:----------------:|
| total comprado | R$ 27.914.065,00 |
| total vendido  | R$ 48.822.994,28 |
| lucro total    | R$ 20.908.929,28 |
| lucro médio    |    R$ 209.089,29 |
| upside médio   |      43,19%      |

**7.4 Terceira situação:** caso sejam comprados os 100 imóveis com os maiores upsides independente da classe.
|    DESCRIÇÃO   |       VALOR      |
|:--------------:|:----------------:|
| total comprado | R$ 28.044.880,00 |
| total vendido  | R$ 49.588.267,98 |
| lucro total    | R$ 21.543.387,98 |
| lucro médio    |    R$ 215.433,87 |
| upside médio   |      43,89%      |

**7.5 Quarta situação:** caso sejam comprados os 50 imóveis com os maiores upsides da classe “compra A” e os 50 com os maiores upsides da classe “compra B”.
|    DESCRIÇÃO   |       VALOR      |
|:--------------:|:----------------:|
| total comprado | R$ 30.448.798,00 |
| total vendido  | R$ 51.000.491,98 |
| lucro total    | R$ 20.551.693,98 |
| lucro médio    |    R$ 205.516,93 |
| upside médio   |      41,02%      |

## 8.0 Conclusão
Diante do desafio apresentado, o presente projeto se torna mais um exemplo da importância do uso de dados para auxiliar em tomadas de decisões dos diferentes times dentro de uma empresa, principalmente do time de negócios. Também foi mostrado como, além das ferramentas usuais de tecnologia e estatística, o conhecimento vindo das mais diversas áreas pode impactar a qualidade da análise dos dados, as várias formas possíveis de responder as duas questões propostas representa muito essa diversidade de ideias.

Além disso, a geração de insights pode fazer com que a equipe de negócios faça novas perguntas ou até mesmo novas análises em cima de dados diferentes gerando cada vez mais sinergia entre o negócio e a análise de dados.

Ademais, este projeto segue uma forma cíclica de construção, de modo que há sempre possíveis próximos passos para caso uma futura nova versão seja feita.

## 9.0 Próximos Passos
- Aumentar a quantidade de tempo abrangida nos cálculos de retorno esperado por estação para que se possa ter um valor mais real, possivelmente também incluindo índices de inflação, taxa de juros e outras informações importantes.
- Adicionar aos cálculos de lucros estratégias de negociação e vendas de forma a aumentar a taxa de retorno dos investimentos para que esta não fique limitada a uma taxa mínima.
