import os, sys
_here = os.path.dirname(os.path.abspath(__file__))  
_src  = os.path.abspath(os.path.join(_here, ".."));     sys.path.insert(0, _here);          sys.path.insert(0, _src)                        
import streamlit as st;     st.set_page_config( page_title= 'HR-End-To-End-Assistant', layout= 'wide') # cd src && python -m streamlit run streamlit-app/app.py
import asyncio
from ui.style import apply_styles;          apply_styles()
from controllers.DataController import DataController
from schemas import build_img_messages_schema, build_pdf_messages_schema
from models import UserEntries
import re
from stores import LLMFactory
from results_page import render_results_page



if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'analysis_response' not in st.session_state:
    st.session_state.analysis_response = None
if 'user_entries' not in st.session_state:
    st.session_state.user_entries = None

if st.session_state.page == 'results':
    render_results_page()
    st.stop()


cell_1, cell_2 = st.columns( [ 2, 1 ] )
cell_1.markdown(  '<h1 style = "font-family:times new roman; font-size:45px;margin-top: -60px;margin-left: -60px;text-align:left" ><i>Candidate Selection Assistant </i></h1>',
            unsafe_allow_html=True)
cell_2.markdown(  '<h1 style = "font-family:times new roman;margin-top: -60px; font-size:57px;text-align:right" >HireVision</h1>',
            unsafe_allow_html=True)

st.sidebar.write( f'''<b style="font-size:120%" >Currently working provider: <i style="color:#D4622A;" >
                 {st.secrets['LLM_PROVIDER'].upper()}</i> </b> ''', unsafe_allow_html=True )

st.sidebar.write( f'''<hr><b style="font-size:120%" >Currently Serving Model: <i style="color:#D4622A;" >
                 { st.secrets[  st.secrets['LLM_PROVIDER'].upper() + '_' + 'MODEL'  ] }</i> </b> ''', unsafe_allow_html=True )

ent_1, ent_2, ent_3 = st.columns( 3 )
ent_4, ent_5 = st.columns( 2 )

seniority = ent_1.select_slider( 'Candidate Seniority', options = UserEntries.model_fields['seniority'].examples ) # type: ignore
years_of_exp = ent_2.slider( 'Years of Experience',
                          min_value= UserEntries.model_fields['years_of_exp'].metadata[0].ge,
                          max_value= UserEntries.model_fields['years_of_exp'].metadata[1].lt,)

job_role = ent_3 = ent_3.text_input( 'Job Role' )

required_skills = ent_4.text_input( 'Required Skills', help= 'Seperate each skill with a space, comma or a new line !' ); required_skills = re.split(r'[\s,\-]+', required_skills)
job_description = ent_5.text_area( 'Job Description' )

cv = st.file_uploader( label= ' Upload The Candidate CV', type= [ 'PNG', 'JPG', 'JPEG', 'PDF', 'DOCX', 'TXT' ])

if cv:
    #st.write( cv.type )
    if not DataController().get_data_type( cv ):
        st.error( 'File Extension Not Supported !' )
        st.stop()

analyze_btn = st.button( 'Analyze' )

if analyze_btn:
    if not cv:
        st.warning( 'Please upload a CV before analyzing.' )
        st.stop()

    with st.spinner( 'Analyzing CV...' ):
        user_entries = UserEntries(
            seniority= seniority, years_of_exp= years_of_exp, job_role= job_role,
            required_skills= required_skills, job_description= job_description  # type: ignore
        )

        provider = LLMFactory().return_provider()
        provider.api_key = st.secrets['LLM_PROVIDER'].upper() + '_API_KEY'

        if DataController().get_data_type( cv ) == 'img':
            messages = asyncio.run( build_img_messages_schema( img= cv, user_entries= user_entries, provider= st.secrets['LLM_PROVIDER'] ))
        elif DataController().get_data_type( cv ) == 'doc':
            messages = asyncio.run( build_pdf_messages_schema( file= cv, user_entries= user_entries, provider= st.secrets['LLM_PROVIDER'] ))

        analysis_response = asyncio.run( provider.analyze_cv( messages= messages ))  # type: ignore

    # Store in session state and navigate to results
    st.session_state.analysis_response = analysis_response
    st.session_state.user_entries = user_entries
    st.session_state.page = 'results'
    st.rerun()