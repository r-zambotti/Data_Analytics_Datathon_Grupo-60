## ----------------------------------------- ##
##                  Imports                  ##
## ----------------------------------------- ##
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

## ----------------------------------------- ##
##                 Streamlit                 ##
## ----------------------------------------- ##

def create_warning(title=None, text=None) -> None:
    '''
    Creates text box with alert style, 
    using HTML and markdown.
    
    Parameters:
    title: str, title of the alert.
    text: str, text of the alert.
    
    Returns:
    None
    '''
    if title is None and text is None:
        st.markdown(f'''
                <div style="background-color: #FED8D4; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">⚠️ Alerta: </p>
                    <p style="color: #000">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                ''', unsafe_allow_html=True)
    
    else:
        st.markdown(f'''
                <div style="background-color: #FED8D4; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">⚠️ {title}: </p>
                    <p style="color: #000">{text}</p>
                </div>
                ''', unsafe_allow_html=True)


def create_insight(title=None, text=None) -> None:
    '''
    Creates text box with alert style, 
    using HTML and markdown.
    
    Parameters:
    title: str, title of the alert.
    text: str, text of the alert.
    
    Returns:
    None
    '''
    if title is None and text is None:
        st.markdown(f'''
                <div style="background-color: #95C0E1; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">🌟 Insight: </p>
                    <p style="color: #000">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                ''', unsafe_allow_html=True)
    
    else:
        st.markdown(f'''
                <div style="background-color: #95C0E1; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">🌟 {title}: </p>
                    <p style="color: #000">{text}</p>
                </div>
                ''', unsafe_allow_html=True)
         

def create_quote(text=None, reference=None, link=None) -> None:
    '''
    Citation format for texts.
    
    Parameters:
    text: str, text to be cited.
    reference: str, author or source of the text.
    link: str, link to the source (optional).
    '''
    
    if link is None:
        st.markdown(f'''
                    <div style="padding-left: 100px; 
                                padding-right: 100px;
                                padding-top: 20px;
                                padding-bottom: 10px;
                                font-family: 'Times New Roman', Times, serif">
                    <p style="font-size: 18px; font-style: italic;">{text}<br>{reference}</p>
                    ''', unsafe_allow_html=True)


    else:
        st.markdown(f'''
                    <div style="padding-left: 100px;
                                padding-right: 100px;
                                padding-top: 20px;
                                padding-bottom: 10px;
                                font-family: 'Times New Roman', Times, serif">
                    <p style="font-size: 18px; font-style: italic;">{text}<br>
                        <a href="{link}" target="_blank style="color: #333333, font-size: 28px">
                        {reference}
                        </a>
                    </p>
                    ''', unsafe_allow_html=True)