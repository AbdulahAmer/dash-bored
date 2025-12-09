from dash import html
from components.controls import (
    upload_component,
    dataset_dropdown,
    view_type_radio,
    theme_toggle,
    chart_type_radio,
    axis_dropdown,
)
from utils.file_utils import list_available_datasets


MAIN_CONTENT_ID = "main-content"


def home_layout():
    dataset_options = list_available_datasets()
    default_value = dataset_options[0]["value"] if dataset_options else None

    return html.Div(
        className="container",
        children=[
            html.H1("DASH-BORED: Simple Drag-and-Drop Dashboard"),
            html.P(
                "Upload a CSV/Excel file or explore the example data to see quick summaries and charts."
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
                ],
            ),
            html.Div(
                className="controls-row",
                children=[
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Chart Type"),
                            chart_type_radio(),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("X Axis"),
                            axis_dropdown("x-axis-column"),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Y Axis"),
                            axis_dropdown("y-axis-column"),
                        ],
                    ),
                ],
            ),
            html.Hr(),
            html.Div(id=MAIN_CONTENT_ID, children="Select a dataset to get started."),
            html.Div(
                className="footer-note",
                children="Tip: Visit /example to see the example dataset with the same controls.",
            ),
        ],
    )
