# Importar bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import statsmodels.api as sm
import seaborn as sns
# import plotly.graph_objects as go
# import plotly.express as px
# import pmdarima as pm
import requests

#from keras.models import Sequential
#from keras.layers import LSTM, Dense
# from plotly.subplots import make_subplots
# from prophet import Prophet
# from prophet.plot import plot_plotly
# from statsmodels.tsa.seasonal import seasonal_decompose
# from statsmodels.tsa.stattools import acf, pacf, adfuller
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from sklearn.metrics import mean_absolute_error, mean_squared_error,accuracy_score
# from sklearn.preprocessing import MinMaxScaler

# from sklearn.model_selection import TimeSeriesSplit
# from statsmodels.tsa.stattools import adfuller

from PIL import Image

# import pickle

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
page_2 = 'Aplicação Analítica 📈'
page_3 = 'Conclusão 📌'
page_4 = 'Referências 📖'

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

# Dashboard
elif page == page_2:

    df = pd.read_csv("https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/df_alunos.csv")

    # Estilizando o título e centralizando
    st.markdown("<h1 style='text-align: center;'>📈 Aplicação Analítica</h1>", unsafe_allow_html=True)

    # CSS para centralizar o rádio
    st.markdown(
        """
        <style>
        
            div[role="radiogroup"] {
                display: flex;
                justify-content: center;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Criando o menu centralizado
    menu = st.radio("", ["Dashboard", "Insight", "Análise Preditiva"], horizontal=True)

    st.markdown('---', unsafe_allow_html=True)

    # Renderizando a opção escolhida
    if menu == "Dashboard":
        st.subheader("📊 Dashboard")
      #  st.write("Aqui você pode visualizar os principais KPIs.")

        # Ajuste a codificação se necessário
        df['ANO_LETIVO'] = df['ANO_LETIVO'].astype(str) 

        # Definir a coluna 'NOME' como índice (opcional)
        df_aluno1 = df.set_index('NOME')
                                
        # Iniciar o estado dos filtros se ainda não estiverem definidos
        if 'ano_selecionado' not in st.session_state:
            st.session_state['ano_selecionado'] = None

        if 'matricula_selecionada' not in st.session_state:
            st.session_state['matricula_selecionada'] = None

        if 'indicador_selecionado' not in st.session_state:
            st.session_state['indicador_selecionado'] = None

        # Criar os widgets de filtro
        col1, col2, col3 = st.columns(3)

        with col1:
            anos_disponiveis = sorted(df['ANO_LETIVO'].unique())
            ano_selecionado = st.selectbox('Selecione o ano', [None] + list(anos_disponiveis), key='ano_selecionado')

        with col2:
            # Remove valores nulos e obtém os valores únicos
            matriculas_disponiveis = df['INST_ENSINO'].dropna().unique()

            # Criar um dicionário para exibir opções em maiúsculas, mas manter os valores originais
            matriculas_maiusculas = {str(m).upper(): m for m in matriculas_disponiveis}

            # Criar o selectbox com as opções em maiúsculas
            matricula_selecionada_maiuscula = st.selectbox(
                'Selecione o tipo de matrícula', 
                [None] + list(matriculas_maiusculas.keys()), 
                key='matricula_selecionada'
            )

            # Recuperar o valor original selecionado
            matricula_selecionada = matriculas_maiusculas.get(matricula_selecionada_maiuscula, None)

        with col3:
            indicadores_disponiveis = ["INDE", "IAA", "IEG", "IPS", "IDA", "IPP", "IAN", "IPV"]
            indicador_selecionado = st.selectbox('Selecione o indicador', [None] + indicadores_disponiveis, key='indicador_selecionado')

        # Aplicar os filtros selecionados
        df_filtrado1 = df_aluno1.copy()

        if ano_selecionado:
            df_filtrado1 = df_filtrado1[df_filtrado1['ANO_LETIVO'] == ano_selecionado]

        if matricula_selecionada:
            df_filtrado1 = df_filtrado1[df_filtrado1['INST_ENSINO'] == matricula_selecionada]

        # Função para criar containers personalizados
        def criar_container_titulo(conteudo_html):
            return st.markdown(conteudo_html, unsafe_allow_html=True)

        # Atualizar os quadros com base no filtro selecionado
        cols_container = st.columns(2, gap="small")

        with cols_container[0]:
            quadro = cols_container[0].container(height=315, border=True)
            total_alunos = len(df_filtrado1)
            quadro.markdown(f'''
                            <p style="font-size: 50px; text-align: center; margin: 0;">
                            <br><b>{total_alunos}</b><br>
                            </p>
                            ''', unsafe_allow_html=True)

            quadro.markdown('''
                            <p style="font-size: 34px; text-align: center;">
                            <b>Alunos Matriculados</b>
                            </p>
                            ''', unsafe_allow_html=True)

        with cols_container[1]:

            cols_container1 = st.columns(2, gap="small")
            with cols_container1[0]:
                # Calcular o total Masculino
                total_masculino = df_filtrado1[df_filtrado1['GENERO'] == 'Masculino']['GENERO'].count()
                quadro = cols_container1[0].container(height=150, border=True)
                quadro.markdown(f'''
                                <p style="font-size: 36px; text-align: center; color: lightblue;">                           
                                <b>{total_masculino}</b><br>
                                👨🏻‍🎓
                                </p>
                                ''', unsafe_allow_html=True)

            with cols_container1[1]:
                # Calcular o total Feminino
                total_feminino = df_filtrado1[df_filtrado1['GENERO'] == 'Feminino']['GENERO'].count()
                quadro = cols_container1[1].container(height=150, border=True)
                quadro.markdown(f'''
                                <p style="font-size: 36px; text-align: center; color: pink;">
                                <b>{total_feminino}</b><br>
                                👩🏼‍🎓
                                </p>
                                ''', unsafe_allow_html=True)

            cols_container2 = st.columns(2, gap="small")
            with cols_container2[0]:
                # Calcular a porcentagem de alunos masculinos
                if total_alunos > 0:
                    perc_masculino = (total_masculino / total_alunos) * 100
                else:
                    perc_masculino = 0
                quadro = cols_container2[0].container(height=150, border=True)
                quadro.markdown(f'''
                                <p style="font-size: 30px; text-align: center; color: lightblue;">
                                <b>{perc_masculino:.2f}% Masculino</b>
                                </p>
                                ''', unsafe_allow_html=True)    

            with cols_container2[1]:
                # Calcular a porcentagem de alunos femininos
                if total_alunos > 0:
                    perc_feminino = (total_feminino / total_alunos) * 100
                else:
                    perc_feminino = 0
                quadro = cols_container2[1].container(height=150, border=True)
                quadro.markdown(f'''
                                <p style="font-size: 30px; text-align: center; color: pink;">
                                <b>{perc_feminino:.2f}% Feminino</b>
                                </p>
                                ''', unsafe_allow_html=True)

        # Criar duas colunas principais para organizar os containers
        col_pedras, col_indicador = st.columns([1, 1], gap="small")

        # Exibir a contagem de alunos por tipo de PEDRA dentro da primeira coluna
        with col_pedras:
            tipos_pedra = df_filtrado1.loc[df_filtrado1['PEDRA'].notna() & (df_filtrado1['PEDRA'] != "nao_informado"), 'PEDRA'].unique()

            num_colunas = 2
            rows = [tipos_pedra[i:i + num_colunas] for i in range(0, len(tipos_pedra), num_colunas)]

            for row in rows:
                cols_pedra = st.columns(num_colunas, gap="small")
                for i, tipo in enumerate(row):
                    total_tipo = len(df_filtrado1[df_filtrado1['PEDRA'] == tipo])
                    with cols_pedra[i]:
                        quadro = cols_pedra[i].container(height=150, border=True)
                        quadro.markdown(f'''
                            <p style="font-size: 30px; text-align: center;">
                            <b>{total_tipo}<br>
                            {tipo}</b>
                            </p>
                        ''', unsafe_allow_html=True)

        # Exibir a média do indicador na segunda coluna
        with col_indicador:
            if indicador_selecionado and indicador_selecionado in df_filtrado1.columns:
                media_indicador = df_filtrado1[indicador_selecionado].mean()
                quadro = st.container(height=315, border=True)
                quadro.markdown(f'''
                                <p style="font-size: 40px; text-align: center;">
                                <br><b>{media_indicador:.2f}%</b>
                                </p>
                                ''', unsafe_allow_html=True)
                quadro.markdown(f'''
                                <p style="font-size: 30px; text-align: center;">
                                <b>Média do indicador {indicador_selecionado}</b>
                                </p>
                                ''', unsafe_allow_html=True)
            else:
                quadro = st.container(height=315, border=True)
                quadro.markdown('''
                                <p style="font-size: 34px; text-align: center;">
                                <br><b>Selecione um indicador para ver a média</b>
                                </p>
                                ''', unsafe_allow_html=True)
                
    elif menu == "Insight":
        st.subheader("💡 Insights")

        # seleção de modelo
        model = st.selectbox('Selecione o modelo:', ['Análise por Aluno', 'Indicadores', 'Pedras', 'Ponto de Virada'])

        st.markdown('<br>', unsafe_allow_html=True)

        if model == 'Análise por Aluno':
            st.subheader('Análise por Aluno', divider='orange')

            # texto 
            st.markdown('''
                <p style="font-size: 18px">
                    Nesse modelo, podemos filtrar de maneira dinâmica cada aluno da associação passos mágicos que estiveram presentes entre os anos de
                    2022 até 2024. Com base nesse filtro, é possível ter uma visão geral da base e começar a dar os primeiros passos em uma análise exploratória.
                    <br>
                </p>
                ''', unsafe_allow_html=True)

            if 'multi' not in st.session_state: 
                st.session_state['multi'] = []

            if 'ano_selecionado2' not in st.session_state:
                st.session_state['ano_selecionado2'] = None

            if 'turma_selecionada' not in st.session_state:
                st.session_state['turma_selecionada'] = None

            if 'fase_selecionada' not in st.session_state:
                st.session_state['fase_selecionada'] = None

            if 'comparador_inde' not in st.session_state:
                st.session_state['comparador_inde'] = 'Nenhum'

            if 'valor_inde' not in st.session_state:
                st.session_state['valor_inde'] = 0

            df_aluno = df.set_index('NOME')
            
            col7, col8= st.columns([3,1])

            with col7:
                def clear_multi():
                    st.session_state.multiselect = []
                    return
                    
                multi = st.multiselect('Selecione um ou mais alunos', df_aluno.index.unique(), key='multiselect')
                st.button("Limpar alunos", on_click=clear_multi)
                                
            with col8:
                anos_disponiveis = df['ANO_LETIVO'].unique()
                ano_selecionado2 = st.selectbox('Selecione o ano', [None] + list(anos_disponiveis), key='ano_selecionado2')

            col9, col10, col11, col12 = st.columns(4)

            with col9:
                turmas_disponiveis = df['TURMA'].unique()
                turma_selecionada = st.selectbox('Selecione a turma', [None] + list(turmas_disponiveis), key='turma_selecionada')

            with col10:
                fases_disponiveis = df['FASE'].unique()
                fase_selecionada = st.selectbox('Selecione a fase', [None] + list(fases_disponiveis), key='fase_selecionada')

            with col11:
                comparador_inde = st.selectbox('Filtrar INDE por', ['Nenhum', 'Maior que', 'Menor que'], key='comparador_inde')

            with col12:
                valor_inde = st.number_input('Digite o valor para o INDE', step=1, key='valor_inde')

            df_filtrado = df_aluno.copy()
            df_filtrado['ATINGIU_PV'] = df_filtrado['ATINGIU_PV']

            def reset_filters():
                st.session_state['aluno_selecionado'] = []
                st.session_state['ano_selecionado2'] = None
                st.session_state['turma_selecionada'] = None
                st.session_state['fase_selecionada'] = None
                st.session_state['comparador_inde'] = 'Nenhum'
                st.session_state['valor_inde'] = 0

            st.button('Limpar Filtros', on_click=reset_filters)

            # Filtragem do dataframe
            if multi:
                df_filtrado = df_filtrado[df_filtrado.index.isin(multi)]

            if ano_selecionado2:
                df_filtrado = df_filtrado[df_filtrado['ANO_LETIVO'] == ano_selecionado2]

            if turma_selecionada:
                df_filtrado = df_filtrado[df_filtrado['TURMA'] == turma_selecionada]

            if fase_selecionada:
                df_filtrado = df_filtrado[df_filtrado['FASE'] == fase_selecionada]

            if comparador_inde == 'Maior que':
                df_filtrado = df_filtrado[df_filtrado['INDE'] > valor_inde]
            elif comparador_inde == 'Menor que':
                df_filtrado = df_filtrado[df_filtrado['INDE'] < valor_inde]

            # Converter colunas numéricas para inteiros (removendo casas decimais)
            for col in df_filtrado.select_dtypes(include=['float']).columns:
                df_filtrado[col] = df_filtrado[col].astype(int)

            # Corrigir exibição removendo separador de milhar
            df_filtrado = df_filtrado.applymap(lambda x: f"{x}" if isinstance(x, int) else x)

            # Estilo CSS para ajustar a largura da tabela
            st.markdown(
                """
                <style>
                .dataframe-container {
                    display: flex;
                    justify-content: flex-start;
                    width: 100%;
                }
                .dataframe-container > div {
                    width: 100%;
                }
                </style>
                """, unsafe_allow_html=True
            )

            # Contêiner para aplicar o estilo apenas à tabela
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.dataframe(df_filtrado)
            st.markdown('</div>', unsafe_allow_html=True)

        elif model == 'Indicadores':

            st.subheader('Indicadores', divider='orange')

            # texto
            st.markdown('''
                        - INDE - Indice do Desenvolvimento Educacional
                        - IAA - Indicador de Auto Avaliçao
                        - IEG - Indicador de Engajamento
                        - IPS - Indicador Psicossocial
                        - IDA - Indicador de Aprendizagem
                        - IPP - Indicador Psicopedagogico
                        - IPV - Indicador de Ponto de Virada
                        ''')        

            # Carregar o DataFrame com tratamento de possíveis issues
            df = pd.read_csv("https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/df_alunos.csv")

            # Definindo os bins do histograma
            bins = [3.03, 3.67, 4.31, 4.96, 5.60, 6.24, 6.88, 7.52, 8.16, 8.80, 9.44]

            col1, col2= st.columns(2)

            with col1:
                anos_disponiveis = sorted(df['ANO_LETIVO'].unique())
                ano_selecionado = st.selectbox('Selecione o ano', [None] + anos_disponiveis)

            with col2:
                indicadores_disponiveis = ["INDE", "IAA", "IEG", "IPS", "IDA", "IPP", "IPV"]
                indicador_selecionado = st.selectbox('Selecione o indicador', [None] + indicadores_disponiveis)

            # Aplicar filtros
            df_filtrado = df.copy()
            if ano_selecionado:
                df_filtrado = df_filtrado[df_filtrado['ANO_LETIVO'] == ano_selecionado]

            # Cálculo dos valores Mínimo, Médio e Máximo
            if indicador_selecionado and not df_filtrado.empty:
                valores_ordenados = df_filtrado[indicador_selecionado].sort_values().values
                minimo = next((val for val in valores_ordenados if val > 0), valores_ordenados[0] if len(valores_ordenados) > 0 else 0)
                media = df_filtrado[indicador_selecionado].mean()
                maximo = df_filtrado[indicador_selecionado].max()

                with st.container():
                    st.markdown("""
                        <style>
                            .metric-container {
                                font-size: 20px;
                                border: 1px solid #808080;
                                padding: 05px;
                                border-radius: 6px;
                                text-align: center;
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="metric-container">Mínimo do {indicador_selecionado}<br><b>{round(minimo, 2)}</b></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="metric-container">Média do {indicador_selecionado}<br><b>{round(media, 2)}</b></div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<div class="metric-container">Máximo do {indicador_selecionado}<br><b>{round(maximo, 2)}</b></div>', unsafe_allow_html=True)

                st.markdown('---')
                # Criar categorias para o histograma
                df_filtrado[f'{indicador_selecionado}_bin'] = pd.cut(df_filtrado[indicador_selecionado], bins=bins)

                # Agrupar por ano letivo e bin
                counts = df_filtrado.groupby(['ANO_LETIVO', f'{indicador_selecionado}_bin']).size().reset_index(name='frequencia')

                # Gráfico de barras
                plt.figure(figsize=(14, 7))
                ax = sns.barplot(x=f'{indicador_selecionado}_bin', y='frequencia', hue='ANO_LETIVO', data=counts, palette='viridis')

                # Anotações no gráfico
                for p in ax.patches:
                    if p.get_height() > 0:
                        ax.annotate(f'{int(p.get_height())}', 
                                    (p.get_x() + p.get_width() / 2., p.get_height()),
                                    ha='center', va='center', fontsize=10, color='black',
                                    xytext=(0, 5), textcoords='offset points')

                plt.xlabel(f'Intervalos do {indicador_selecionado}', fontsize=12)
                plt.ylabel('Alunos', fontsize=12)
                plt.title(f'Distribuição do {indicador_selecionado} por Ano Letivo', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.legend(title='Ano Letivo', fontsize=10, title_fontsize=12)
                plt.tight_layout()
                st.pyplot(plt)

            else:
                st.markdown(
                    """
                    <div style="text-align: center;">
                        <br>Por favor, selecione um indicador para visualizar os dados.<b>
                    </div>
                    """, unsafe_allow_html=True
                )

        elif model == 'Pedras':
            
            df = pd.read_csv("https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/df_pedra_geral.csv")


            st.subheader('Pedras', divider='orange')

            # texto
            st.markdown('''
                        Classificação referente a cada tipo de pedra com base no INDE de cada aluno:
                        - Quartzo – 2,405 a 5,506
                        - Agata – 5,506 a 6,868
                        - Ametista – 6,868 a 8,230
                        - Topazio – 8,230 a 9,294
                        ''', unsafe_allow_html=True)
            
            df['ano_letivo'] = df['ano_letivo'].astype(str) 
            
            df_pedra = df.set_index('ano_letivo')

            # Criar sessão de estado para os filtros se ainda não existirem
            for key in ['ano_selecionado3', 'pedra_selecionada', 'genero_selecionado']:
                if key not in st.session_state:
                    st.session_state[key] = None

            col1, col2, col3 = st.columns(3)

            with col1:
                anos_disponiveis3 = sorted(df['ano_letivo'].unique())
                ano_selecionado3 = st.selectbox('Selecione o ano', [None] + list(anos_disponiveis3), key='ano_selecionado3')     

            with col2:
                # Remover "nao_informado" da lista de opções
                pedras_disponiveis = sorted(df['pedra'].unique())
                pedras_disponiveis = [p for p in pedras_disponiveis if p != "nao_informado"]
                
                pedra_selecionada = st.selectbox('Selecione a pedra', [None] + pedras_disponiveis, key='pedra_selecionada')  

            with col3:
                generos_disponiveis = sorted(df['genero'].unique())
                genero_selecionado = st.selectbox('Selecione o gênero', [None] + list(generos_disponiveis), key='genero_selecionado')    

            # Aplicar filtros
            df_filtrado = df.copy()
            if ano_selecionado3:
                df_filtrado = df_filtrado[df_filtrado['ano_letivo'] == ano_selecionado3]
            if pedra_selecionada:
                df_filtrado = df_filtrado[df_filtrado['pedra'] == pedra_selecionada]
            if genero_selecionado:
                df_filtrado = df_filtrado[df_filtrado['genero'] == genero_selecionado]

            # Remover a categoria "nao_informado" antes de calcular os dados
            df_filtrado = df_filtrado[df_filtrado['pedra'] != "nao_informado"]

            # Criar dataframe de contagem
            df_pedra_contagem = df_filtrado.groupby(['ano_letivo', 'pedra']).size().unstack(fill_value=0)

            # Garantir que o total de pedras seja baseado em todos os registros do ano, excluindo "nao_informado"
            df_total_geral = df[df['pedra'] != "nao_informado"].groupby(['ano_letivo', 'pedra']).size().unstack(fill_value=0)
            total_pedra_geral = df_total_geral.sum(axis=1)

            # Calcular percentual com base no total original de todas as pedras, sem "nao_informado"
            df_pedra_percentual = df_pedra_contagem.divide(total_pedra_geral, axis=0) * 100
            df_pedra_percentual = df_pedra_percentual.fillna(0)  # Substituir NaN por 0 se necessário

            # Cores para o gráfico
            cores = {
                'Quartzo': 'red',
                'Agata': 'yellow',
                'Ametista': 'lightblue',
                'Topazio': 'lightgreen'
            }   

            # Criar o gráfico
            st.subheader("Gráfico com a quantidade total de alunos por pedra")
            fig, ax = plt.subplots(figsize=(12, 6))

            # Remover fundo branco
            fig.patch.set_alpha(0)  # Remove fundo do gráfico
            ax.set_facecolor("none")  # Remove fundo do eixo
            ax.patch.set_alpha(0)  # Remove fundo interno do gráfico

            if ano_selecionado3:
                # Se um único ano for selecionado, usar gráfico de barras
                df_pedra_contagem = df_filtrado['pedra'].value_counts()
                ax.bar(df_pedra_contagem.index, df_pedra_contagem.values, 
                    color=[cores.get(p, 'gray') for p in df_pedra_contagem.index])
                ax.set_ylabel("Total de Pedras", color="white")
                ax.set_xlabel("Pedra", color="white")
                
                for i, v in enumerate(df_pedra_contagem.values):
                    ax.text(i, v + 0.5, str(v), ha='center', color="white")  # Ajuste de cor do texto
            else:
                # Se nenhum ano for selecionado, manter o gráfico de linhas
                for pedra in df_pedra_contagem.columns:
                    ax.plot(
                        df_pedra_contagem.index,
                        df_pedra_contagem[pedra],
                        marker='o',
                        label=pedra,
                        color=cores.get(pedra, 'gray')
                    )
                    for i, count in enumerate(df_pedra_contagem[pedra]):
                        ax.text(df_pedra_contagem.index[i], count, str(count), ha='center', va='bottom', color="white")

                ax.set_xlabel("Ano da Pesquisa", color="white")
                ax.legend(title="Pedra")

            # Configurações do gráfico
            ax.set_title("Alunos separados por PEDRA - Quantidade de alunos", color="white")
            ax.grid(color='gray', linestyle='--', linewidth=0.5)  # Grid mais suave
            ax.tick_params(axis='x', colors='white')  # Cor dos valores no eixo X
            ax.tick_params(axis='y', colors='white')  # Cor dos valores no eixo Y
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Exibir no Streamlit
            st.pyplot(fig)

            # Criar o gráfico de distribuição percentual de alunos por pedra
            st.subheader("Gráfico de distribuição percentual de alunos por pedra")
            fig, ax = plt.subplots(figsize=(10, 6))

            # Remover fundo branco do gráfico
            fig.patch.set_alpha(0)  # Remove o fundo branco do gráfico
            ax.set_facecolor("none")  # Remove o fundo dos eixos
            ax.patch.set_alpha(0)  # Remove fundo do plot

            bar_width = 0.15
            y_pos = np.arange(len(df_pedra_percentual.index))

            barras = []
            for i, pedra in enumerate(df_pedra_percentual.columns):
                bars = ax.bar(y_pos + i * bar_width, df_pedra_percentual[pedra], bar_width, color=cores.get(pedra, 'gray'), label=pedra)
                barras.append((bars, df_pedra_percentual[pedra]))

            # Adicionar porcentagens corretamente
            for bars, valores in barras:
                for bar, valor in zip(bars, valores):
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height, f'{valor:.1f}%', ha='center', va='bottom', color='white')  # Cor do texto alterada

            # Ajustes visuais
            ax.set_xticks(y_pos + 1.5 * bar_width)
            ax.set_xticklabels(df_pedra_percentual.index, color='white')  # Cor do eixo X
            ax.set_xlabel("Ano", color='white')
            ax.set_ylabel("Porcentagem de Alunos", color='white')
            ax.set_title("Distribuição percentual de alunos por pedra", color='white')
            ax.legend()
            ax.set_ylim(0, 70)
            ax.grid(color='gray', linestyle='--', linewidth=0.5)  # Grid mais suave

            plt.tight_layout()
            st.pyplot(fig)

        else:
            st.subheader('Ponto de Virada', divider='orange')

            # texto
            st.markdown('''
                        <p style="font-size: 18px">
                            O XGBoost, ou <i>Extreme Gradient Boosting</i>, é um algoritmo de aprendizado de máquina supervisionado e baseado em árvores de decisão.
                            O modelo é uma implementação otimizada do Gradient Boosting e pode ser utilizado para problemas de regressão e classificação. O XGBoost é 
                            amplamente utilizado em competições de ciência de dados e é conhecido por sua eficiência e desempenho.
                            <br>
                        </p>
                        ''', unsafe_allow_html=True)

    elif menu == "Análise Preditiva":
        st.subheader("🔮 Análise Preditiva")
       # st.write("Aqui você pode acessar modelos preditivos.")

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
