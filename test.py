import altair as alt
import streamlit as st
from vega_datasets import data
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import date
import sqlite3
from sqlite3 import Error
import mysql.connector


""" """""""""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = mysql.connector.connect(user='u152993259_webmasteramd15', password='Jesussauve7',
                              host='sql735.main-hosting.eu',
                              database=db_file)
        
    except Error as e:
        print(e)

    return conn

def insert_executed_action(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO Action_executee(expert,date,mission,champ_activites,temps_travail,lieu)
              VALUES(%s,%s,%s,%s,%s,%s) '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(mission,date_debut,date_fin,expert,champs_activites,temps_travail)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid
def insert_expert_activite(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO Expert_activite(mission,champs_activites,temps_travail)
              VALUES(?,?,?) '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def update_expert_activite(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = '''UPDATE Expert_activite SET address = '?' WHERE address = '?' '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid
def update_expert_planifie(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(mission,date_debut,date_fin,expert,champs_activites,temps_travail)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def select_all_actions(conn):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''SELECT * from Action_executee'''
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    conn.commit()
    return cur


def update_mission_executee(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(mission,date_debut,date_fin,expert,champs_activites,temps_travail)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid
def update_mission_planifiee(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(mission,date_debut,date_fin,expert,champs_activites,temps_travail)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor(buffered=True)
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def select_from_mission(conn):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''SELECT DISTINCT mission from Mission_executee'''
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    conn.commit()
    return cur


def select_from_experts(conn):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''SELECT DISTINCT nom from Expert_activite'''
    cur = conn.cursor(buffered=True)
    cur.execute(sql)
    conn.commit()
    return cur
def highlight_survived(s):
    return ['background-color: lightgreen']*len(s) if 50<s else ['background-color: pink']*len(s)

def color_survived(val):
    color = 'green' if 50<val else 'pink'
    return f'background-color: {color}'

full_message_temp ="""
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">SYSTEME DE SUIVI DES MISSIONS</h1>
</div>
"""
""""""""""""


#st.image("Capture d’écran 2022-10-17 175305.png", use_column_width=False)
title = "SYSTEME DE SUIVI DES MISSIONS | planification"
st.markdown(full_message_temp.format('royalblue','white'),unsafe_allow_html=True)


hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """


today = date.today()


#st.set_page_config(layout="wide")
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login('Connexion', 'main')

if authentication_status:
    expert_name = st.session_state["name"]
    st.write(f"{today}")
    
    authenticator.logout('Se déconnecter', 'main')

    
    
    database = "u152993259_sse"
    conn = create_connection(database)
    records1 = select_from_mission(conn).fetchall()
    records2 = select_from_experts(conn).fetchall()

    experts_table = select_all_actions(conn).fetchall()
    missions_table = select_all_actions(conn).fetchall()

    missions_list = []
    experts_list = []
    
    for row in records1:
        missions_list.append(row[0])
    for row in records2:
        experts_list.append(row[0])

    # Loading the cars dataset
    df = data.cars()

    # List of quantitative data items
    item_list = [
        col for col in df.columns if df[col].dtype in ['float64', 'int64']]

    # List of Origins
    origin_list = list(df['Origin'].unique())

    # Create the column of YYYY 
    df['YYYY'] = df['Year'].apply(lambda x: x.year)
    min_year = df['YYYY'].min()
    max_year = df['YYYY'].max()

    
    st.sidebar.image("Capture d’écran 2022-10-17 175305.png", use_column_width=False)
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    with st.sidebar:
            choice = option_menu(None,["Accueil", 'Mes Activités'], 
        icons=['house','list-task','gear'], default_index=0,styles={
            "nav-link-selected": {"background-color": "red"},
        })
    # Sidebar
    st.sidebar.title(f"{expert_name} ")
    st.sidebar.markdown('###')
    st.sidebar.markdown("### Parametres")
    
    
    
    # Layout (Content)
    Main_df = pd.DataFrame({"Mission": [""], "CHAMP D'ACTIVITES": [""], "TEMPS DE TRAVAIL (Part de la journée)": [None], "LIEU": [""]})

    if choice == "Accueil":


        Mission_list = missions_list
        
        Activities_group_list = ["Réunions cadrage /démarrage","Atelier cadrage","Outils collecte","Rapport cadrage/démarrage","Collecte données 1 (entretiens )","Collecte données 2 (Revue doc/BD)","Reunion étape mise en œuvre","Rapports d'étude","Atelier examen /validation","Gestion / suivi de projet","Montage offres techniques","Gestion et animation du pôle"]
        Working_time = [str(1),str(0.75),str(0.5),str(0.25)]
        Working_Places = ["A distance","Au Bureau"]
        st.markdown(f"Veuillez entrer vos activités de la journée cliquez sur enregistrer")
        df = pd.DataFrame({"Mission": [""], "CHAMP D'ACTIVITES": [""], "TEMPS DE TRAVAIL (Part de la journée)": [None], "LIEU": [""]})

        df["Mission"] = (
        df["Mission"].astype("category").cat.add_categories(Mission_list)
    )
        df["CHAMP D'ACTIVITES"] = (
        df["CHAMP D'ACTIVITES"].astype("category").cat.add_categories(Activities_group_list)
    )
        df["TEMPS DE TRAVAIL (Part de la journée)"] = (
        df["TEMPS DE TRAVAIL (Part de la journée)"].astype("category").cat.add_categories(Working_time)
    )
        df["LIEU"] = (
        df["LIEU"].astype("category").cat.add_categories(Working_Places)
    )
        edited_df = st.experimental_data_editor(df, num_rows="dynamic")
        st.write("ATTENTION : Une fois enregistrée, vous ne pourrez plus modifier votre feuille de temps.")
        if st.button('Enregistrer'):
            database = "u152993259_sse"
            conn = create_connection(database)
            
            part_journée = 0
            for i in range(len(edited_df)):
                part_journée = part_journée + float(edited_df.loc[i,"TEMPS DE TRAVAIL (Part de la journée)"])
            if 1<part_journée:
                st.write("Impossible d'enregistrer si le total Part de ma journée dépasse 1")

            if part_journée<=1:
                for i in range(len(edited_df)):
                    expert = expert_name
                    date = today
                    mission_executée = edited_df.loc[i,"Mission"]
                    champ_act_executé = edited_df.loc[i,"CHAMP D'ACTIVITES"]
                    Temps_tra_executé = float(edited_df.loc[i,"TEMPS DE TRAVAIL (Part de la journée)"])
                    lieu = edited_df.loc[i,"LIEU"]
                    action_executed = (expert,date,mission_executée,champ_act_executé,Temps_tra_executé,lieu)
                    action_executed_id = insert_executed_action(conn, action_executed)
                st.write("Enregistré avec succès !")





    if choice == "Mes Activités":
        experts_table = pd.DataFrame(experts_table, columns = ["Numero","Expert","Date","Mission","Activité","Temps de travail","Lieu de travail" ])
        
        experts_table["taux d'exécution %"] = 0
        for i in range(len(experts_table)):
            if experts_table.loc[i,"Activité"] == "Réunions cadrage /démarrage":
                experts_table.loc[i,"taux d'exécution %"] = 5
            elif experts_table.loc[i,"Activité"] == "Atelier cadrage":
                experts_table.loc[i,"taux d'exécution %"] = 5
            elif experts_table.loc[i,"Activité"] == "Outils collecte":
                experts_table.loc[i,"taux d'exécution %"] = 15
            elif experts_table.loc[i,"Activité"] == "Collecte données 1 (entretiens )":
                experts_table.loc[i,"taux d'exécution %"] = 30
            elif experts_table.loc[i,"Activité"] == "Collecte données 2 (Revue doc/BD)":
                experts_table.loc[i,"taux d'exécution %"] = 45
            elif experts_table.loc[i,"Activité"] == "Reunion étape mise en œuvre":
                experts_table.loc[i,"taux d'exécution %"] = 60
            elif experts_table.loc[i,"Activité"] == "Rapports d'étude":
                experts_table.loc[i,"taux d'exécution %"] = 80
            elif experts_table.loc[i,"Activité"] == "Atelier examen /validation":
                experts_table.loc[i,"taux d'exécution %"] = 100
            else:
                experts_table.loc[i,"taux d'exécution %"] = None
                
                
        table_summary = experts_table.groupby("Mission")["taux d'exécution %"].max()
        table_summary = table_summary.to_frame()
        st.dataframe(table_summary.style.applymap(color_survived, subset=["taux d'exécution %"]))

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')