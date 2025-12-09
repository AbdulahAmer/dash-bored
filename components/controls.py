from dash import dcc, html


def upload_component(id="upload-data"):
    return dcc.Upload(
        id=id,
        children=html.Div(
            ["Drag and drop a CSV/Excel file here, or click to select."],
            className="upload-box",
        ),
        style={"width": "100%"},
        multiple=False,
    )


def dataset_dropdown(id="dataset-dropdown", options=None, value=None):
    return dcc.Dropdown(
        id=id,
        options=options or [],
        value=value,
        clearable=False,
        placeholder="Select a dataset",
    )


def view_type_radio(id="view-type", value="table"):
    return dcc.RadioItems(
        id=id,
        options=[
            {"label": "Table", "value": "table"},
            {"label": "Summary", "value": "summary"},
            {"label": "Chart", "value": "chart"},
        ],
        value=value,
        inline=True,
        inputClassName="form-check-input",
        labelClassName="form-check-label",
    )


def theme_toggle(id="theme-toggle", value="light"):
    return dcc.RadioItems(
        id=id,
        options=[
            {"label": "Light", "value": "light"},
            {"label": "Dark", "value": "dark"},
        ],
        value=value,
        inline=True,
    )


def chart_type_radio(id="chart-type", value="histogram"):
    return dcc.RadioItems(
        id=id,
        options=[
            {"label": "Histogram", "value": "histogram"},
            {"label": "Bar", "value": "bar"},
            {"label": "Scatter", "value": "scatter"},
        ],
        value=value,
        inline=True,
    )


def axis_dropdown(id, options=None, value=None, placeholder="Select column"):
    return dcc.Dropdown(
        id=id,
        options=options or [],
        value=value,
        placeholder=placeholder,
        clearable=True,
    )
