import streamlit as st
import pandas as pd

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if "df" not in st.session_state:
    empty_df = pd.DataFrame()
    csv = convert_df(empty_df)
    st.session_state["df"] = empty_df
    st.session_state["csv"] = csv

st.sidebar.markdown("## Citation to Original Document")
st.sidebar.markdown('[Van Name Edwards, Burton. "The Manuscript Transmission of Carolingian Biblicial Commentaries"](https://wjbmattingly-carolingian-mss-home-bixjsx.streamlitapp.com/). Accessed 06/01/2018.')

title = st.title("Carolingian Exegesis Manuscripts")
#load the data
df = pd.read_csv("data/bvne_mss.csv")
df = df.iloc[: , 1:]

def add_session_state(label, column):
    data = list(set(df.dropna()[column].tolist()))
    data.sort()
    st.session_state[label] = data

def modify_list(df, column):
    new_list = list(set(df.dropna()[column].tolist()))
    new_list.sort()
    return new_list

if "people" not in st.session_state:
    add_session_state("people", "person")
if "book_types" not in st.session_state:
    add_session_state("book_types", "type")
if "books" not in st.session_state:
    add_session_state("books", "book")

idx = []

def update(matcher, new):
    global idx

# books = list(set(df.dropna().book.tolist()))
# books.sort()
matches = df



searches = st.sidebar.multiselect("Select Exegete(s)", st.session_state["people"])
search_types = st.sidebar.multiselect("Select Exegesis Types", st.session_state["book_types"])
search_books = st.sidebar.multiselect("Select Books", st.session_state["books"])
search_libraries =st.sidebar.text_input("Search for Library")


if searches:
    matches = matches.loc[matches["person"].isin(searches)]
if search_types:
    matches = matches.loc[matches["type"].isin(search_types)]
if search_books:
    matches = matches.loc[matches["book"].isin(search_books)]
if search_libraries:
    column_select = st.sidebar.selectbox("Select Column", ['shelfmark', 'ms'])
    matches = matches.loc[matches[column_select].str.contains(search_libraries)]


# temp_df = pd.DataFrame(matches)
csv = convert_df(matches)
st.session_state["csv"] = csv
st.session_state["df"] = matches

if len(st.session_state['df']) != 2744:
    st.markdown(st.session_state["df"].to_markdown(), unsafe_allow_html=True)
    # st.dataframe(st.session_state["df"])

st.sidebar.markdown("## Save Results")
filename = st.sidebar.text_input("Type Filename", "results.csv")
if ".csv" not in filename:
    filename = filename+".csv"

st.sidebar.download_button(
   "Press to Download",
   st.session_state["csv"] ,
   filename,
   "text/csv",
   key='download-csv'
)
