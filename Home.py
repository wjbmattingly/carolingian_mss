import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if "df" not in st.session_state:
    empty_df = pd.DataFrame()
    csv = convert_df(empty_df)
    st.session_state["df"] = empty_df
    st.session_state["csv"] = csv

def load_list(file):
    final  = []
    with open (file, "r", encoding="utf_8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            if line != "":
                final.append(line)
    return (final)
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
title = st.title("Carolingian Exegesis Manuscripts")
#load the data
df = pd.read_csv("data/bvne_mss.csv")
df = df.iloc[: , 1:]


people = load_list("data/people.txt")
books = load_list("data/book.txt")
writing_type = load_list("data/type.txt")
shelfmarks = load_list("data/shelfmark.txt")

#Load exegetes
form = st.sidebar.form("Options")
form.write("Select your Exegete(s)")
col1, col2 = form.columns(2)

Abbo = col1.checkbox("Abbo")
Adalbert = col2.checkbox("Adalbert")

Adrevald = col1.checkbox("Adrevald")
Adso = col2.checkbox("Adso")

Alcuin = col1.checkbox("Alcuin")
Ambrosius = col2.checkbox("Ambrosius")

Angelomus = col1.checkbox("Angelomus")
Anonymous = col2.checkbox("Anonymous")

Auxilius = col1.checkbox("Auxilius")
Beatus = col2.checkbox("Beatus")

Berengaudus = col1.checkbox("Berengaudus")
Candidus_Brunn = col2.checkbox("Candidus_Brunn")

Christian = col1.checkbox("Christian")
Claudius = col2.checkbox("Claudius")

Erchambertus = col1.checkbox("Erchambertus")
Felix = col2.checkbox("Felix")

Florus = col1.checkbox("Florus")
Haimo = col2.checkbox("Haimo")

Hatto = col1.checkbox("Hatto")
Heiric = col2.checkbox("Heiric")

Helisachar = col1.checkbox("Helisachar")
Hincmar = col2.checkbox("Hincmar")

Hrabanus = col1.checkbox("Hrabanus")
Johannes = col2.checkbox("Johannes")

Josephus = col1.checkbox("Josephus")
Notker = col2.checkbox("Notker")

Odo = col1.checkbox("Odo")
Otfrid = col2.checkbox("Otfrid")

Paschasius = col1.checkbox("Paschasius")
Paul = col2.checkbox("Paul")

Petrus = col1.checkbox("Petrus")
Prudentius = col2.checkbox("Prudentius")

Pseudo_Alcuin = col1.checkbox("Pseudo_Alcuin")
Pseudo_Bede = col2.checkbox("Pseudo_Bede")

Pseudo_Einhard = col1.checkbox("Pseudo_Einhard")
Pseudo_Haimo = col2.checkbox("Pseudo_Haimo")

Pseudo_Hrabanus = col1.checkbox("Pseudo_Hrabanus")
Pseudo_Jerome = col2.checkbox("Pseudo_Jerome")

Pseudo_Remigius = col1.checkbox("Pseudo_Remigius")
Pseudo_Salonius = col2.checkbox("Pseudo_Salonius")

Rahingus = col1.checkbox("Rahingus")
Remigiius = col2.checkbox("Remigiius")

Remigius = col1.checkbox("Remigius")
Sedulius = col2.checkbox("Sedulius")

Smaragdus = col1.checkbox("Smaragdus")
Theodulf = col2.checkbox("Theodulf")

Thietland = col1.checkbox("Thietland")
Walahfrid = col2.checkbox("Walahfrid")

Wigbod = col1.checkbox("Wigbod")
Winitharius = col2.checkbox("Winitharius")




search = form.form_submit_button("Search")

if search:
    total = [Abbo, Adalbert, Adrevald, Adso, Alcuin, Ambrosius, Angelomus, Anonymous, Auxilius, Beatus, Berengaudus, Candidus_Brunn, Christian, Claudius, Erchambertus, Felix, Florus, Haimo, Hatto, Heiric, Helisachar, Hincmar, Hrabanus, Johannes, Josephus, Notker, Odo, Otfrid, Paschasius, Paul, Petrus, Prudentius, Pseudo_Alcuin, Pseudo_Bede, Pseudo_Einhard, Pseudo_Haimo, Pseudo_Hrabanus, Pseudo_Jerome, Pseudo_Remigius, Pseudo_Salonius, Rahingus, Remigiius, Remigius, Sedulius, Smaragdus, Theodulf, Thietland, Walahfrid, Wigbod, Winitharius]

    searches  = []
    y=0
    for x in total:
        if x == True:
            searches.append(people[y])
        y=y+1
    st.write(f"Running Search on {searches}")
    matches = []
    for index, row in df.iterrows():
        if row["person"] in searches:
            matches.append(row)
    temp_df = pd.DataFrame(matches)
    csv = convert_df(temp_df)
    st.session_state["csv"] = csv
    st.session_state["df"] = temp_df
    st.markdown(st.session_state["df"].to_markdown(), unsafe_allow_html=True)
    # df1 = temp_df[['text', 'shelfmark', 'person']]
    # df1.to_csv("temp/temp.csv")
    #
    # net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    # net.barnes_hut()
    # net_data = pd.read_csv("temp/temp.csv")
    #
    # sources = net_data['text']
    # targets = net_data['shelfmark']
    # people = net_data['person']
    #
    # edge_data = zip(sources, targets, people)
    #
    #
    # for e in edge_data:
    #     src = e[0]
    #     dst = e[1]
    #     prsn = e[2]
    #
    #     net.add_node(src, src, title=src)
    #     net.add_node(dst, dst, title=dst, color="green")
    #     net.add_node(prsn, title=prsn, color="red")
    #     net.add_edge(src, dst)
    #     net.add_edge(prsn, src)
    #
    # neighbor_map = net.get_adj_list()
    #
    # # add neighbor data to node hover data
    # for node in net.nodes:
    #     node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    #     node['value'] = len(neighbor_map[node['id']])
    #
    # net.save_graph('temp/temp.html')

    # my_expander = st.expander("Expand to see a list of manuscripts...")
    # my_expander.markdown(temp_df.to_markdown(), unsafe_allow_html=True)
    # HtmlFile = open('temp/temp.html', 'r', encoding='utf-8')
    # source_code = HtmlFile.read()
    # components.html(source_code, height = 1000, width=1000)
