<p align="center">
  <img src="banner.png" >
</p>

# Smart Network Slicing (SNSM)
<sub>Projeto de dissertação de mestrado apresentado ao Programa de [Pós-Graduação em Computação ](https://www.ic.uff.br/) da Universidade Federal Fluminense.</sub>
<sub>Orientadora: Profa. [Flavia C. Delicato](https://sites.google.com/view/professorflaviadelicato/home) </sub>
</p>

O **Smart Network Slicing Manager (SNSM)** é um sistema autônomo desenvolvido para alocação inteligente de recursos. Ele atua complementarmente à camada de orquestração do Management and Orchestration (MANO), e é capaz de distribuir os recursos de rede, armazenamento e processamento entre as fatias de rede dinamicamente. Para tal, o SNSM dispõe de componentes que empregam algoritmos de ML (supervisionado) para classificar e agrupar os fluxos de rede, de acordo com os padrões de tráfego do respectivo Network Slice. Além disso, o SNSM emprega redes neurais recorrentes para previsões dos recursos computacionais necessários às VNFs dos Network Slices . A principal contribuição deste trabalho está na automação do gerenciamento de recursos para compartilhamento eficiente da infraestrutura em ambientes 5G. O modelo Random Forest foi aplicado em dataset contendo fluxos de rede uma rede IP real e obteve acurácia de 98,6% na classificação das aplicações. Além disso, foram aplicadas Redes Neurais Recorrentes do tipo LSTM e GRU para previsão de recursos computacionais, utilizando um dataset com dados reais de um provedor de nuvem. O sistema foi implementado simulando três Network Slices e alocou com sucesso os recursos necessários para atender a cada um deles, mostrando-se uma solução promissora para alocação dinâmica de recursos em ambientes 5G.
  
## Arquitetura:
Veja os tutoriais publicados do Sigmoidal:

* **Como usar o Histograma para Data Science:** https://bit.ly/2L2cMwy
* **Como Implementar Regressão Linear com Python:** https://bit.ly/2Li5pzY
* **Data Science: Investigando o naufrágio do Titanic:** https://bit.ly/2Ubr5SH
* **Como Tratar Dados Ausentes com Pandas:** https://bit.ly/31KWSMN
* **XGBoost: aprenda este algoritmo de Machine Learning em Python:** https://bit.ly/2UbRhws
* **Como criar uma Wordcloud em Python:** https://bit.ly/2OxsphM
* **Como lidar com dados desbalanceados:** https://bit.ly/2ZlaNsV


## Código Fonte:
Os códigos foram disponibilizados nos seguintes diretórios:

* **Como usar o Histograma para Data Science:** https://bit.ly/2L2cMwy
* **Como Implementar Regressão Linear com Python:** https://bit.ly/2Li5pzY
* **Data Science: Investigando o naufrágio do Titanic:** https://bit.ly/2Ubr5SH
* **Como Tratar Dados Ausentes com Pandas:** https://bit.ly/31KWSMN
* **XGBoost: aprenda este algoritmo de Machine Learning em Python:** https://bit.ly/2UbRhws
* **Como criar uma Wordcloud em Python:** https://bit.ly/2OxsphM
* **Como lidar com dados desbalanceados:** https://bit.ly/2ZlaNsV

---


