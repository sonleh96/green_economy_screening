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
df_source = pd.read_csv('data/source.csv')
# Creating dashboard 
desc = Div(text=open("description.html").read(), sizing_mode="stretch_width")

region_list = ['All']
region_list.extend(list(df_source.REGION_NAME.unique()))

region = Select(title="Region", value="All",
               options=region_list, width=400)
year = Slider(title="Year", start=2014, end=2019, value=2014, step=1, width=400)
province = TextInput(title="Province name contains", width=400)
district = TextInput(title="District names contains", width=400)
ur_zone = RadioButtonGroup(labels=['Total', 'Urban', 'Rural'], active=0, width=400)

source = ColumnDataSource(data=dict(ECON_SCORE=[], ENVR_SCORE=[], YEAR=[], 
                                    NAME_1=[], NAME_2=[], REGION_NAME=[], 
                                    POP_ZONE=[], COLOR=[]))
columns = [
            TableColumn(field="NAME_1", title="Province"),
            TableColumn(field="NAME_2", title="District"),
            TableColumn(field="ECON_SCORE", title="Economic Score", formatter=NumberFormatter(format="0.")),
            TableColumn(field="ENVR_SCORE", title="Environment Score", formatter=NumberFormatter(format="0."))
        ]
source_table = DataTable(source=source, name="Table", 
                         columns=columns,
                         width=400, height=250)
source_table_div = Div(text="Score Table (Command + Click to deselect)",
                       width=400, align='start')
reset_button = Button(label="Refresh Button", width=400)


TOOLTIPS=[
    ("Province", "@NAME_1"),
    ("District", "@NAME_2"),
    ("Region", "@REGION_NAME"),
    ("Year", "@YEAR"),
    ("Economic Score", "@ECON_SCORE"),
    ("Environment Score", "@ENVR_SCORE")
]

p = figure(height=600, width=600, toolbar_location='above', 
           tooltips=TOOLTIPS, sizing_mode="scale_both",
           x_range=(-5.0, 105.0), y_range=(-5, 105.0),
           tools='reset, pan, box_zoom, wheel_zoom, save')
p.circle(x="ENVR_SCORE", y="ECON_SCORE", source=source, size=4, 
         line_color=None, color="COLOR", alpha=3)

p.xaxis.fixed_location = 50.0
p.yaxis.fixed_location = 50.0
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

topleft1 = Label(x=-5, y=102, x_units='data', y_units='data', text='Good Economy',render_mode='css', text_color='green', level='underlay',
                 text_font_size='15px', border_line_color='white', border_line_alpha=0, background_fill_color='white', background_fill_alpha=0)
topleft2 = Label(x=-5, y=100, x_units='data', y_units='data',text='Brown Environment ', render_mode='css',text_color='red', 
                 text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

topright1 = Label(x=90, y=102, x_units='data', y_units='data',text='Good Economy',render_mode='css',text_color='green', 
                  text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)
topright2 = Label(x=90, y=100, x_units='data', y_units='data',text='Green Environment ',render_mode='css',text_color='green',
                  text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

botleft1 = Label(x=-5, y=-3, x_units='data', y_units='data',text='Bad Economy', render_mode='css',text_color='red', 
                 text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)
botleft2 = Label(x=-5, y=-5, x_units='data', y_units='data',text='Brown Environment ', render_mode='css',text_color='red', 
                 text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

botright1 = Label(x=90, y=-3, x_units='data', y_units='data',text='Bad Economy', render_mode='css',text_color='red', 
                  text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)
botright2 = Label(x=90, y=-5, x_units='data', y_units='data',text='Green Environment ', render_mode='css',text_color='green', 
                  text_font_size='15px',border_line_color='white', border_line_alpha=0,background_fill_color='white', background_fill_alpha=0)

p.add_layout(Title(text="Environment Score", align="center", text_font_size='20px'), "below")
p.add_layout(Title(text="Economic Score", align="center", text_font_size='20px'), "left")
p.add_layout(BoxAnnotation(bottom=50, left=50, fill_alpha=0.1, fill_color='green'))
p.add_layout(BoxAnnotation(top=50, right=50, fill_alpha=0.1, fill_color='red'))
p.add_layout(BoxAnnotation(bottom=50, right=50, fill_alpha=0.1, fill_color='yellow'))
p.add_layout(BoxAnnotation(top=50, left=50, fill_alpha=0.1, fill_color='yellow'))

for citation in [topleft1, topleft2, topright1, topright2, botleft1, botleft2, botright1, botright2]:
    p.add_layout(citation)

def select_region():
    region_val = region.value
    province_val = province.value.strip()
    district_val = district.value.strip()
    ur_zone_val = ur_zone.active
    
    selected = df_source[
        df_source['YEAR'] == year.value
    ]
    if (region_val != "All"):
        selected = selected[selected.REGION_NAME.str.contains(region_val)==True]
    if (province_val != "All"):
        selected = selected[selected.NAME_1.str.contains(province_val)==True]
    if (district_val != "All"):
        selected = selected[selected.NAME_2.str.contains(district_val)==True]
    if (ur_zone_val == 0):
        selected = selected[selected.POP_ZONE == 'total']
    elif (ur_zone_val == 1):
        selected = selected[selected.POP_ZONE == 'urban']
    else:
        selected = selected[selected.POP_ZONE == 'rural']
    
    
    return selected


def update():
    df_sel = select_region()
    
    source.data = dict(
        ENVR_SCORE=df_sel["ENVR_SCORE"],
        ECON_SCORE=df_sel["ECON_SCORE"],
        NAME_1=df_sel["NAME_1"],
        NAME_2=df_sel["NAME_2"],
        REGION_NAME=df_sel["REGION_NAME"],
        YEAR=df_sel["YEAR"],
        POP_ZONE=df_sel["POP_ZONE"],
        COLOR=df_sel["COLOR"]
    )
    
def reset():
    df_reset = df_source[
        (df_source['YEAR'] == df_source['YEAR'].min()) & \
        (df_source['POP_ZONE'] == 'total')
    ]
    source.data = dict(
        ENVR_SCORE=df_reset["ENVR_SCORE"],
        ECON_SCORE=df_reset["ECON_SCORE"],
        NAME_1=df_reset["NAME_1"],
        NAME_2=df_reset["NAME_2"],
        REGION_NAME=df_reset["REGION_NAME"],
        YEAR=df_reset["YEAR"],
        POP_ZONE=df_reset["POP_ZONE"],
        COLOR=df_reset["COLOR"]
    )  
    
value_controls = [region, province, district, year]
for control in value_controls:
    control.on_change('value', lambda attr, old, new: update())
active_controls = [ur_zone]
for control in active_controls:
    control.on_change('active', lambda attr, old, new: update())
        
# controls = [reset_button, region, province, district, ur_zone, year, 
#             source_table_div, source_table]
controls = [region, province, district, ur_zone, year, 
            source_table_div, source_table]

inputs = column(*controls, width=320)

l = column(desc, row(p, inputs), sizing_mode="scale_both")

update()  # initial load of the data
# reset_button.on_click(reset)

curdoc().add_root(l)
curdoc().title = "Green Economy"