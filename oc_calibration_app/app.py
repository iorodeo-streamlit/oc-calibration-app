import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from data_fitting import polyfit_thru_zero
from data_fitting import polyfit_unconstrained

st.title('oc-calibration-app')

st.subheader('Generate json calibrations for the Open Colorimeter')

test_name = st.text_input('Test Name',value='My Test')

units = st.text_input('Units', value='ppm')

led = st.number_input('LED (nm)', value = 630, min_value=0, max_value=1000, step=1, format='%d')

fit_type = st.selectbox('Fit Type', ('linear', 'polynomial')) 

is_constrained = st.checkbox('constrain regression to go through point (0,0)', value=True)

if fit_type == 'polynomial':
    fit_order = st.number_input('Fit Order', value=2, min_value=1, max_value=10)
else:
    fit_order = 1

msg  = f'Upoad a CSV file containing your calibration measurements. The data file should '
msg += f'consist of two columns. The first column should be the test values in {units} and '
msg += f'the second column should consist of the corresponding absorbances.'

st.caption(msg)
uploaded_file = st.file_uploader("Upload CSV", type=".csv")

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df.columns = [units, 'absorbance']

    num_pts = df.shape[0]
    if (fit_order > num_pts-1):
        fit_order = min(fit_order, num_pts-1)
        st.caption(f'warning reduced to {fit_order}') 

    abso = df['absorbance']
    meas = df[units]
    if is_constrained:
        coef, abso_fit, meas_fit = polyfit_thru_zero(abso, meas, fit_order)
    else:
        coef, abso_fit, meas_fit = polyfit_unconstrained(abso, meas, fit_order)

    fig, ax = plt.subplots(1,1)
    ax.plot(abso_fit, meas_fit, 'r')
    ax.plot(abso, meas, 'o')
    ax.grid(True)
    ax.set_xlabel('absorbance')
    ax.set_ylabel(units)
    st.pyplot(fig)

    cal = {}
    cal[test_name] = {
        'units'    :  units, 
        'led'      :  led,
        'fit_type' :  fit_type, 
        'fit_coef' :  coef.tolist(),
        'range'    :  {'min': abso.min(), 'max': abso.max()},
        }


    st.json(json.dumps(cal), expanded=True)

    st.download_button(
            label = 'Download json calibration data',
            data = json.dumps(cal, indent=4),
            file_name = f'calibration.json', 
            mime='text/plain'
            )


            



            








    
