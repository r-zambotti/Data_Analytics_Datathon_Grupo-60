## ----------------------------------------- ##
##                  Imports                  ##
## ----------------------------------------- ##

import yfinance as yf

import time

import pandas as pd
import numpy as np

from pandas.tseries.offsets import YearEnd
from pandas.tseries.holiday import USFederalHolidayCalendar

import pandas_ta as ta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker

import seaborn as sns

import scipy.stats as stats

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm

from sklearn.model_selection import TimeSeriesSplit
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# import itertools

import streamlit as st

import warnings
warnings.filterwarnings('ignore')

## ----------------------------------------- ##
##          Data Collection & Cleaning       ##
## ----------------------------------------- ##

def get_yfinance_prices(tickers, start, end):
    '''
    Get close prices from yfinance for a list of tickers.
    
    Parameters:
    tickers (dict): dictionary with tickers and names
    start (str): start date
    end (str): end date
    
    Returns:
    df (pd.DataFrame): dataframe with close prices
    '''
    df = pd.DataFrame()
    for ticker, name in tickers.items():
        try:
            df[name] = yf.download(ticker, start=start, end=end)['Close']
            # sleep for 1 second
            time.sleep(1)
            df.index.name = 'date'
        except:
            print(f'Error downloading {name}')
    return df


## ----------------------------------------- ##
##            Plots & Statistics             ##
## ----------------------------------------- ##

def plot_series(dataframe, series, same_ax=True,  
                title=None, xlabel=None, ylabel=None, 
                figsize=(15, 6), color='#1f3979',
                grid=True, legend=False):
    ''' Plots one or multiple time series.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe containing the time series.
    series : str or list
        Name of the column(s) to be plotted.
    same_ax : bool, optional
        If True, plots all series in the same axis. The default is True.
    title : str
        Title of the plot.
    xlabel : str
        Label of the x axis.
    ylabel : str
        Label of the y axis.
    figsize : tuple, optional
        Figure size. The default is (15, 6).
    color : str, optional
        Color of the plot. The default is '#1f3979'.
    grid : bool, optional
        If True, shows grid. The default is True.
    legend : bool, optional
        If True, shows legend. The default is False.
        
    '''
    # if series is a string, convert to list
    if type(series) == str:
        series = [series]
    
    # plot in the same axis
    if same_ax:
        plt.figure(figsize=figsize)
        for serie in series:
            plt.plot(dataframe[serie], color=color, label=serie)
        plt.title(title, fontsize=20)
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        if grid:
            plt.grid(True, alpha=0.5, linestyle='--')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))
        plt.xticks(fontsize=12, rotation=30)
        plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        plt.yticks(fontsize=12)
        if legend:
            plt.legend(loc='best')
        plt.tight_layout()
        plt.show()
    # plot in individual subplots
    else:
        fig, ax = plt.subplots(len(series), 1, figsize=(15, 5*len(series)))
        for i, serie in enumerate(series):
            ax[i].plot(dataframe[serie], color=color)
            ax[i].set_title(serie)
            ax[i].spines['right'].set_visible(False)
            ax[i].spines['top'].set_visible(False)
            ax[i].yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
            ax[i].xaxis.set_major_locator(mdates.YearLocator(1))
            ax[i].tick_params(axis='x', labelrotation=30)
            if grid:
                ax[i].grid(True, alpha=0.5, linestyle='--')
        plt.tight_layout()
        plt.show()


def plot_acf_pacf(series, lags):
    ''' Plots the autocorrelation and 
    partial autocorrelation functions.
    
    Parameters
    ----------
    series : pandas.Series
        Time series.
    lags : int or list
        Number of lags to be plotted.
    
    '''
    if type(lags) == int:
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        sm.graphics.tsa.plot_acf(series, lags=lags, ax=ax[0], color='#1f3979')
        sm.graphics.tsa.plot_pacf(series, lags=lags, ax=ax[1], color='#e34592')
        plt.title(f'Correlação e Autocorrelação com lags: {lags}', fontsize=20)
        
    elif type(lags) == list:
        # plot in individual subplots
        fig, ax = plt.subplots(len(lags), 2, figsize=(15, 5*len(lags)))
        for i, lag in enumerate(lags):
            sm.graphics.tsa.plot_acf(series, lags=lag, ax=ax[i, 0])
            sm.graphics.tsa.plot_pacf(series, lags=lag, ax=ax[i, 1])
            ax[i, 0].set_title(f'Correlação com lags: {lag}')
            ax[i, 1].set_title(f'Autocorrelação com lags: {lag}')
    else:
        raise TypeError('lags must be an integer or a list of integers.')
    plt.tight_layout()
    plt.gca().spines['right'].set_visible(False) # colocar em folha de estilo
    plt.gca().spines['top'].set_visible(False)
    plt.show()


