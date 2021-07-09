import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

def load_list(file):
    final  = []
    with open (file, "r", encoding="utf_8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            if line != "":
                final.append(line)
    return (final)

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
Abbo = form.checkbox("Abbo")
Adalbert = form.checkbox("Adalbert")
Adrevald = form.checkbox("Adrevald")
Adso = form.checkbox("Adso")
Alcuin = form.checkbox("Alcuin")
Ambrosius = form.checkbox("Ambrosius")
Angelomus = form.checkbox("Angelomus")
Anonymous = form.checkbox("Anonymous")
Auxilius = form.checkbox("Auxilius")
Beatus = form.checkbox("Beatus")
Berengaudus = form.checkbox("Berengaudus")
Candidus_Brunn = form.checkbox("Candidus_Brunn")
Christian = form.checkbox("Christian")
Claudius = form.checkbox("Claudius")
Erchambertus = form.checkbox("Erchambertus")
Felix = form.checkbox("Felix")
Florus = form.checkbox("Florus")
Haimo = form.checkbox("Haimo")
Hatto = form.checkbox("Hatto")
Heiric = form.checkbox("Heiric")
Helisachar = form.checkbox("Helisachar")
Hincmar = form.checkbox("Hincmar")
Hrabanus = form.checkbox("Hrabanus")
Johannes = form.checkbox("Johannes")
Josephus = form.checkbox("Josephus")
Notker = form.checkbox("Notker")
Odo = form.checkbox("Odo")
Otfrid = form.checkbox("Otfrid")
Paschasius = form.checkbox("Paschasius")
Paul = form.checkbox("Paul")
Petrus = form.checkbox("Petrus")
Prudentius = form.checkbox("Prudentius")
Pseudo_Alcuin = form.checkbox("Pseudo_Alcuin")
Pseudo_Bede = form.checkbox("Pseudo_Bede")
Pseudo_Einhard = form.checkbox("Pseudo_Einhard")
Pseudo_Haimo = form.checkbox("Pseudo_Haimo")
Pseudo_Hrabanus = form.checkbox("Pseudo_Hrabanus")
Pseudo_Jerome = form.checkbox("Pseudo_Jerome")
Pseudo_Remigius = form.checkbox("Pseudo_Remigius")
Pseudo_Salonius = form.checkbox("Pseudo_Salonius")
Rahingus = form.checkbox("Rahingus")
Remigiius = form.checkbox("Remigiius")
Remigius = form.checkbox("Remigius")
Sedulius = form.checkbox("Sedulius")
Smaragdus = form.checkbox("Smaragdus")
Theodulf = form.checkbox("Theodulf")
Thietland = form.checkbox("Thietland")
Walahfrid = form.checkbox("Walahfrid")
Wigbod = form.checkbox("Wigbod")
Winitharius = form.checkbox("Winitharius")




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

    df1 = temp_df[['text', 'shelfmark']]
    df1.to_csv("temp/temp.csv")

    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    net.barnes_hut()
    net_data = pd.read_csv("temp/temp.csv")

    sources = net_data['text']
    targets = net_data['shelfmark']

    edge_data = zip(sources, targets)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        # w = e[2]

        net.add_node(src, src, title=src)
        net.add_node(dst, dst, title=dst, color="green")
        net.add_edge(src, dst)

    neighbor_map = net.get_adj_list()

    # add neighbor data to node hover data
    for node in net.nodes:
        node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])

    net.save_graph('temp/temp.html')
    my_expander = st.beta_expander("Expand to see a list of manuscripts...")
    my_expander.table(temp_df)
    HtmlFile = open('temp/temp.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 1000, width=1000)
