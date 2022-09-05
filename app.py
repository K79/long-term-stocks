import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st


st.title('高配当日本株の株価可視化アプリ')

st.sidebar.write("""
#高配当日本株
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** の高配当日本株
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 10000.0, (0.0, 10000.0)
    )

    tickers = {
        'INPEX':'1605.T',
        '花王':'4452.T',
        'アステラス製薬':'4503.T',
        'ブリヂストン':'5108.T',
        '小松製作所':'6301.T',
        'クボタ':'6326.T',
        '伊藤忠商事':'8001.T',
        '三井物産':'8031.T',
        '日本取引所':'8697.T'

        
        
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['INPEX','花王', 'アステラス製薬','ブリヂストン','小松製作所','クボタ','伊藤忠商事','三井物産', '日本取引所']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (円)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': '株価(円)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("株価(円):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラー"
    )