def plot_decomposition(df, column, period=252, model='multiplicative'):
    ''' Decomposes a time series and plots it.
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame with time series.
    column : str
        Column name of the time series.
    period : int, optional
        Seasonal period. The default is 252.
    model : str, optional
        Model to be used in the decomposition. The default is 'multiplicative'.
    
    '''
    # decompose
    decomp = seasonal_decompose(df[column], model=model, period=period)
    
    # plot with subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15, 8))
    decomp.observed.plot(ax=ax1, color='#1f3979')
    ax1.set_ylabel('Observado')
    decomp.trend.plot(ax=ax2, color='#1f3979')
    ax2.set_ylabel('Tendência')
    decomp.seasonal.plot(ax=ax3, color='#1f3979')
    ax3.set_ylabel('Sazonalidade')
    decomp.resid.plot(ax=ax4, color='#1f3979')
    ax4.set_ylabel('Resíduos')
    plt.suptitle(f'Decomposição de {column}', fontsize=20)
    plt.tight_layout()
    plt.show()


def normality_test(data, alpha=0.05) -> dict:
    '''
    Performs the Kolmogorov-Smirnov test for normality.
    
    Parameters:
    data: pd.Series
    alpha: float
    
    Returns:
    dict
    '''
    stat, p = stats.kstest(data, 'norm')
    result_dict = {'statistic': stat,
                     'p-value': p,
                     'alpha': alpha,
                     'normal': False}
    
    if p > alpha:
        result_dict['normal'] = True
        
    return result_dict


def stationarity_test(dataframe, column, window=252):
    ''' Performs the Dickey-Fuller test and plots 
    the rolling mean and rolling standard deviation.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe containing the time series.
    column : str
        Column name of the time series.
    window : int, optional
        Rolling window. The default is 252.
    
    Returns
    -------
    None.
    '''
    # perform Dickey-Fuller test
    dftest = adfuller(dataframe[column], autolag='AIC')
    # create a series with the results
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    # loop through the critical values
    for key, value in dftest[4].items():
        # add the critical values to the series
        dfoutput[r'Critical Value (%s)' %key] = value
    
    # plot rolling mean and standard deviation
    plt.figure(figsize=(15, 5))
    plt.plot(dataframe[column], color='#1f3979', label='Original')
    plt.plot(dataframe[column].rolling(window=window).mean(), color='#e34592', label='Rolling Mean')
    # std as area between rolling mean and rolling std
    plt.fill_between(dataframe.index, dataframe[column].rolling(window=window).mean() - dataframe[column].rolling(window=window).std(),
                        dataframe[column].rolling(window=window).mean() + dataframe[column].rolling(window=window).std(), 
                        color='#f6c409', alpha=0.2)
    plt.legend(loc='best')
    plt.title(f'Média Móvel e Desvio Padrão de {column}', fontsize=20)
    plt.xticks(rotation=45) # repensar rotação
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.tight_layout()
    plt.show()
    
    # print the results
    print(dfoutput)
    print('--'*20)
    print('Results of Dickey-Fuller Test:')
    if dfoutput['Test Statistic'] < dfoutput['Critical Value (1%)']:
        print('The Test Statistic is lower than the Critical Value (1%). The series is stationary.')
    elif dfoutput['Test Statistic'] < dfoutput['Critical Value (5%)']:
        print('The Test Statistic is lower than the Critical Value (5%). The series is stationary.')
    elif dfoutput['Test Statistic'] < dfoutput['Critical Value (10%)']:
        print('The Test Statistic is lower than the Critical Value (10%). The series is stationary.')
    else:
        print('The Test Statistic is higher than the Critical Values. The series is not stationary.')
        
    if dfoutput['p-value'] < 0.05:
        print('The p-value is lower than 0.05. The series is stationary.')
    else:
        print('The p-value is higher than 0.05. The series is not stationary.')


## ----------------------------------------- ##
## Data Transformation & Feature Engineering ##
## ----------------------------------------- ##

def map_lag(dataframe, column, lags):
    ''' Maps exacly the same date from 
    the previous year, two and three years ago, 
    six months ago, three months ago and one month ago.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe containing the time series.
    column : str
        Column name of the time series.
    lag : int
        Number of lags in days.
    
    Returns
    -------
    pandas.DataFrame
        Dataframe containing the time series with lag features.
    '''
    
    df = dataframe.copy()
    
    target_map = df[column].to_dict()
    
    # calculate 1 year ago from date
    for lag in lags:
        df[f'lag_{lag}'] = (df.index - pd.Timedelta(days=lag)).map(target_map)
    
    return df


