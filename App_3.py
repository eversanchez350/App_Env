import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px

##SE INICICA CARGANDO LAS BASES DE DATOS
##CARGANDO BASES DE DATOS 
## Se cargará cada uno de los archivos
Atlantic = pd.read_csv("ATLANTIC SOUTH AREA.csv")
Chicago = pd.read_csv("CHICAGO AREA.csv")
NEA = pd.read_csv("NEW ENGLAND AREA.csv")
NYC = pd.read_csv("NEW YORK CITY AREA.csv")

Minutos = pd.read_csv("Minutos.csv")

with open('BD_Credito.json') as file:
    BD_Credito = json.load(file)
    
##TRANSFORMANDO EL JSON EN DATAFRAME
Credito=pd.DataFrame(BD_Credito["data"])

##CREANDO UNA TABLA GENERAL DE LAS CIUDADES
CIUDADES=Atlantic.append(Chicago.append(NEA.append(NYC)))

###HACIENDO RESUMEN VARIABLES NUMERICAS
Atl_Des_Num=Atlantic.describe(percentiles=[0,0.05,0.1,0.25,0.5,0.75,0.9,0.95,1]).transpose()
Chi_Des_Num=Chicago.describe(percentiles=[0,0.05,0.1,0.25,0.5,0.75,0.9,0.95,1]).transpose()
NEA_Des_Num=NEA.describe(percentiles=[0,0.05,0.1,0.25,0.5,0.75,0.9,0.95,1]).transpose()
NYC_Des_Num=NYC.describe(percentiles=[0,0.05,0.1,0.25,0.5,0.75,0.9,0.95,1]).transpose()
Min_Des_Num=Minutos.describe(percentiles=[0,0.05,0.1,0.25,0.5,0.75,0.9,0.95,1]).transpose()
Cre_Des_Num=Credito.describe(percentiles=[0,0.05,0.1,0.25,0.5,0.75,0.9,0.95,1]).transpose()

bases=[{'label': 'Atlantic','value':'ATL'},
       {'label': 'Chicago','value':'Chi'},
       {'label': 'New England','value':'NEA'},
       {'label': 'New York','value':'NYC'},
       {'label': 'Minutos','value':'Mins'},
       {'label': 'Creditos','value':'Cre'}]

Atlantic_list = [{'label':'new_cell','value':'new_cell'},
                {'label':'area','value':'area'},
                {'label':'creditcd','value':'creditcd'}]


#Atlantic_list = [{'label':i,"value":i} for i in CIUDADES.columns]


#------------------------------------------------------------------------------
#CREANDO EL DASH
app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Ciudades', children=[
        html.H1(children='Reporte Resumen Tablas'),
        html.Div(id='output_data',children='''Lista de Tablas para ver resumen'''),
        html.Br(),
        dcc.Dropdown(id='my_dropdown',
            options=Atlantic_list,
            value='new_cell',
            optionHeight=35,                    #height/space between dropdown options
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='Resumen Variables Tabla',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
        ),
        html.Br(),
        html.Div([
            dcc.Graph(id='our_graph')
        ],className='nine columns'),
        html.Br(),
        dt.DataTable(id='tbl',
                     columns=[{"name": 'Valor', "id": 'Valor'},{"name": 'Cantidad', "id": 'Cantidad'},{"name": 'Porcentaje', "id": 'Porcentaje'}])
        ]),
        ##SECOND TAB
        dcc.Tab(label='Minutos',value='sub-1'),
        ##THIRD TAB
        dcc.Tab(label='Creditos',value='sub-2')
    
    ])
])

#------------------------------------------------------------------------------
#HACIENDO LOS CALLBACKS
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):
    dff=CIUDADES
    fig = px.pie(dff,names=column_chosen)
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':'Resumen Variables Categóricas Atlantic',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig
#------------------------------------------------------------------------------
#---------------------------------------------------------------
# For tutorial purposes to show the user the search_value

@app.callback(
    Output(component_id='output_data', component_property='children'),
    [Input(component_id='my_dropdown', component_property='search_value')]
)

def build_graph(data_chosen):
    return ('Seleccione la variable para mirar su resumen: ')
#---------------------------------------------------------------
#------------------------------------------------------------------------------
#HACIENDO LOS CALLBACKS
@app.callback(
    Output(component_id='tbl', component_property='data'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_table(column_chosen):
    dff=CIUDADES
    tabla = dff[column_chosen].value_counts()
    tabla=pd.DataFrame(tabla.reset_index())
    tabla.columns=['Valor','Cantidad']
    tabla["Porcentaje"]=round(tabla["Cantidad"]/tabla["Cantidad"].sum()*100,2)
    tabla=tabla.to_dict("records")
    return tabla

if __name__ == '__main__':
    app.run_server(debug=True,port=8051)
    #app.run_server(host="0.3.1.0", port="8050", debug=True)
    