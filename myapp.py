import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput, Label, RadioButtonGroup, TableColumn, Button
from bokeh.models import NumberFormatter, Title, BoxAnnotation
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.widgets import DataTable

# Loading data 
df_source = pd.read_csv('data/source_v2.csv')
# Creating dashboard 
desc = Div(text=open("description.html").read(), sizing_mode="stretch_width")

min_year = df_source.YEAR.min() 
max_year = df_source.YEAR.max() 

region_list = ['All']
region_list.extend(list(df_source.REGION_NAME.unique()))

region = Select(title="Region", value="All",
               options=region_list, width=400)
year = Slider(title="Year", start=min_year, end=max_year, value=min_year, step=1, width=400)
province = TextInput(title="Province name contains", width=400)
district = TextInput(title="District names contains", width=400, value='Dong Da')
ur_zone = RadioButtonGroup(labels=['Total', 'Urban', 'Rural'], active=0, width=400)
ur_zone_line = RadioButtonGroup(labels=['Total', 'Urban', 'Rural'], active=0, width=400)

source = ColumnDataSource(data=dict(x=[], y=[],
                                    ECON_SCORE=[], ENVR_SCORE=[], FOREST_SCORE=[], AIR_SCORE=[], TEMP_SCORE=[],
                                    YEAR=[], NAME_1=[], NAME_2=[], REGION_NAME=[], POP_ZONE=[], COLOR=[]))

columns = [
            TableColumn(field="NAME_1", title="Province"),
            TableColumn(field="NAME_2", title="District"),
            TableColumn(field="ECON_SCORE", title="Economic Score", formatter=NumberFormatter(format="0.")),
            TableColumn(field="ENVR_SCORE", title="Environment Score", formatter=NumberFormatter(format="0.")),
            TableColumn(field="FOREST_SCORE", title="Deforestation Score", formatter=NumberFormatter(format="0.")),
            TableColumn(field="AIR_SCORE", title="Air Pollution Score", formatter=NumberFormatter(format="0.")),
            TableColumn(field="TEMP_SCORE", title="Temperature Score", formatter=NumberFormatter(format="0."))
          ]

source_table = DataTable(source=source, name="Table", 
                         columns=columns,
                         width=400, height=740)
source_table_div = Div(text="Score Table (Command + Click to deselect)",
                       width=400, align='start')
reset_button = Button(label="Refresh Button", width=400)

axis_map = {
    "Environment Score": "ENVR_SCORE",
    "Deforestation Score": "FOREST_SCORE",
    "Air Pollution Score": "AIR_SCORE",
    "Temperature Score": "TEMP_SCORE"
}

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Environment Score")

space_div = Div(text="", height=20, align='start')

TOOLTIPS_SCATTER=[
    ("Province", "@NAME_1"),
    ("District", "@NAME_2"),
    ("Region", "@REGION_NAME"),
    ("Year", "@YEAR")
]

p = figure(height=600, width=600, toolbar_location='above', 
           tooltips=TOOLTIPS_SCATTER, sizing_mode="scale_both",
           x_range=(-5.0, 105.0), y_range=(-5, 105.0),
           tools='reset, pan, box_zoom, wheel_zoom, save')
p.circle(x="x", y="y", source=source, size=4, 
         line_color=None, color="COLOR", alpha=3)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

topleft1 = Label(x=-4, y=102, x_units='data', y_units='data', text='Good Economy',render_mode='css', text_color='green', level='underlay',
                 text_font_size='12px', border_line_color='white', border_line_alpha=0, background_fill_color='white', background_fill_alpha=0)
