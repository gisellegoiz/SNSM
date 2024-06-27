<p align="center">
  <img src="banner.png" >
</p>

# SNSM - Smart Network Slicing
<sub>*Bem-vindo(a) à página do código-fonte do projeto de mestrado.</sub>

<div style="text-align: justify;">
A arquitetura baseada em nuvem das redes 5G proporciona maior flexibilidade e agilidade na implantação de novos serviços.
O Third Generation Partnership Project
(3GPP) projetou três principais grupos de serviços:
enhanced Mobile Broadband
(eMBB),
massive Machine Type Communications 
(mMTC) e
Ultra Reliable Low Latency Communications
(URLLC), cada um com um conjunto de aplicações que compõem uma diversificada gama de casos de uso para as redes 5G. Nesse contexto, tecnologias como
Network Functions Virtualization
(NFV) e
Network Slicing
são fundamentais para atender as novas demandas. Enquanto a NFV permite a virtualização das funções de rede, o paradigma do
Network Slicing 
incorpora a divisão lógica dos recursos de rede em fatias, fornecendo tratamento diferenciado a cada fatia. Diante desse cenário, um dos principais desafios trazidos pelas redes 5G está relacionado a alocação eficiente de recursos. Eles devem atender a diferentes requisitos de negócios respeitando os respectivos
Service Level Agreement
(SLAs). Sem um sistema de gerenciamento que forneça a flexibilidade exigida pelas demandas dinâmicas das redes 5G, não é possível alcançar a agilidade e escalabilidade esperadas. Isso reforça a necessidade de sistemas de gerenciamento inteligentes, que prevejam as oscilações de demanda e tenham capacidade para tomada de decisões, com o mínimo de intervenção humana. Em meio a este cenário, a utilização de algoritmos de
Machine Learning
(ML) para o desenvolvimento de sistemas autônomos tem atraído o foco da academia e da indústria, pois pode ser uma tecnologia chave para habilitação plena das redes 5G e além. Em face do exposto, esta dissertação de mestrado apresenta o
Smart Network Slicing Manager
(SNSM), um sistema autônomo para alocação inteligente de recursos. Ele atua complementarmente à camada de orquestração do
Management
and
Orchestration
(MANO), e é capaz de distribuir os recursos de rede, armazenamento e processamento entre as fatias de rede dinamicamente. Para tal, o SNSM dispõe de componentes que empregam algoritmos de ML (supervisionado) para classificar e agrupar os fluxos de rede, de acordo com os padrões de tráfego do respectivo Network Slice. Além disso, o SNSM emprega redes neurais recorrentes para previsões dos recursos computacionais necessários às VNFs dos
Network Slices
. A principal contribuição deste trabalho está na automação do gerenciamento de recursos para compartilhamento eficiente da infraestrutura em ambientes 5G. O modelo Random Forest foi aplicado em dataset contendo fluxos de rede uma rede IP real e obteve acurácia de 98,6% na classificação das aplicações. Além disso, foram aplicadas Redes Neurais Recorrentes do tipo LSTM e GRU para previsão de recursos computacionais, utilizando um dataset com dados reais de um provedor de nuvem. O sistema foi implementado simulando três Network Slices e alocou com sucesso os recursos necessários para atender a cada um deles, mostrando-se uma solução promissora para alocação dinâmica de recursos em ambientes 5G.
</div>
  
**Background in:** Python, Machine Learning, Space Operations and Mathematical Optimisation.

**Links:**
* [Blog](http://sigmoidal.ai)
* [LinkedIn](https://www.linkedin.com/in/carlosfab)
* [Medium](https://www.medium.com)


## Projetos:
Veja os tutoriais publicados do Sigmoidal:

* **Como usar o Histograma para Data Science:** https://bit.ly/2L2cMwy
* **Como Implementar Regressão Linear com Python:** https://bit.ly/2Li5pzY
* **Data Science: Investigando o naufrágio do Titanic:** https://bit.ly/2Ubr5SH
* **Como Tratar Dados Ausentes com Pandas:** https://bit.ly/31KWSMN
* **XGBoost: aprenda este algoritmo de Machine Learning em Python:** https://bit.ly/2UbRhws
* **Como criar uma Wordcloud em Python:** https://bit.ly/2OxsphM
* **Como lidar com dados desbalanceados:** https://bit.ly/2ZlaNsV

---


