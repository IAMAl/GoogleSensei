#encoding:utf-8
import urllib
import urllib.request
import pandas as pd
import json
import sys
from time import sleep
import streamlit as st
import csv


def scrape_serps(key,maxrank,df_api,api_counter,j,try_cnt,file_wt_en=False,file_name='data'):
    phrase = urllib.parse.quote(key)
    try:
        url_list = []
        title_list = []
        snippet_list = []
        a = list(df_api["log"])
        cnt=1
        while(cnt<maxrank*10):
            if api_counter < 99:
                #print("[page_num]-->"+str(cnt))
                API_KEY = df_api["API_KEY"][j]
                ENGINE_ID = df_api["API_ID"][j]
                #print (CYAN+"[api_cnt]-->"+GREEN+str(api_counter)+ENDC)
                #print ("[API_KEY]-->"+str(API_KEY))
                #print ("[API_NUM]-->"+str(j))
                #print ("[SUGGEST]-->"+key)

                req_url = "https://www.googleapis.com/customsearch/v1?hl=ja&key="+API_KEY+"&cx="+ENGINE_ID+"&alt=json&q="+ phrase +"&start="+ str(cnt)
                #print("[req_url]-->"+str(req_url))
                headers = {"User-Agent": 'Mozilla /5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5110e Safari/601.1'}

                req = urllib.request.Request(req_url)
                res = urllib.request.urlopen(req)
                dump = json.loads(res.read())

                hit = dump["queries"]["request"][0]["totalResults"]
                #print(hit)
                for p in range(len(dump["items"])):
                    url_list.append(dump['items'][p]['link'])
                    title_list.append(dump['items'][p]['title'])
                    snippet_list.append(dump['items'][p]['snippet'].replace('\n',''))
                #print(GREEN+'[len_list]-->'+str(len(dump["items"]))+ENDC)

                if int(hit) < 11:
                    cnt = 100
                api_counter = api_counter + 1
                cnt = cnt +10
            else:
                j = j + 1
                api_counter = 0
            #print('_____________________________')

        if file_wt_en:
            with open(file_name+'.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\n') # 行末は改行
                for i,u in enumerate(url_list):
                    data = [key,url_list[i],title_list[i],snippet_list[i]]
                    writer.writerow(data)

        if len(dump["items"]) >= 1:
            return url_list,title_list,snippet_list,df_api,api_counter,j
        else:
            return ['no'],['no'],['no'],df_api,api_counter,j

    # if 503 or 403error returned (when the http server do not temporary accept your request)
    except Exception as e:
        try_cnt += 1
        sleep(1)
        if try_cnt <= 3:
            scrape_serps(phrase,maxrank,df_api,api_counter,j,try_cnt)
            #scrape_serps(key_,page,df_api,api_counter,j)
        else:
            st.text('server error occurred')
            st.text(title_list)
            st.text(df_api)
            st.text(api_counter)
            st.text(j)


def ng_item_remover(ng_words, df):

    #progress on removing NG words
    progress_bar = st.progress(0)

    #make new data frame
    column_names = ["title", "link", "snippet"]
    new_df = pd.DataFrame(columns = column_names)

    #remove item having NG word(s)
    for ng_no, ng_word in enumerate(ng_words):
        progress_bar.progress(ng_no + 1)
        for row_no in range(len(df)):
            if ng_word in df("snipets"):
                new_df = df.drop(df.index[row_no])

    return new_df


def main(suggests, query_en=False, query_file_name='suggest', file_wt_en=False,file_name='data', page=1):
    api_counter = 0
    j = 0
    

    if query_en:
        df = pd.read_csv(query_file_name+".csv",header=None)
        df.columns=["suggest"]
        sg = list(df["suggest"])
    else:
        sg = suggests

    urls = []
    titles = []
    snippets = []

    urls_ = []
    titles_ = []
    snippets_ = []

    sgs = []
    df_api = pd.read_csv("api.csv")
    ct = 0

    for key in sg:
        ct = ct + 1
        try_cnt = 0
        try: 
            url_list,title_list,snippet_list,df_api,api_counter,j = scrape_serps(key,page,df_api,api_counter,j,try_cnt)
            urls_.extend(url_list)
            titles_.extend(title_list)
            snippets_.extend(snippet_list)
            if url_list[0]!='NULL':
                for i in range(len(url_list)):#Deffault: page*10
                    sgs.append(key)
                urls += [url_list]
        except:
            st.text('exceptional error occurred and skipped')

    urls = pd.DataFrame(urls)
    titles = pd.DataFrame(titles)
    snippets = pd.DataFrame(snippets)
    #df = pd.concat([df,urls],axis=1)
    #df.to_csv("urls.csv")
    #df_ = pd.concat([pd.Series(urls_),pd.Series(sgs)],axis=1)
    #df_.columns = ["url","suggest"]


    de = pd.concat([pd.Series(urls), pd.Series(titles), pd.Series(snippets)],axis=1)
    de.columns = ["url","title","snippets"]

    return de


st.sidebar.title("グーグル先生")

suggests = st.sidebar.text_input(label='Search Words')
if not suggests:
    suggests = 'google'

ng_words = st.sidebar.text_input(label='NG Words')
ng_words = ng_words.split()
query_file_name = []
query_en = st.sidebar.checkbox('Set Query')
if query_en:
    query_file_name = st.sidebar.text_input(label='Query')
    query_file_name = query_file_name.split()

file_wt_en = st.sidebar.checkbox('Output Result')
file_name = []
if file_wt_en:
    file_name = st.sidebar.text_input('Result')
    
page = st.sidebar.number_input(label='Number of Pages', min_value=1, max_value=10, value=1, format='%d')
page = int(page)

start_search = st.sidebar.button('Search')
if start_search:
    df = main(suggests, query_en, query_file_name, file_wt_en, file_name, page)
    df = ng_item_remover(ng_words, df)
    st.write(df)