# Importar bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import pmdarima as pm

from keras.models import Sequential
from keras.layers import LSTM, Dense
from plotly.subplots import make_subplots
from prophet import Prophet
from prophet.plot import plot_plotly
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf, adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error, mean_squared_error,accuracy_score
from sklearn.preprocessing import MinMaxScaler

from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.stattools import adfuller

import pickle

from utils import (normality_test, 
                   create_warning, 
                   create_quote, 
                   create_curiosity, 
                   create_insight, 
                   create_analysis, 
                   insert_image)

# layout
st.set_page_config(layout='centered', 
                   page_title='ONG PASSOS MÁGICOS', 
                   page_icon='⚡', initial_sidebar_state='auto')

# paginação
page_0 = 'Introdução'
page_1 = 'Análise'
page_2 = 'Modelos'
page_3 = 'Conclusão'
page_4 = 'Referências'

# menu lateral
st.sidebar.title('Menu')
page = st.sidebar.radio('Selecione a página:', 
                        [page_0, page_1, page_2, page_3, page_4])
     
# Introdução
if page == page_0:
    
    # título da página
    st.title('Impacto')
    
    # descrição
    st.markdown('''
                Modelos de forecasting para o preço diário do petróleo Brent (U$D ), 
                <br>desenvolvido para a <b>Pós-Tech Data Analytics — FIAP</b>, em Março-Maio de 2024.
                <br><br>
                Comparação entre os modelos <b>XGBoost</b> e <b>Prophet</b>.
                ''', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    
    create_warning('Importante', 
                   '''
                        Este artigo tem fins exclusivamente educacionais 
                        e não se trata de recomendação para investimento de qualquer natureza.
                    ''')
    
    st.markdown('<br>', unsafe_allow_html=True)

    # expansão com nota técnica
    with st.expander('🗒️ Nota Técnica'):
        st.markdown('''
        #### Dados do projeto

        **🚀 Objetivo**: prever o preço do petróleo Brent (U$D ) para o próximo dia.

        ---
        
        **🛸 Modelos**: os dados utilizados para análise e treinamento no modelo foram coletados em 18/05/2024 e correspondem ao período de 20/05/1987 a 13/05/2024.
        - [XGBoost](https://xgboost.readthedocs.io/en/stable/)
        - [Prophet](https://facebook.github.io/prophet/)

        ---
        
        **📡 Fontes de dados**:
        - [IPEA](http://www.ipeadata.gov.br/Default.aspx)
        - [FRED](https://fred.stlouisfed.org/series/DCOILBRENTEU)
        - [Yahoo Finance](https://finance.yahoo.com/quote/CL=F?p=CL=F)

        ---
        
        **🧑🏻‍🚀 Autor**: 
        - [Vinícius Prado Lima](https://www.linkedin.com/in/viniplima/)

        ---
        
        **🪐 Repositório**: 
        - [GitHub](https://github.com/euvina/brent_oil_price_forecasting)

        ---
        
        ''')
    
    st.markdown('---')
    
    # contexto para o objeto de estado
    st.markdown('## O Petróleo')
    
    st.markdown('''
                <p style="font-size: 18px">
                A palavra “petróleo” é originária do latim, a partir dos termos <i>“petra”</i> e <i>“oleum”</i> - 
                que significam “óleo de pedra”.<br>
                Esse óleo bruto é composto, principalmente, por hidrocarbonetos, e resultante de um processo de transformação 
                que ocorre ao longo de milhares de anos, em bacias sedimentares.
                </p>
                ''', unsafe_allow_html=True)  
    
    create_quote('''
                O petróleo começa com a formação das bacias sedimentares, 
                cujo requisito básico é a disponibilidade de área para a acumulação de sedimentos 
                (material desagregado e transportado por rios, geleiras, vento e mar). 
                A Terra possui sete grandes placas tectônicas e algumas microplacas. 
                Seu movimento ao longo da história geológica é responsável pela formação das 
                principais bacias sedimentares (espaços que abrigam sedimentos) em todo o mundo. 
                Elas ocorrem tanto em terra quanto nos oceanos.
                ''', 
                'Nos Bastidores da Terra - Superinteressante', 
                'https://super.abril.com.br/coluna/deriva-continental/nos-bastidores-da-terra-geologa-explica-a-formacao-do-petroleo')
    
    
    st.markdown('''
                <p style="font-size: 18px">
                Vestígios de matéria orgânica em decomposição - principalmente algas e plânctons - 
                se acumulam no fundo de corpos de água, como mares e lagos. 
                Esses restos são cobertos por camadas de sedimentos que exercem cada vez mais pressão e, 
                dado o calor ao longo do tempo, ocorre a formação do petróleo. Esse processo é extremamente lento 
                e, por isso, o petróleo é considerado um <b>recurso não renovável</b>.<br><br>
                ''' , unsafe_allow_html=True)
    
    insert_image(image_path = r'img/bacias_sedimentares_revista_superinteressante.webp',
                 source = 'https://super.abril.com.br/coluna/deriva-continental/nos-bastidores-da-terra-geologa-explica-a-formacao-do-petroleo',
                 caption = 'Processo de formação do petróleo nas bacias sedimentares - Revista Superinteressante')
                  
    st.markdown('''
                <p style="font-size: 18px"><br>
                    Estudos geofísicos aéreos e terrestres são realizados para 
                    a identificação de bacias sedimentares com maiores chances de encontrar petróleo.
                    A profundidade dos poços de petróleo em áreas terrestres (<i>onshore</i>) varia, em média, 
                    entre 1.500 e 3.000 metros. Já em áreas no mar (<i>offshore</i>), pode atingir até 10.000 metros. 
                    Portanto, a extração do petróleo em terra firme é diferente da exploração em mar - 
                    e ambos os procedimentos são complexos.<br>
                    <b>80 milhões de barris</b> de petróleo são extraídos por dia em todo o mundo, 
                    onde cada barril contém <b>159 litros</b> de petróleo.</b><br><br>
                </p>
                ''', unsafe_allow_html=True)
    
    create_warning(' Perigo',
            '''
            Os meios de exploração do petróleo, bem como a queima constante, são altamente danosos ao meio ambiente.
            A extração de petróleo é uma atividade que emite gases de efeito estufa, contribuindo para o aquecimento global.
            Também, o derramamento de petróleo no mar causa uma série de prejuízos ao ecossistema marinho, afetando a vida existente naquele local.
            Esses fatos reforçam a necessidade de investimento em fontes de energia limpa e renovável.
            ''')  

# Análise
elif page == page_1:
    # carregar dados
    data = pd.read_parquet(r'data/data_w_indicators.parquet')
    # sidebar - adicionar filtros
    st.sidebar.title('⚙️ Filtros')
    # filtros de ano com slider
    min_year = data.index.year.min()
    min_year = int(min_year)
    max_year = data.index.year.max()
    max_year = int(max_year)
    # filtro de preço com slider
    min_price = data['brent'].min()
    min_price = int(min_price)
    max_price = data['brent'].max()
    max_price = int(max_price)

    year_slider = st.sidebar.slider('Ano', min_year, max_year, (min_year, max_year))
    price_slider = st.sidebar.slider('Preço (U$D )', min_price, max_price, (min_price, max_price))
    # título da página
    st.title('Análise sobre o petróleo Brent')
    # texto sobre o petróleo Brent
    st.markdown('''
                <br>
                    <p style="font-size: 18px">
                    <b style = "font-size: 22px">O petróleo Brent</b> é uma classificação de petróleo extraído do Mar do Norte. 
                    Assim como o petróleo West Texas Intermediate (WTI), 
                    o petróleo Brent é um dos principais tipos de petróleo cru negociados no mercado internacional. 
                    Ambos são usados como referência para o preço do petróleo em todo o mundo e 
                    amplamente negociados em <b>mercados de futuros</b>.<br><br>
                    </p>
                ''', unsafe_allow_html=True)
                    
    create_curiosity('Mercado Futuro', 
                    '''
                    Onde são negociados contratos de compra ou venda de um ativo em uma data futura.<br>
                    O petróleo é negociado primeiro em mercados de futuros e, em seguida, 
                    esses contrados são comercializados em bolsas de <i>commodities</i>, 
                    como a Intercontinental Exchange (ICE) em Londres.
                    ''')
    
    st.markdown('''
                <p style="font-size: 18px">
                <br><br>
                    O preço do petróleo é regulado pela Organização dos Países Exportadores de Petróleo (OPEP) ou, 
                    em inglês, Organization of the Petroleum Exporting Countries (OPEC) - 
                    um cartel intergovernamental de 13 nações, fundado em 15 de setembro de 1960.
                    O preço sofre influência de fatores como a produção e o transporte, 
                    a demanda por produtos petrolíferos e a especulação do mercado.
                    A unidade de medida dada para transações é geralmente dólares americanos por barril. 
                    O gráfico a seguir mostra a evolução do preço do petróleo Brent ao longo dos anos:
                </p>
                ''', unsafe_allow_html=True)
    

    df = data.loc[(data.index.year >= year_slider[0]) & (data.index.year <= year_slider[1]) & 
                  (data['brent'] >= price_slider[0]) & (data['brent'] <= price_slider[1])]
    # gráfico com plotly para brent
    fig = px.line(df, x=df.index, y='brent', 
                  title='Preço do petróleo Brent - Fechamento diário',
                  labels={'brent': 'Preço (U$D )', 'date': 'Data'},                      
                  color_discrete_sequence=['#4089FF'],
                  template='plotly_dark')
    fig.update_layout(title_font_size=20) 
    fig.update_xaxes(title=None)
    fig.update_yaxes(range=[0, df['brent'].max() * 1.1])
    st.plotly_chart(fig, use_container_width=True)
    
    create_quote('''
                    Desde 1973, a posição da OPEP sempre foi a de desacelerar a produção – 
                    através de uma política de cotas para cada país-membro – 
                    quando surgiam sinais de queda nos preços, 
                    de modo a diminuir a oferta e reequilibrar as cotações.
                    ''', 
                    'Os limites do preço do petróleo - IPEA', 
                    'https://desafios.ipea.gov.br/index.php?option=com_content&view=article&id=3261&catid=28&Itemid=39')
    
    st.markdown('''
            <br>
                <p style="font-size: 18px">
                Ao longo dos 37 anos de registro, o valor do dinheiro teve grandes alterações. Também, 
                mudou o comportamento do mercado e a tecnologia evoluiu. Sem levar em conta tais componentes,
                ainda é possível enxergar, no gráfico acima, o efeito de marcos importantes:<br>
                <br>
                - A mínima do período data de 10 de Dezembro de 1998, com preço equivalente a U$D 9.10.<br>
                - A segunda menor mínima ocorreu na Pandemia de COVID-19, em 21 de Abril de 2020, com preço em U$D 9.12.<br>
                - Em 2008, o preço do barril de petróleo Brent atingiu o valor recorde de U$D 143.95. Com a grande recessão, 
                o preço caiu para U$D 33.73 no mesmo ano. A variação agressiva foi de -326.78%.<br>
                - As guerras entre EUA e Iraque (2003) e entre Rússia e Ucrânia (2022) 
                também impactaram diretamente no preço do petróleo - por questões de oferta e demanda, 
                dificuldades na produção e circulação de mercadorias, além da especulação do mercado.</b>
                <br><br>
                </p>
            ''', unsafe_allow_html=True)

    create_insight('Volatilidade', 
                   '''
                        Acompanhar fatos históricos e incorporá-los no treinamento do modelo é essencial. 
                        No entanto, cada novo evento pode gerar diferentes e imprevisíveis impactos no preços dos ativos.
                    ''')
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # gráfico boxplot
    fig = px.box(df, x=df.index.year, y='brent', 
                title='Volatilidade anual no preço do Brent', 
                labels={'value': 'U$D '}, template='plotly_dark',
                color_discrete_sequence=['#4089FF'])
    fig.update_layout(title_font_size=20)
    fig.update_xaxes(title=None)
    fig.update_yaxes(range=[0, df['brent'].max() * 1.1])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('---')
    
    st.title('Análise de Série Temporal')
            
    # diferenciação e variação percentual
    st.markdown('''
                <br>
                    <p style="font-size: 18px">
                    <b>Diferenciar</b> uma série temporal é importante por diversos motivos, como:<br>
                    - Estacionariedade: a média e a variância são constantes ao longo do tempo.<br>
                    - Sazonalidade: permite minimizar ciclos que se repetem em intervalos regulares.<br>
                    - Tendência: ajuda a remover tendências para facilitar a modelagem.
                    <br><br>
                    </p>
                ''', unsafe_allow_html=True)
    
    # código para diferença
    with st.expander('🐍 Exibir código Python'):
        st.code('''
                # diferenciar série temporal
                df['brent_diff'] = df['brent'].diff()
                # variação percentual
                df['brent_pct'] = df['brent'].pct_change() * 100
                ''')   

    # same chart with make_sublots and y lower lim = 0
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=['Original', 'Diferença', 'Variação (%)'])
    # original
    fig.add_trace(go.Scatter(x=df.index, y=df['brent'], name='Original',
                            line=dict(color='#4089FF')), row=1, col=1)
    # diferença
    fig.add_trace(go.Scatter(x=df.index, y=df['brent_diff'], name='Diferença',
                            line=dict(color='#4089FF')), row=2, col=1)
    # variação percentual
    fig.add_trace(go.Scatter(x=df.index, y=df['brent_pct'], name='Variação (%)',
                            line=dict(color='#4089FF')), row=3, col=1)
    
    # atualizar layout
    fig.update_layout(title='Preço do Petróleo Brent - Original, Diferença e Variação (%)',
                    title_font_size=20, showlegend=False, template='plotly_dark',
                    hovermode='x unified', height=600)
    fig.update_yaxes(range=[0, df['brent'].max() * 1.1], row=1, col=1)
    fig.update_yaxes(range=[-20, 20], row=2, col=1)
    fig.update_yaxes(range=[-60, 60], row=3, col=1)
    fig.update_xaxes(title='')
    st.plotly_chart(fig, use_container_width=True)
    
    
    # teste de estacionariedade
    st.markdown('''
                <p style="font-size: 18px">
                Com o teste estatístico de Dickey-Fuller, podemos verificar se a série temporal é estacionária.<br>
                - <b>Hipótese nula (H0)</b>: a série temporal não é estacionária.<br>
                - <b>Hipótese alternativa (H1)</b>: a série temporal é estacionária.<br>
                <br>
                ''', unsafe_allow_html=True)

    with st.expander('🐍 Exibir código Python'):
        st.code('''
                # teste de estacionariedade
                !pip install statsmodels
                from statsmodels.tsa.stattools import adfuller
                
                # executar teste
                adfuller(df['brent'].dropna())
                
                # resultados: 
                # - estatística do teste
                # - p-valor
                # - lags
                # - número de observações
                # - valores críticos
                ''')
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # expandir resultados
    with st.expander('📊 Resultados do Teste de Dickey-Fuller'):
        # executar teste de Dickey-Fuller em brent_diff
        # auto-lag = AIC (Akaike Information Criterion):
            # penaliza a complexidade do modelo
        dftest = adfuller(df['brent_diff'], autolag='AIC', regression='c')
        # criar dataframe com resultados
        results_keys = ['Estatística do Teste', 'p-valor', 'Lags', 'Observações', 
                        'Valor Crítico (1%)', 'Valor Crítico (5%)', 'Valor Crítico (10%)']
        result_values = [dftest[0], dftest[1], dftest[2], dftest[3], 
                        dftest[4]['1%'], dftest[4]['5%'], dftest[4]['10%']]
        # criar dicionário com chave e resultados
        results_dict = dict(zip(results_keys, result_values))
        # exibir resultados em diciário
        st.write(results_dict)   

    st.markdown('<br>', unsafe_allow_html=True)
    
    create_analysis('Resultados do Teste de Dickey-Fuller',
                    '''
                    Conforme os resultados do teste de Dickey-Fuller, 
                    a série temporal da diferença do preço do petróleo Brent é estacionária,
                    uma vez que tanto o p-valor é menor que 0.05, 
                    quanto a estatística do teste é menor que os valores críticos da série.
                    ''')
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    # buttom to select 1 of 2 charts
    selected_chart = st.radio('Selecione o gráfico:', ['Diferença', 'Variação Percentual (%)'])
    if selected_chart == 'Diferença':
        
        # histograma com a diferença
        fig = px.histogram(df, x='brent_diff', nbins=100,
                        title='Histograma da Diferença Diária no Preço do Petróleo Brent', 
                        color_discrete_sequence=['#4089FF'], 
                        marginal='box', histnorm='probability density',
                        labels={'value': 'Diferença'}, template='plotly_dark')
        fig.update_traces(marker_line_color='white', marker_line_width=1)
        fig.update_xaxes(title_text=None)
        fig.update_yaxes(title_text='')
        fig.update_layout(title_font_size=20,
                          width=600, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # histograma com a variação percentual
        fig = px.histogram(df, x='brent_pct', nbins=100,
                        title='Histograma da Variação Percentual Diária no Preço do Petróleo Brent', 
                        color_discrete_sequence=['#4089FF'], marginal='box',
                        labels={'value': 'Percentual de Mudança'}, template='plotly_dark')
        fig.update_traces(marker_line_color='white', marker_line_width=1)
        fig.update_xaxes(title_text=None)
        fig.update_yaxes(title_text='')
        fig.update_layout(title_font_size=20,
                          width=600, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown('''
                <p style="font-size: 18px">
                    <br>
                    O histograma da série diferenciada é mais próximo de uma 
                    distribuição normal do que a série original.
                    Para verificar a normalidade, o teste de Kolmogorov-Smirnov é aplicado, onde: <br>
                    - <b>Hipótese nula (H0)</b>: a série diferenciada segue uma distribuição normal.<br>
                    - <b>Hipótese alternativa (H1)</b>: a série diferenciada não segue uma distribuição normal.<br>
                    <br>
                </p>
                ''', unsafe_allow_html=True)
    
    # resultados do teste de Kolmogorov-Smirnov
    with st.expander('📊 Resultados do Teste de Kolmogorov-Smirnov'):
        ks_results = normality_test(df['brent_diff'].dropna())
        # rename keys 'statistic' to 'Estátistica do Teste' and 'pvalue' to 'p-valor'
        ks_results = {k.replace('statistic', 'Estatística do Teste').replace('p-value', 'p-valor'): v 
                     for k, v in ks_results.items()}
        st.write(ks_results)
        
    st.markdown('<br>', unsafe_allow_html=True)
    
    create_analysis('Resultados do Teste de Kolmogorov-Smirnov',
                    '''
                    De acordo com o teste estatístico de Kolmogorov-Smirnov,
                    o p-valor é menor que 0.05, indicando que a hipótese nula é rejeitada.
                    Então, a série diferenciada <b>não</b> segue uma distribuição normal.
                    ''')   
    
    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('''
                <p style="font-size: 18px">
                    <br>
                    O gráfico a seguir mostra a variação do preço do barril de petróleo Brent ao longo do tempo.
                    Note que as maiores variações correspondem ao mês de Maio, como nos anos 2008, 2009, 2020 e 2022. 
                    Por sua vez, as 2 maiores baixas do preço correspondem a Outubro/2008, em vista da Grande Recessão, e 
                    Março/2020, início da Pandemia de COVID-19.
                    <br>
                </p>
                ''', unsafe_allow_html=True)

    fig = px.imshow(df.pivot_table(index='year', columns=df.index.month, values='brent_diff'),
                labels=dict(color='Variação Brent'),
                title='Variação do Preço do Brent ao longo do tempo',
                color_continuous_scale='RdBu',
                width=800, height=1000,
                template='plotly_dark')
    # mostrar meses 1 por 1
    fig.update_xaxes(tickvals=list(range(1, 13)),
                    ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                    side='top', title='')
    fig.update_yaxes(title='')
    fig.update_layout(title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)
    
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                    A variação diária do petróleo Brent teve evolução constante nos últimos 10 anos dos dados (2014-2024), exceto em 2020.
                    A média de variação entre 2014 e 2019 foi de -0.007%, com desvio padrão de 2.16%. Durante os anos de 2020 e 2021,
                    a variação média foi de 0.15%, com desvio padrão de 5.05%. Além disso, a variação máxima sobre o preço diário 
                    durante a pandemia foi de 50.98%.<br><br>
                    A plotagem da variável em 3 dimensões, onde o eixo do gráfico que contém a data é 
                    desmembrado em 2 outros eixos (ano e mês), ajuda a enxergar padrões, 
                    como ciclos de sazonalidade e tendências:
                    <br>
                </p>
                ''', unsafe_allow_html=True)    


    # brent 3d x ano x mês
    fig = px.scatter_3d(df, x=df.index.year, y=df.index.month, z='brent',
                        title='Preço do Petróleo Brent x Ano x Mês',
                        labels={'x': 'Ano', 'y': 'Mês', 'z': 'Preço'},
                        color=df.index.month,
                        color_continuous_scale='PuBu',
                        width=1000, height=800,
                        opacity=0.7,
                        template='plotly_dark')

    fig.update_layout(scene=dict( 
                                xaxis_title='Ano',
                                yaxis_title='Mês',
                                zaxis_title='Preço (U$D )'),
                                coloraxis_colorbar=dict(title='Mês'),
                                title_font_size=20)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # divider
    st.markdown('---')
    # título
    st.title('Features')
    
    st.markdown('''
                <p style="font-size: 18px">
                    <b><i>Features</i></b> podem ser extraídas a partir de datas, como:<br><br>
                    - mês e dia do mês<br>
                    - ano, trimestre e dia do ano<br>
                    - semana, dia da semana e semana do ano (calendário ISO 8601)
                    <br>
                </p>
                ''', unsafe_allow_html=True)
    
    with st.expander('🐍 Exibir código Python'):
        st.code('''
                !pip install pandas             # instalar biblioteca Pandas
                import pandas as pd             # importar biblioteca Pandas
                
                # função para adicionar features de data
                def date_features(dataframe):
        
                df = dataframe.copy()
                df.index.rename('date', inplace=True)
                
                df['year'] = df.index.year
                df['month'] = df.index.month
                df['day'] = df.index.day
                df['day_of_week'] = df.index.dayofweek
                df['day_of_year'] = df.index.dayofyear
                df['week_of_year'] = df.index.isocalendar().week
                df['quarter'] = df.index.quarter
                
                return df
                
                # aplicar função
                df = date_features(df)
                ''')    
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                Para a construção dos modelos de previsão, além do preço do petróleo Brent,
                outros índices representativos foram utilizados como regressores (<i>features</i>):
                
                - **SP500**: Índice de ações da bolsa de valores dos EUA (unidade: pontos)
                - **Exxon**: Ações da Exxon Mobil Corporation (unidade: U$D )
                - **BP**: Ações da British Petroleum (unidade: U$D )
                <br>
                ''', unsafe_allow_html=True)
    
    # plot
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=['SP500', 'Exxon', 'BP'])
    # SP500
    fig.add_trace(go.Scatter(x=df.index, y=df['sp500'], name='SP500',
                            line=dict(color='#4089FF')), row=1, col=1)
    # Exxon
    fig.add_trace(go.Scatter(x=df.index, y=df['exxon'], name='Exxon',
                            line=dict(color='#4089FF')), row=2, col=1)
    # BP
    fig.add_trace(go.Scatter(x=df.index, y=df['bp'], name='BP',
                            line=dict(color='#4089FF')), row=3, col=1)

    # atualizar layout
    fig.update_layout(title='Índices de Ações e Ações de Empresas de Petróleo',
                    title_font_size=20, showlegend=False, template='plotly_dark')
    fig.update_xaxes(title_text='')
    st.plotly_chart(fig)
    
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                A análise de correlação de Pearson ajuda a entender como as variáveis se relacionam entre si.
                Para dados econômicos, fatos similares acontecem entre os preços absolutos e, portanto, 
                correlações altas são esperadas. Portanto, também é importante visualizar a 
                correlação entre as séries diferenciadas. 
                </p>
                ''', unsafe_allow_html=True)
    
    
    # selecionar se série diferenciada ou não
    selected_series = st.radio('Selecione a série:', ['Original', 'Diferença'])
    
    if selected_series == 'Original':
        # control for selected features
        price_cols = ['brent', 'sp500', 'exxon', 'bp']
        # checkbox
        selected_features = st.multiselect('⚙️ Selecione as features:', 
                                        price_cols, price_cols)
        # plotar correlação
        corr = df[selected_features].corr().round(2)
        fig = px.imshow(corr, color_continuous_scale='blues', 
                        title='Correlação entre as variáveis',
                        labels=dict(color='Correlação'),
                        text_auto=True,
                        template='plotly_dark',
                        width=600, height=600)
        fig.update_layout(title_font_size=20)
        fig.update_traces(textfont_size=18)
        fig.update_xaxes(title=None, tickfont_size=18)
        fig.update_yaxes(title=None, tickfont_size=18)
        st.plotly_chart(fig, use_container_width=True)
        # else
    else:
        # control for selected features
        diff_cols = ['brent_diff', 'sp500_diff', 'exxon_diff', 'bp_diff']
        # checkbox
        selected_features = st.multiselect('⚙️ Selecione as features:', 
                                        diff_cols, diff_cols)
        # plotar correlação
        corr = df[selected_features].corr().round(2)
        fig = px.imshow(corr, color_continuous_scale='blues', 
                        title='Correlação entre as variáveis',
                        labels=dict(color='Correlação'),
                        text_auto=True,
                        template='plotly_dark',
                        width=600, height=600)
        fig.update_layout(title_font_size=20)
        fig.update_traces(textfont_size=18)
        fig.update_xaxes(title=None, tickfont_size=18)
        fig.update_yaxes(title=None, tickfont_size=18)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<br>', unsafe_allow_html=True)
    
    # insight
    create_insight('Correlação',
                '''
                Ao considerar todo o período dos dados, 
                a correlação dos preços absolutos entre Brent e Exxon é forte (85%), 
                já com as séries diferenciadas passa a ser baixa (33%).
                Além disso, note que nenhuma das correlações apresentadas é negativa.
                ''')
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    # select one feature to plot with brent
    features_to_plot = ['exxon', 'sp500', 'bp']
    selected_feature = st.selectbox('⚙️ Selecione a feature para plotar com Brent:', features_to_plot)
    # plotar gráfico
    fig = px.scatter(df, x='brent', y=selected_feature,
                    title=f'Petróleo Brent x {selected_feature.title()}',
                    color=df.index.year,
                    color_continuous_scale='ice',
                    width=800, height=800,
                    template='plotly_dark')

    fig.update_layout(coloraxis_colorbar=dict(title='Ano'),
                    title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)
    # divider    
    st.markdown('---')
    
    st.markdown('''
                <p style="font-size: 18px">
                Alguns indicadores utilizados para a <b>análise técnica</b> de ativos financeiros
                podem ser úteis para entender a tendência e volatilidade dos preços, como:
                </p>
                ''', unsafe_allow_html=True)

    # lista de indicadores
    st.markdown('''
                - **EMA**: Exponential Moving Average, ou Média Móvel Exponencial,
                            com janelas de 14, 26, 200 dias.
                - **MACD**: Moving Average Convergence Divergence, ou Convergência e Divergência de Médias Móveis,
                            com 12 dias para a média rápida, 26 dias para a média lenta e 9 dias para o sinal.
                - **RSI**: Relative Strength Index, ou Índice de Força Relativa, com janela de 14 dias.
                ''', unsafe_allow_html=True)
    
    with st.expander('🐍 Exibir código Python'):
        st.code('''    
                !pip install pandas_ta             # instalar biblioteca
                import pandas_ta as ta             # importar biblioteca
                
                # função
                def create_ta_indicators(df, column) -> pd.DataFrame:
        
                df[f'{column}_rsi'] = ta.rsi(df[column], length=14)
                df[f'{column}_macd'] = ta.macd(df[column], fast=12, slow=26, signal=9)[['MACD_12_26_9']]
                df[f'{column}_macd_signal'] = ta.macd(df[column], fast=12, slow=26, signal=9)[['MACDs_12_26_9']]
                df[f'{column}_macd_hist'] = ta.macd(df[column], fast=12, slow=26, signal=9)[['MACDh_12_26_9']]
                df[f'{column}_ema_14'] = ta.ema(df[column], length=14)
                df[f'{column}_ema_26'] = ta.ema(df[column], length=26)
                df[f'{column}_ema_200'] = ta.ema(df[column], length=200)
        
                # remover valores nulos
                df.dropna(inplace=True)
                
                return df
                
                # aplicar função
                df = create_ta_indicators(df, 'brent')
                ''')

    # pular linha
    st.markdown('<br>', unsafe_allow_html=True)
    
    # selecione o indicador
    indicators = ['EMA', 'MACD', 'RSI']
    selected_indicator = st.selectbox('⚙️ Selecione o indicador:', indicators)

    if selected_indicator == 'EMA':
        # renomear colunas para Preço Original, 14 dias, 26 dias e 200 dias
        ema_cols = ['brent', 'brent_ema_14', 'brent_ema_26', 'brent_ema_200']
        # plotar gráfico
        fig = px.line(df[ema_cols], title='EMA do Preço do Petróleo Brent',
                        labels={'value': 'Preço (U$D )', 'date': 'Data'},
                        template='plotly_dark')
        fig.update_layout(title_font_size=20)
        fig.update_xaxes(title=None)
        fig.update_yaxes(range=[0, df['brent'].max() * 1.1])
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<br>', unsafe_allow_html=True)

        st.markdown('''
                    <p style="font-size: 18px">
                    EMA (<i>Exponential Moving Average</i>, ou Média Móvel Exponencial)
                    é um indicador de análise técnica que suaviza os preços e é utilizado para 
                    identificar a direção da tendência. A EMA dá um peso maior aos valores mais recentes, 
                    enquanto a Média Móvel Simples (SMA) dá o mesmo peso a todos os valores. 
                    A EMA de 14 dias é mais sensível às mudanças de preço, 
                    enquanto a EMA de 200 dias é mais lenta e é utilizada para identificar a tendência de longo prazo.
                    </p>
                    ''', unsafe_allow_html=True)

        st.latex(r'''
                EMA_{t} = \frac{P_{t}*k + EMA_{t-1}*(1-k)}{1}
                ''')

        st.markdown('''
                    Onde:<br>
                    t = período de tempo recente<br>
                    P = preço do ativo<br>
                    k = calculado como 2/(n+1), onde n é o número de dias para suavização<br>
                    ''', unsafe_allow_html=True)
    
    elif selected_indicator == 'MACD':
        # MACD
        fig = px.line(df, x=df.index, 
                  y=['brent_macd', 'brent_macd_signal', 'brent_macd_hist'],
                  title='MACD do Preço do Petróleo Brent',
                  labels={'value': 'MACD'}, template='plotly_dark')
        fig.update_layout(title_font_size=20)
        fig.update_xaxes(title=None)
        fig.update_yaxes(range=[df['brent_macd'].min() * 1.1, df['brent_macd'].max() * 1.1])
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">
                    MACD (<i>Moving Average Convergence Divergence</i>, ou Média Móvel Convergência/Divergência),
                    é um indicador que mostra a relação entre duas médias móveis de valores. 
                    A MACD é calculada subtraindo a EMA de 26 dias da EMA de 12 dias. 
                    O sinal é a EMA de 9 dias da MACD. O histograma é a diferença entre a MACD e o sinal.
                    </p>
                    ''', unsafe_allow_html=True)
        
        st.latex(r'''
                MACD = EMA_{12} - EMA_{26}
                ''')
        st.latex(r'''
                Sinal = EMA_{9}(MACD_p)
                ''')
        st.latex(r'''
                Histograma = MACD - Sinal
                ''')
        
        st.markdown('''
                    Onde:<br>
                    MACD = Média Móvel Convergência/Divergência<br>
                    EMA = Média Móvel Exponencial<br>
                    ''', unsafe_allow_html=True)

    else:
        # RSI
        fig = px.line(df, x=df.index, y='brent_rsi', 
                  title='RSI do Preço do Petróleo Brent', 
                  labels={'value': 'RSI'}, template='plotly_dark')
        fig.add_hline(y=70, line_dash='dot', line_color='red', 
                      annotation_text='70', annotation_position='bottom right')
        fig.add_hline(y=30, line_dash='dot', line_color='green',
                        annotation_text='30', annotation_position='top right')
        fig.update_layout(title_font_size=20)
        fig.update_xaxes(title=None)
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">
                    RSI (<i>Relative Strength Index</i>, ou Índice de Força Relativa),  é um indicador  
                    que mede a força e a velocidade das mudanças no valor de um ativo. O RSI varia de 0 a 100 e é normalmente 
                    usado para identificar condições de sobrecompra e sobrevenda. Um ativo é considerado sobrecomprado 
                    quando o RSI está acima de 70 e sobrevendido quando está abaixo de 30.
                    </p>
                    ''', unsafe_allow_html=True)
        
        st.latex(r'''
                RSI = 100 - \frac{100}{1 + RS}
                ''')
        
        st.markdown('''
                    Onde:<br>
                    ''', unsafe_allow_html=True)
        
        st.latex(r'''
                RS = \frac{Média_{ganhos}}{Média_{perdas}}
                ''')

    
    st.markdown('<br>', unsafe_allow_html=True)
    # divider
    st.markdown('---')
    # texto
    st.markdown('''### Dataframe Final''')
    st.markdown('''
                Com isso, o dataframe completo pode ser visualizado abaixo:
                ''', unsafe_allow_html=True)
    # dataframe
    # controles para ordenar o dataframe: ascending or descending
    ascending = st.checkbox('Índice decrescente', value=False)
    if ascending:
        df = df.sort_index(ascending=False)
    # mostrar dataframe
    st.dataframe(df)
    

