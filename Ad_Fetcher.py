import streamlit as st
import pandas as pd

from bs4 import BeautifulSoup

from time import sleep
import warnings

from datetime import datetime
import requests

warnings.filterwarnings('ignore')
st.set_page_config(layout="wide")

st.title('Address _Fetcher_')
try:
    def deg_to_dms(deg, pretty_print=None, ndp=4):


        m, s = divmod(abs(deg)*3600, 60)
        d, m = divmod(m, 60)
        if deg < 0:
            d = -d
        d, m = int(d), int(m)
        if pretty_print:
            if pretty_print=='latitude':
                hemi = 'N' if d>=0 else 'S'
            elif pretty_print=='longitude':
                hemi = 'E' if d>=0 else 'W'
            else:
                hemi = '?'
            return '{d:d}° {m:d}′ {s:.{ndp:d}f}″ {hemi:1s}'.format(
                        d=abs(d), m=m, s=s, hemi=hemi, ndp=ndp)
        return d, m, s





    df = pd.DataFrame([])
    col1, col2 = st.columns([1,3])


    with col1:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            print(uploaded_file.name)
            dataframe = pd.read_csv(uploaded_file)
        number = st.text_input('Cursor')

    button1 = st.button('run')


    if st.session_state.get('button') != True:
        st.session_state['button'] = button1

    def call_back():
        return st.session_state['button'] == True


    now = datetime.now()
    
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    if button1:

        if st.session_state['button'] == True:
            try:
                st.write('Start time:       ',dt_string)



                tab1, tab2, tab3 = st.tabs(["Counting","Scheduler", "Result"])
                if number !='':
                    dataframe = dataframe.iloc[int(number)+1:]
                else:
                    dataframe = dataframe
                with col2:
                    with tab2:
                        st.dataframe(dataframe)
                        print('-------------------Program running-----------------------------------------------------------------------------')
                        store= []

                        recordm = dataframe
                        lat = recordm['Latitude'].to_list()
                        lon = recordm['Longitude'].to_list()
                        id = recordm['Sublocationid'].to_list()
                        locality = recordm['Beats LocalityName'].to_list()
                        counter = 0
                        for i in range(len(recordm)):

                        

                            lat2 = deg_to_dms(lat[i],pretty_print='latitude')

                            long2 = deg_to_dms(lon[i],pretty_print='longitude')


                            header = {'content-type':
                                	'application/json'}

                            url = f'https://www.google.com/maps/place/{lat2}+{long2}/'
                            response = requests.get(url,headers = header)

                            soup = BeautifulSoup(response.text)
                            meta1 = soup.findAll('meta')
                            meta = soup.find(itemprop="name")
                            print(meta['content'].split('·')[1].strip())
                            store = (meta['content'].split('·')[1].strip())



                            tab3 = tab3.empty()
                            data = pd.DataFrame({'Sublocationid':[id[i]],'Beatslocatliy':[locality[i]],'lat':[lat[i]],'lon':[lon[i]],'Address':[store]})
                            df = df.append(data)
                            tab1 = tab1.empty()
                            with tab1:
                                    counter+=1
                                    st.write('Total count: ',len(dataframe),'       out of which        ',counter,' Row Completed')
                            with tab3:
                                    col1,col2 = st.columns([3,1])
                                    with col1:
                                        st.dataframe(df)

                                    with col2:
                                            if len(dataframe) == len(df):
                                                def convert_df(df):
                                                
                                                    return df.to_csv().encode('utf-8')

                                                csv = convert_df(df)

                                                st.download_button(
                                                label="Download data as CSV",
                                                data=csv,
                                                file_name='Loaction.csv',
                                                mime='text/csv',
                                                        on_click=call_back)
                if len(df) == len(dataframe):
                    st.write('End time:       ',dt_string)          
            except Exception as e:
                if len(df) >= 1:
                    def convert_df(df):
                        return df.to_csv().encode('utf-8')

                    csv = convert_df(df)

                    st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='location.csv',
                    mime='text/csv',
                    on_click=call_back)

except Exception as e:
    print(f"Current Error is:- {e}")



                          



            


