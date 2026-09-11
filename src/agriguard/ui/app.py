"""Streamlit application entry point."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
import streamlit as st
from pydantic import ValidationError
from agriguard.settings import get_settings
from agriguard.models import CropCase
from agriguard.orchestration.graph import AgriGuardWorkflow
from agriguard.ui.components import render_result

st.set_page_config(page_title='AgriGuard AI',page_icon='🌱',layout='wide')
st.title('AgriGuard AI')
st.caption('Grounded and safety-aware multi-agent crop protection assistant')
st.info('Prototype guidance only. It does not replace diagnosis by a qualified agricultural professional. Do not apply a chemical unless its label and local guidance support the crop and use.')

@st.cache_resource
def workflow():return AgriGuardWorkflow(get_settings())

with st.form('crop-case'):
    a,b,c=st.columns(3)
    crop=a.selectbox('Crop',['chrysanthemum','tomato','chilli','other'])
    stage=b.text_input('Crop stage',placeholder='Flowering')
    severity=c.selectbox('Severity',['low','medium','severe'],index=1)
    location=st.text_input('Location',placeholder='Bagepally')
    symptoms=st.text_area('Observed symptoms',placeholder='Describe affected plant part, colour, insects, spots and how quickly the problem is spreading.')
    submitted=st.form_submit_button('Analyse case',type='primary')
if submitted:
    try:
        case=CropCase(crop=crop,stage=stage,location=location,symptoms=symptoms,severity=severity)
        with st.spinner('Agents are analysing the case...'):result=workflow().run(case)
        st.session_state['last_result']=result
    except ValidationError as exc:st.error('Please complete every required field. '+str(exc.errors()[0]['msg']))
    except Exception as exc:st.error(f'The case could not be processed safely: {type(exc).__name__}')
if st.session_state.get('last_result'):render_result(st,st.session_state['last_result'])
