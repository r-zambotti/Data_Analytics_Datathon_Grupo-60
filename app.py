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
import requests

#from keras.models import Sequential
#from keras.layers import LSTM, Dense
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

from PIL import Image

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
                   page_title='Associação Passos Mágicos - Tech Challenge - FIAP', 
                   page_icon='🌟', initial_sidebar_state='auto')

#Dados
url = "https://github.com/wesleyesantos/Postech-Datathon/raw/main/PEDE_PASSOS_DATASET_FIAP.csv"
url1 = "https://github.com/4ca63473-734d-4d8c-8181-9635c1837ddc"
response = requests.get(url)
csv_data = response.content
response1 = requests.get(url1)
file_data = response1.content

# paginação
page_0 = 'Introdução ✨'
page_1 = 'Análise Exploratória 🎲'
page_2 = 'Dashboard 📈'
page_3 = 'Conclusão'
page_4 = 'Referências'

# menu lateral
st.sidebar.title('Menu')
page = st.sidebar.radio('Selecione a página:', 
                        [page_0, page_1, page_2, page_3, page_4])
     
# Introdução
if page == page_0:
    
    # título da página
    st.title('Impacto causado pela ONG Passos Mágicos 💫')
    
    # descrição
    st.markdown('''
                Analisando impacto causado pelas ações voluntárias da ONG Passos Mágicos, desenvolvendo uma análise exploratória, gerando insight e dashboard interativos.<br> 
                <br>Desenvolvido para a <b>Pós-Tech Data Analytics — FIAP</b>.
                ''', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    
    create_warning('Importante', 
                   '''
                        Este artigo tem fins exclusivamente educacionais.<br><br>
                        Para acessar os Dados do projeto, clicar na opção abaixo "Nota Técnica". 
                    ''')
    
    st.markdown('<br>', unsafe_allow_html=True)

    # expansão com nota técnica
    with st.expander('🗒️ Nota Técnica'):
        st.markdown('''
        #### Dados do projeto

        **🚀 Objetivo**: Analisar impacto causado pela ONG Passos Mágicos.

        ---
        
        **🛸 Modelos**: os dados utilizados para análise e treinamento no modelo foram coletados em 18/05/2024 e correspondem ao período de 20/05/1987 a 13/05/2024.
        - [XGBoost](https://xgboost.readthedocs.io/en/stable/)
        - [Prophet](https://facebook.github.io/prophet/)

        ---
        
        **📡 Base de Dados e Dicionário**:
        ''')

        tab9, tab10 = st.tabs(tabs=['Base de Dados', 'Dicionário'])

        with tab9:
            st.markdown('''Base de dados PEDE (Pesquisa Extensiva do Desenvolvimento Educacional)''',unsafe_allow_html=True)
            
            st.download_button(label="Baixar Base PEDE (csv)",data=csv_data,file_name="PEDE_PASSOS_DATASET_FIAP.csv",mime="text/csv")

        with tab10:
            st.markdown('''###### <font color='blue'>Estrutura da Base''',unsafe_allow_html=True)
            st.download_button(label="Dicionário da base PEDE",data=file_data,file_name="Dicionário dados PEDE.pdf",mime="application/pdf")

            st.markdown('''###### <font color='blue'>Estrutura da Base''',unsafe_allow_html=True)
            data_dict = {
            "INSTITUICAO_ENSINO_ALUNO_2020": "Mostra instituição de Ensino do Aluno em 2020",
            "NOME": "Nome do Aluno (dados estão anonimizados)",
            "IDADE_ALUNO_2020": "Idade do Aluno em 2020",
            "PEDRA_2020": "Classificação do Aluno baseado no número do INDE (2020), o conceito de classificação é dado por: Quartzo – 2,405 a 5,506 / Ágata – 5,506 a 6,868 / Ametista – 6,868 a 8,230 / Topázio – 8,230 a 9,294",
            "IAA_2020": "Indicador de Auto Avaliação – Média das Notas de Auto Avaliação do Aluno em 2020",
            "IEG_2020": "Indicador de Engajamento – Média das Notas de Engajamento do Aluno em 2020",
            "IPS_2020": "Indicador Psicossocial – Média das Notas Psicossociais do Aluno em 2020",
            "IDA_2020": "Indicador de Aprendizagem - Média das Notas do Indicador de Aprendizagem 2020",
            "IPP_2020": "Indicador Psicopedagógico – Média das Notas Psicopedagógicas do Aluno em 2020",
            "IPV_2020": "Indicador de Ponto de Virada – Média das Notas de Ponto de Virada do Aluno em 2020",
            "IAN_2020": "Indicador de Adequação ao Nível – Média das Notas de Adequação do Aluno ao nível atual em 2020",
            "INDE_2020": "Índice do Desenvolvimento Educacional – Métrica de Processo Avaliativo Geral do Aluno, dado pela ponderação dos indicadores: IAN, IDA, IEG, IAA, IPS, IPP e IPV em 2020.",
            "DESTAQUE_IEG_2020": "Observações dos Avaliadores Sobre o Aluno referente ao 'Indicador de Engajamento' em 2020",
            "DESTAQUE_IDA_2020": "Observações dos Avaliadores Sobre o Aluno referente ao 'Indicador de Aprendizagem' em 2020",
            "DESTAQUE_IPV_2020": "Observações dos Avaliadores Sobre o Aluno referente ao 'Indicador de Ponto de Virada' em 2020",
            "PONTO_VIRADA_2020": "Campo do Tipo Booleano que sinaliza se o Aluno atingiu o 'Ponto de Virada' em 2020",
            "PEDRA_2021": "Classificação do Aluno baseado no número do INDE (2021), o conceito de classificação é dado por: Quartzo – 2,405 a 5,506 / Ágata – 5,506 a 6,868 / Ametista – 6,868 a 8,230 / Topázio – 8,230 a 9,294",
            "IAA_2021": "Indicador de Auto Avaliação – Média das Notas de Auto Avaliação do Aluno em 2021",
            "IEG_2021": "Indicador de Engajamento – Média das Notas de Engajamento do Aluno em 2021",
            "IPS_2021": "Indicador Psicossocial – Média das Notas Psicossociais do Aluno em 2021",
            "IDA_2021": "Indicador de Aprendizagem - Média das Notas do Indicador de Aprendizagem 2021",
            "IPP_2021": "Indicador Psicopedagógico – Média das Notas Psicopedagógicas do Aluno em 2021",
            "IPV_2021": "Indicador de Ponto de Virada – Média das Notas de Ponto de Virada do Aluno em 2021",
            "IAN_2021": "Indicador de Adequação ao Nível – Média das Notas de Adequação do Aluno ao nível atual em 2021",
            "INDE_2021": "Índice do Desenvolvimento Educacional – Métrica de Processo Avaliativo Geral do Aluno, dado pela ponderação dos indicadores: IAN, IDA, IEG, IAA, IPS, IPP e IPV em 2021.",
            "REC_EQUIPE_1_2021": "Recomendação: da Equipe de Avalição: 1 em 2021",
            "REC_EQUIPE_2_2021": "Recomendação: da Equipe de Avalição: 2 em 2021",
            "REC_EQUIPE_3_2021": "Recomendação: da Equipe de Avalição: 3 em 2021",
            "REC_EQUIPE_4_2021": "Recomendação: da Equipe de Avalição: 4 em 2021",
            "REC_PSICO_2021": "Mostra qual a recomendação da equipe de psicologia sobre o Aluno em 2021",
            "PONTO_VIRADA_2021": "Campo do Tipo Booleano que sinaliza se o Aluno atingiu o 'Ponto de Virada' em 2021",
            "PEDRA_2022": "Classificação do Aluno baseado no número do INDE (2022), o conceito de classificação é dado por: Quartzo – 2,405 a 5,506 / Ágata – 5,506 a 6,868 / Ametista – 6,868 a 8,230 / Topázio – 8,230 a 9,294",
            "IAA_2022": "Indicador de Auto Avaliação – Média das Notas de Auto Avaliação do Aluno em 2022",
            "IEG_2022": "Indicador de Engajamento – Média das Notas de Engajamento do Aluno em 2022",
            "IPS_2022": "Indicador Psicossocial – Média das Notas Psicossociais do Aluno em 2022",
            "IDA_2022": "Indicador de Aprendizagem - Média das Notas do Indicador de Aprendizagem 2022",
            "IPP_2022": "Indicador Psicopedagógico – Média das Notas Psicopedagógicas do Aluno em 2022",
            "IPV_2022": "Indicador de Ponto de Virada – Média das Notas de Ponto de Virada do Aluno em 2022",
            "IAN_2022": "Indicador de Adequação ao Nível – Média das Notas de Adequação do Aluno ao nível atual em 2022",
            "INDE_2022": "Índice do Desenvolvimento Educacional – Métrica de Processo Avaliativo Geral do Aluno, dado pela ponderação dos indicadores: IAN, IDA, IEG, IAA, IPS, IPP e IPV em 2022.",
            "REC_PSICO_2022": "Mostra qual a recomendação da equipe de psicologia sobre o Aluno em 2022",
            "REC_AVA_1_2022": "Recomendação da Equipe de Avalição 1 em 2022",
            "REC_AVAL_2_2022": "Recomendação da Equipe de Avalição: 2 em 2022",
            "REC_AVAL_3_2022": "Recomendação da Equipe de Avalição: 3 em 2022",
            "REC_AVAL_4_2022": "Recomendação da Equipe de Avalição: 4 em 2022",
            "DESTAQUE_IEG_2022": "Observações dos Mestres Sobre o Aluno referente ao 'Indicador de Engajamento' em 2022",
            "DESTAQUE_IDA_2022": "Observações dos Mestres Sobre o Aluno referente ao 'Indicador de Aprendizagem' em 2022",
            "DESTAQUE_IPV_2022": "Observações dos Mestres Sobre o Aluno referente ao 'Indicador de Ponto de Virada' em 2022",
            "PONTO_VIRADA_2022": "Campo do Tipo Booleano que sinaliza se o Aluno atingiu o 'Ponto de Virada' em 2022",
            "INDICADO_BOLSA_2022": "Campo do Tipo Booleano que sinaliza se o Aluno foi indicado para alguma Bolsa no Ano de 2022"
            }

            df = pd.DataFrame(list(data_dict.items()), columns=["Nome da Coluna", "Detalhamento dos dados"])

            st.markdown('''A base contém 50 colunas referente ao período de 2020 a 2022, com colunas adicionais no decorrer dos anos.''', unsafe_allow_html=True)

            st.table(df)    
            
        st.markdown('''        
        ---
        
        **📡 Fontes de dados**:
        - [IPEA](http://www.ipeadata.gov.br/Default.aspx)
        - [FRED](https://fred.stlouisfed.org/series/DCOILBRENTEU)
        - [Yahoo Finance](https://finance.yahoo.com/quote/CL=F?p=CL=F)

        ---
        
        **🧑🏻‍🚀 Autores**: 
        - [Victor Novais de Oliveira](https://www.linkedin.com)
        - [Rodrigo Zambotti de Andrade](https://www.linkedin.com)
        - [Arencio Job Pereira](https://www.linkedin.com)  
        - [Bruno Akio Matsuzaki Shimada](https://www.linkedin.com)                     

        ---
        
        **🪐 Repositório**: 
        - [GitHub](https://github.com/r-zambotti/Data_Analytics_Datathon_Grupo-60.git)

        ---
        
        ''')
    
    st.markdown('---')
    
    # contexto para o objeto de estudo
    st.markdown('## Sobre a Associação Passos Mágicos')
    
    st.markdown('''
                <p style="font-size: 18px">
                A Associação Passos Mágicos tem uma trajetória de 30 anos de atuação, trabalhando na transformação da vida de crianças e jovens de baixa renda os levando a melhores oportunidades de vida.<br>

                A transformação, idealizada por Michelle Flues e Dimetri Ivanoff, começou em 1992, atuando dentro de orfanatos, no município de Embu-Guaçu.
                Em 2016, depois de anos de atuação, decidem ampliar o programa para que mais jovens tivessem acesso a essa fórmula mágica para transformação.
                Passaram então a atuar como um projeto social e educacional, criando assim a Associação Passos Mágicos.
                </p>
                ''', unsafe_allow_html=True)  
    
    create_quote('''
            "Investir em educação é plantar as sementes de um futuro promissor para cada criança".<br>
            ''','- Associação Passos Mágicos')

    # contexto missão, programas e impactos - menu de tabelas
    tab1, tab2, tab3 = st.tabs(
    tabs=["Missão e Visão", "Programas e Atividades", "Impacto e Resultados"])

    with tab1:
        st.markdown('''
                    <p style="font-size: 18px">
                    🎯<b> Missão:</b> A missão da Passos Mágicos é transformar a vida de jovens e crianças, fornecendo ferramentas que os levem a melhores oportunidades de vida. <br><br>
                    👁 <b> Visão:</b> A visão da organização é viver em um Brasil onde todas as crianças e jovens tenham iguais oportunidades para realizar seus sonhos e se tornem agentes transformadores de suas próprias vidas.
                    </p>
                    ''', unsafe_allow_html=True)

    with tab2:
        st.markdown(''' 
                    <p style="font-size: 18px">
                    A Passos Mágicos oferece uma variedade de programas educacionais e de apoio, incluindo:
                    </p>
                    ''', unsafe_allow_html=True)
        
        st.markdown('''- <b>Educação de qualidade:</b> Acesso a ensino de alta qualidade para crianças e jovens;            
                    ''', unsafe_allow_html=True)
        
        st.markdown('''- <b>Assistência psicológica e psicopedagógica:</b> Suporte emocional e educacional para ajudar no desenvolvimento integral dos alunos;
                    ''', unsafe_allow_html=True)
        
        st.markdown('''- <b>Ampliação da visão de mundo: </b>Projetos de intercâmbio e apadrinhamento que visam integrar os alunos a diferentes culturas e ambientes;
                    ''', unsafe_allow_html=True)
        
        st.markdown('''- <b>Campanhas de arrecadação:</b> Anualmente, são promovidas campanhas para arrecadar fundos e presentes para as crianças e adolescentes atendidos pela instituição.
                    ''', unsafe_allow_html=True)

    with tab3:
        st.markdown('''
                    <p style="font-size: 18px">
                    Desde sua fundação, a Passos Mágicos tem expandido significativamente seu alcance e impacto. 
                    Em 2016, a organização formalizou-se como um projeto social e educacional, ampliando suas atividades para beneficiar mais jovens. Atualmente, 
                    a instituição atende centenas de crianças e adolescentes, oferecendo bolsas de estudo, suporte psicológico e oportunidades de intercâmbio.
                    </p>
                    ''', unsafe_allow_html=True)
        
    st.markdown('---')

    # Inserindo imagem da ONG Passos Mágicos

    image =  Image.open("img/passos_magicos.png")
    st.image(image, caption= "Imagem oficial da ONG Passos Mágicos")
    
# Análise Exploratória
elif page == page_1:

    st.title('Análise Exploratória 🔎')
    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('''
                A análise Exploratória do projeto foi realizada com a base <b><font color='blue'>PEDE (Pesquisa Extensiva do Desenvolvimento Educacional)</b></font> da Passos Mágicos e foi disponibilizada toda documentação 
                explicando como foram criadas cada índice e métricas já existentes. A PASSOS MÁGICOS utiliza uma métrica chamada <b><font color='blue'>INDE (Índice Nacional de Desenvolvimento Educacional)</b></font> para avaliar 
                os alunos essa métrica é composta por alguns indicadores que são separados em 3 dimensões principais onde avaliam vários critérios como adequação de nível, desempenho acadêmico, engajamento, autoavaliação, aspectos 
                psicossociais e psicopedagógicos, essas dimensões estão divididas conforme abaixo e cada uma delas trazem os seguintes indicadores:
                ''', unsafe_allow_html=True)
    
    st.markdown('''
                - Dimensão acadêmica: Com os indicadores IEG, IDA e IAN
                ''',  unsafe_allow_html=True)
    
    st.markdown('''
                - Dimensão psicossocial: Com os indicadores IAA e IPS
                ''',  unsafe_allow_html=True)
    
    st.markdown('''
                - Dimensão psicopedagógica: Com os indicadores IPP e IPV
                ''',  unsafe_allow_html=True)

    st.markdown('''
                Quanto ao <b><font color='blue'>INDE </b></font> geral tem uma média de 7,07, obtendo uma variação bem grande entre o mínimo de 2,46 e máximo de 9,71; 
                ao realizar a análise por ano podemos observar que tem um aumento na quantidade de alunos e os níveis do INDE caem, nos trazendo o desafio de começar a segregar essa informação para buscar o gap.
                ''', unsafe_allow_html=True) 

    st.markdown('''
                O indicador <b><font color='blue'>IDA</b></font> se sobresai como o mais baixo de todos os anos que é um indicador de participação dos projetos e atividades pedagógicas, 
                e devido a esse defasamento o maior indicador que temos é o <b><font color='blue'>IAA</b></font> que é o indice de atenção psicológica e psicopedagógica aos alunos.
                ''', unsafe_allow_html=True)

    #Análise dos Indicadores
    st.subheader('Análise dos Indicadores', divider='orange')

    #Divindo cada indicador em selectbox para melhor visualização
    indicador = st.selectbox('Selecione o indicador:', ['INDE','Pedras','IEG', 'IDA', 'IAN', 'IAA', 'IPS', 'IPP', 'IPV', 'Ponto de Virada'])

    #Tabela INDE
    if indicador == 'INDE':
        
        st.markdown('''
                    <p style="font-size: 18px">
                    O <b><font color='blue'>Índice de Desenvolvimento Educacional (INDE)</b></font> da Associação Passos Mágicos é uma métrica utilizada para avaliar o progresso educacional dos alunos atendidos pela instituição. 
                    Esse índice é calculado com base em diversos fatores, incluindo:
                    </p>
                    ''', unsafe_allow_html=True)    
        
        st.markdown('''
                    - <b><font color='blue'>Desempenho Acadêmico:</b></font> Avaliação das notas dos alunos em disciplinas como Português, Matemática e Inglês.
                    ''', unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Apoio Psicológico e Psicopedagógico:</b></font> Impacto das intervenções psicológicas e psicopedagógicas no desenvolvimento dos alunos.
                    ''', unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Participação em Atividades Extracurriculares:</b></font> Envolvimento dos alunos em atividades que ampliam sua visão de mundo, como intercâmbios e projetos culturais.
                    ''', unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Evolução ao Longo do Ano:</b></font> Comparação das notas e do desenvolvimento dos alunos entre o início e o final do ano letivo.
                    ''', unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">
                    O INDE é uma ferramenta crucial para a Passos Mágicos, pois permite monitorar e ajustar suas estratégias educacionais, garantindo que cada aluno receba o suporte necessário para alcançar seu pleno potencial.
                    </p>
                    ''', unsafe_allow_html=True)

    #Tabela Pedras
    if indicador == 'Pedras':

        st.markdown('''
                    As <b><font color='blue'>Pedras</b></font> podem ser definidas como o quanto os alunos estão pontuando, então ele entra num esquema de classificação, 
                    o que traz mais clareza na análise e atenção para o desenvolvimento de cada aluno e também dá uma visão mais competitiva aos alunos, porém eles irão almejar as melhores classificações. 
                    Até o último relatório PEDE tinhamos 4 pedras que são:
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Quartzo:</b></font> Alunos com INDE entre <b><font color='blue'>2,405 a 5,506</b></font>.
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Ágata:</b></font> Alunos com INDE entre <b><font color='blue'>5,506 a 6,868</b></font>.
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Ametista:</b></font> Alunos com INDE entre <b><font color='blue'>6,868 a 8,230</b></font>.
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    - <b><font color='blue'>Topázio:</b></font> Alunos com INDE entre <b><font color='blue'>8,230 a 9,294</b></font>.
                    ''',unsafe_allow_html=True)
        
    #Tabela IEG    
    if indicador == 'IEG':

        st.markdown('''
                    ###### <font color='blue'>IEG (Índice de Engajamento Global)
                    ''',unsafe_allow_html=True )
        
        st.markdown('''
                    Avalia o nível de envolvimento dos alunos em atividades extracurriculares e programas de intercâmbio. Este índice é importante para entender como as experiências 
                    fora da sala de aula contribuem para o desenvolvimento pessoal e acadêmico dos alunos.
                    ''')

    #Tabela IDA
    if indicador == 'IDA':

        st.markdown('''
                    ###### <font color='blue'>IDA (Índice de Desenvolvimento Acadêmico)
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    Mede o progresso acadêmico dos alunos, considerando notas, frequência escolar e participação em atividades educacionais. 
                    Este índice ajuda a identificar áreas que necessitam de melhorias e a eficácia das intervenções pedagógicas.
                    ''')

    #Tabela IAN
    if indicador == 'IAN':

        st.markdown('''
                    ######  <font color='blue'>IAN (Índice de Aproveitamento Nutricional)
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    Avalia a qualidade da alimentação fornecida às crianças e jovens, medindo o impacto da nutrição no desempenho escolar e no bem-estar geral dos alunos.
                    ''')
        
    #Tabela IAA
    if indicador == 'IAA':

        st.markdown('''
                    ######  <font color='blue'>IAA (Índice de Atendimento e Acompanhamento)
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    Mede a qualidade e a frequência do atendimento psicológico e psicopedagógico oferecido aos alunos. 
                    Este índice é crucial para garantir que os alunos recebam o suporte necessário para superar desafios emocionais e acadêmicos.
                    ''')
        
    #Tabela IPS
    if indicador == 'IPS':

        st.markdown('''
                    ######  <font color='blue'>IPS (Índice de Participação Social)
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    Avalia o envolvimento dos alunos em atividades comunitárias e projetos sociais. Este índice ajuda a medir o impacto dos programas da Passos Mágicos na formação de cidadãos conscientes e ativos na sociedade.
                    ''')
        
    #Tabela IPP
    if indicador == 'IPP':

        st.markdown('''
                    ###### <font color='blue'>IPP (Índice de Progresso Pessoal)
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    Mede o desenvolvimento pessoal dos alunos, considerando aspectos como autoestima, habilidades sociais e resiliência. 
                    Este índice é importante para avaliar o impacto das intervenções da Passos Mágicos no crescimento pessoal dos alunos.
                    ''')
        
    #Tabela IPV
    if indicador == 'IPV':

        st.markdown('''
                    ###### <font color='blue'>IPV (Índice de Permanência e Valorização)
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    Avalia a taxa de retenção dos alunos nos programas da Passos Mágicos e a valorização dos mesmos pelos beneficiários e suas famílias. 
                    Este índice é fundamental para entender a satisfação e o comprometimento dos alunos com os programas oferecidos.
                    ''')
        
    #Tabela Ponto de Virada   
    if indicador == 'Ponto de Virada':
        
        st.markdown(''' 
                    O Ponto de virada indica que o aluno atingiu um passo mágico, é a conquista de uma habilidade fundamental, 
                    é medido através das notas, avaliações e outros dados, e demonstra que o aluno teve um grande progresso, 
                    essa evolução o ajudará a enfrentar vários desafios que encontrará pela frente, assim como:
                    ''' )
        
        st.markdown('''
                    - Os alunos poderão superar dificuldades em matérias específicas e melhorar seu desempenho acadêmico,
                    - Isso pode incluir avanços em leitura, matemática, ciências e outras áreas,
                    - O ponto de virada traz consigo uma sensação de realização e confiança,
                    - Os alunos se sentirão mais capazes e confiantes em suas habilidades,
                    - Eles desenvolverão habilidades de comunicação, resolução de conflitos, empatia e trabalho em equipe,
                    - Isso os ajudará a lidar com situações sociais e emocionais,
                    - O ponto de virada também envolve uma ampliação da visão de mundo,
                    - Os alunos estarão mais abertos a diferentes culturas, perspectivas e oportunidades,
                    - Os alunos serão incentivados a assumir o protagonismo em suas vidas,
                    - Eles tomarão decisões mais conscientes e terão maior autonomia,
                    - O ponto de virada ensina a importância da persistência e da resiliência,
                    - Os alunos saberão que podem superar obstáculos com esforço contínuo.
                    ''')

    # carregar dados
    # data = pd.read_parquet(r'data/data_w_indicators.parquet')
    # # sidebar - adicionar filtros
    # st.sidebar.title('⚙️ Filtros')
    # # filtros de ano com slider
    # min_year = data.index.year.min()
    # min_year = int(min_year)
    # max_year = data.index.year.max()
    # max_year = int(max_year)
    # # filtro de preço com slider
    # min_price = data['brent'].min()
    # min_price = int(min_price)
    # max_price = data['brent'].max()
    # max_price = int(max_price)

# Dashboard
elif page == page_2:
    # título
    st.title('Modelos de Previsão')
#     # seleção de modelo
#     model = st.selectbox('Selecione o modelo:', ['XGBoost', 'Prophet'])
    
#     st.markdown('<br>', unsafe_allow_html=True)
    
#     if model == 'XGBoost':
#         # texto
#         st.markdown('''
#                     <p style="font-size: 18px">
#                         O XGBoost, ou <i>Extreme Gradient Boosting</i>, é um algoritmo de aprendizado de máquina supervisionado e baseado em árvores de decisão.
#                         O modelo é uma implementação otimizada do Gradient Boosting e pode ser utilizado para problemas de regressão e classificação. O XGBoost é 
#                         amplamente utilizado em competições de ciência de dados e é conhecido por sua eficiência e desempenho.
#                         <br>
#                     </p>
#                     ''', unsafe_allow_html=True)
        
#         with st.expander('🐍 Exibir código Python'):
#             # código
#             st.code('''
#                     # importar o XGBoost
#                     !pip install xgboost                 # instalar biblioteca
#                     import xgboost as xgb                # importar biblioteca
#                     ''')
        
#         # markdown
#         st.markdown('''
#                     <p style="font-size: 18px">
#                         <br>
#                         As colunas categóricas devem ser transformadas em variáveis numéricas antes de treinar o modelo.
#                         Para isso, podemos utilizar a técnica <i>One-Hot Encoding</i>.<br>
#                     </p>
#                     ''', unsafe_allow_html=True)
        
#         # código
#         with st.expander('🐍 Exibir código Python'):
#             st.code('''
#                         # One-Hot Encoding
#                         df = pd.get_dummies(df_baseline, 
#                                 columns=['month', 'year', 'weekday'],
#                                 drop_first=True)
                        
#                         # caracteres minúsculos
#                         df.columns = df.columns.str.lower()
                        
#                         print(f'Quantidade de colunas: {df.shape[1]}')
#                         ''')
        
#         # divider
#         st.markdown('---')
        
#         # selecione o modelo
#         model_type = st.radio('Selecione o modelo:', ['Baseline', 'Final'])
#         if model_type == 'Baseline':
#             # texto
#             # preparação dos dados - título
#             st.markdown('''#### Preparação dos dados''')
#             st.markdown(r'''
#                         <p style="font-size: 18px">
#                         Para o modelo baseline, utilizamos 80% dos dados para treino e 20% para teste.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # baseline - divisão dos dados
#                         X = df_baseline.drop(columns=['brent'])
#                         y = df_baseline['brent']

#                         # train test split
#                         train_baseline_size = int(df_baseline.shape[0] * 0.8)

#                         # 80% treino, 20% teste
#                         X_train_baseline, X_test_baseline = X[:train_baseline_size], X[train_baseline_size:]
#                         y_train_baseline, y_test_baseline = y[:train_baseline_size], y[train_baseline_size:]
#                         ''')
                
#             # gráfico com divisão dos dados
#             baseline_xgb_df = pd.read_parquet(r'data/xgboost_baseline_train_test.parquet')
#             fig = px.line(baseline_xgb_df, x='date', y='brent', 
#                 title='XGBoost Baseline - Treino e Teste', 
#                 color='set', 
#                 color_discrete_map={'train': '#4089FF', 
#                                     'test': '#f6c409'},
#                 template='plotly_dark')
#             # adicionar linha para divisão
#             train_baseline_size = int(baseline_xgb_df.shape[0] * 0.8)
#             fig.add_shape(type='line', 
#                         x0=baseline_xgb_df.iloc[train_baseline_size]['date'],
#                         y0=0, x1=baseline_xgb_df.iloc[train_baseline_size]['date'],
#                         y1=baseline_xgb_df['brent'].max()*1.1,
#                         line=dict(color='white', width=1, dash='dash'))
                            
#             fig.update_layout(title_font_size=20)
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             st.plotly_chart(fig, use_container_width=True)
                
#             st.markdown('''#### Treinamento do modelo''')
#             # selecionar modelo baseline ou final - colocar isso para cima e mudar o código
#             # texto
#             st.markdown('''<p style="font-size: 18px">
#                         Com os dados preparados, podemos treinar o modelo XGBoost. 
#                         Como vamos prever valores de preço, utilizamos a classe XGBRegressor. 
#                         Para o treinamento do modelo baseline, não utilizamos
#                         colunas de indicadores técnicos, como EMA, MACD e RSI.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # Construção do modelo baseline
#                         xgb_baseline = xgb.XGBRegressor(n_estimators=1000,                 # número de árvores
#                                                         max_depth=3,                       # profundidade máxima = 3 níveis
#                                                         booster='gbtree',                  # default
#                                                         early_stopping_rounds=50,          # cessa após 50 iterações sem melhorar
#                                                         objective='reg:squarederror' ,     # função objetivo = erro quadrático
#                                                         learning_rate=0.01,               # taxa de aprendizado menor, para evitar o overfitting
#                                                         random_state=19)                   # para reprodução

#                         # Treinamento do modelo baseline
#                         xgb_baseline.fit(X_train_baseline, y_train_baseline,
#                                         eval_set=[(X_train_baseline, y_train_baseline),    # avaliação no treino
#                                                     (X_test_baseline, y_test_baseline)],   # avaliação no teste
#                                                     verbose=True)                          # exibir resultados durante o treino
#                         ''')
                
#             st.markdown('''<br>''', unsafe_allow_html=True)
                
#             # importância das features
#             importance_baseline_df = pd.read_parquet(r'data/xgboost_baseline_importance.parquet')
            
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Exxon Mobil, o índice SP500 e o ano de 2012 são as features mais importantes no modelo baseline.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # code
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # Importância das features
#                         importance_baseline_df = pd.DataFrame({'feature': X_train_baseline.columns,
#                                                                 'importance': xgb_baseline.feature_importances_})
                        
#                         # Ordenar
#                         importance_baseline_df = importance_baseline_df.sort_values('importance', ascending=False)
#                         ''')
            
#             st.markdown('''<br>''', unsafe_allow_html=True)
            
#             # plot
#             fig = px.bar(importance_baseline_df, x='importance', y='feature',
#                         title='10 Features mais importantes',
#                         labels={'importance': 'Importância', 'feature': 'Feature'},
#                         template='plotly_dark')
#             fig.update_layout(title_font_size=20)
#             fig.update_xaxes(title=None, showgrid=True,
#                              range=[0, importance_baseline_df['importance'].max() * 1.2])
#             fig.update_yaxes(title=None)
#             st.plotly_chart(fig, use_container_width=True)
            
#             # realizar previsões
#             st.markdown('''#### Previsões''')
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Com o modelo treinado, podemos realizar previsões para o preço do petróleo Brent.
#                         </p>
#                         ''', unsafe_allow_html=True)
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # previsões
#                         y_pred_baseline = xgb_baseline.predict(X_test_baseline)
                        
#                         # dataframe com previsões
#                         predictions_baseline_df = pd.DataFrame({'date': X_test_baseline.index,
#                                                                 'brent': y_test_baseline,
#                                                                 'brent_pred': y_pred_baseline})
                        
#                         ''')
#             # plotar previsões
#             baseline_xgb_pred_df = pd.read_parquet(r'data/xgboost_baseline_prediction.parquet')
            
#             fig = px.line(baseline_xgb_pred_df, x='date', y=['brent', 'prediction'],
#                 title='XGBoost Baseline - Predição vs Real', 
#                 color_discrete_map={'brent': '#4089FF', 
#                                     'prediction': '#e34592'},
#                 labels={'variable': 'variável', 'value': 'preço (U$D )'},
#                 template='plotly_dark')
#             fig.update_layout(title_font_size=20)
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             st.plotly_chart(fig, use_container_width=True)
        
#             # métricas
#             st.markdown('''#### Avaliação do modelo''')
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Para avaliar o modelo, utilizamos as métricas RMSE, MAE e MAPE.<br>
#                         </p>
#                         ''', unsafe_allow_html=True)  
#             # RMSE  
#             st.markdown('''
#                         - **RMSE** - *Root Mean Squared Error*, ou Raiz do Erro Quadrático Médio:
#                         ''')
#             st.latex(r'''
#                     RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_{true} - y_{pred})^2}
#                     ''')
#             # MAE
#             st.markdown('''
#                         - **MAE** - *Mean Absolute Error*, ou Erro Médio Absoluto:
#                         ''')
#             st.latex(r'''
#                     MAE = \frac{1}{n} \sum_{i=1}^{n} |y_{true} - y_{pred}|
#                     ''')
#             # MAPE
#             st.markdown('''
#                         - **MAPE** - *Mean Absolute Percentage Error*, ou Erro Percentual Absoluto Médio:
#                         ''')
#             st.latex(r'''
#                     MAPE = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{y_{true} - y_{pred}}{y_{true}} \right| \times 100
#                     ''')
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # importar métricas
#                         from sklearn.metrics import mean_absolute_error, mean_squared_error
                        
#                         # função para calcular MAPE
#                         def mean_absolute_percentage_error(y_true, y_pred) -> float:
#                             return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
                        
#                         # métricas
#                         rmse_baseline = np.sqrt(mean_squared_error(y_test_baseline, y_pred_baseline))
#                         mae_baseline = mean_absolute_error(y_test_baseline, y_pred_baseline)
#                         mape_baseline = mean_absolute_percentage_error(y_test_baseline, y_pred_baseline)
                        
#                         # print
#                         print(f'RMSE: {rmse_baseline:.2f}')
#                         print(f'MAE: {mae_baseline:.2f}')
#                         print(f'MAPE: {mape_baseline:.2f}')
#                         ''')
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#             # botão para exibir scores
#             if st.button('📊 Exibir Scores'):
#                 scores_baseline_df = pd.read_parquet(r'data/xgboost_baseline_scores.parquet')
#                 scores_baseline_df = scores_baseline_df.T
#                 scores_baseline_df.columns = scores_baseline_df.iloc[0]
#                 # drop first row
#                 scores_baseline_df = scores_baseline_df[1:]
#                 # mostrar dataframe
#                 st.dataframe(scores_baseline_df)
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#             baseline_metrics_text = r'''
#                         A RMSE é dada na mesma unidade de medida do dataset original e mostra que o modelo baseline está errando, em média, U$D 23.52.<br>
#                         A MAE é uma métrica absoluta e indica que as previsões do modelo estão desviando, em média, U$D 17.1 do valor real.<br>
#                         A diferença entre RMSE e MAE é que a primeira dá mais peso para erros maiores, 
#                         enquanto a segunda trata todos os erros de forma igual.<br>
#                         A MAPE é uma porcentagem e indica que as previsões do modelo estão desviando, em média, 22.96% do valor real.
#                         '''
#             create_analysis('Resultados do Modelo Baseline', baseline_metrics_text)
            
#             st.markdown('<br>', unsafe_allow_html=True)

                
#         else:
#             # preparação dos dados - título
#             st.markdown('''#### Preparação dos dados''')
#             # texto
#             st.markdown(r'''
#                         <p style="font-size: 18px">
#                         Para a divisão dos dados em treino e teste, a classe TimeSeriesSplit do Scikit-Learn se utiliza do 
#                         método de validação cruzada (ou cross validation), que segmenta os dados de treino em K grupos 
#                         (chamados <i>folds</i>), consecutivos e ordenados. Em seguida, treina o modelo em etapas, a partir 
#                         de um pequeno conjunto inicial, que se expande com mais dados de treino - em direção ao futuro. 
#                         Se K é igual a 5, por exemplo, o modelo é treinado 5 vezes, com volume incremental de dados, onde  
#                         cada nova dobra incorpora os dados da dobra anterior e expande o conjunto de treino. 
#                         Após cada treinamento, o modelo executa previsões, a serem avaliadas pela métrica escolhida pelo usuário.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # modelo final - divisão dos dados
#                         X = df.drop(columns=['brent'])
#                         y = df['brent']
                        
#                         # time series split
#                         tscv = TimeSeriesSplit(n_splits=5)
                        
#                         # iterar sobre as divisões
#                         for train_index, test_index in tscv.split(X):
#                             X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#                             y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#                         ''')
                
#             # gráfico com divisão dos dados
#             df = pd.read_parquet(r'data/data_w_indicators.parquet')
#             X = df.drop(columns=['brent'])
#             y = df['brent']
#             # time series split
#             tscv = TimeSeriesSplit(n_splits=5)
#             # iterar sobre as divisões
#             i = 1
#             for train_index, test_index in tscv.split(X):
#                 X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#                 y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#                 # dataframe com divisões
#                 df_split = df.iloc[test_index]
#                 df_split['set'] = f'set_{i}'
#                 if i == 1:
#                     df_final = df_split
#                 else:
#                     df_final = pd.concat([df_final, df_split])
#                 i += 1
#             # plotar gráfico
#             fig = px.line(df_final, x=df_final.index, y='brent',
#                         title='XGBoost Final - Divisão dos Dados',
#                         color='set', 
#                         template='plotly_dark')
#             fig.update_layout(title_font_size=20)
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             st.plotly_chart(fig, use_container_width=True)
            
#             st.markdown('''#### Treinamento do modelo''')
#             # texto
#             st.markdown('''<p style="font-size: 18px">
#                         A melhor escolha pode ser encontrada através da técnica Grid Search, 
#                         que itera sobre as opções listadas pelo usuário e treina modelos únicos, 
#                         gerados a partir da combinação de todos os parâmetros. 
#                         Vale ressaltar que, quanto mais opções são fornecidas, mais tempo será consumido na execução.
#                         ''', unsafe_allow_html=True)
            
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # Importar Grid Search
#                         from sklearn.model_selection import GridSearchCV
                                                
#                         # Converter X e y para numpy arrays
#                         X = np.array(X)
#                         y = np.array(y)
                        
#                         # Grid Search
#                         params = {'n_estimators': [100, 500, 1000, 2000],
#                                   'max_depth': [3, 5, 7, 9],
#                                   'learning_rate': [0.001, 0.01, 0.1]
                        
#                         xgb_final = xgb.XGBRegressor(objective='reg:squarederror', 
#                                                      random_state=19)
                        
#                         grid_search = GridSearchCV(estimator=xgb_final, 
#                                                 param_grid=params, 
#                                                 scoring='neg_mean_squared_error', 
#                                                 cv=tscv, 
#                                                 verbose=1)
                        
#                         grid_search.fit(X, y)
                        
#                         # Melhores parâmetros
#                         best_params = grid_search.best_params_
#                         # Melhor modelo
#                         best_model = grid_search.best_estimator_
#                         # Melhor score
#                         best_score = grid_search.best_score_
                        
#                         # Criar dataframe com resultados
#                         results_df = pd.DataFrame(grid_search.cv_results_)
#                         results_df = results_df.sort_values(by='rank_test_score')
#                         ''')
#             # plotar importância das features
#             # importância das features
#             importance_final_df = pd.read_parquet(r'data/xgboost_best_importance.parquet')
#             # plot
#             fig = px.bar(importance_final_df, x='importance', y='feature',
#                         title='10 Features mais importantes',
#                         labels={'importance': 'Importância', 'feature': 'Feature'},
#                         template='plotly_dark')
#             fig.update_layout(title_font_size=20)
#             fig.update_xaxes(title=None, showgrid=True,
#                              range=[0, importance_final_df['importance'].max() * 1.2])
#             fig.update_yaxes(title=None)
#             st.plotly_chart(fig, use_container_width=True)
            
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Os anos de 2012, 2011 e 2013 são as features mais importantes para o modelo final.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # resultados
#             st.markdown('''<br>''', unsafe_allow_html=True)
#             st.markdown('''#### Avaliação do modelo''')
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Com isso, treinamos 48 modelos e o melhor foi obtido com os parâmetros:<br>
#                         - <b>n_estimators</b>: 1000<br>
#                         - <b>max_depth</b>: 3<br>
#                         - <b>learning_rate</b>: 0.1<br>
#                         </p>
#                         ''', unsafe_allow_html=True)
#             # previsões
#             st.markdown('''#### Previsões''')
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Com o modelo treinado, realizamos previsões para o preço do petróleo Brent.
#                         </p>
#                         ''', unsafe_allow_html=True)
#             # plotar
#             final_xgb_pred_df = pd.read_parquet(r'data/xgboost_best_prediction.parquet')
#             fig = px.line(final_xgb_pred_df, x='date', y=['brent', 'prediction'],
#                 title='XGBoost Final - Predição vs Real', 
#                 color_discrete_map={'brent': '#4089FF', 
#                                     'prediction': '#e34592'},
#                 labels={'variable': 'variável', 'value': 'preço (U$D )'},
#                 template='plotly_dark')
#             fig.update_layout(title_font_size=20)
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             st.plotly_chart(fig, use_container_width=True)
            
#             # métricas
#             st.markdown('''#### Avaliação do modelo''')
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Para avaliar o modelo, utilizamos as métricas:<br>
#                         </p>
#                         ''', unsafe_allow_html=True)
#             # RMSE
#             st.markdown('''
#                         - **RMSE** - *Root Mean Squared Error*, ou Raiz do Erro Quadrático Médio:
#                         ''')
#             st.latex(r'''
#                     RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_{true} - y_{pred})^2}
#                     ''')
#             # MAE
#             st.markdown('''
#                         - **MAE** - *Mean Absolute Error*, ou Erro Médio Absoluto:
#                         ''')
#             st.latex(r'''
#                     MAE = \frac{1}{n} \sum_{i=1}^{n} |y_{true} - y_{pred}|
#                     ''')
#             # MAPE
#             st.markdown('''
#                         - **MAPE** - *Mean Absolute Percentage Error*, ou Erro Percentual Absoluto Médio:
#                         ''')
#             st.latex(r'''
#                     MAPE = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{y_{true} - y_{pred}}{y_{true}} \right| \times 100
#                     ''')
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#             # botão para exibir scores
#             if st.button('📊 Exibir Scores'):
#                 scores_best_df = pd.read_parquet(r'data/xgboost_best_scores.parquet')
#                 scores_best_df = scores_best_df.iloc[[-1]]
#                 scores_best_df = scores_best_df.T
#                 scores_best_df.columns = scores_best_df.iloc[0]
#                 scores_best_df = scores_best_df[1:]
#                 scores_best_df = scores_best_df.rename(columns={'XGBoost Best5': 'XGBoost Best'})
#                 # mostrar dataframe
#                 st.dataframe(scores_best_df)
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#             create_analysis('Resultados do Modelo Final', 
#                             r'''
#                                 Em comparação com modelo baseline, houve melhora considerável nas métricas de avaliação:<br>
#                                 A RMSE melhorou em 38.08%, a MAE melhorou em 37.51% e a MAPE melhorou em 38.5%
#                              ''')
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#     else:
#         # modelo Prophet
#         # texto
#         st.markdown('''
#                     <p style="font-size: 18px">
#                     O Prophet, criado pelo Facebook em 2008 sob autoria dos cientistas de dados Sean J. Taylor e Ben Letham, 
#                     é uma biblioteca open-source baseada em modelos decomponíveis de séries temporais. 
#                     A ferramenta lida bem com dados ausentes e outliers, e foi projetada para ser fácil de usar. 
#                     O Prophet usa 3 componentes principais para a decomposição: tendência (<i>trend</i>), 
#                     sazonalidade (<i>seasonality</i>) e feriados (<i>holidays</i>). 
#                     Assim, pode ser expressado através da equação:
#                     </p>
#                     ''', unsafe_allow_html=True)
        
#         st.latex(r'''
#                     y(t) = g(t) + s(t) + h(t) + e(t)
#                   ''')
        
#         # text
#         st.markdown('''
#                     Em que:
#                     - Growth g(t): representa a curva de crescimento linear ou logística, para modelar mudanças não periódicas em séries temporais. Por padrão, o Prophet usa o modelo de crescimento linear para as previsões.
#                     - Seasonality s(t): a série de Fourier é usada para modelar efeitos sazonais ou mudanças periódicas (por exemplo: o ciclo semanal, mensal e anual). Para aprender e prever tais efeitos, o Prophet depende da série de Fourier para fornecer um modelo flexível.
#                     - Feriados e eventos h(t): o Prophet considera o efeito de feriados e permite adicionar os parâmetro supper_window e lower_window, que estendem os efeitos dos feriados em torno de suas datas.
#                     - Termo de erro e(t): o termo de erro leva em conta quaisquer mudanças incomuns não acomodadas pelo modelo.
#                     ''')
        
#         # código
#         with st.expander('🐍 Exibir código Python'):
#             st.code('''
#                     # importar o Prophet
#                     !pip install prophet                 # instalar biblioteca
#                     from prophet import Prophet          # importar biblioteca
#                     ''')
        
#         st.markdown('<br>', unsafe_allow_html=True)
        
#         # markdown
#         st.markdown('''
#                     <p style="font-size: 18px">
#                     Para utilizar o Prophet, é necessário criar um dataframe com duas colunas: ds (data) e y (valor).
#                     Em seguida, instanciamos o modelo Prophet, ajustamos os dados de treino e realizamos previsões.
#                     </p>
#                     ''', unsafe_allow_html=True)
        
#         # código
#         with st.expander('🐍 Exibir código Python'):
#             st.code('''
#                     # criar dataframe
#                     df_prophet = df[['date', 'brent']].copy()
#                     df_prophet.columns = ['ds', 'y']
#                     ''')
        
#         # divider
#         st.markdown('---')   
        
#         # selecione o modelo
#         model_type = st.radio('Selecione o modelo:', ['Baseline', 'Final'])
#         if model_type == 'Baseline':
#             # preparação dos dados - título
#             st.markdown('''#### Preparação dos dados''')
#             # texto
#             st.markdown(r'''
#                         <p style="font-size: 18px">
#                         Para o modelo baseline, utilizaremos as colunas sp500, exxon e bp como regressores. Além disso,
#                         utilizaremos 80% dos dados para treino e 20% para teste.
#                         </p>
#                         ''', unsafe_allow_html=True)

#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # baseline - divisão dos dados
#                         baseline_train_size = int(len(df_baseline) * 0.8)

#                         baseline_train = df_baseline.iloc[:baseline_train_size].copy()
#                         baseline_test = df_baseline.iloc[baseline_train_size:].copy()
#                         ''')
            
#             # gráfico com divisão dos dados
#             prophet_baseline_train_df = pd.read_parquet(r'data/prophet_baseline_train.parquet')
#             prophet_baseline_test_df = pd.read_parquet(r'data/prophet_baseline_test.parquet')
            
#             fig = go.Figure()
#             fig.add_trace(go.Scatter
#                         (x=prophet_baseline_train_df['ds'], y=prophet_baseline_train_df['y'],
#                         mode='lines', name='Treino', line=dict(color='#4089FF')))
#             fig.add_trace(go.Scatter
#                         (x=prophet_baseline_test_df['ds'], y=prophet_baseline_test_df['y'],
#                         mode='lines', name='Teste', line=dict(color='#f6c409')))
#             fig.update_layout(title='Prophet Baseline - Treino e Teste',
#                             title_font_size=20, template='plotly_dark')
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             st.plotly_chart(fig, use_container_width=True)
            
#             # markdown
#             st.markdown('''#### Treinamento do modelo''')
#             # texto
#             st.markdown('''<p style="font-size: 18px">
#                         Com os dados preparados, podemos treinar o modelo Prophet.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # Instanciar o modelo Prophet
#                         baseline_model = Prophet()     # parâmetros default
                        
#                         # Ajustar o modelo
#                         baseline_model.fit(baseline_train)
#                         ''')
            
#             # previsões
#             st.markdown('''#### Previsões''')
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Com o modelo treinado, realizamos previsões para o preço do petróleo Brent.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         from prophet.make_future_dataframe import make_future_dataframe
                        
#                         # Criar dataframe futuro
#                         future_baseline = baseline_model.make_future_dataframe(periods=len(baseline_test),
#                                                                                 freq='B')     # dias úteis
                        
#                         # Realizar previsões
#                         forecast_baseline = baseline_model.predict(future_baseline)
#                         ''')
                
#             # previsões
#             prophet_baseline_forecast_df = pd.read_parquet(r'data/prophet_baseline_forecast.parquet')
#             # carregar modelo baseline com pickle
#             with open(r'models/prophet_baseline_model.pkl', 'rb') as file:
#                 prophet_baseline = pickle.load(file)
            
#             fig = plot_plotly(prophet_baseline, prophet_baseline_forecast_df)
#             fig.update_layout(title='Prophet Baseline - Predição vs. Real', title_font_size=20)
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             # scatter to blue
#             fig.for_each_trace(lambda t: t.update(marker=dict(color='#4089FF')))
#             # line to pink
#             fig.for_each_trace(lambda t: t.update(line=dict(color='#e34592')))
#             st.plotly_chart(fig, use_container_width=True)
            
#             # avaliação com cross-validation
#             st.markdown('''#### Avaliação do modelo''')
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Para avaliar o modelo, utilizamos a técnica de validação cruzada (cross-validation).
#                         O Prophet possui uma função interna para realizar a validação cruzada, que divide os dados em
#                         janelas temporais e treina o modelo em cada uma delas.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         from prophet.diagnostics import cross_validation
#                         from prophet.diagnostics import performance_metrics
                        
#                         # Realizar cross-validation
#                         cv_baseline = cross_validation(baseline_model,
#                                                         initial='200 days',
#                                                         period='60 days',
#                                                         horizon='30 days')
                        
#                         # Métricas
#                         metrics_baseline = performance_metrics(cv_baseline)
#                         ''')
            
#             # botão para exibir scores
#             if st.button('📊 Exibir Scores'):
#                 # dataframe com scores
#                 prophet_baseline_dict = {'Horizonte': '3 dias',
#                                         'RMSE': 15.2261,
#                                         'MAE': 8.9039,
#                                         'MAPE': 0.1953}
#                 st.write(prophet_baseline_dict)
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#             prophet_metrics_text = r'''
#                         Para um horizonte de previsão de 3 dias, o modelo atingiu<br> 
#                         RMSE de 15.22, MAE de 8.90 e MAPE de 19.53%.
#                         '''
            
#             create_analysis('Resultados do Modelo Baseline', prophet_metrics_text)
            
#             st.markdown('<br>', unsafe_allow_html=True)
            
#         else:
#             # preparação dos dados - título
#             st.markdown('''#### Preparação dos dados''')
#             # texto
#             st.markdown(r'''
#                         <p style="font-size: 18px">
#                         Para o modelo final, utilizaremos todas as colunas do dataset como regressores. Além disso,
#                         utilizaremos a função Grid Search para encontrar os melhores parâmetros para o modelo.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # final - divisão dos dados
#                         final_train_size = int(len(df_final) * 0.8)

#                         final_train = df_final.iloc[:final_train_size].copy()
#                         final_test = df_final.iloc[final_train_size:].copy()
#                         ''')
            
#             # gráfico com divisão dos dados
#             prophet_final_train_df = pd.read_parquet(r'data/prophet_final_train.parquet')
#             prophet_final_test_df = pd.read_parquet(r'data/prophet_final_test.parquet')
            
#             fig = go.Figure()
#             fig.add_trace(go.Scatter
#                         (x=prophet_final_train_df['ds'], y=prophet_final_train_df['y'],
#                         mode='lines', name='Treino', line=dict(color='#4089FF')))
#             fig.add_trace(go.Scatter
#                         (x=prophet_final_test_df['ds'], y=prophet_final_test_df['y'],
#                         mode='lines', name='Teste', line=dict(color='#f6c409')))
#             fig.update_layout(title='Prophet Final - Treino e Teste',
#                             title_font_size=20, template='plotly_dark')
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             st.plotly_chart(fig, use_container_width=True)
            
#             # markdown
#             st.markdown('''#### Treinar o modelo''')
#             # texto
#             st.markdown('''<p style="font-size: 18px">
#                         Com os dados preparados, podemos criar a lista de parâmetros e realizar a busca dos melhores parâmetros, 
#                         com base na métrica MAPE.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         import itertools
#                         from prophet.make_holidays import make_holidays
                        
#                         # Criar lista de parâmetros
#                         param_grid = {
#                                         'changepoint_prior_scale': np.linspace(0.001, 0.5, 3),
#                                         'seasonality_prior_scale': np.linspace(0.01, 10, 3),
#                                         'holidays_prior_scale': [0.1, 10],
#                                      }
                        
#                         # Combinar parâmetros
#                         all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
                        
#                         results = []
#                         periods=252
                        
#                         # Iterar sobre os parâmetros
#                         for i, params in enumerate(all_params):
#                             # Instanciar o modelo
#                             model = Prophet(**params)
                            
#                             # Adicionar regressores
#                             for regressor in regressors.columns:
#                                 model.add_regressor(regressor)
                                
#                             # Adicionar feriados
#                             model.add_country_holidays(country_name='US')
                            
#                             # Ajustar o modelo
#                             model.fit(train)
                            
#                             # Criar dataframe futuro
#                             future = model.make_future_dataframe(periods=periods, 
#                                                                 freq='B', 
#                                                                 include_history=True)
                                                                
#                             # Adicionar regressores
#                             for regressor in regressors.columns:
#                                 future[regressor] = df[regressor]
                                
#                             # Realizar previsões
#                             forecast = model.predict(future)
                            
#                             # predictions
#                             predictions = forecast[['ds', 'yhat']].tail(periods)
#                             # calculate the error
#                             error = mape(df['y'], forecast['yhat'])
#                             # append the results
#                             results.append([params, error])
                            
#                         results = pd.DataFrame(results, columns=['params', 'mape'])
#                         results = results.sort_values('mape', ascending=True)
                        
#                         best_params = results.iloc[0, 0]
#                         ''')
                
#             # markdown
#             st.markdown('''
#                         <p style="font-size: 18px"><br>
#                         O melhor modelo, com MAPE de 12.13%, foi obtido com os seguintes parâmetros:<br>
#                         - <b>changepoint_prior_scale</b>: 0.5<br>
#                         - <b>seasonality_prior_scale</b>: 0.01<br>
#                         - <b>holidays_prior_scale</b>: 0.01
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # markdown
#             st.markdown('''#### Avaliação do modelo''')
#             # texto
#             st.markdown('''
#                         <p style="font-size: 18px">
#                         Agora, modelos treinar o melhor modelo e realizar previsões.
#                         Com isso, podemos avaliar o modelo com a validação cruzada.
#                         </p>
#                         ''', unsafe_allow_html=True)
            
#             # código
#             with st.expander('🐍 Exibir código Python'):
#                 st.code('''
#                         # Instanciar o modelo
#                         best_model = Prophet(**best_params)
                        
#                         # Adicionar regressores
#                         for regressor in regressors.columns:
#                             final_model.add_regressor(regressor)
                        
#                         # Adicionar feriados
#                         final_model.add_country_holidays(country_name='US')
                        
#                         # Ajustar o modelo
#                         final_model.fit(final_train)
                        
#                         # Realizar cross-validation
#                         cv_final = cross_validation(final_model,
#                                                     initial='200 days',
#                                                     period='60 days',
#                                                     horizon='30 days')
                        
#                         # Métricas
#                         metrics_final = performance_metrics(cv_final)
#                         ''')
            
#             # plotar
#             prophet_final_forecast_df = pd.read_parquet(r'data/prophet_final_forecast.parquet')
#             # carregar modelo final com pickle
#             with open(r'models/prophet_final_model.pkl', 'rb') as file:
#                 prophet_final = pickle.load(file)
                
#             fig = plot_plotly(prophet_final, prophet_final_forecast_df)
#             fig.update_layout(title='Prophet Final - Predição vs. Real', title_font_size=20)
#             fig.update_xaxes(title=None)
#             fig.update_yaxes(title='Preço (U$D )')
#             # scatter to blue
#             fig.for_each_trace(lambda t: t.update(marker=dict(color='#4089FF')))
#             # line to pink
#             fig.for_each_trace(lambda t: t.update(line=dict(color='#e34592')))
#             st.plotly_chart(fig, use_container_width=True)
            
#             # botão para exibir scores
#             if st.button('📊 Exibir Scores'):
#                 # dataframe com scores
#                 prophet_final_dict = {'Horizonte': '3 dias',
#                                       'RMSE': 10.7325,
#                                       'MAE': 6.1403,
#                                       'MAPE': 0.1211}
#                 st.write(prophet_final_dict)

#             st.markdown('<br>', unsafe_allow_html=True)
            
#             prophet_metrics_text = r'''
#                         Para um horizonte de previsão de 3 dias, o modelo atingiu<br>
#                         RMSE de 10.73, MAE de 6.14 e MAPE de 12.11%.<br>
#                         Em comparação com o modelo baseline, houve melhora de<br>15.22% sobre a métrica RMSE, 8.9% sobre a MAE e 
#                         37.97% sobre a MAPE.
#                         '''

#             create_analysis('Resultados do Modelo Final', prophet_metrics_text)

# conclusão
# elif page == page_3:
#     # título
#     st.title('Conclusão')
#     # separador
#     st.markdown('<br>', unsafe_allow_html=True)
#     # texto
#     st.markdown('''
#                 <p style="font-size: 20px">
#                     Neste projeto, foram treinados dois modelos para prever o preço do petróleo Brent: XGBoost e Prophet.
#                     <br><br>
#                     O modelo XGBoost obteve <b>RMSE de 15.89</b>, <b>MAE de 12.31</b> e <b>MAPE de 16.06%</b>, 
#                     o modelo Prophet obteve <b>RMSE de 10.73</b>, <b>MAE de 6.14</b> e <b>MAPE de 12.11%</b>. 
#                     Com base nas configurações atuais, o modelo Prophet obteve melhores métricas de avaliação.
#                     <br>
#                 </p>
#                 ''', unsafe_allow_html=True)

#     st.markdown('<br>', unsafe_allow_html=True)
    
#     st.markdown('---')
    
#     # próximos passos
#     st.markdown('''## Principais Insights''')
    
#     # texto
#     st.markdown('''
#                 <p style="font-size: 18px">
#                     Os principais <i>insights</i> e respectivas etapas de melhorias ao projeto,
#                     obtidos durante os processos de análise dos dados e construção dos modelos, são retratados a seguir:
#                     <br>
#                 </p>
#                 ''', unsafe_allow_html=True) 
                
#     # melhoria do modelo XGBoost
#     st.markdown('''#### Melhoria do Modelo XGBoost''')
#     # texto
#     st.markdown('''
#                 <p style="font-size: 18px">
#                     - <b>Próximo passo:</b> utilizar outros modelos para que o XGBoost possa extrapolar previsões para 
#                       além dos limites dos dados de treinamento.
#                 <br>
#                 </p>
#                 ''', unsafe_allow_html=True)    
    
#     create_insight(
#                     'Extrapolação de Dados na Previsão',
#                     '''
#                         O modelo XGBoost, assim como quaisquer algoritmos baseados em árvore, 
#                         possui uma desvantagem para tarefas de regressão: suas predições respeitarão os 
#                         limites dos dados utilizados no treinamento. Ou seja, existe dificuldade em <b>extrapolar</b> os 
#                         valores máximo e mínimo do intervalo de dados de treinamento. Por isso, se faz interessante 
#                         combinar esse modelo a outros, como modelos lineares ou mesmo Redes Neurais Recorrentes, 
#                         como <i>Long Short-Term Memory</i> (LSTM).
#                     '''
#                     )

#     st.markdown('<br>', unsafe_allow_html=True)

#     # título
#     st.markdown('''#### Modelos de *Ensemble Learning*''')
#     # texto
#     st.markdown('''
#                 <p style="font-size: 18px">
#                     O preço do petróleo é influenciado por diversos fatores, como oferta e demanda.
#                     Além disso, eventos globais, como guerras e desastres naturais, também podem afetá-lo.
#                     Logo, essa série temporal não é estacionária e possui comportamento não linear. Fatos inesperados, 
#                     como os apresentados na seção "Análise", não são facilmente capturados por um único modelo.<br><br>
#                     - <b>Próximo passo:</b> empregar a técnica de <i>ensemble learning</i> para combinar modelos.
#                     <br>
#                 </p>
#                 ''', unsafe_allow_html=True)
    
#     # criar insight
#     create_insight('Complexidade do Preço do Petróleo', 
#                    '''
#                         Sugere-se a utilização de <i>ensemble learning</i> para combinar modelos de previsão.
#                         Esses modelos não precisam se voltar apenas ao preço do petróleo, mas também a outros fatores fundamentais - como produção e mercado.<br>
#                         Um modelo de classificação para prever "alta" ou "baixa" do preço do petróleo pode compor uma <i>feature</i> adicional.<br>
#                         Redes Neurais Convolucionais, ou <i>Convolutional Neural Networks</i> (CNN) são eficazes para análise de imagens de satélite e previsão de eventos climáticos.
#                         CNNs também podem ser usadas para previsão, a partir de gráficos de <i>candlestick</i>, utilizados por <i>traders</i> para análise técnica.
#                     ''')
    
#     st.markdown('<br>', unsafe_allow_html=True)
    
#     st.markdown('''#### Análise de Sentimentos & Mercado Futuro''')

#     st.markdown('''
#                 <p style="font-size: 18px">
#                     A análise de sentimentos é uma técnica de Processamento de Linguagem Natural,
#                     ou <i>Natural Language Processing</i> (NLP), que visa identificar e classificar a polaridade 
#                     emocional de um texto. Ela utiliza algoritmos e modelos de aprendizado de máquina para 
#                     atribuir uma pontuação de sentimento a cada trecho, indicando se é positivo, negativo ou neutro.
#                     Para melhoria do modelo, um passo importante é a construção de uma <i>feature</i> que 
#                     capture a opinião pública sobre o mercado de petróleo em tempo real, a partir de notícias e redes sociais. 
#                     Implementar esses sentimentos no modelo ajuda a incorporar tendências emergentes e 
#                     mudanças de humor que não seriam capturadas apenas por dados históricos de preços.<br><br>
#                     - <b>Próximo passo:</b> integrar o modelo com outras fontes de dados sobre o mercado de futuro.
#                     <br>
#                 </p>
#                 ''', unsafe_allow_html=True)

#     create_insight('Mercado Futuro & Análise de Sentimento', 
#                      '''
#                         A análise de sentimento também contribui para a estabilidade das previsões, 
#                         conforme medido pelo EV (<i>Error Variance</i>, ou Variância do Erro). A adição de sentimentos extraídos por textos 
#                         tende a estabilizar os resultados, reduzindo a variabilidade das previsões e tornando-as mais confiáveis.<br>
#                         Além disso, criar features baseadas em contratos futuros de petróleo e ajudará a 
#                         entender dados de extração e estoque. Também, o volume de transações no mercado de futuro é componente essencial para o cálculo 
#                         de outros indicadores técnicos, como o <i>Open Interest</i>, que mede o número de contratos em aberto.
#                       ''')
    
#     st.markdown('<br>', unsafe_allow_html=True)    
    
#     # título
#     st.markdown('''#### Database na Nuvem''')
#     # texto
#     st.markdown('''
#                 <p style="font-size: 18px">
#                     MLOps é uma prática que visa integrar o desenvolvimento de modelos de Machine Learning 
#                     com a operação de sistemas. Para essa etapa, é importante criar um pipeline de dados.<br><br>
#                     - <b>Próximo passo:</b> <i>deploy</i> da aplicação na nuvem, com a Amazon Web Services (AWS).<br>
#                         * <b>Amazon S3</b> para armazenamento do modelo<br>
#                         * <b>Amazon Redshift</b> para armazenamento dos dados estruturados<br>
#                         * <b>Amazon Glue</b> para ETL - <i>Extract Transform Load</i><br>
#                         * <b>Amazon SageMaker</b> para treinamento de modelos de Machine Learning<br>
#                 </p>
#                 ''', unsafe_allow_html=True)

#     # criar insight
#     create_insight(
#                     'Vantagens de um Database na Nuvem',
#                    '''
#                         - Escalabilidade: aumenta ou diminui a capacidade de armazenamento conforme a demanda.<br>
#                         - Segurança: os dados são armazenados em servidores seguros e protegidos por criptografia.<br>
#                         - Acessibilidade: os dados podem ser acessados de qualquer lugar e a qualquer momento.<br>
#                         - Backup: salvamento automático de dados, que podem ser recuperados em caso de falhas.<br>
#                         - Integração: integração com outras ferramentas, como pipelines de dados e APIs.
#                         '''
#                      )
    
#     st.markdown('<br>', unsafe_allow_html=True)
    
#     st.markdown('''#### Desenvolver API''')

#     st.markdown('''<p style="font-size: 18px">
#                 API, ou <i>Application Programming Interface</i>, é um conjunto de regras e protocolos que 
#                 permitem a comunicação entre sistemas.<br><br>
#                 - <b>Próximo passo:</b> criar API para disponibilizar o modelo para usuários e outras aplicações.
#                 <br>
#                 </p>
#                 ''', unsafe_allow_html=True)
                        
#     # criar insight
#     create_insight('API', 
#                    '''
#                         - Facilita o acesso às previsões do modelo, permitindo que outras aplicações e sistemas consumam os dados.<br>
#                         - Pode ser utilizada para criar dashboards, relatórios e aplicações web que consomem as previsões do modelo.<br>
#                         - Permite integração com outros sistemas, como CRMs (<i>Customer Relationship Management</i>) e 
#                           ERPs (<i>Enterprise Resource Planning).
#                     ''')
    
#     st.markdown('<br>', unsafe_allow_html=True)
    
    
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

# linkedin = 'https://www.linkedin.com/in/viniplima/'
# github = 'https://github.com/euvina/'

# mail = 'pradolimavinicius@gmail.com'
# subject = 'Contato via Streamlit - Projeto Previsão de Preço do Petróleo Brent'

# # área de contato
# st.markdown('''<p style="font-size: 18px; text-align: center;">
#             📧 Entre em contato:<br>
#             <a href="mailto:{}?subject={}">
#             <img src="https://img.shields.io/badge/-Gmail-D14836?style=for-the-badge&logo=Gmail&logoColor=white" alt="Gmail">
#             </a>
#             <a href="{}">
#             <img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white" alt="GitHub">
#             </a>
#             <a href="{}">
#             <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=LinkedIn&logoColor=white" alt="LinkedIn">
#             </a>
#             </p>'''.format(mail, subject, linkedin, github), unsafe_allow_html=True)
