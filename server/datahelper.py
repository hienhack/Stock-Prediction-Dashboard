import pandas as pd

def addROC(df: pd.DataFrame) -> pd.DataFrame:
    df['ROC'] = ((df['Close'] - df['Close'].shift(12)) / (df['Close'].shift(12))) * 100
    return df

def addRSI(df):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def addMovingAverage(df):
    df['Moving Average'] = df['Close'].rolling(window=14).mean()
    return df

def prepare_data(df):
    if df.empty:
        raise ValueError("No data found. Please check the period and interval values.")
    df = addROC(df)
    df = addRSI(df)
    df = addMovingAverage(df)
    df = df.dropna()
    return df