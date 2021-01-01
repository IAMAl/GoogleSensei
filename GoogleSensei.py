import streamlit

st.sidebar.title("グーグル先生")

st.sidebar.text("Search Words")
suggests = st.sidebar.text_input()

st.sidebar.text("NG Words")
ng_words = st.sidebar.text_input()

start_search = 

query_en = 
query_file_name = 
file_wt_en = 
file_name = 

if start_search:
    df = main(suggests, query_en, query_file_name, file_wt_en,file_name)
    df = ng_item_remover(ng_words, df)
    st.write(df)