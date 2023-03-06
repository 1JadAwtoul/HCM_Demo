import streamlit as st
import app_config as cfg
import pandas as pd
from streamlit_option_menu import option_menu

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sendgrid
from sendgrid.helpers.mail import Mail
from email.message import EmailMessage

import sys



# ------ PAGE LAYOUT CALL ------
cfg.app_config()

# ------ VIEW MANAGEMENT ------
view_select = option_menu(
    menu_title=None,
    options=['Live HC Dashboard', 'HC Management'],
    icons=['people-fill', 'person-check'],
    orientation='horizontal'
)

# ------ DATA RETRIEVAL & MANIPULATION ------
# Loading data from the database (in this case an excel file)
associate_df = pd.read_csv('associate_db.csv')
managers_df = pd.read_csv('manager_db.csv')

# Joining data to add managers to unified table. 
team_data = pd.merge(associate_df, managers_df, on='team')

blue_team_df = team_data[team_data['team'] == 'Blue']
red_team_df = team_data[team_data['team'] == 'Red']
yellow_team_df = team_data[team_data['team'] == 'Yellow']

blue_hc = blue_team_df['associate_name'].count()
b_manager = blue_team_df['manager_name'].values[0]

red_hc = red_team_df['associate_name'].count()
r_manager = red_team_df['manager_name'].values[0]

yellow_hc = yellow_team_df['associate_name'].count()
y_manager = yellow_team_df['manager_name'].values[0]

def update_xlsx_db(associate_df, id, name, team):
    if name in associate_df['associate_name'].tolist():
        associate_df.loc[associate_df['associate_name'] == name, ['id', 'team']] = [id, team]
        updated_associate_df = associate_df
    updated_associate_df.to_csv('associate_db.csv', index=False)


requests_df = pd.DataFrame(columns=['id', 'source_team', 'destination_team'])

if view_select == 'Live HC Dashboard':
    with st.expander('TEAM HC SUMMARY', expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Blue Team")      
            st.metric('HC', blue_hc)
            st.metric('Manager', b_manager)
            blue_team_df.loc[:, ['id', 'associate_name']]

        with col2:
            st.subheader("Red Team")
            st.metric('HC', red_hc)
            st.metric('Manager',r_manager)
            red_team_df.loc[:, ['id', 'associate_name']]

        with col3:
            st.subheader("Yellow Team")
            st.metric('HC', yellow_hc)
            st.metric('Manager', y_manager)
            yellow_team_df.loc[:, ['id', 'associate_name']]


if view_select == 'HC Management':
    
    
    with st.form(key='request_form'):
        def display_form():
            st.header("Request Headcount Change")
            col1, col2 = st.columns(2)
            with col1:
                source_team = st.selectbox("Select Source Team", team_data['team'].unique())
            with col2:
                destination_team = st.selectbox("Select Destination Team", team_data['team'].unique())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                filtered_source_team = team_data[team_data['team']== source_team]
                selected_associate = st.selectbox("Select Associate", filtered_source_team['associate_name'].unique())
            with col2:
                filtered_source_team = team_data[team_data['associate_name'] == selected_associate]
                aa_id = st.selectbox("Associate ID", filtered_source_team['id'].unique())
            with col3:
                aa_manager = st.selectbox("Team Manager", options=filtered_source_team['manager_name'].unique())


            submit_button = st.form_submit_button("submit Request")
            return source_team, selected_associate, destination_team, aa_id, aa_manager, submit_button

        source_team, selected_associate, destination_team, aa_id, aa_manager, submit_button = display_form()
        
        sg_api_key = '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'
        sender_email = 'abdellahawtoul@gmail.com'
        recipient_email = 'abdellahawtoul@gmail.com'
        subject = '[REQUEST] Headcount Change'
        email_content = f'A change has been requested for associate <strong>[ID - {aa_id}] {selected_associate} </strong> '\
                        f'to move from team <strong>{source_team}</strong> '\
                        f'to team <strong>{destination_team}</strong> '
        body = email_content

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.add_alternative(body, subtype='html')

    if submit_button:
        new_request = {
            'id': aa_id,
            'source_team': source_team,
            'selected_associate': selected_associate,
            'destination_team': destination_team,
            }
        requests_df = requests_df.append(new_request, ignore_index=True)
        
        with smtplib.SMTP('smtp.sendgrid.net', 587) as smtp:
            smtp.starttls()
            smtp.login('apikey', sg_api_key)
            smtp.send_message(msg)
        for i, request in requests_df.iterrows():
            index_to_update = associate_df.loc[associate_df['associate_name'] == selected_associate].index
            associate_df.loc[index_to_update, 'team'] = destination_team

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Requests List")
        requests_df
    with col2:
        if st.button("Approve Request"):
            update_xlsx_db(associate_df=associate_df, name=selected_associate ,id=aa_id, team=destination_team)
            st.success("HC Change Executed and Database Updated")

