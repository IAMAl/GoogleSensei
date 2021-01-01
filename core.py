#encoding:utf-8
import urllib
import urllib.request
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
            print ('server error occured')
            print(title_list)
            print(df_api)
            print(api_counter)
            print(j)

def ng_item_remover(ng_words, df):

    #progress on removing NG words
    progress_bar = st.progress(0)

    #make new data frame
    de = pd.hogege()

    #remove item having NG word(s)
    for ng_no ng_word in enumerate(ng_words):
        progress_bar.progress(ng_no + 1)
        for row_no in range(len(df)):
            if ng_word in df("snipets"):
                de = df.drop(df.index[row_no])

    return de