def date_features(dataframe):
    ''' Takes the index, changes his name to date,
    and creates datetime features for the index.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe containing the time series.
    
    Returns
    -------
    pandas.DataFrame
        Dataframe containing the time series with datetime features.
    '''
    
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

# generate calendar
def generate_calendar(year, drop_index=False):
    '''
    Simple function to generate a calendar containing
    US holidays, weekdays and  holiday weeks.
    '''
    start_date = pd.to_datetime('1/1/'+str(year))
    end_date = start_date + YearEnd()
    DAT = pd.date_range(str(start_date), str(end_date), freq='D')
    MO = [d.strftime('%B') for d in DAT]
    holidays = USFederalHolidayCalendar().holidays(start=start_date, end=end_date)

    cal_df = pd.DataFrame({'date':DAT, 'month':MO})
    cal_df['year'] = [format(d, '%Y') for d in DAT]
    cal_df['weekday'] = [format(d, '%A') for d in DAT]
    cal_df['is_weekday'] = cal_df.weekday.isin(['Monday','Tuesday','Wednesday','Thursday','Friday'])
    cal_df['is_weekday'] = cal_df['is_weekday'].astype(int)
    cal_df['is_holiday'] = cal_df['date'].isin(holidays)
    cal_df['is_holiday'] = cal_df['is_holiday'].astype(int)
    cal_df['is_holiday_week'] = cal_df.is_holiday.rolling(window=7,center=True,min_periods=1).sum()
    cal_df['is_holiday_week'] = cal_df['is_holiday_week'].astype(int)
    
    if not drop_index: cal_df.set_index('date', inplace=True)
    
    return cal_df

def make_calendars(year_list, drop_index):
    cal_df = pd.DataFrame()
    for year in year_list:
        cal_df = pd.concat([cal_df, generate_calendar(year, drop_index)], axis=0)
    return cal_df


def rolling_dataframe(dataframe, column, window, plot=True):
    ''' Calculates the rolling mean and 
    standard deviation of a time series.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe containing the time series.
    column : str
        Column name of the time series.
    window : int
        Window size.
    plot : bool, optional
    
    Returns
    -------
    pandas.DataFrame
        Dataframe containing the rolling mean and standard deviation.
    '''
    df_rolling = dataframe.copy()
    df_rolling['rolling_mean'] = df_rolling[column].rolling(window=window).mean()
    df_rolling['rolling_std'] = df_rolling[column].rolling(window=window).std()
    
    if plot:
        fig, ax = plt.subplots(figsize=(15, 5))
        df_rolling[column].plot(ax=ax, label='Original', color='#1f3979')
       # rolling as dashed line
        df_rolling['rolling_mean'].plot(ax=ax, label='Rolling Mean', color='#e34592', style='--', linewidth=2)
        # std as sum of rolling mean and rolling std fill
        ax.fill_between(df_rolling.index, df_rolling['rolling_mean'] - df_rolling['rolling_std'], 
                        df_rolling['rolling_mean'] + df_rolling['rolling_std'], color='#e34592', alpha=0.2)
        # title
        plt.title(f'Média Móvel e Desvio Padrão de {column}', fontsize=20)
        plt.ylim(df_rolling[column].min() * 0.95, df_rolling[column].max() * 1.05)
        plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()
    
    # drop NaNs
    df_rolling.dropna(inplace=True)
    
    return df_rolling


def create_ta_indicators(df, column) -> pd.DataFrame:
    '''
    Adds technical analysis indicators to the dataframe:
    - RSI (14 days)
    - MACD (12, 26, 9)
    - EMA (14, 26, 200)
    
    Parameters:
    - df: pandas.DataFrame
    - column: str
    
    Returns:
    - df: pandas.DataFrame
    '''
    
    df[f'{column}_rsi'] = ta.rsi(df[column], length=14)
    df[f'{column}_macd'] = ta.macd(df[column], fast=12, slow=26, signal=9)[['MACD_12_26_9']]
    df[f'{column}_macd_signal'] = ta.macd(df[column], fast=12, slow=26, signal=9)[['MACDs_12_26_9']]
    df[f'{column}_macd_hist'] = ta.macd(df[column], fast=12, slow=26, signal=9)[['MACDh_12_26_9']]
    df[f'{column}_ema_14'] = ta.ema(df[column], length=14)
    df[f'{column}_ema_26'] = ta.ema(df[column], length=26)
    df[f'{column}_ema_200'] = ta.ema(df[column], length=200)
    
    # dropar vazios
    df.dropna(inplace=True)
    
    return df


