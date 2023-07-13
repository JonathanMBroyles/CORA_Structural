#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import math


# # Read the necessary CSV files to visualize the data

# In[2]:


# Read Structural CSV File
df_master = pd.read_csv("Compiled Structural Data v4.csv")


# In[3]:


df_grouped_mean_Total_EC = df_master.groupby(["Concrete Floor System","Span Length (feet)"])["Total EC (kg CO2e/m2)"].mean()


# In[4]:


span_length_ft = range(10,(51),1)
RC_Flat_Plate_EC = df_grouped_mean_Total_EC[164:205].values
RC_Flat_Slab_EC = df_grouped_mean_Total_EC[205:246].values
RC_One_Way_Slab_EC = df_grouped_mean_Total_EC[246:287].values
RC_Voided_Plate_EC = df_grouped_mean_Total_EC[369:410].values
Two_Way_Beam_EC = df_grouped_mean_Total_EC[287:328].values
Two_Way_Waffle_EC = df_grouped_mean_Total_EC[328:369].values
PT_Flat_Plate_EC = df_grouped_mean_Total_EC[0:41].values
PT_Hollow_Core_Slab_EC = df_grouped_mean_Total_EC[41:82].values
PT_Voided_Plate_Ortho_EC = df_grouped_mean_Total_EC[123:164].values
PT_Voided_Plate_Diag_EC = df_grouped_mean_Total_EC[82:123].values


# In[5]:


floor_array = np.array([RC_Flat_Plate_EC,RC_Flat_Slab_EC,RC_One_Way_Slab_EC,Two_Way_Beam_EC,Two_Way_Waffle_EC,RC_Voided_Plate_EC,
                            PT_Flat_Plate_EC,PT_Hollow_Core_Slab_EC,PT_Voided_Plate_Ortho_EC, PT_Voided_Plate_Diag_EC])
floor_array = floor_array.T
floor_columns = ["RC Flat Plate", "RC Flat Slab", "RC One-Way Slab", "RC Two-Way Slab with Beams", "RC Two-Way Waffle Slab", "RC Voided Plate", "PT Flat Plate",
                          "PT Hollow Core Slab","PT Voided Plate (Orthogonal Layout)", "PT Voided Plate (Diagonal Layout)"]
df_Composite_EC = pd.DataFrame(floor_array, columns = floor_columns)


# In[6]:


from PIL import Image
pyLogo = Image.open("cora-logo-300dpi.png")


# In[7]:


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']) # , external_stylesheets=external_stylesheets

app.layout = html.Div([
    html.H1("Estimating the Embodied Carbon of Concrete Floor Systems: Conceptual Design Phase \n(Version 1.0)", style = {"textAlign": "center"}),
    
    html.H2("Concrete Floor Systems", style = {"textAlign": "center"}),
    dcc.Checklist(
        id="Floor System Checklist",
        options=["RC Flat Plate", "RC Flat Slab", "RC One-Way Slab", "RC Two-Way Slab with Beams", "RC Two-Way Waffle Slab", "RC Voided Plate", "PT Flat Plate", "PT Hollow Core Slab", "PT Voided Plate (Orthogonal Layout)", "PT Voided Plate (Diagonal Layout)"],
        value=["RC Flat Plate", "RC Voided Plate", "PT Flat Plate"],
        inline=True),

    
    html.H3("Floor System Span Length (feet)", style = {"textAlign": "center"}),
    dcc.RangeSlider(min = 10, max = 50, step = 1, value = [10,50],
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode = "drag",
        id = "Span Length (L)"),
    
#     html.Label("Concrete Compressive Strength (f'c):"),
#     dcc.Slider(3, 10,
#                step=None,
#                marks={
#                    3: '3 ksi',
#                    3.5: '3.5 ksi',
#                    4: '4 ksi',
#                    4.5: '4.5 ksi',
#                    5: '5 ksi',
#                    5.5: '5.5 ksi',
#                    6: '6 ksi',
#                    7: '7 ksi',
#                    8: '8 ksi',
#                    10: '10 ksi'
#                },
#                value=4,
#                id="Concrete Compressive Strength (f'c)"
#     ),
    
#     html.Label("Uniform Live Load (LL):"),
#      dcc.Slider(40, 150,
#                step=None,
#                marks={
#                    40: '40 psf',
#                    50: '50 psf',
#                    60: '60 psf',
#                    80: '80 psf',
#                    100: '100 psf',
#                    125: '125 psf',
#                    150: '150 psf'
#                },
#                value=40,
#                id="Uniform Live Load (LL)"
#     ),
    
    html.H2("Composite Embodied Carbon Trendlines", style = {"textAlign": "center"}),
    dcc.Graph(id='Composite_EC_Graphic'),
    
    html.Div(id='slider-output-container')
], style = {"margin": 30})

@app.callback(
    Output('Composite_EC_Graphic', 'figure'),
    Input("Floor System Checklist", 'value'),
    Input("Span Length (L)", 'value')
#     Input("Concrete Compressive Strength (f'c)", 'value'),
#     Input("Uniform Live Load (LL)", 'value')
)

def update_graph(floor_systems, span_length_range):
    spans = range(span_length_range[0],(span_length_range[1] + 1),1)
    
    data = pd.DataFrame()

    for i in floor_systems:
        dummy = df_Composite_EC[i]
        data[i] = np.array(dummy)
    
    data_live = data.iloc[(span_length_range[0] - 10):(span_length_range[-1] - 9),:]
    data_live.index = range(span_length_range[0],(span_length_range[1] + 1),1)
    
    fig = px.line(data_live, template = "plotly_white") #, template = "plotly_white"
    
    fig.layout.images = [dict(
            source=pyLogo,
            xref="paper", yref="paper",
            x = 0.5, y = 0.05,
            sizex = 1, sizey = 1, sizing="stretch", opacity=0.2,
            xanchor = "center", yanchor = "bottom"
        )]
    
    fig.update_traces(mode='lines+markers')
    
    fig.update_layout(
    title=None,
    xaxis_title="Span Length (ft)",
    yaxis_title="Embodied Carbon (kgCO2e/m2)")
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

