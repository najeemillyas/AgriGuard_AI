"""Reusable Streamlit result rendering."""

def render_result(st,state):
    assessment=state.safety
    labels={'approve':'Approved','approve_with_warning':'Approved with warning','block':'Blocked','escalate':'Escalated'}
    st.subheader(labels[assessment.decision])
    c1,c2,c3=st.columns(3);c1.metric('Confidence',f'{assessment.overall_confidence:.0%}');c2.metric('Risk',assessment.risk_level.title());c3.metric('Weather',state.weather.spray_status.title())
    if assessment.decision=='escalate':st.error(f'Expert review required. {assessment.reason}');st.write('Escalation ID:',state.escalation_id)
    elif assessment.decision=='approve_with_warning':st.warning(assessment.reason)
    else:st.success(assessment.reason)
    if state.advisory:
        st.markdown(f"### Likely problem\n{state.advisory.likely_problem}")
        st.markdown(f"### Evidence\n{state.advisory.evidence_summary}")
        if assessment.decision != 'escalate':
            st.markdown('### Immediate actions');[st.write(f'- {x}') for x in state.advisory.immediate_actions]
            st.markdown('### Treatment options');[st.write(f'- {x}') for x in state.advisory.treatment_options]
        else:
            st.warning('Treatment instructions are withheld until expert review.')
        st.markdown(f"### Weather precaution\n{state.advisory.weather_precaution}")
        st.markdown('### Safety precautions');[st.write(f'- {x}') for x in state.advisory.safety_precautions]
        if state.advisory.uncertainties:st.markdown('### Uncertainties');[st.write(f'- {x}') for x in state.advisory.uncertainties]
        st.markdown('### Sources');[st.write(f'- {x}') for x in state.advisory.source_names]
    with st.expander('Agent and tool trace',expanded=True):
        st.dataframe([{'Time':e.timestamp.isoformat(timespec='seconds'),'Component':e.component,'Action':e.action,'Outcome':e.outcome,'Reason':e.reason,'Duration ms':e.duration_ms} for e in state.trace],use_container_width=True)