def time_series_split(df, n_splits=5, test_size=365, plot=True, y='preco_petroleo_brent'):
    """
    Split time series data into train and test sets.
    
    df: pandas DataFrame
    n_splits: int, number of splits
    test_size: int, size of test set
    plot: bool, plot train and test sets
    y: str, column name to plot
    
    return: list of tuples (train_index, test_index)
    """
    # sort df
    df = df.sort_index()
    # create time series split
    tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)
    
    for train_index, test_index in tscv.split(df):
        train = df.iloc[train_index]
        test = df.iloc[test_index]
        
    if plot:
        fig, ax = plt.subplots(figsize=(15, 15), nrows=n_splits, ncols=1)
        for i, (train_index, test_index) in enumerate(tscv.split(df)):
            train = df.iloc[train_index]
            test = df.iloc[test_index]
            sns.lineplot(x=train.index, y=y, data=train, 
                         ax=ax[i], label='train', color='#1f3979')
            sns.lineplot(x=test.index, y=y, data=test, 
                         ax=ax[i], label='test', color='#e34592')
            ax[i].axvline(x=test.index.min(), color='black', linestyle='--')
            ax[i].set_title(f'Fold {i+1}')
            ax[i].set_xlabel('Data')
            ax[i].set_ylabel('Preço')
            ax[i].legend(loc='upper right')
        plt.tight_layout()
        plt.show()
        
    return train, test


## ----------------------------------------- ##
##      Model Construction & Evaluation      ##
## ----------------------------------------- ##

def transform_prophet(df, y, regressors=None) -> pd.DataFrame:
    ''' Transform dataframe to be used in prophet.
    
    Parameters
    ----------
    df : pandas dataframe
        Dataframe with date as index and y and regressors as columns.
    y : str
        Name of column with y.
    regressors : list
        List with names of columns with regressors.
    
    '''
    # create dataframe
    df_prophet = pd.DataFrame()
    
    # add date
    df_prophet['ds'] = df.index
    
    # add y
    df_prophet['y'] = df[y].values
    
    # add regressors
    if regressors is not None:
        for regressor in regressors:
            df_prophet[regressor] = df[regressor].values

    return df_prophet


def mape(y_true, y_pred, round=None) -> float:
    ''' Calculates the mean absolute percentage error.
    
    Parameters
    ----------
    y_true : array-like
        Ground truth (correct) target values.
    y_pred : array-like
        Estimated target values.
    round : int, optional
        Number of decimal places to round the result. The default is None.
    
    Returns
    -------
    float
        Mean absolute percentage error.
    '''

    if round is not None:
        return np.round(np.mean(np.abs((y_true - y_pred) / y_true)) * 100, round)
    
    else:
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


## ----------------------------------------- ##
##                 Streamlit                 ##
## ----------------------------------------- ##

def insert_image(image_path, caption, source=None, width=600) -> None:
    '''
    Insert image in the streamlit app.
    
    Parameters:
    image_path: str, path to the image.
    caption: str, caption of the image.
    source: str, source of the image.
    width: int, width of the image. Default is 600.
    
    Returns:
    None
    '''

    st.image(image_path, width=width)
    # legenda
    if source is None:
        st.markdown(f'<p style=font-size: 12px">{caption}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style=font-size: 12px">{caption} | <a href="{source}" target="_blank">[Link]</a></p>', unsafe_allow_html=True)
    

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


def create_analysis(title=None, text=None) -> None:
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
                <div style="background-color: #C7E0AF; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">🔎 Análise: </p>
                    <p style="color: #000">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                ''', unsafe_allow_html=True)
    
    else:
        st.markdown(f'''
                <div style="background-color: #C7E0AF; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">🔎 {title}: </p>
                    <p style="color: #000">{text}</p>
                </div>
                ''', unsafe_allow_html=True)
        

def create_curiosity(title=None, text=None) -> None:
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
                <div style="background-color: #CFCFCF; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">📖 Curiosidade: </p>
                    <p style="color: #000">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                </div>
                ''', unsafe_allow_html=True)
    
    else:
        st.markdown(f'''
                <div style="background-color: #CFCFCF; padding: 30px; border-radius: 10px">
                    <p style="color: #000; font-size: 18px; font-weight: bold">📖 {title}: </p>
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