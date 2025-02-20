# Importar bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

from PIL import Image
from io import BytesIO

from utils import (create_warning, 
                   create_quote, 
                   create_insight)

# layout
st.set_page_config(layout='centered', 
                   page_title='Associação Passos Mágicos - Tech Challenge - FIAP', 
                   page_icon='🌟', initial_sidebar_state='auto')

#Bases
base_alunos = "https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/df_alunos.csv"
base_evasao = "https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/Evasao.csv"
base_pedra_geral = "https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/df_pedra_geral.csv"
base_evasao_por_motivo = "https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/Bases/EvasaoPorMotivo.csv"

#Dicionário
url_file_data = "https://raw.githubusercontent.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/main/file/Dicion%C3%A1rio%20Dados%20Datathon.pdf"

#Link para download das bases
url = base_alunos
response = requests.get(url)
csv_data = response.content

response = requests.get(url_file_data)
file_data = response.content

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
                Analisando impacto causado pelas ações voluntárias da ONG Passos Mágicos, desenvolvendo uma análise exploratória, gerando insights e dashboard interativos.<br> 
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

        **🎯 Objetivo**: Analisar impacto causado pela ONG Passos Mágicos e gerar dashboard dinâmicos para auxiliar na análise exploratória com o objetivo de auxliar a associação Passos Mágicos a tomar a melhor decisão.

        ---        
        
        **📡 Base de Dados e Dicionário**:
        ''')

        tab0, tab1 = st.tabs(tabs=['Base de Dados', 'Dicionário'])

        with tab0:
            # Função para carregar o arquivo Excel com cache
            @st.cache_data
            def carregar_dados(url):
                return pd.read_excel(url, sheet_name=None, engine="openpyxl")

            with st.container():
                st.markdown('''Base de dados PEDE (Pesquisa Extensiva do Desenvolvimento Educacional)''', unsafe_allow_html=True)

                # URL do arquivo
                url = "https://github.com/r-zambotti/Data_Analytics_Datathon_Grupo-60/raw/refs/heads/main/Bases/PEDE_PASSOS_2024.xlsx"

                opcao = st.radio("Selecione para download:", ["Base de Dados PEDE", "Base de Dados Tratada"], horizontal=True)

                if opcao == "Base de Dados PEDE":
                    # Carrega os dados do Excel usando cache
                    xls = carregar_dados(url)

                    # Criar buffer para download
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        for sheet_name, df in xls.items():
                            df.to_excel(writer, index=False, sheet_name=sheet_name)

                    excel_data = output.getvalue()

                    st.download_button(
                        label="Baixar Base PEDE (xlsx)",
                        data=excel_data,
                        file_name="PEDE_PASSOS_2024.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                if opcao == "Base de Dados Tratada":
                    st.download_button(label="Baixar Base Tratada (csv)",data=csv_data,file_name="df_alunos.csv",mime="text/csv")

        with tab1:
            st.markdown('''                   
                        ###### Download do dicionário
                        ''',unsafe_allow_html=True)
            
            st.download_button(label="Dicionário da base PEDE",data=file_data,file_name="Dicionário dados PEDE.pdf",mime="application/pdf")
            
        st.markdown('''        
        ---
        **📡 Fontes de dados**:
        - [Passos Mágicos](https://passosmagicos.org.br/)
        - [Google Drive](https://drive.google.com/drive/folders/1Z1j6uzzCOgjB2a6i3Ym1pmJRsasfm7cD)
        ---
        
        **🧑🏻‍🚀 Autores**: 
        - [Victor Novais de Oliveira](https://www.linkedin.com/in/victor-novais-166369171/)
        - [Rodrigo Zambotti de Andrade](https://www.linkedin.com/in/rodrigo-zambotti-369840a4?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)
        - [Arencio Job Pereira](https://www.linkedin.com)  
        - [Bruno Akio Matsuzaki Shimada](www.linkedin.com/in/bruno-shimada-763726211)                     
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

    # Link correto para incorporação (substitua pelo ID do seu vídeo)
    video_id = "36ZfZQa68og"  # Substitua pelo ID do vídeo do YouTube
    youtube_link = f"https://www.youtube.com/embed/{video_id}"

    # Incorporar o vídeo no Streamlit
    st.markdown(
        f'<iframe width="700" height="400" src="{youtube_link}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
)


# Análise Exploratória
elif page == page_1:

    st.title('Análise Exploratória 🔎')
    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown('''
                O projeto teve sua análise exploratória realizada com base nos dados da PEDE (Pesquisa Extensiva do Desenvolvimento Educacional), disponibilizados pela Passos Mágicos. 
                A documentação completa, que explica a construção dos índices e métricas já existentes, foi compartilhada, trazendo à tona os detalhes da metodologia aplicada. 
                A Passos Mágicos utiliza o INDE (Índice Nacional de Desenvolvimento Educacional) como uma métrica central para avaliar o desempenho dos estudantes. O INDE é formado por um conjunto de indicadores, 
                distribuídos em três dimensões principais, que abrangem critérios como adequação de nível, desempenho acadêmico, engajamento, autoavaliação, aspectos psicossociais e psicopedagógicos. Essas dimensões são organizadas da seguinte maneira, 
                cada uma com seus respectivos indicadores:                              
                ''', unsafe_allow_html=True)
    
    st.markdown('''
                - Dimensão acadêmica: IEG, IAN e IDA
                ''',  unsafe_allow_html=True)
    
    st.markdown('''
                - Dimensão psicopedagógica: IPP e IPV
                ''',  unsafe_allow_html=True)
    
    st.markdown('''
                - Dimensão psicossocial: IPS e IAA
                ''',  unsafe_allow_html=True)

    st.markdown('''
                O INDE geral apresenta uma média de 6,84, com uma amplitude significativa entre os valores mínimo e máximo, que variam de 3,03 a 9,53. 
                Ao analisar os dados por ano, percebe-se um crescimento no número de alunos, porém acompanhado de uma queda nos níveis do INDE. Esse cenário nos coloca diante de um desafio importante: 
                a necessidade de segmentar essas informações para identificar e compreender as lacunas existentes, buscando estratégias que possam reverter essa tendência e fortalecer o desempenho educacional.
                ''', unsafe_allow_html=True) 

    st.markdown('''
                Com base nas análises realizadas, observa-se que a maioria dos estudantes se concentra nos intervalos de scores entre (6.88, 7.52], o que reflete um desempenho consistente e relativamente elevado em diversas métricas. 
                A tendência geral aponta para um crescimento no número de estudantes nos intervalos superiores ao longo dos anos, indicando melhorias significativas nos índices de desenvolvimento educacional, autoavaliação, engajamento, 
                aspectos psicossociais, aprendizagem e pontos de virada.
  ''', unsafe_allow_html=True)

    #Análise dos Indicadores
    st.subheader('Análise dos Indicadores', divider='orange')

    #Divindo cada indicador em selectbox para melhor visualização
    indicador = st.selectbox('Selecione o indicador:', ['INDE','Pedras','IEG', 'IDA', 'IAN', 'IAA', 'IPS', 'IPP', 'IPV'])

    #Tabela INDE
    if indicador == 'INDE':
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O INDE (índice do desenvolvimento educacional), como medida síntese do presente processo avaliativo, é composto
                    por uma dimensão acadêmica, uma dimensão psicossocial e uma dimensão psicopedagógica. Essas dimensões são observadas por meio do resultado
                    de sete indicadores <b>(IAN, IDA, IEG, IAA, IPS, IPP e IPV)</b>, que aglutinados por ponderação, formam o índice sintético (INDE). <br>

                    No quadro abaixo, pode ser visto uma apresentação esquemática da relação entre as três dimensões de avaliação, e os indicadores, em suas duas categorias de classificação 
                    e a sua aplicação pelas faixas de Fase de ensino da Associação Passos Mágicos. 

                    </p>
                    ''', unsafe_allow_html=True)    

        image =  Image.open("img/inde_indicadores.png")
        st.image(image, caption= "Dimensões e Indicadores do INDE")       

    #Tabela Pedras
    if indicador == 'Pedras':

        st.markdown('''
                    <p style="font-size: 18px">

                    As pedras são definidas com base no índice do desenvolvimento educacional (INDE). Com base nas médias geradas pelos indicadores, conseguimos calcular como cada pedra será criada e atribuida a cada aluno.<br>  
                    Como um dos principais objetivos do cálculo do INDE é ter um parâmetro de avaliação do desenvolvimento educacional dos estudantes da Associção Passos Mágicos, as suas medidas de variabilidade (médida, mediana e moda), 
                    nos possibilitam a formação de um critério de classificação de nota padronizada. Esse critério nos permite calcular intervalos de valor do INDE a partir do desempenho de todos os estudantes, comparando-os numa base mais justa, 
                    e não simplesmente ordenando suas notas pelos seus valores absolutos. Assim, os resultados individuais do INDE levarão em conta as condições de dispersão das notas de todo o conjunto de estudantes. <b> A classificação das notas 
                    se dará então pela sua distância em relação à média geral e não por seu valor absoluto</b>. <br>
                    Segue imagem abaixo para melhor entendimento: 

                    </p>
                    ''',unsafe_allow_html=True)

        image =  Image.open("img/notas_padronizadas.png")
        st.image(image, caption= "Projeção Normal e limites da nota padronizada INDE escolar")

        st.markdown('''
            <p style="font-size: 18px">

            Com base nessas notas, geramos as seguintes médias para cada tipo de pedra: 
            - Quartzo: Alunos com INDE entre 3.032 a 5.996.
            - Ágata: Alunos com INDE entre 6.0092 a 6.9995.
            - Ametista: Alunos com INDE entre 7.0000 a 8.058.
            - Topázio: Alunos com INDE entre 8.0026 a 9.5313.

            </p>
            ''',unsafe_allow_html=True)
        
    #Tabela IEG    
    if indicador == 'IEG':

        st.markdown('''
                    <p style="font-size: 18px">

                    ###### IEG (Indicador de Engajamento)

                    </p>
                    ''',unsafe_allow_html=True )
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O Indicador de Engajamento - IEG, registra a participação em ações de voluntariado dos estudantes universitários, e a entrega das lições de casa dos estudantes em fase escolar.
                    O indicador dos escolares foi produzido a partir dos registros feitos, diariamente, pela equipe pedagógica, no sistema escolar da Associação. 

                    </p>
                    ''',unsafe_allow_html=True )

    #Tabela IDA
    if indicador == 'IDA':

        st.markdown('''
                    <p style="font-size: 18px">

                    ###### IDA (Indicador de Desempenho Acadêmico)

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O IDA expressa a proficiência dos estudantes da Fase 0 (alfabetização), até a Fase 7 (3º ano do ensino médio), nas provas aplicadas pela Associação Passos Mágicos, numa mesma base númerica (de 0 a 10 pontos). 
                    Para esses estudantes essa é uma medida uniforme de avaliação, pois essas provas se referem aos conteúdos e às habilidades associadas a esses conteúdos, que foram desenvolvidos no contexto do Programa de Aceleração do Conhecimento.                
                    Para os estudantes da Fase 8, bolsistas universitários, esse indicador expressa a média anual das avaliações de cada disciplina cursada em seus respectivos cursos, na mesma base númerica (de 0 a 10 pontos).

                    </p>
                    ''',unsafe_allow_html=True)

    #Tabela IAN
    if indicador == 'IAN':

        st.markdown('''
                    <p style="font-size: 18px">

                    ###### IAN (Indicador de Adequação de Nível)

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O indicador de Adequação de Nível registra a condinção de adequação do estudante, por meio da avaliação pedagógica e multidisciplinar da Associação,
                    à Fase de Ensino efetivamente designada. Isso significa que o estudante é designado para a Fase de Ensino que seja compatível com o atual estágio de desenvolvimento das suas 
                    capacidades e habilidades acadêmicas.<br>
                    Sendo assim, cabe confrontar o diagnóstico de atribuição da Fase de Ensino efetivamente designada aos estudantes, com o seu respectivo desempenho acadêmico, para verificar
                    se não existe um desempenho acadêmico advindo, meramente, da defasagem no Nível de Ensino. Isso seria observado, caso o desempenho acadêmico dos estudantes com defasagem fosse superior à média dos
                    estudantes em geral, ou mesmo dos estudantes sem defasagens.

                    </p>
                    ''',unsafe_allow_html=True )

        image =  Image.open("img/ian_avaliacoes.png")
        st.image(image, caption= "Tabela de adequação de nível") 
        
    #Tabela IAA
    if indicador == 'IAA':

        st.markdown('''
                    <p style="font-size: 18px">

                    ###### IAA (Indicador de Autoavaliação)

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O indicador de autoavaliação - IAA, é um indicador de avaliação da dimensão psicossocial, isto é, seus resultados são uma medida produzida pelo próprio estudante, a partir de respostas sobre ele mesmo a respeito de aspesctos
                    da sua vida e da sua experiência cotidiana. <br>

                    O questionário de autoavaliação investigou seis aspectos da vida do estudante, sendo esses: 
                    - Q1: Como se sente consigo mesmo?
                    - Q2: Como se sente sobre os estudos?
                    - Q3: Como se sente sobre a sua vida familiar? 
                    - Q4: Como se sente sobre sua relação com os amigos?
                    - Q5: Como se sente sobre a Associação Passos Mágicos? 
                    - Q6: Como se sente sobre seus Professores na Passos Mágicos?

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    Confira na imagem abaixo: 

                    </p>
                    ''',unsafe_allow_html=True)        


        image =  Image.open("img/iaa_avaliacoes.png")
        st.image(image, caption= "Questionário de autoavaliação") 
        
    #Tabela IPS
    if indicador == 'IPS':

        st.markdown('''
                    <p style="font-size: 18px">

                    ######  IPS (Indicador de Psicossocial)

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O indicador Psicossocial - IPS, é um indicador de conselho da dimensão psicossocial, seus resultados foram obtidos por meio de avaliações feitas pela equipe de psicologia da Associação Passos Mágicos. 
                    Nas avaliações que resultaram na nota IPS, foram analisados quatro aspectos do desenvolvimento dos estudantes em 2022. Os elementos de avaliação, suas categorias de avaliação e seus pesos estão relacionados abaixo:

                    </p>
                    ''',unsafe_allow_html=True )

        image =  Image.open("img/ips_avaliacoes.png")
        st.image(image, caption= "Questões de avaliação do IPS, categorias e seus valores")
        
    #Tabela IPP
    if indicador == 'IPP':

        st.markdown('''
                    <p style="font-size: 18px">

                    ###### IPP (Indicador Psicopedagógico)

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O indicador Psicopedagógico - IPP, é um indicador de conselho da dimensão psicopedagógica, seus resultados foram obtidos por meio de avaliações individuais,
                    feitas por membro da equipe de professores e psicopedagogos da Associação Passos Mágicos.<bre>
                    A avaliação que produziou o IPP, foi feita pela análise individual de cada avaliador, de forma independente e sem conluio com os demais avaliadores,
                    buscando avaliar quatro aspectos dos estudantes:
                    - Desenvolvimento cognitivo;
                    - Desenvolvimento emocional; 
                    - Desenvolvimento comportamental; 
                    - Desenvolvimento social.<br>

                    </p>
                    ''',unsafe_allow_html=True)
                    
        st.markdown('''
                    <p style="font-size: 18px">
                    
                    Os avaliadores caracterizaram cada um desses aspectos, respondendo qual condição descreve melhor o seu desenvolvimento atual, as quais, então,
                    um valor. É calculado, então, o valor médio das avaliações, em cada questão, e ao final, somam-se essas médidas resultando numa nota de base comum, de 0 a 10.  
                    As questãoes, e os seus valores, então logo abaixo:                

                    </p>
                    ''',unsafe_allow_html=True)

        image =  Image.open("img/ipp_avaliacoes.png")
        st.image(image, caption= "Questões de avaliação Psicopedagógico")                   
        
    #Tabela IPV
    if indicador == 'IPV':

        st.markdown('''
                    <p style="font-size: 18px">

                    ###### IPV (Indicador de Ponto de Virada)

                    </p>
                    ''',unsafe_allow_html=True)
        
        st.markdown('''
                    <p style="font-size: 18px">

                    O indicador do Ponto de Virada - IPV, é um indicador de conselho da dimensão psicopedagógica, seus resultados foram obtidos
                    por meio de avaliações individuais, geitas por membros da equipe de professores e psicopedagogos da Associação Passos Mágicos. <br>

                    O que se chama Ponto de Virada é um estágio do desenvolvimento do estudante, no qual ele demonstra de forma ativa, por meio da sua trajetória dentro da associação, estar consciente da importância da educação, do valor do saber e da importância de aprender. 
                    Passar pelo Ponto de Virada deve sifnificar estar apto a iniciar a transformação da sua vida por meio da educação. Portanto, não se trata de um ponto de chegada, mas um momento no qual se inica uma importante mudança.<br>

                    A avaliação do IPV foi feita pela avaliação de três aspectos do desenvolvimento do estudante durante o ano letivo: 
                    - Integração à associação; 
                    - Desenovlvimento emocional;
                    - Potencial acadêmico. 

                    </p>
                    ''',unsafe_allow_html=True )

        st.markdown('''
                    <p style="font-size: 18px">
                    
                    Abaixo é demonstrado a estrutura de avaliação do IPV:                

                    </p>
                    ''',unsafe_allow_html=True)

        image =  Image.open("img/ipv_avaliacoes.png")
        st.image(image, caption= "Questões de avaliação do IPV")        


# Aplicação Analítica
elif page == page_2:

    df = pd.read_csv(base_alunos)

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
    menu = st.radio("", ["Dashboard", "Insight"], horizontal=True, label_visibility="collapsed")

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
        model = st.selectbox('Selecione o modelo:', ['Análise por Aluno', 'Defasagem', 'Desistência', 'Indicadores', 'Pedras', 'Ponto de Virada'])

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

        elif model == 'Defasagem': 

            st.subheader('Defasagem', divider='orange')

            st.markdown('''
                <p style="font-size: 18px">
                Permite verifica de forma dinâmica a defasagem dos alunos com base no gênero e ano, sendo o eixo X os níveis de defasagem existente na base.<br></p>                                            
                    1º gráfico irá demonstrar a quantidade de alunos por gênero e o seu nível de defasagem; <br>
                    2º gráfico irá apresnetar a média de idade em cada nível de defasagem.
                        
                ''', unsafe_allow_html=True)
            
            st.markdown('---')
            
            df = pd.read_csv(base_alunos)
            
            # Converter o ano para string
            df['ANO_LETIVO'] = df['ANO_LETIVO'].astype(str)

            # Criar filtros no Streamlit
            col1, col2 = st.columns(2)

            with col1:
                anos_disponiveis = sorted(df['ANO_LETIVO'].unique())
                ano_selecionado6 = st.selectbox('Selecione o ano:', [None] + list(anos_disponiveis), key='ano_selecionado6')

            with col2:
                generos_disponiveis = sorted(df['GENERO'].unique())
                genero_selecionado3 = st.selectbox('Selecione o gênero:', [None] + list(generos_disponiveis), key='genero_selecionado3')    

            # Aplicar filtros
            df_defasagem = df.copy()

            if ano_selecionado6:
                df_defasagem = df_defasagem[df_defasagem['ANO_LETIVO'] == ano_selecionado6]

            if genero_selecionado3:
                df_defasagem = df_defasagem[df_defasagem['GENERO'] == genero_selecionado3]

            #Gráfico 1: Distribuição da Defasagem por Gênero
            st.subheader("Gráfico de defasagem por Gênero")

            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.set_style("whitegrid")

            sns.countplot(data=df_defasagem, x="DEFASAGEM", hue="GENERO", palette="coolwarm", ax=ax1)

            # Adicionar rótulos e título
            ax1.set_xlabel("Defasagem", fontsize=14, fontweight="bold")
            ax1.set_ylabel("Quantidade de Alunos", fontsize=14, fontweight="bold")
            ax1.set_title("Distribuição da Defasagem por Gênero", fontsize=16, fontweight="bold")

            # Exibir os valores nas barras
            for p in ax1.patches:
                ax1.annotate(f"{int(p.get_height())}",
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5),
                            textcoords='offset points')

            # Exibir o gráfico no Streamlit
            st.pyplot(fig1)

            #Gráfico 2: Média de Idade por Nível de Defasagem**
            st.subheader("Gráfico por Média de idade por nível de Defasagem")

            fig2, ax2 = plt.subplots(figsize=(10, 6))

            sns.barplot(data=df_defasagem, x="DEFASAGEM", y="IDADE", palette="viridis", ci=None, ax=ax2)

            # Adicionar rótulos e título
            ax2.set_xlabel("Defasagem", fontsize=14, fontweight="bold")
            ax2.set_ylabel("Média de Idade", fontsize=14, fontweight="bold")
            ax2.set_title("Média de Idade por Nível de Defasagem", fontsize=16, fontweight="bold")

            # Exibir os valores acima das barras
            for p in ax2.patches:
                ax2.annotate(f"{p.get_height():.0f}",
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=12, color='black', xytext=(0, 5),
                            textcoords='offset points')

            # Exibir o gráfico no Streamlit
            st.pyplot(fig2)
            
        elif model == 'Desistência':

            st.subheader('Desistência', divider='orange')
                          
            # Carregar o DataFrame com tratamento de possíveis issues

            df = pd.read_csv(base_evasao)
            
            tabela=df
            tabela = tabela.rename(columns={
                tabela.columns[0]: 'Período',
                tabela.columns[1]: 'Alunos Reprovados',
                tabela.columns[2]: 'Alunos Desistentes',
                tabela.columns[3]: 'Total de Alunos',
                tabela.columns[4]: 'Desistência%'
            })
            tabela = tabela.dropna(axis=1, how='all')
        
            st.markdown('''
                        Dados calculados por desistência/ano:
                        ''')  
            st.write(tabela)

            siglaPeriodo_list = df['siglaPeriodo'].tolist()
            totalReprovado_list = df['TotalReprovado'].tolist()
            totalDesistente_list = df['TotalDesistente'].tolist()
            totalAlunos_list = df['TotalAlunos'].tolist()
            percDesistencia_list = df['Perc'].tolist()

            # Convertendo os valores para porcentagens
            total = np.add(totalAlunos_list, totalDesistente_list)
            percent1 = np.divide(totalAlunos_list, total) * 100
            percent2 = np.divide(totalDesistente_list, total) * 100

            x = np.arange(len(siglaPeriodo_list))
            largura = 0.8

            # Plotando as barras
            plt.figure(figsize=(12, 6)) # <-- Aumentar o tamanho do gráfico aqui
            plt.bar(x, percent2, largura, label='Desistentes', color='orange', alpha=0.7)
            plt.bar(x, percent1, bottom=percent2, label='Total de Alunos', color='blue', alpha=0.7)

            plt.plot(x, percent2, marker='o', linestyle='-', color='red', label='Perc Desistência')

            # Adicionando rótulos e título
            plt.xlabel('Período')
            plt.ylabel('Porcentagem (%)')
            plt.xticks(x, siglaPeriodo_list)

            # Criando a legenda fora da área do gráfico
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')


            with st.expander('☁️ Exibir query'):
                    st.code('''
                SELECT
                    tb.siglaPeriodo AS Periodo,
                    COUNTIF( tb.SituacaoAlunoTurma ="Reprovado" ) AS Alunos_Reprovados,
                    COUNTIF( tb.SituacaoAlunoTurma ="Desistente" ) AS Alunos_Desistentes,
                    COUNT(1) AS Total_Alunos,
                    (COUNTIF( tb.SituacaoAlunoTurma ="Desistente" ) / COUNT(1) ) * 100 AS Evasao
                    FROM (
                    SELECT
                        al.IdAluno,
                        pe.siglaPeriodo,
                        sat.SituacaoAlunoTurma,
                    FROM
                        `datathonpm.PassoMagicos.TbAluno` al
                    JOIN
                        `datathonpm.PassoMagicos.TbAlunoTurma` alt
                    ON
                        al.IdAluno = alt.IdAluno
                    JOIN
                        `datathonpm.PassoMagicos.TbTurma` tu
                    ON
                        tu.IdTurma = alt.IdTurma
                    JOIN
                        `datathonpm.PassoMagicos.TbPeriodo`pe
                    ON
                        pe.idPeriodo = tu.IdPeriodo
                    JOIN
                        `datathonpm.PassoMagicos.TbSituacaoAlunoTurma`sat
                    ON
                        sat.IdSituacaoAlunoTurma = alt.IdSituacaoAlunoTurma
                    WHERE
                        pe.SiglaPeriodo < 2024
                    GROUP BY
                        al.IdAluno,
                        pe.siglaPeriodo,
                        sat.SituacaoAlunoTurma) tb
                    GROUP BY
                    tb.siglaPeriodo
                            ''')
                        
            # Mostrando o gráfico
            plt.tight_layout() # Ajusta o layout para evitar sobreposição
            st.pyplot(plt)

            st.markdown('''
                        Intensidade dos Motivos de Inativação:
                        ''')  
      
            df = pd.read_csv(base_evasao_por_motivo)

            df_pivot = df.pivot(index='ano', columns='MotivoInativacao', values='Total').fillna(0)

            df_pivot_transposed = df_pivot.T

            plt.figure(figsize=(12, 6))
            sns.heatmap(df_pivot_transposed, annot=True, fmt=".0f", cmap="Blues")
            plt.xlabel('Ano')  
            plt.ylabel('Motivo de Inativação')  
            st.pyplot(plt)

            with st.expander('☁️ Exibir query'):
                    st.code('''
                SELECT
                EXTRACT(year  FROM    TIMESTAMP(alt.DataSituacaoInativo)) ano,
                mi.MotivoInativacao,
                COUNT(1) Total
                FROM
                `datathonpm.PassoMagicos.TbAluno` al
                JOIN
                `datathonpm.PassoMagicos.TbAlunoTurma` alt
                ON
                al.IdAluno = alt.IdAluno
                JOIN
                `datathonpm.PassoMagicos.TbMotivoInativacao` mi
                ON
                alt.IdMotivoInativacao = mi.IdMotivoInativacao
                JOIN
                `datathonpm.PassoMagicos.TbTurma` tu
                ON
                tu.IdTurma = alt.IdTurma
                JOIN
                `datathonpm.PassoMagicos.TbPeriodo`pe
                ON
                pe.idPeriodo = tu.IdPeriodo
                JOIN
                `datathonpm.PassoMagicos.TbSituacaoAlunoTurma`sat
                ON
                sat.IdSituacaoAlunoTurma = alt.IdSituacaoAlunoTurma
                WHERE
                alt.IdSituacaoAlunoTurma = 14
                AND EXTRACT(year  FROM    TIMESTAMP(DataSituacaoInativo)) < 2024
                GROUP BY
                EXTRACT(year  FROM    TIMESTAMP(DataSituacaoInativo)),
                mi.MotivoInativacao
                            ''')

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
            df = pd.read_csv(base_alunos)

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
            
            df = pd.read_csv(base_pedra_geral)
            
            plt.rcParams.update({'font.size': 14})  # Ajuste para aumentar toda a fonte do gráfico

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

            # Detectar o tema do Streamlit
            tema = st.get_option("theme.base")
            if tema == "dark":
                texto_cor = "white"
                fundo_grafico = "black"
                grade_cor = "gray"
                legenda_fundo = "black"
                legenda_borda = "white"
            else:
                texto_cor = "black"
                fundo_grafico = "white"
                grade_cor = "lightgray"
                legenda_fundo = "white"
                legenda_borda = "black"

            # Cores para o gráfico
            cores = {
                'Quartzo': '#E63946',  # Vermelho forte
                'Agata': '#F4A261',  # Laranja queimado
                'Ametista': '#6A4C93',  # Roxo escuro
                'Topazio': '#2A9D8F'  # Verde azulado
            }   

            # --------- GRÁFICO 1: Quantidade total de alunos por pedra --------- #
            st.subheader("Gráfico com a quantidade total de alunos por pedra")

            fig, ax = plt.subplots(figsize=(10, 6))

            # Ajustar fundo do gráfico
            fig.patch.set_facecolor(fundo_grafico)
            ax.set_facecolor(fundo_grafico)

            if ano_selecionado3:
                # Se um único ano for selecionado, usar gráfico de barras
                df_pedra_contagem = df_filtrado['pedra'].value_counts()
                ax.bar(df_pedra_contagem.index, df_pedra_contagem.values, 
                    color=[cores.get(p, 'gray') for p in df_pedra_contagem.index])
                ax.set_ylabel("Total de Pedras", color=texto_cor)
                ax.set_xlabel("Pedra", color=texto_cor)
                
                for i, v in enumerate(df_pedra_contagem.values):
                    ax.text(i, v + 0.5, str(v), ha='center', color=texto_cor)
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
                        ax.text(df_pedra_contagem.index[i], count, str(count), ha='center', va='bottom', color=texto_cor)

                ax.set_xlabel("Ano da Pesquisa", color=texto_cor)
                leg = ax.legend()
                leg.get_frame().set_facecolor(legenda_fundo)
                leg.get_frame().set_edgecolor(legenda_borda)
                for text in leg.get_texts():
                    text.set_color(texto_cor)

            ax.set_title("Alunos separados por PEDRA - Quantidade de alunos", color=texto_cor)
            ax.grid(color=grade_cor, linestyle='--', linewidth=0.5)
            ax.tick_params(axis='x', colors=texto_cor)
            ax.tick_params(axis='y', colors=texto_cor)

            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

            # --------- GRÁFICO 2: Distribuição percentual de alunos por pedra --------- #
            st.subheader("Gráfico de distribuição percentual de alunos por pedra")

            fig2, ax2 = plt.subplots(figsize=(10, 6))

            # Ajustar fundo do gráfico
            fig2.patch.set_facecolor(fundo_grafico)
            ax2.set_facecolor(fundo_grafico)

            bar_width = 0.15
            y_pos = np.arange(len(df_pedra_percentual.index))

            barras = []
            for i, pedra in enumerate(df_pedra_percentual.columns):
                bars = ax2.bar(y_pos + i * bar_width, df_pedra_percentual[pedra], bar_width, color=cores.get(pedra, 'gray'), label=pedra)
                barras.append((bars, df_pedra_percentual[pedra]))

            # Adicionar porcentagens corretamente
            for bars, valores in barras:
                for bar, valor in zip(bars, valores):
                    height = bar.get_height()
                    if height > 0:
                        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{valor:.1f}%', ha='center', va='bottom', color=texto_cor, fontsize=12)

            # Ajustes visuais
            ax2.set_xticks(y_pos + 1.5 * bar_width)
            ax2.set_xticklabels(df_pedra_percentual.index, color=texto_cor, fontsize=12)
            ax2.set_xlabel("Ano", color=texto_cor, fontsize=14)
            ax2.set_ylabel("Porcentagem de Alunos", color=texto_cor, fontsize=14)
            ax2.set_title("Distribuição percentual de alunos por pedra", color=texto_cor, fontsize=16)
            ax2.set_ylim(0, 70)
            ax2.grid(color=grade_cor, linestyle='--', linewidth=0.5)

            # Ajustar a legenda
            leg2 = ax2.legend()
            leg2.get_frame().set_facecolor(legenda_fundo)
            leg2.get_frame().set_edgecolor(legenda_borda)
            for text in leg2.get_texts():
                text.set_color(texto_cor)

            plt.tight_layout()
            ax2.tick_params(axis='x', colors=texto_cor)
            ax2.tick_params(axis='y', colors=texto_cor)

            # Exibir segundo gráfico
            st.pyplot(fig2)


        elif model == "Ponto de Virada":
     
            st.subheader('Ponto de Virada', divider='orange')

            st.markdown('''
                <p style="font-size: 18px">
                De forma dinâmica, é possível verificar através do ANO, GÊNERO, FASE e PV (Ponto de Virada) 
                o resultado final da base e identificar insight e entender o comportamento do ponto de virada para 
                alcançar ou se manter na mesma fase.<br>
                        ''', unsafe_allow_html=True)  
            st.markdown('''
                Segue detalhes de cada fase: 
                - ALFA (1° e 2° ano);
                - Fase 1 (3° e 4° ano);
                - Fase 2 (5° e 6° ano);
                - Fase 3 (7° e 8° ano);
                - Fase 4 (9° ano);
                - Fase 5 (1° EM);
                - Fase 6 (2° EM);
                - Fase 7 (3° EM);
                - Fase 8 (Universitários)
                - Fase 9 (Formados (EAD))   
                ''')
                                           
            df = pd.read_csv(base_alunos)

            df['ANO_LETIVO'] = df['ANO_LETIVO'].astype(str) 
            
            df_atingiu_pv = df.set_index('ANO_LETIVO')


            # Criar sessão de estado para os filtros se ainda não existirem
            for key in ['ano_selecionado5', 'genero_selecionado2', 'fase_selecionada', 'pv_selecionado']:
                if key not in st.session_state:
                    st.session_state[key] = None

                    # Criar os widgets de filtro
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                anos_disponiveis = sorted(df['ANO_LETIVO'].unique())
                ano_selecionado5 = st.selectbox('Selecione o ano:', [None] + list(anos_disponiveis), key='ano_selecionado')

            with col2:
                generos_disponiveis = sorted(df['GENERO'].unique())
                genero_selecionado2 = st.selectbox('Selecione o gênero:', [None] + list(generos_disponiveis), key='genero_selecionado2')    

            with col3:
                fases_disponiveis = sorted (df['FASE'].unique())
                fase_selecionada = st.selectbox('Selecione a fase:', [None] + fases_disponiveis, key='fase_selecionada')

            with col4:
                pv_disponiveis = sorted (df['ATINGIU_PV'].unique())
                pv_selecionado = st.selectbox('Ponto de virada:', [None] + pv_disponiveis, key='atingiu_pv')

            # Aplicar filtros
            df_ponto_virada = df.copy()

            if ano_selecionado5:
                df_ponto_virada = df_ponto_virada[df_ponto_virada['ANO_LETIVO'] == ano_selecionado5]

            if genero_selecionado2:
                df_ponto_virada = df_ponto_virada[df_ponto_virada['GENERO'] == genero_selecionado2]

            if fase_selecionada:
                df_ponto_virada = df_ponto_virada[df_ponto_virada['FASE'] == fase_selecionada]

            if pv_selecionado:
                df_ponto_virada = df_ponto_virada[df_ponto_virada['ATINGIU_PV'] == pv_selecionado]


            st.subheader("Gráfico de ponto de virada por ANO")

            # Aumentar o tamanho das fontes
            sns.set_context("talk")  # Opções: "paper", "notebook", "talk", "poster"

            # Definir a ordem personalizada das fases
            ordem_fases = ["ALFA", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            # Primeiro gráfico: Quantidade de alunos por ano letivo
            fig1, ax1 = plt.subplots(figsize=(14, 7))

            sns.countplot(
                x="ANO_LETIVO",
                hue="ATINGIU_PV",
                data=df_ponto_virada,
                palette="viridis",
                ax=ax1
            )

            # Adicionar valores acima das barras
            for p in ax1.patches:
                if p.get_height() > 0:
                    ax1.annotate(
                        f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=14, color='black', xytext=(0, 5),
                        textcoords='offset points'
                    )

            ax1.set_xlabel("Ano Letivo", fontsize=12)
            ax1.set_ylabel("Quantidade de Alunos", fontsize=12)
            ax1.set_title("Alunos que Atingiram o Ponto de Virada por Ano", fontsize=14, fontweight="bold")
            ax1.legend(title="Atingiu PV", fontsize=10, title_fontsize=12)

            st.pyplot(fig1)  # Exibir o primeiro gráfico no Streamlit

            st.markdown('---')

            st.subheader("Gráfico de ponto de virada por FASE")

            # Segundo gráfico: Quantidade de alunos por fase e situação de PV
            fig2, ax2 = plt.subplots(figsize=(14, 7))

            # Garantir que a coluna 'FASE' siga a ordem desejada
            df_ponto_virada["FASE"] = pd.Categorical(df_ponto_virada["FASE"], categories=ordem_fases, ordered=True)

            sns.countplot(
                x="FASE",
                hue="ATINGIU_PV",
                data=df_ponto_virada,
                palette="coolwarm",
                ax=ax2,
                order=ordem_fases  
            )

            # Adicionar valores acima das barras
            for p in ax2.patches:
                if p.get_height() > 0:
                    ax2.annotate(
                        f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=14, color='black', xytext=(0, 5),
                        textcoords='offset points'
                    )

            ax2.set_xlabel("Fase", fontsize=14)
            ax2.set_ylabel("Quantidade de Alunos", fontsize=14)
            ax2.set_title("Quantidade de Alunos por Fase e Situação de PV", fontsize=14, fontweight="bold")
            ax2.legend(title="Atingiu PV", fontsize=10, title_fontsize=14)

            st.pyplot(fig2)  # Exibir o segundo gráfico no Streamlit

# conclusão
elif page == page_3:

    # título
    st.title('Conclusão 📍')

    st.markdown('---')

    create_insight(
        'Conclusão Geral',
        '''
        Este projeto teve como objetivo analisar o impacto da ONG Passos Mágicos no desenvolvimento educacional de crianças e jovens em situação de vulnerabilidade social, 
        utilizando dados do período de 2020 a 2024. A combinação de ciência de dados e storytelling foi fundamental para transformar um grande volume de informações em insights acionáveis.<br><br>
        Com o uso do Google Colab para exploração e tratamento de dados e o Streamlit para a criação de um dashboard interativo, foi possível apresentar de forma intuitiva os principais indicadores de performance.
        A análise revelou tendências significativas que demonstram o impacto positivo da ONG em diversos aspectos-chave:<br><br>
        - <b>Redução da Defasagem Escolar:</b> Observou-se uma tendência de diminuição da defasagem entre idade e série, refletindo a eficácia das intervenções pedagógicas da ONG.<br>
        - <b>Aumento no "Ponto de Virada" (PV):</b> Houve um crescimento constante no número de alunos que atingiram o PV, indicando o fortalecimento de competências acadêmicas e socioemocionais.<br>
        - <b>Evolução por Gênero e Faixa Etária:</b> A distribuição equilibrada entre gêneros e a melhoria dos resultados em diferentes faixas etárias destacam o caráter inclusivo das ações da ONG.<br>
        - <b>Impacto Longitudinal:</b> A progressão consistente no desempenho acadêmico ao longo dos anos sugere que o impacto da ONG é cumulativo e sustentável.<br><br>
        Esses resultados não apenas evidenciam o papel transformador da Passos Mágicos, mas também oferecem subsídios valiosos para a tomada de decisões estratégicas. O uso de visualizações interativas facilita o acompanhamento dos indicadores, permitindo que gestores e stakeholders da ONG identifiquem oportunidades de melhoria e ampliem o impacto de suas iniciativas.
        Dessa forma, este trabalho reforça a importância da análise de dados no terceiro setor, demonstrando como a tecnologia pode ser uma aliada poderosa na promoção da transformação social por meio da educação.                  
        '''
    )
    
    st.markdown('---')
    
    with st.expander('🚀 Principais Insights'):

        # Texto de introdução
        st.markdown('''
                    #### Principais Insights
                    Os principais <i>insights</i> e respectivas etapas de melhorias ao projeto,
                    obtidos durante os processos de análise dos dados e construção dos modelos, são retratados a seguir.

                    ---
                    ''', unsafe_allow_html=True)

        # Lista de opções para o st.radio
        opcoes = ["Defasagem", "Desistência", "Indicadores", "Pedras", "Ponto de Virada"]

        # Cria o st.radio para selecionar uma opção
        escolha = st.radio("**Selecione um Insight:**", opcoes)

        # Variável para armazenar o texto a ser exibido
        texto_exibido = ""

        if escolha == "Defasagem":
            texto_exibido = """
            ### Defasagem
            A análise dos gráficos mostra padrões importantes sobre a defasagem escolar e como ela se relaciona com idade e gênero. A maioria dos alunos está no nível esperado de desempenho, enquanto aqueles com defasagem, tanto para mais quanto para menos, são minoria.

            Os dados indicam que alunos com maior defasagem negativa costumam ser mais velhos, o que sugere dificuldades no aprendizado que podem ser trabalhadas com estratégias de recuperação. Já os alunos com defasagem positiva têm idades mais próximas entre si, o que pode indicar um desempenho avançado e a necessidade de estímulos para manter seu desenvolvimento.

            Além disso, as diferenças entre gêneros, mesmo que sutis, reforçam a importância de uma abordagem de ensino inclusiva e adaptável. Essas informações podem ajudar a instituição PASSOS MÁGICOS a aprimorar sua metodologia, reduzir desigualdades e melhorar o desempenho de todos os alunos.
            """

        elif escolha == "Desistência":
            texto_exibido = """
            ### Desistência
            1. Motivos Mais Comuns de Inativação
            Falta de retorno às tentativas de contato: Esse motivo aparece com frequência em 2022 (256 casos) e 2023 (55 casos), indicando que muitos responsáveis não respondem às tentativas de contato da organização.
            Mudança de bairro/cidade/distância: Esse motivo também é significativo, especialmente em 2022 (209 casos) e 2023 (54 casos), sugerindo que a localização geográfica é um fator importante para a inativação.
            Outras prioridades/trabalho: Esse motivo é relevante em ambos os anos, com 126 casos em 2022 e 87 casos em 2023, indicando que compromissos profissionais ou outras prioridades podem impedir a continuidade.
            2. Variação Anual dos Motivo
            2022 vs. 2023: Em 2022, os motivos mais comuns foram "Falta de retorno às tentativas de contato" e "Mudou de bairro/cidade/distância". Em 2023, esses motivos continuam relevantes, mas com números menores, possivelmente indicando uma melhora nas estratégias de engajamento ou mudanças nas circunstâncias dos participantes.
            Motivos Menos Comuns: Alguns motivos, como "Iniciou curso superior sem auxílio da Passos" (6 casos em 2023) e "Suspensão - Comportamento inadequado" (6 casos em 2023), são menos frequentes, mas ainda relevantes para análises específicas.
            3. Tendências ao Longo do Tempo
            Redução em Certos Motivos: Alguns motivos, como "Falta de retorno às tentativas de contato", tiveram uma redução significativa de 2022 para 2023 (de 256 para 55 casos). Isso pode indicar que a organização melhorou suas estratégias de comunicação ou que os responsáveis estão mais engajados.
            Aumento em Outros Motivos: Motivos como "Sem responsável para levar a criança até a unidade" (66 casos em 2023) e "Sem condição financeira para o transporte público" (29 casos em 2023) podem indicar desafios socioeconômicos que estão se tornando mais prevalentes.
            4. Distribuição dos Motivos
            Concentração de Motivos: Alguns anos têm uma concentração maior de motivos específicos. Por exemplo, em 2022, "Falta de retorno às tentativas de contato" e "Mudou de bairro/cidade/distância" dominam os números, enquanto em 2023 há uma distribuição mais equilibrada entre vários motivos.
            Motivos Específicos por Ano: Em 2021, os números são menores, mas ainda é possível identificar motivos como "Conflito com horário escolar / período integral" (8 casos) e "Desinteresse / Falta de retorno" (10 casos).
            5. Implicações para Ações Futuras
            Melhoria na Comunicação: Dado o alto número de casos de "Falta de retorno às tentativas de contato", a organização pode precisar revisar e melhorar suas estratégias de comunicação com os responsáveis.
            Apoio Financeiro e Logístico: Motivos como "Sem condição financeira para o transporte público" e "Sem responsável para levar a criança até a unidade" sugerem a necessidade de apoio logístico e financeiro para as famílias.
            Adaptação às Necessidades dos Participantes: Motivos como "Não se adaptou às aulas/não acompanhou" (13 casos em 2023) e "Excesso de atividades" (33 casos em 2023) indicam a necessidade de revisar o currículo e a carga horária para melhor atender às necessidades dos participantes.
            6. Análise de Dados Antigos (2021
            Embora os dados de 2021 sejam limitados, eles mostram que alguns motivos, como "Conflito com horário escolar / período integral" e "Desinteresse / Falta de retorno", já estavam presentes, sugerindo que esses são desafios persistentes.
            """

        elif escolha == "Indicadores":
            texto_exibido = """
            ### Indicadores
            O INDE é o indicador principal, com ele é decidido várias ações. Com base em outros indicadores, conseguimos chegar numa nota média no INDE, sendo assim, decidimos apresentar apenas este indicador na conclusão do nossos insight. 

            Em suma, o indicador INDE apresentou uma média de 6.84, com valores variando de 3.03 a 9.53. A maioria dos alunos está concentrada nas faixas intermediárias (5.6 a 8.8), indicando um desempenho de moderado a alto.

            Em 2024, houve um aumento no número de alunos com INDE mais elevado e uma redução na quantidade de estudantes nos níveis mais baixos, 
            sugerindo melhorias no desempenho educacional, é importante manter ações voltadas ao fortalecimento do aprendizado, especialmente para os alunos que ainda se encontram nos níveis mais baixos.

            Para manter essa evolução, é essencial continuar investindo em suporte pedagógico e acompanhamento individualizado, garantindo que mais alunos alcancem níveis mais altos de desenvolvimento e garantir que cheguem às fases universitárias e de formação.
            """

        elif escolha == "Pedras":
            texto_exibido = """
            ### Pedras
            Os gráficos demonstram como a quantidade e a distribuição dos alunos por pedra evoluíram de 2020 a 2024, separando os dados por gênero.

            O grupo Topázio cresceu bastante e se tornou o mais numeroso, enquanto o Quartzo, que antes tinha mais alunos, perdeu participação. Já os grupos Ágata e Ametista se mantiveram mais estáveis.

            Além disso, o número de alunas aumentou mais do que o de alunos, principalmente nos grupos de maior desempenho. Esses dados sugerem uma melhora geral no rendimento dos estudantes ao longo dos anos.

            **Considerações Finais:**
            - Crescimento do Topázio: Mais alunos estão atingindo níveis mais altos de desempenho.
            - Declínio do Quartzo: Menos alunos permanecem nas classificações mais baixas.
            - Diferenças por Gênero: As alunas tiveram um crescimento maior, especialmente nos grupos com melhor desempenho.
            """

        elif escolha == "Ponto de Virada":
            texto_exibido = """
            ### Ponto de Virada
            O número de alunos que não atingiram o ponto de virada em 2024 teve um aumento significativo, enquanto os alunos que atingiram teve uma queda, 
            o que pode sinalizar desafios para determinadas turmas ou fases.

            As fases iniciais possuem mais alunos, mas há uma queda significativa conforme avançam, o que pode indicar evasão ou dificuldades acadêmicas. 
            É necessário reforçar o acompanhamento nas fases intermediárias e incentivar a continuidade dos estudos para melhorar os resultados.


            **Conclusão e Recomendações:**
            - O aumento dos alunos que não atingiram o ponto de virada em 2024 exige uma análise para identificar as dificuldades.
            - Estratégias de acompanhamento nas fases intermediárias são necessárias, pois há uma queda significativa no número de alunos conforme avançam.
            - Incentivo à continuidade nos estudos deve ser reforçado para garantir que mais alunos cheguem às fases universitárias e de formação.
            """

        st.markdown('---')

        # Exibe o texto manipulado usando st.markdown
        st.markdown(texto_exibido)

    st.markdown('---')
    
    create_insight(
        'Próximos passos',

        '''
        Com base na análise realizada sobre o impacto da ONG Passos Mágicos no desenvolvimento educacional de crianças e jovens em situação de vulnerabilidade social,
        é crucial planejar os próximos passos para aprimorar ainda mais as iniciativas e garantir um impacto sustentável e significativo. Aqui estão algumas sugestões de melhoria focadas em potencializar o trabalho da associação:

        <b>1 - Reforço das Intervenções Pedagógicas Personalizadas:</b>

        - Utilizar os dados para identificar alunos com maiores dificuldades e oferecer apoio individualizado. Ferramentas de aprendizado adaptativo e tutoria personalizada podem ser implementadas para atender às necessidades específicas de cada aluno, reduzindo ainda mais a defasagem escolar.
        
        <b>2- Ampliação de Programas de Desenvolvimento Socioemocional:</b>

        - Fortalecer os programas focados no desenvolvimento de competências socioemocionais, já que o aumento no "Ponto de Virada" (PV) indica sucesso nessas áreas. Isso pode incluir oficinas, atividades extracurriculares e acompanhamento psicológico para ajudar os alunos a desenvolverem resiliência, empatia e habilidades de comunicação.
        
        <b>3 - Expansão das Tecnologias Educacionais:</b>

        - Investir em tecnologias educacionais que facilitem o aprendizado interativo e a personalização. A utilização de plataformas como Google Colab e Streamlit demonstrou ser eficaz, e novas ferramentas podem ser exploradas para enriquecer ainda mais a experiência de aprendizado dos alunos.

        <b>4 - Capacitação e Formação de Educadores:</b>

        - Oferecer programas de capacitação contínua para os educadores e voluntários da ONG. A formação em metodologias pedagógicas inovadoras e o uso de tecnologia na educação são essenciais para garantir a qualidade das intervenções.         
        '''
    )

# referências        
else:

    st.title('Referências 📝')
    st.markdown('---')     
    # subtítulo
    st.header('Fontes de dados')
    st.markdown('''
                <p style="font-size: 18px">
                    Os dados utilizados neste projeto foram obtidos a partir das fontes listadas abaixo:
                </p>
                ''', unsafe_allow_html=True)
    
        # lista de fontes de dados
    st.markdown('''
                #### [**Passos Mágicos**](https://passosmagicos.org.br/quem-somos/) -  Associação Passos Mágicos
                Associação Passos Mágicos tem uma trajetória de 30 anos de atuação, 
                trabalhando na transformação da vida de crianças e jovens de baixa renda os levando a melhores oportunidades de vida.
                ''')
    
    st.markdown('''
                #### [**Google**](https://drive.google.com/drive/folders/1Z1j6uzzCOgjB2a6i3Ym1pmJRsasfm7cD) - Repositório Google Drive
                Repositório disponobiliado pela FIAP com a bases de dados, dicionário de dados, relatórios e documentação.
                ''')
    
    st.markdown(''' 
                #### [**GITHUB**](https://github.com/r-zambotti/Data_Analytics_Datathon_Grupo-60) - Repositório do projeto  
                O repositório "Data_Analytics_Datathon_Grupo-60" no GitHub foi criado para a análise exploratória da  
                metodologia "Passos Mágicos".  
                Contém notebook Jupyter (Data_Analytics_Datathon_Grupo_60.ipynb) que realiza as análise dos dados fornecidos.  
                Arquivos Python (app.py e utils.py) que auxiliam no processamento dos dados e na execução de funcionalidades adicionais.  
                A licença do projeto é MIT.  
                ''')
    st.markdown('---')     
    # subtítulo para Bibliografia
    st.header('Bibliografia')
    # lista de links
    st.markdown('''
                    - [**ASSOCIAÇÃO PASSOS MÁGICOS**](https://passosmagicos.org.br/quem-somos/) -  Associação Passos Mágicos
                    - [**Google Drive**](https://drive.google.com/drive/folders/1Z1j6uzzCOgjB2a6i3Ym1pmJRsasfm7cD) - Base de dados FIAP
                    - [**Relatorio_PEDE2022**](https://drive.google.com/file/d/1KrQR6Q7PvX_tZEPyKmc3c6HlTmfy1lDe/view) - SILVA, Dario Rodrigues da. Pesquisa Extensiva do Desenvolvimento Educacional - PEDE 2022. 
                      Associação Passos Mágicos. São Paulo, p. 217. 2023.    
                    - [**Dicionário Dados Datathon**](https://drive.google.com/file/d/1Z8Rs6SLicxMJUu_zwrYD399mPvs-djVb/view?usp=drive_link) -  Dicionário de Dados Dataset PEDE_PASSOS                           
                ''')
# footer
st.markdown('<br>', unsafe_allow_html=True)

st.markdown('---')

# texto -> Agradecimentos
st.markdown('''<p style="font-size: 18px; text-align: center;">
            Obrigado por acompanhar este projeto! 🚀
            <br>
            </p>''', unsafe_allow_html=True)