from dash import html
from components.controls import (
    upload_component,
    dataset_dropdown,
    view_type_radio,
    theme_toggle,
    chart_type_radio,
    axis_dropdown,
    color_picker,
    comparison_toggle,
)
from utils.file_utils import list_available_datasets


MAIN_CONTENT_ID = "main-content"
SECONDARY_CONTENT_ID = "secondary-content"
VIEW_CONTAINER_ID = "view-container"


def _chart_controls():
    return html.Div(
        className="controls-row",
        children=[
            html.Div(
                className="control-card",
                children=[html.Strong("Chart Type"), chart_type_radio()],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("X Axis"), axis_dropdown("x-axis-column")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("Y Axis"), axis_dropdown("y-axis-column")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("Color By"), axis_dropdown("color-column", placeholder="Optional")],
            ),
            html.Div(
                className="control-card narrow-card",
                children=[html.Strong("Base Color"), color_picker("color-picker")],
            ),
        ],
    )


def _comparison_controls():
    return html.Div(
        id="comparison-controls",
        className="controls-row",
        children=[
            html.Div(
                className="control-card",
                children=[html.Strong("Compare View"), view_type_radio("compare-view-type", value="chart")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("Compare Chart"), chart_type_radio("compare-chart-type", value="scatter")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("X Axis"), axis_dropdown("compare-x-axis")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("Y Axis"), axis_dropdown("compare-y-axis")],
            ),
            html.Div(
                className="control-card",
                children=[
                    html.Strong("Color By"),
                    axis_dropdown("compare-color-column", placeholder="Optional"),
                ],
            ),
            html.Div(
                className="control-card narrow-card",
                children=[html.Strong("Base Color"), color_picker("compare-color-picker", "#b95c70")],
            ),
        ],
        style={"display": "none"},
    )


def home_layout():
    dataset_options = list_available_datasets()
    default_value = dataset_options[0]["value"] if dataset_options else None

    return html.Div(
        className="container",
        children=[
            html.H1("DASH-BORED: Simple Drag-and-Drop Dashboard"),
            html.P(
                "Upload a CSV/Excel file or explore the example data to see quick summaries and charts.",
            ),
            html.Div(className="control-card", children=[upload_component()]),
            html.Div(
                className="status-text",
                id="last-uploaded-filename",
                children="No file uploaded yet.",
            ),
            html.Div(
                className="controls-row",
                children=[
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Dataset"),
                            dataset_dropdown(value=default_value),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("View"),
                            view_type_radio(),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Theme"),
                            theme_toggle(),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Layout"),
                            comparison_toggle(),
                        ],
                    ),
                ],
            ),
            _chart_controls(),
            _comparison_controls(),
            html.Hr(),
            html.Div(
                id=VIEW_CONTAINER_ID,
                className="view-single",
                children=[
                    html.Div(className="view-card", children=[html.H3("Primary View"), html.Div(id=MAIN_CONTENT_ID)]),
                    html.Div(
                        className="view-card",
                        children=[html.H3("Comparison View"), html.Div(id=SECONDARY_CONTENT_ID)],
                    ),
                ],
            ),
            html.Div(
                className="footer-note",
                children="Tip: Visit /example to see the example dataset with the same controls.",
            ),
        ],
    )