elif page == page_2:
    # título
    st.title('Modelos de Previsão')
    # seleção de modelo
    model = st.selectbox('Selecione o modelo:', ['XGBoost', 'Prophet'])
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    if model == 'XGBoost':
        # texto
        st.markdown('''
                    <p style="font-size: 18px">
                        O XGBoost, ou <i>Extreme Gradient Boosting</i>, é um algoritmo de aprendizado de máquina supervisionado e baseado em árvores de decisão.
                        O modelo é uma implementação otimizada do Gradient Boosting e pode ser utilizado para problemas de regressão e classificação. O XGBoost é 
                        amplamente utilizado em competições de ciência de dados e é conhecido por sua eficiência e desempenho.
                        <br>
                    </p>
                    ''', unsafe_allow_html=True)
        
        with st.expander('🐍 Exibir código Python'):
            # código
            st.code('''
                    # importar o XGBoost
                    !pip install xgboost                 # instalar biblioteca
                    import xgboost as xgb                # importar biblioteca
                    ''')
        
        # markdown
        st.markdown('''
                    <p style="font-size: 18px">
                        <br>
                        As colunas categóricas devem ser transformadas em variáveis numéricas antes de treinar o modelo.
                        Para isso, podemos utilizar a técnica <i>One-Hot Encoding</i>.<br>
                    </p>
                    ''', unsafe_allow_html=True)
        
        # código
        with st.expander('🐍 Exibir código Python'):
            st.code('''
                        # One-Hot Encoding
                        df = pd.get_dummies(df_baseline, 
                                columns=['month', 'year', 'weekday'],
                                drop_first=True)
                        
                        # caracteres minúsculos
                        df.columns = df.columns.str.lower()
                        
                        print(f'Quantidade de colunas: {df.shape[1]}')
                        ''')
        
        # divider
        st.markdown('---')
        
        # selecione o modelo
        model_type = st.radio('Selecione o modelo:', ['Baseline', 'Final'])
        if model_type == 'Baseline':
            # texto
            # preparação dos dados - título
            st.markdown('''#### Preparação dos dados''')
            st.markdown(r'''
                        <p style="font-size: 18px">
                        Para o modelo baseline, utilizamos 80% dos dados para treino e 20% para teste.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # baseline - divisão dos dados
                        X = df_baseline.drop(columns=['brent'])
                        y = df_baseline['brent']

                        # train test split
                        train_baseline_size = int(df_baseline.shape[0] * 0.8)

                        # 80% treino, 20% teste
                        X_train_baseline, X_test_baseline = X[:train_baseline_size], X[train_baseline_size:]
                        y_train_baseline, y_test_baseline = y[:train_baseline_size], y[train_baseline_size:]
                        ''')
                
            # gráfico com divisão dos dados
            baseline_xgb_df = pd.read_parquet(r'data/xgboost_baseline_train_test.parquet')
            fig = px.line(baseline_xgb_df, x='date', y='brent', 
                title='XGBoost Baseline - Treino e Teste', 
                color='set', 
                color_discrete_map={'train': '#4089FF', 
                                    'test': '#f6c409'},
                template='plotly_dark')
            # adicionar linha para divisão
            train_baseline_size = int(baseline_xgb_df.shape[0] * 0.8)
            fig.add_shape(type='line', 
                        x0=baseline_xgb_df.iloc[train_baseline_size]['date'],
                        y0=0, x1=baseline_xgb_df.iloc[train_baseline_size]['date'],
                        y1=baseline_xgb_df['brent'].max()*1.1,
                        line=dict(color='white', width=1, dash='dash'))
                            
            fig.update_layout(title_font_size=20)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            st.plotly_chart(fig, use_container_width=True)
                
            st.markdown('''#### Treinamento do modelo''')
            # selecionar modelo baseline ou final - colocar isso para cima e mudar o código
            # texto
            st.markdown('''<p style="font-size: 18px">
                        Com os dados preparados, podemos treinar o modelo XGBoost. 
                        Como vamos prever valores de preço, utilizamos a classe XGBRegressor. 
                        Para o treinamento do modelo baseline, não utilizamos
                        colunas de indicadores técnicos, como EMA, MACD e RSI.
                        </p>
                        ''', unsafe_allow_html=True)
            
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # Construção do modelo baseline
                        xgb_baseline = xgb.XGBRegressor(n_estimators=1000,                 # número de árvores
                                                        max_depth=3,                       # profundidade máxima = 3 níveis
                                                        booster='gbtree',                  # default
                                                        early_stopping_rounds=50,          # cessa após 50 iterações sem melhorar
                                                        objective='reg:squarederror' ,     # função objetivo = erro quadrático
                                                        learning_rate=0.01,               # taxa de aprendizado menor, para evitar o overfitting
                                                        random_state=19)                   # para reprodução

                        # Treinamento do modelo baseline
                        xgb_baseline.fit(X_train_baseline, y_train_baseline,
                                        eval_set=[(X_train_baseline, y_train_baseline),    # avaliação no treino
                                                    (X_test_baseline, y_test_baseline)],   # avaliação no teste
                                                    verbose=True)                          # exibir resultados durante o treino
                        ''')
                
            st.markdown('''<br>''', unsafe_allow_html=True)
                
            # importância das features
            importance_baseline_df = pd.read_parquet(r'data/xgboost_baseline_importance.parquet')
            
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Exxon Mobil, o índice SP500 e o ano de 2012 são as features mais importantes no modelo baseline.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # code
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # Importância das features
                        importance_baseline_df = pd.DataFrame({'feature': X_train_baseline.columns,
                                                                'importance': xgb_baseline.feature_importances_})
                        
                        # Ordenar
                        importance_baseline_df = importance_baseline_df.sort_values('importance', ascending=False)
                        ''')
            
            st.markdown('''<br>''', unsafe_allow_html=True)
            
            # plot
            fig = px.bar(importance_baseline_df, x='importance', y='feature',
                        title='10 Features mais importantes',
                        labels={'importance': 'Importância', 'feature': 'Feature'},
                        template='plotly_dark')
            fig.update_layout(title_font_size=20)
            fig.update_xaxes(title=None, showgrid=True,
                             range=[0, importance_baseline_df['importance'].max() * 1.2])
            fig.update_yaxes(title=None)
            st.plotly_chart(fig, use_container_width=True)
            
            # realizar previsões
            st.markdown('''#### Previsões''')
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Com o modelo treinado, podemos realizar previsões para o preço do petróleo Brent.
                        </p>
                        ''', unsafe_allow_html=True)
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # previsões
                        y_pred_baseline = xgb_baseline.predict(X_test_baseline)
                        
                        # dataframe com previsões
                        predictions_baseline_df = pd.DataFrame({'date': X_test_baseline.index,
                                                                'brent': y_test_baseline,
                                                                'brent_pred': y_pred_baseline})
                        
                        ''')
            # plotar previsões
            baseline_xgb_pred_df = pd.read_parquet(r'data/xgboost_baseline_prediction.parquet')
            
            fig = px.line(baseline_xgb_pred_df, x='date', y=['brent', 'prediction'],
                title='XGBoost Baseline - Predição vs Real', 
                color_discrete_map={'brent': '#4089FF', 
                                    'prediction': '#e34592'},
                labels={'variable': 'variável', 'value': 'preço (U$D )'},
                template='plotly_dark')
            fig.update_layout(title_font_size=20)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            st.plotly_chart(fig, use_container_width=True)
        
            # métricas
            st.markdown('''#### Avaliação do modelo''')
            st.markdown('''
                        <p style="font-size: 18px">
                        Para avaliar o modelo, utilizamos as métricas RMSE, MAE e MAPE.<br>
                        </p>
                        ''', unsafe_allow_html=True)  
            # RMSE  
            st.markdown('''
                        - **RMSE** - *Root Mean Squared Error*, ou Raiz do Erro Quadrático Médio:
                        ''')
            st.latex(r'''
                    RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_{true} - y_{pred})^2}
                    ''')
            # MAE
            st.markdown('''
                        - **MAE** - *Mean Absolute Error*, ou Erro Médio Absoluto:
                        ''')
            st.latex(r'''
                    MAE = \frac{1}{n} \sum_{i=1}^{n} |y_{true} - y_{pred}|
                    ''')
            # MAPE
            st.markdown('''
                        - **MAPE** - *Mean Absolute Percentage Error*, ou Erro Percentual Absoluto Médio:
                        ''')
            st.latex(r'''
                    MAPE = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{y_{true} - y_{pred}}{y_{true}} \right| \times 100
                    ''')
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # importar métricas
                        from sklearn.metrics import mean_absolute_error, mean_squared_error
                        
                        # função para calcular MAPE
                        def mean_absolute_percentage_error(y_true, y_pred) -> float:
                            return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
                        
                        # métricas
                        rmse_baseline = np.sqrt(mean_squared_error(y_test_baseline, y_pred_baseline))
                        mae_baseline = mean_absolute_error(y_test_baseline, y_pred_baseline)
                        mape_baseline = mean_absolute_percentage_error(y_test_baseline, y_pred_baseline)
                        
                        # print
                        print(f'RMSE: {rmse_baseline:.2f}')
                        print(f'MAE: {mae_baseline:.2f}')
                        print(f'MAPE: {mape_baseline:.2f}')
                        ''')
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            # botão para exibir scores
            if st.button('📊 Exibir Scores'):
                scores_baseline_df = pd.read_parquet(r'data/xgboost_baseline_scores.parquet')
                scores_baseline_df = scores_baseline_df.T
                scores_baseline_df.columns = scores_baseline_df.iloc[0]
                # drop first row
                scores_baseline_df = scores_baseline_df[1:]
                # mostrar dataframe
                st.dataframe(scores_baseline_df)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            baseline_metrics_text = r'''
                        A RMSE é dada na mesma unidade de medida do dataset original e mostra que o modelo baseline está errando, em média, U$D 23.52.<br>
                        A MAE é uma métrica absoluta e indica que as previsões do modelo estão desviando, em média, U$D 17.1 do valor real.<br>
                        A diferença entre RMSE e MAE é que a primeira dá mais peso para erros maiores, 
                        enquanto a segunda trata todos os erros de forma igual.<br>
                        A MAPE é uma porcentagem e indica que as previsões do modelo estão desviando, em média, 22.96% do valor real.
                        '''
            create_analysis('Resultados do Modelo Baseline', baseline_metrics_text)
            
            st.markdown('<br>', unsafe_allow_html=True)

                
        else:
            # preparação dos dados - título
            st.markdown('''#### Preparação dos dados''')
            # texto
            st.markdown(r'''
                        <p style="font-size: 18px">
                        Para a divisão dos dados em treino e teste, a classe TimeSeriesSplit do Scikit-Learn se utiliza do 
                        método de validação cruzada (ou cross validation), que segmenta os dados de treino em K grupos 
                        (chamados <i>folds</i>), consecutivos e ordenados. Em seguida, treina o modelo em etapas, a partir 
                        de um pequeno conjunto inicial, que se expande com mais dados de treino - em direção ao futuro. 
                        Se K é igual a 5, por exemplo, o modelo é treinado 5 vezes, com volume incremental de dados, onde  
                        cada nova dobra incorpora os dados da dobra anterior e expande o conjunto de treino. 
                        Após cada treinamento, o modelo executa previsões, a serem avaliadas pela métrica escolhida pelo usuário.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # modelo final - divisão dos dados
                        X = df.drop(columns=['brent'])
                        y = df['brent']
                        
                        # time series split
                        tscv = TimeSeriesSplit(n_splits=5)
                        
                        # iterar sobre as divisões
                        for train_index, test_index in tscv.split(X):
                            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                        ''')
                
            # gráfico com divisão dos dados
            df = pd.read_parquet(r'data/data_w_indicators.parquet')
            X = df.drop(columns=['brent'])
            y = df['brent']
            # time series split
            tscv = TimeSeriesSplit(n_splits=5)
            # iterar sobre as divisões
            i = 1
            for train_index, test_index in tscv.split(X):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                # dataframe com divisões
                df_split = df.iloc[test_index]
                df_split['set'] = f'set_{i}'
                if i == 1:
                    df_final = df_split
                else:
                    df_final = pd.concat([df_final, df_split])
                i += 1
            # plotar gráfico
            fig = px.line(df_final, x=df_final.index, y='brent',
                        title='XGBoost Final - Divisão dos Dados',
                        color='set', 
                        template='plotly_dark')
            fig.update_layout(title_font_size=20)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('''#### Treinamento do modelo''')
            # texto
            st.markdown('''<p style="font-size: 18px">
                        A melhor escolha pode ser encontrada através da técnica Grid Search, 
                        que itera sobre as opções listadas pelo usuário e treina modelos únicos, 
                        gerados a partir da combinação de todos os parâmetros. 
                        Vale ressaltar que, quanto mais opções são fornecidas, mais tempo será consumido na execução.
                        ''', unsafe_allow_html=True)
            
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # Importar Grid Search
                        from sklearn.model_selection import GridSearchCV
                                                
                        # Converter X e y para numpy arrays
                        X = np.array(X)
                        y = np.array(y)
                        
                        # Grid Search
                        params = {'n_estimators': [100, 500, 1000, 2000],
                                  'max_depth': [3, 5, 7, 9],
                                  'learning_rate': [0.001, 0.01, 0.1]
                        
                        xgb_final = xgb.XGBRegressor(objective='reg:squarederror', 
                                                     random_state=19)
                        
                        grid_search = GridSearchCV(estimator=xgb_final, 
                                                param_grid=params, 
                                                scoring='neg_mean_squared_error', 
                                                cv=tscv, 
                                                verbose=1)
                        
                        grid_search.fit(X, y)
                        
                        # Melhores parâmetros
                        best_params = grid_search.best_params_
                        # Melhor modelo
                        best_model = grid_search.best_estimator_
                        # Melhor score
                        best_score = grid_search.best_score_
                        
                        # Criar dataframe com resultados
                        results_df = pd.DataFrame(grid_search.cv_results_)
                        results_df = results_df.sort_values(by='rank_test_score')
                        ''')
            # plotar importância das features
            # importância das features
            importance_final_df = pd.read_parquet(r'data/xgboost_best_importance.parquet')
            # plot
            fig = px.bar(importance_final_df, x='importance', y='feature',
                        title='10 Features mais importantes',
                        labels={'importance': 'Importância', 'feature': 'Feature'},
                        template='plotly_dark')
            fig.update_layout(title_font_size=20)
            fig.update_xaxes(title=None, showgrid=True,
                             range=[0, importance_final_df['importance'].max() * 1.2])
            fig.update_yaxes(title=None)
            st.plotly_chart(fig, use_container_width=True)
            
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Os anos de 2012, 2011 e 2013 são as features mais importantes para o modelo final.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # resultados
            st.markdown('''<br>''', unsafe_allow_html=True)
            st.markdown('''#### Avaliação do modelo''')
            st.markdown('''
                        <p style="font-size: 18px">
                        Com isso, treinamos 48 modelos e o melhor foi obtido com os parâmetros:<br>
                        - <b>n_estimators</b>: 1000<br>
                        - <b>max_depth</b>: 3<br>
                        - <b>learning_rate</b>: 0.1<br>
                        </p>
                        ''', unsafe_allow_html=True)
            # previsões
            st.markdown('''#### Previsões''')
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Com o modelo treinado, realizamos previsões para o preço do petróleo Brent.
                        </p>
                        ''', unsafe_allow_html=True)
            # plotar
            final_xgb_pred_df = pd.read_parquet(r'data/xgboost_best_prediction.parquet')
            fig = px.line(final_xgb_pred_df, x='date', y=['brent', 'prediction'],
                title='XGBoost Final - Predição vs Real', 
                color_discrete_map={'brent': '#4089FF', 
                                    'prediction': '#e34592'},
                labels={'variable': 'variável', 'value': 'preço (U$D )'},
                template='plotly_dark')
            fig.update_layout(title_font_size=20)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            st.plotly_chart(fig, use_container_width=True)
            
            # métricas
            st.markdown('''#### Avaliação do modelo''')
            st.markdown('''
                        <p style="font-size: 18px">
                        Para avaliar o modelo, utilizamos as métricas:<br>
                        </p>
                        ''', unsafe_allow_html=True)
            # RMSE
            st.markdown('''
                        - **RMSE** - *Root Mean Squared Error*, ou Raiz do Erro Quadrático Médio:
                        ''')
            st.latex(r'''
                    RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_{true} - y_{pred})^2}
                    ''')
            # MAE
            st.markdown('''
                        - **MAE** - *Mean Absolute Error*, ou Erro Médio Absoluto:
                        ''')
            st.latex(r'''
                    MAE = \frac{1}{n} \sum_{i=1}^{n} |y_{true} - y_{pred}|
                    ''')
            # MAPE
            st.markdown('''
                        - **MAPE** - *Mean Absolute Percentage Error*, ou Erro Percentual Absoluto Médio:
                        ''')
            st.latex(r'''
                    MAPE = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{y_{true} - y_{pred}}{y_{true}} \right| \times 100
                    ''')
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            # botão para exibir scores
            if st.button('📊 Exibir Scores'):
                scores_best_df = pd.read_parquet(r'data/xgboost_best_scores.parquet')
                scores_best_df = scores_best_df.iloc[[-1]]
                scores_best_df = scores_best_df.T
                scores_best_df.columns = scores_best_df.iloc[0]
                scores_best_df = scores_best_df[1:]
                scores_best_df = scores_best_df.rename(columns={'XGBoost Best5': 'XGBoost Best'})
                # mostrar dataframe
                st.dataframe(scores_best_df)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            create_analysis('Resultados do Modelo Final', 
                            r'''
                                Em comparação com modelo baseline, houve melhora considerável nas métricas de avaliação:<br>
                                A RMSE melhorou em 38.08%, a MAE melhorou em 37.51% e a MAPE melhorou em 38.5%
                             ''')
            
            st.markdown('<br>', unsafe_allow_html=True)
            
    else:
        # modelo Prophet
        # texto
        st.markdown('''
                    <p style="font-size: 18px">
                    O Prophet, criado pelo Facebook em 2008 sob autoria dos cientistas de dados Sean J. Taylor e Ben Letham, 
                    é uma biblioteca open-source baseada em modelos decomponíveis de séries temporais. 
                    A ferramenta lida bem com dados ausentes e outliers, e foi projetada para ser fácil de usar. 
                    O Prophet usa 3 componentes principais para a decomposição: tendência (<i>trend</i>), 
                    sazonalidade (<i>seasonality</i>) e feriados (<i>holidays</i>). 
                    Assim, pode ser expressado através da equação:
                    </p>
                    ''', unsafe_allow_html=True)
        
        st.latex(r'''
                    y(t) = g(t) + s(t) + h(t) + e(t)
                  ''')
        
        # text
        st.markdown('''
                    Em que:
                    - Growth g(t): representa a curva de crescimento linear ou logística, para modelar mudanças não periódicas em séries temporais. Por padrão, o Prophet usa o modelo de crescimento linear para as previsões.
                    - Seasonality s(t): a série de Fourier é usada para modelar efeitos sazonais ou mudanças periódicas (por exemplo: o ciclo semanal, mensal e anual). Para aprender e prever tais efeitos, o Prophet depende da série de Fourier para fornecer um modelo flexível.
                    - Feriados e eventos h(t): o Prophet considera o efeito de feriados e permite adicionar os parâmetro supper_window e lower_window, que estendem os efeitos dos feriados em torno de suas datas.
                    - Termo de erro e(t): o termo de erro leva em conta quaisquer mudanças incomuns não acomodadas pelo modelo.
                    ''')
        
        # código
        with st.expander('🐍 Exibir código Python'):
            st.code('''
                    # importar o Prophet
                    !pip install prophet                 # instalar biblioteca
                    from prophet import Prophet          # importar biblioteca
                    ''')
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        # markdown
        st.markdown('''
                    <p style="font-size: 18px">
                    Para utilizar o Prophet, é necessário criar um dataframe com duas colunas: ds (data) e y (valor).
                    Em seguida, instanciamos o modelo Prophet, ajustamos os dados de treino e realizamos previsões.
                    </p>
                    ''', unsafe_allow_html=True)
        
        # código
        with st.expander('🐍 Exibir código Python'):
            st.code('''
                    # criar dataframe
                    df_prophet = df[['date', 'brent']].copy()
                    df_prophet.columns = ['ds', 'y']
                    ''')
        
        # divider
        st.markdown('---')   
        
        # selecione o modelo
        model_type = st.radio('Selecione o modelo:', ['Baseline', 'Final'])
        if model_type == 'Baseline':
            # preparação dos dados - título
            st.markdown('''#### Preparação dos dados''')
            # texto
            st.markdown(r'''
                        <p style="font-size: 18px">
                        Para o modelo baseline, utilizaremos as colunas sp500, exxon e bp como regressores. Além disso,
                        utilizaremos 80% dos dados para treino e 20% para teste.
                        </p>
                        ''', unsafe_allow_html=True)

            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # baseline - divisão dos dados
                        baseline_train_size = int(len(df_baseline) * 0.8)

                        baseline_train = df_baseline.iloc[:baseline_train_size].copy()
                        baseline_test = df_baseline.iloc[baseline_train_size:].copy()
                        ''')
            
            # gráfico com divisão dos dados
            prophet_baseline_train_df = pd.read_parquet(r'data/prophet_baseline_train.parquet')
            prophet_baseline_test_df = pd.read_parquet(r'data/prophet_baseline_test.parquet')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter
                        (x=prophet_baseline_train_df['ds'], y=prophet_baseline_train_df['y'],
                        mode='lines', name='Treino', line=dict(color='#4089FF')))
            fig.add_trace(go.Scatter
                        (x=prophet_baseline_test_df['ds'], y=prophet_baseline_test_df['y'],
                        mode='lines', name='Teste', line=dict(color='#f6c409')))
            fig.update_layout(title='Prophet Baseline - Treino e Teste',
                            title_font_size=20, template='plotly_dark')
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            st.plotly_chart(fig, use_container_width=True)
            
            # markdown
            st.markdown('''#### Treinamento do modelo''')
            # texto
            st.markdown('''<p style="font-size: 18px">
                        Com os dados preparados, podemos treinar o modelo Prophet.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # Instanciar o modelo Prophet
                        baseline_model = Prophet()     # parâmetros default
                        
                        # Ajustar o modelo
                        baseline_model.fit(baseline_train)
                        ''')
            
            # previsões
            st.markdown('''#### Previsões''')
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Com o modelo treinado, realizamos previsões para o preço do petróleo Brent.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        from prophet.make_future_dataframe import make_future_dataframe
                        
                        # Criar dataframe futuro
                        future_baseline = baseline_model.make_future_dataframe(periods=len(baseline_test),
                                                                                freq='B')     # dias úteis
                        
                        # Realizar previsões
                        forecast_baseline = baseline_model.predict(future_baseline)
                        ''')
                
            # previsões
            prophet_baseline_forecast_df = pd.read_parquet(r'data/prophet_baseline_forecast.parquet')
            # carregar modelo baseline com pickle
            with open(r'models/prophet_baseline_model.pkl', 'rb') as file:
                prophet_baseline = pickle.load(file)
            
            fig = plot_plotly(prophet_baseline, prophet_baseline_forecast_df)
            fig.update_layout(title='Prophet Baseline - Predição vs. Real', title_font_size=20)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            # scatter to blue
            fig.for_each_trace(lambda t: t.update(marker=dict(color='#4089FF')))
            # line to pink
            fig.for_each_trace(lambda t: t.update(line=dict(color='#e34592')))
            st.plotly_chart(fig, use_container_width=True)
            
            # avaliação com cross-validation
            st.markdown('''#### Avaliação do modelo''')
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Para avaliar o modelo, utilizamos a técnica de validação cruzada (cross-validation).
                        O Prophet possui uma função interna para realizar a validação cruzada, que divide os dados em
                        janelas temporais e treina o modelo em cada uma delas.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        from prophet.diagnostics import cross_validation
                        from prophet.diagnostics import performance_metrics
                        
                        # Realizar cross-validation
                        cv_baseline = cross_validation(baseline_model,
                                                        initial='200 days',
                                                        period='60 days',
                                                        horizon='30 days')
                        
                        # Métricas
                        metrics_baseline = performance_metrics(cv_baseline)
                        ''')
            
            # botão para exibir scores
            if st.button('📊 Exibir Scores'):
                # dataframe com scores
                prophet_baseline_dict = {'Horizonte': '3 dias',
                                        'RMSE': 15.2261,
                                        'MAE': 8.9039,
                                        'MAPE': 0.1953}
                st.write(prophet_baseline_dict)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            prophet_metrics_text = r'''
                        Para um horizonte de previsão de 3 dias, o modelo atingiu<br> 
                        RMSE de 15.22, MAE de 8.90 e MAPE de 19.53%.
                        '''
            
            create_analysis('Resultados do Modelo Baseline', prophet_metrics_text)
            
            st.markdown('<br>', unsafe_allow_html=True)
            
        else:
            # preparação dos dados - título
            st.markdown('''#### Preparação dos dados''')
            # texto
            st.markdown(r'''
                        <p style="font-size: 18px">
                        Para o modelo final, utilizaremos todas as colunas do dataset como regressores. Além disso,
                        utilizaremos a função Grid Search para encontrar os melhores parâmetros para o modelo.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # final - divisão dos dados
                        final_train_size = int(len(df_final) * 0.8)

                        final_train = df_final.iloc[:final_train_size].copy()
                        final_test = df_final.iloc[final_train_size:].copy()
                        ''')
            
            # gráfico com divisão dos dados
            prophet_final_train_df = pd.read_parquet(r'data/prophet_final_train.parquet')
            prophet_final_test_df = pd.read_parquet(r'data/prophet_final_test.parquet')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter
                        (x=prophet_final_train_df['ds'], y=prophet_final_train_df['y'],
                        mode='lines', name='Treino', line=dict(color='#4089FF')))
            fig.add_trace(go.Scatter
                        (x=prophet_final_test_df['ds'], y=prophet_final_test_df['y'],
                        mode='lines', name='Teste', line=dict(color='#f6c409')))
            fig.update_layout(title='Prophet Final - Treino e Teste',
                            title_font_size=20, template='plotly_dark')
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            st.plotly_chart(fig, use_container_width=True)
            
            # markdown
            st.markdown('''#### Treinar o modelo''')
            # texto
            st.markdown('''<p style="font-size: 18px">
                        Com os dados preparados, podemos criar a lista de parâmetros e realizar a busca dos melhores parâmetros, 
                        com base na métrica MAPE.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        import itertools
                        from prophet.make_holidays import make_holidays
                        
                        # Criar lista de parâmetros
                        param_grid = {
                                        'changepoint_prior_scale': np.linspace(0.001, 0.5, 3),
                                        'seasonality_prior_scale': np.linspace(0.01, 10, 3),
                                        'holidays_prior_scale': [0.1, 10],
                                     }
                        
                        # Combinar parâmetros
                        all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
                        
                        results = []
                        periods=252
                        
                        # Iterar sobre os parâmetros
                        for i, params in enumerate(all_params):
                            # Instanciar o modelo
                            model = Prophet(**params)
                            
                            # Adicionar regressores
                            for regressor in regressors.columns:
                                model.add_regressor(regressor)
                                
                            # Adicionar feriados
                            model.add_country_holidays(country_name='US')
                            
                            # Ajustar o modelo
                            model.fit(train)
                            
                            # Criar dataframe futuro
                            future = model.make_future_dataframe(periods=periods, 
                                                                freq='B', 
                                                                include_history=True)
                                                                
                            # Adicionar regressores
                            for regressor in regressors.columns:
                                future[regressor] = df[regressor]
                                
                            # Realizar previsões
                            forecast = model.predict(future)
                            
                            # predictions
                            predictions = forecast[['ds', 'yhat']].tail(periods)
                            # calculate the error
                            error = mape(df['y'], forecast['yhat'])
                            # append the results
                            results.append([params, error])
                            
                        results = pd.DataFrame(results, columns=['params', 'mape'])
                        results = results.sort_values('mape', ascending=True)
                        
                        best_params = results.iloc[0, 0]
                        ''')
                
            # markdown
            st.markdown('''
                        <p style="font-size: 18px"><br>
                        O melhor modelo, com MAPE de 12.13%, foi obtido com os seguintes parâmetros:<br>
                        - <b>changepoint_prior_scale</b>: 0.5<br>
                        - <b>seasonality_prior_scale</b>: 0.01<br>
                        - <b>holidays_prior_scale</b>: 0.01
                        </p>
                        ''', unsafe_allow_html=True)
            
            # markdown
            st.markdown('''#### Avaliação do modelo''')
            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                        Agora, modelos treinar o melhor modelo e realizar previsões.
                        Com isso, podemos avaliar o modelo com a validação cruzada.
                        </p>
                        ''', unsafe_allow_html=True)
            
            # código
            with st.expander('🐍 Exibir código Python'):
                st.code('''
                        # Instanciar o modelo
                        best_model = Prophet(**best_params)
                        
                        # Adicionar regressores
                        for regressor in regressors.columns:
                            final_model.add_regressor(regressor)
                        
                        # Adicionar feriados
                        final_model.add_country_holidays(country_name='US')
                        
                        # Ajustar o modelo
                        final_model.fit(final_train)
                        
                        # Realizar cross-validation
                        cv_final = cross_validation(final_model,
                                                    initial='200 days',
                                                    period='60 days',
                                                    horizon='30 days')
                        
                        # Métricas
                        metrics_final = performance_metrics(cv_final)
                        ''')
            
            # plotar
            prophet_final_forecast_df = pd.read_parquet(r'data/prophet_final_forecast.parquet')
            # carregar modelo final com pickle
            with open(r'models/prophet_final_model.pkl', 'rb') as file:
                prophet_final = pickle.load(file)
                
            fig = plot_plotly(prophet_final, prophet_final_forecast_df)
            fig.update_layout(title='Prophet Final - Predição vs. Real', title_font_size=20)
            fig.update_xaxes(title=None)
            fig.update_yaxes(title='Preço (U$D )')
            # scatter to blue
            fig.for_each_trace(lambda t: t.update(marker=dict(color='#4089FF')))
            # line to pink
            fig.for_each_trace(lambda t: t.update(line=dict(color='#e34592')))
            st.plotly_chart(fig, use_container_width=True)
            
            # botão para exibir scores
            if st.button('📊 Exibir Scores'):
                # dataframe com scores
                prophet_final_dict = {'Horizonte': '3 dias',
                                      'RMSE': 10.7325,
                                      'MAE': 6.1403,
                                      'MAPE': 0.1211}
                st.write(prophet_final_dict)

            st.markdown('<br>', unsafe_allow_html=True)
            
            prophet_metrics_text = r'''
                        Para um horizonte de previsão de 3 dias, o modelo atingiu<br>
                        RMSE de 10.73, MAE de 6.14 e MAPE de 12.11%.<br>
                        Em comparação com o modelo baseline, houve melhora de<br>15.22% sobre a métrica RMSE, 8.9% sobre a MAE e 
                        37.97% sobre a MAPE.
                        '''

            create_analysis('Resultados do Modelo Final', prophet_metrics_text)

# conclusão
elif page == page_3:
    # título
    st.title('Conclusão')
    # separador
    st.markdown('<br>', unsafe_allow_html=True)
    # texto
    st.markdown('''
                <p style="font-size: 20px">
                    Neste projeto, foram treinados dois modelos para prever o preço do petróleo Brent: XGBoost e Prophet.
                    <br><br>
                    O modelo XGBoost obteve <b>RMSE de 15.89</b>, <b>MAE de 12.31</b> e <b>MAPE de 16.06%</b>, 
                    o modelo Prophet obteve <b>RMSE de 10.73</b>, <b>MAE de 6.14</b> e <b>MAPE de 12.11%</b>. 
                    Com base nas configurações atuais, o modelo Prophet obteve melhores métricas de avaliação.
                    <br>
                </p>
                ''', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('---')
    
    # próximos passos
    st.markdown('''## Principais Insights''')
    
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                    Os principais <i>insights</i> e respectivas etapas de melhorias ao projeto,
                    obtidos durante os processos de análise dos dados e construção dos modelos, são retratados a seguir:
                    <br>
                </p>
                ''', unsafe_allow_html=True) 
                
    # melhoria do modelo XGBoost
    st.markdown('''#### Melhoria do Modelo XGBoost''')
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                    - <b>Próximo passo:</b> utilizar outros modelos para que o XGBoost possa extrapolar previsões para 
                      além dos limites dos dados de treinamento.
                <br>
                </p>
                ''', unsafe_allow_html=True)    
    
    create_insight(
                    'Extrapolação de Dados na Previsão',
                    '''
                        O modelo XGBoost, assim como quaisquer algoritmos baseados em árvore, 
                        possui uma desvantagem para tarefas de regressão: suas predições respeitarão os 
                        limites dos dados utilizados no treinamento. Ou seja, existe dificuldade em <b>extrapolar</b> os 
                        valores máximo e mínimo do intervalo de dados de treinamento. Por isso, se faz interessante 
                        combinar esse modelo a outros, como modelos lineares ou mesmo Redes Neurais Recorrentes, 
                        como <i>Long Short-Term Memory</i> (LSTM).
                    '''
                    )

    st.markdown('<br>', unsafe_allow_html=True)

    # título
    st.markdown('''#### Modelos de *Ensemble Learning*''')
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                    O preço do petróleo é influenciado por diversos fatores, como oferta e demanda.
                    Além disso, eventos globais, como guerras e desastres naturais, também podem afetá-lo.
                    Logo, essa série temporal não é estacionária e possui comportamento não linear. Fatos inesperados, 
                    como os apresentados na seção "Análise", não são facilmente capturados por um único modelo.<br><br>
                    - <b>Próximo passo:</b> empregar a técnica de <i>ensemble learning</i> para combinar modelos.
                    <br>
                </p>
                ''', unsafe_allow_html=True)
    
    # criar insight
    create_insight('Complexidade do Preço do Petróleo', 
                   '''
                        Sugere-se a utilização de <i>ensemble learning</i> para combinar modelos de previsão.
                        Esses modelos não precisam se voltar apenas ao preço do petróleo, mas também a outros fatores fundamentais - como produção e mercado.<br>
                        Um modelo de classificação para prever "alta" ou "baixa" do preço do petróleo pode compor uma <i>feature</i> adicional.<br>
                        Redes Neurais Convolucionais, ou <i>Convolutional Neural Networks</i> (CNN) são eficazes para análise de imagens de satélite e previsão de eventos climáticos.
                        CNNs também podem ser usadas para previsão, a partir de gráficos de <i>candlestick</i>, utilizados por <i>traders</i> para análise técnica.
                    ''')
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('''#### Análise de Sentimentos & Mercado Futuro''')

    st.markdown('''
                <p style="font-size: 18px">
                    A análise de sentimentos é uma técnica de Processamento de Linguagem Natural,
                    ou <i>Natural Language Processing</i> (NLP), que visa identificar e classificar a polaridade 
                    emocional de um texto. Ela utiliza algoritmos e modelos de aprendizado de máquina para 
                    atribuir uma pontuação de sentimento a cada trecho, indicando se é positivo, negativo ou neutro.
                    Para melhoria do modelo, um passo importante é a construção de uma <i>feature</i> que 
                    capture a opinião pública sobre o mercado de petróleo em tempo real, a partir de notícias e redes sociais. 
                    Implementar esses sentimentos no modelo ajuda a incorporar tendências emergentes e 
                    mudanças de humor que não seriam capturadas apenas por dados históricos de preços.<br><br>
                    - <b>Próximo passo:</b> integrar o modelo com outras fontes de dados sobre o mercado de futuro.
                    <br>
                </p>
                ''', unsafe_allow_html=True)

    create_insight('Mercado Futuro & Análise de Sentimento', 
                     '''
                        A análise de sentimento também contribui para a estabilidade das previsões, 
                        conforme medido pelo EV (<i>Error Variance</i>, ou Variância do Erro). A adição de sentimentos extraídos por textos 
                        tende a estabilizar os resultados, reduzindo a variabilidade das previsões e tornando-as mais confiáveis.<br>
                        Além disso, criar features baseadas em contratos futuros de petróleo e ajudará a 
                        entender dados de extração e estoque. Também, o volume de transações no mercado de futuro é componente essencial para o cálculo 
                        de outros indicadores técnicos, como o <i>Open Interest</i>, que mede o número de contratos em aberto.
                      ''')
    
    st.markdown('<br>', unsafe_allow_html=True)    
    
    # título
    st.markdown('''#### Database na Nuvem''')
    # texto
    st.markdown('''
                <p style="font-size: 18px">
                    MLOps é uma prática que visa integrar o desenvolvimento de modelos de Machine Learning 
                    com a operação de sistemas. Para essa etapa, é importante criar um pipeline de dados.<br><br>
                    - <b>Próximo passo:</b> <i>deploy</i> da aplicação na nuvem, com a Amazon Web Services (AWS).<br>
                        * <b>Amazon S3</b> para armazenamento do modelo<br>
                        * <b>Amazon Redshift</b> para armazenamento dos dados estruturados<br>
                        * <b>Amazon Glue</b> para ETL - <i>Extract Transform Load</i><br>
                        * <b>Amazon SageMaker</b> para treinamento de modelos de Machine Learning<br>
                </p>
                ''', unsafe_allow_html=True)

    # criar insight
    create_insight(
                    'Vantagens de um Database na Nuvem',
                   '''
                        - Escalabilidade: aumenta ou diminui a capacidade de armazenamento conforme a demanda.<br>
                        - Segurança: os dados são armazenados em servidores seguros e protegidos por criptografia.<br>
                        - Acessibilidade: os dados podem ser acessados de qualquer lugar e a qualquer momento.<br>
                        - Backup: salvamento automático de dados, que podem ser recuperados em caso de falhas.<br>
                        - Integração: integração com outras ferramentas, como pipelines de dados e APIs.
                        '''
                     )
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('''#### Desenvolver API''')

    st.markdown('''<p style="font-size: 18px">
                API, ou <i>Application Programming Interface</i>, é um conjunto de regras e protocolos que 
                permitem a comunicação entre sistemas.<br><br>
                - <b>Próximo passo:</b> criar API para disponibilizar o modelo para usuários e outras aplicações.
                <br>
                </p>
                ''', unsafe_allow_html=True)
                        
    # criar insight
    create_insight('API', 
                   '''
                        - Facilita o acesso às previsões do modelo, permitindo que outras aplicações e sistemas consumam os dados.<br>
                        - Pode ser utilizada para criar dashboards, relatórios e aplicações web que consomem as previsões do modelo.<br>
                        - Permite integração com outros sistemas, como CRMs (<i>Customer Relationship Management</i>) e 
                          ERPs (<i>Enterprise Resource Planning).
                    ''')
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    
# referências        
else:
    st.title('Referências')
    st.markdown('<br>', unsafe_allow_html=True)
    # subtítulo
    st.header('Fontes de dados')
    st.markdown('''
                <p style="font-size: 18px">
                    Os dados utilizados neste projeto foram obtidos a partir das fontes listadas abaixo:
                </p>
                ''', unsafe_allow_html=True)
    
    # lista de fontes de dados
    st.markdown('''
                #### [**IPEA**](http://www.ipeadata.gov.br/Default.aspx) - Instituto de Pesquisa Econômica Aplicada
                Portal de dados econômicos do governo brasileiro, disponibiliza dados de diversos indicadores econômicos, 
                como inflação, PIB, taxa de juros, câmbio e preços de *commodities*. As séries temporais podem ser baixadas 
                em formato `.csv`. O IPEA também permite acesso através de requisições `HTTP` por meio de API.
                ''')
    
    with st.expander('🐍 Exibir código Python'):
        st.code('''
                # acessar dados do IPEA
                
                !pip install ipeadatapy                 # instalar biblioteca
                import ipeadatapy as ipea               # importar biblioteca
                
                #ipea.list_series()                     # lista de séries disponíveis
                
                df = ip.timeseries(ipea_table_code)     # obter dados do petróleo Brent
                ''')
    
    st.markdown('''
                #### [**FRED**](https://fred.stlouisfed.org/series/DCOILBRENTEU) - Federal Reserve Economic Data
                Banco de dados econômicos mantido pelo Federal Reserve Bank of St. Louis, nos EUA. 
                Ele contém uma vasta quantidade de dados econômicos, incluindo séries temporais de preços de *commodities*, 
                como o [**petróleo Brent**](https://fred.stlouisfed.org/series/DCOILBRENTEU).
                Os dados podem ser baixados em formato `.csv`. O FRED disponibiliza também permite acesso através de requisições `HTTP` por meio de API.
                ''')

    with st.expander('🐍 Exibir código Python'):
        st.code('''
                    # acessar dados do FRED
                    
                    !pip install pandas_datareader            # instalar biblioteca
                    import pandas_datareader as pdr           # importar biblioteca
                    
                    df = pdr.get_data_fred('DCOILBRENTEU')    # obter dados do petróleo Brent
                ''')

    st.markdown('''
                #### [**Yahoo Finance**](https://finance.yahoo.com/quote/CL=F?p=CL=F) - Yahoo Finance
                Plataforma de notícias e dados financeiros, permite acessar cotações de ativos, índices 
                e preços de *commodities*. Os dados podem ser baixados em formato `.csv` e também acessados por meio de API.
                A biblioteca [`yfinance`](https://pypi.org/project/yfinance/) permite acessar os dados do Yahoo Finance diretamente no Python:
                ''')
    
    with st.expander('🐍 Exibir código Python'):
        st.code('''
                    # acessar dados do Yahoo Finance
                    
                    !pip install yfinance            # instalar biblioteca
                    import yfinance as yf            # importar biblioteca
                    
                    df = yf.download('BZ=F')         # obter dados do petróleo Brent
                ''')

    st.markdown('<br>', unsafe_allow_html=True)
    # subtítulo para Bibliografia
    st.header('Bibliografia')
    # lista de links
    st.markdown('''
                    - [**OPEC**](https://www.opec.org/opec_web/en/about_us/24.htm) - Organization of the Petroleum Exporting Countries
                    - [**CBI**](https://cbie.com.br/) - Centro Brasileiro de Infraestrutura
                    - [**Investopedia**](https://www.investopedia.com/terms/f/futuresmarket.asp) - Futures Market
                    - [**Wikipedia**](https://en.wikipedia.org/wiki/Brent_Crude) - Brent Crude Oil
                    - [**AWS**](https://aws.amazon.com/pt/) - Amazon Web Services
                    - [**Super Interessante**](https://super.abril.com.br/coluna/deriva-continental/nos-bastidores-da-terra-geologa-explica-a-formacao-do-petroleo) - Nos bastidores da Terra: geóloga explica a formação do petróleo
                    - [**Forecasting Oil Price Using Web-based Sentiment Analysis**](https://www.mdpi.com/1996-1073/12/22/4291) - 
                        Energies (2019), por ZHAO, Lu-Tao; ZENG, Guan-Rong; WANG, Wen-Jing; ZHANG, Zhi-Gang
                    - [**Análise prática de séries temporais: predição com estatística e aprendizado de máquina**](https://www.amazon.com.br/Análise-Prática-Séries-Temporais-Estatística/dp/8550815624) - 
                        Alta Books (2021), por NIELSEN, Aileen
                ''')
    
    
# footer
st.markdown('<br>', unsafe_allow_html=True)

st.markdown('---')

# texto -> Agradecimentos
st.markdown('''<p style="font-size: 18px; text-align: center;">
            Obrigado por acompanhar este projeto! 🚀
            <br>
            </p>''', unsafe_allow_html=True)

linkedin = 'https://www.linkedin.com/in/viniplima/'
github = 'https://github.com/euvina/'

mail = 'pradolimavinicius@gmail.com'
subject = 'Contato via Streamlit - Projeto Previsão de Preço do Petróleo Brent'

# área de contato
st.markdown('''<p style="font-size: 18px; text-align: center;">
            📧 Entre em contato:<br>
            <a href="mailto:{}?subject={}">
            <img src="https://img.shields.io/badge/-Gmail-D14836?style=for-the-badge&logo=Gmail&logoColor=white" alt="Gmail">
            </a>
            <a href="{}">
            <img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white" alt="GitHub">
            </a>
            <a href="{}">
            <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=LinkedIn&logoColor=white" alt="LinkedIn">
            </a>
            </p>'''.format(mail, subject, linkedin, github), unsafe_allow_html=True)