topleft2 = Label(x=-4, y=100, x_units='data', y_units='data',text='Brown Environment ', render_mode='css',text_color='red', 
                 text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

topright1 = Label(x=92, y=102, x_units='data', y_units='data',text='Good Economy',render_mode='css',text_color='green', 
                  text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)
topright2 = Label(x=92, y=100, x_units='data', y_units='data',text='Green Environment ',render_mode='css',text_color='green',
                  text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

botleft1 = Label(x=-4, y=-3, x_units='data', y_units='data',text='Bad Economy', render_mode='css',text_color='red', 
                 text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)
botleft2 = Label(x=-4, y=-5, x_units='data', y_units='data',text='Brown Environment ', render_mode='css',text_color='red', 
                 text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

botright1 = Label(x=92, y=-3, x_units='data', y_units='data',text='Bad Economy', render_mode='css',text_color='red', 
                  text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)
botright2 = Label(x=92, y=-5, x_units='data', y_units='data',text='Green Environment ', render_mode='css',text_color='green', 
                  text_font_size='12px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

p.add_layout(BoxAnnotation(bottom=50, left=50, fill_alpha=0.1, fill_color='green'))
p.add_layout(BoxAnnotation(top=50, right=50, fill_alpha=0.1, fill_color='red'))
p.add_layout(BoxAnnotation(bottom=50, right=50, fill_alpha=0.1, fill_color='yellow'))
p.add_layout(BoxAnnotation(top=50, left=50, fill_alpha=0.1, fill_color='yellow'))

for citation in [topleft1, topleft2, topright1, topright2, botleft1, botleft2, botright1, botright2]:
    p.add_layout(citation)
    
source_line = ColumnDataSource(data=dict(
                                    SCORE_1=[], SCORE_2=[],
                                    TIME=[], ZONE=[]))

TOOLTIPS_LINE=[
    ("Economic Score", "@SCORE_1"),
    ("Environment Score", "@SCORE_2"),
    ("Year", "@YEAR")
]

ts = figure(height=300, width=600, toolbar_location='above', tooltips=TOOLTIPS_LINE,
            x_range=(min_year-1,max_year+1), sizing_mode="scale_both",
            tools='reset, pan, box_zoom, wheel_zoom, save')
ts.line(x="TIME", y="SCORE_1", source=source_line,
        legend_label="Economic", line_color="orange", line_width=3)
ts.line(x="TIME", y="SCORE_2", line_color='green', source=source_line,
        legend_label="Environment", line_width=3)

ts.xgrid.grid_line_color = None
ts.ygrid.grid_line_color = None
ts.legend.location = 'center_left'

def select_region():
    region_val = region.value
    province_val = province.value.strip()
    ur_zone_val = ur_zone.active
    
    selected = df_source[
        df_source['YEAR'] == year.value
    ]
    if (region_val != "All"):
        selected = selected[selected.REGION_NAME.str.contains(region_val)==True]
    if (province_val != "All"):
        selected = selected[selected.NAME_1.str.contains(province_val)==True]
    if (ur_zone_val == 0):
        selected = selected[selected.POP_ZONE == 'total']
    elif (ur_zone_val == 1):
        selected = selected[selected.POP_ZONE == 'urban']
    else:
        selected = selected[selected.POP_ZONE == 'rural']
    
    
    return selected

def select_district():
    district_val = district.value.strip()
    ur_zone_line_val = ur_zone_line.active
    
    sel_dist = df_source[
        (df_source.NAME_2.str.contains(district_val)==True)
    ]

    if (ur_zone_line_val == 0):
        sel_dist = sel_dist[sel_dist.POP_ZONE == 'total']
    elif (ur_zone_line_val == 1):
        sel_dist = sel_dist[sel_dist.POP_ZONE == 'urban']
    else:
        sel_dist = sel_dist[sel_dist.POP_ZONE == 'rural']
    
    sel_dist = sel_dist.rename({'ECON_SCORE': 'SCORE_1',
                                'ENVR_SCORE': 'SCORE_2',
                                'YEAR': 'TIME',
                                'POP_ZONE': 'ZONE'}, axis=1)
    sel_dist.to_csv('test.csv')
    
    return sel_dist, district_val


def update():
    df_sel = select_region()
    x_name = axis_map[x_axis.value]
    
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = "Economic Score"
    
    source.data = dict(
        x=df_sel[x_name],
        y=df_sel["ECON_SCORE"],
        ENVR_SCORE=df_sel["ENVR_SCORE"],
        ECON_SCORE=df_sel["ECON_SCORE"],
        FOREST_SCORE=df_sel["FOREST_SCORE"],
        AIR_SCORE=df_sel["AIR_SCORE"],
        TEMP_SCORE=df_sel["TEMP_SCORE"],
        NAME_1=df_sel["NAME_1"],
        NAME_2=df_sel["NAME_2"],
        REGION_NAME=df_sel["REGION_NAME"],
        YEAR=df_sel["YEAR"],
        POP_ZONE=df_sel["POP_ZONE"],
        COLOR=df_sel["COLOR"]
        )
        
    df_dist, dist = select_district()
    
    ts.xaxis.axis_label = "Year"
    ts.yaxis.axis_label = "Score"
    ts.title.text = dist + ' district'
    
    source_line.data = dict(
        SCORE_2=df_dist["SCORE_2"],
        SCORE_1=df_dist["SCORE_1"],
        TIME=df_dist["TIME"],
        ZONE=df_dist["ZONE"]
    )

    
value_controls = [region, province, district, year, x_axis]
for control in value_controls:
    control.on_change('value', lambda attr, old, new: update())
active_controls = [ur_zone, ur_zone_line]
for control in active_controls:
    control.on_change('active', lambda attr, old, new: update())
        
controls = [region, province, ur_zone, year, 
            x_axis, source_table_div, source_table, space_div, district, ur_zone_line]


inputs = column(*controls, width=320)

l = row(column(p, ts, sizing_mode="scale_both"), inputs)

# l = column(desc, row(p, inputs), sizing_mode="scale_both")

update()  # initial load of the data


curdoc().add_root(l)
curdoc().title = "Green Economy"