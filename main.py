import streamlit
import pandas as pd
import core.scrape_serps

def main(suggests, query_en=False, query_file_name='suggest', file_wt_en=False,file_name='data'):
    api_counter = 0
    j = 0
    page = input("how many page do you want?(1or2)")
    page = int(page)

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
            print('exceptional error occured and skipped')

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