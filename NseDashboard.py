from nselib import capital_market
from nselib import derivatives
import streamlit as st,pandas as pd
from bs4 import BeautifulSoup
import requests

st.header("Indian Stock Dashboard 2024")

data_type=st.selectbox("Type of Data:",options=["Google Finance Data","NSE lib Data"])

if(data_type=="Google Finance Data"):
   
    ticker=st.sidebar.text_input("symbol code","INFY")
    exchange=st.sidebar.text_input("Exchange","NSE")

    url=f'https://www.google.com/finance/quote/{ticker}:{exchange}'

    response=requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price=float(soup.find(class_='YMlKec fxKbKc').text.strip()[1:].replace(",",""))
    privous_close=float(soup.find(class_='P6K39c').text.strip()[1:].replace(",",""))
    news=soup.find(class_='Yfwt5').text
    revenue=soup.find(class_='QXDnM').text
    about=soup.find(class_='bLLb2d').text

    dict1={'Price':price,'Privous_close':privous_close,'News':news,
        'About':about,'Revenue':revenue}

    df=pd.DataFrame(dict1,index=['Extracted Data']).T
    st.write(df)
    

if(data_type=="NSE lib Data"):
        
    #st.header("Indian Stock Financial Dashboard 2024")

    instrument = st.sidebar.selectbox("Instrument Type", options=("NSE Equity makrket" , "NSE Derivaties Market"))
    if instrument == "NSE Equity makrket":
        data_info = st.sidebar.selectbox("Data to extract", options =("bhav_copy_equities","bhav_copy_with_delivery","equity_list","fno_equity_list",
                                                                    "market_watch_all_indices","nifty50_equity_list","block_deals_data","bulk_deal_data",
                                                                    "index_vix_data","short_selling_data","deliverable_positions_data","index_data",
                                                                    "price_volum & deliverable_positions_data","Price_volum_data"))
        if(data_info=="equity_list")or(data_info=="fno_equity_list")or(data_info=="market_watch_all_indices")or(data_info== "nifty50_equity_list"):
            data=getattr(capital_market,data_info)()
        if(data_info=="bhav_copy_equities")or(data_info=="bhav_copy_with_delivery"):
            date=st.sidebar.text_input("Date","1-05-2024")
            data=getattr(capital_market,data_info)(date)
        if(data_info=="block_deals_data")or(data_info=="bulk_deal_data")or(data_info=="index_vix_data")or(data_info=="short_selling_data"):
            period=st.sidebar.text_input("Period","1M")
            data=getattr(capital_market,data_info)(period=period_) 
            
    if instrument == "NSE Derivaties Market":
        data_info = st.sidebar.selectbox("Data to extract", options =("expiry_dates_future","expire_date_optuins_index","fii_derivatives_statictics"
                                                                    "fno_bhav_copy","future_price_volum_data","nse_live_option_chain",
                                                                    "option_price_volum_data","participant_wise_open_interest",
                                                                    "participant_wise_trading_volum"))
        if(data_info=="expiry_dates_future")or(data_info=="expire_date_optuins_index"):
            data=getattr(derivatives,data_info)()
        if(data_info=="fii_derivatives_staticticsfno_bhav_copy")or(data_info=="fno_bhav_copy")or(data_info=="participant_wise_trading_volum"):
            date=st.sidebar.text_input("Date","1-05-2024")
            data=getattr(derivatives,data_info)(date)
            
    st.write(data)
        
    