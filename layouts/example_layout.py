from dash import html
from components.controls import (
    dataset_dropdown,
    view_type_radio,
    theme_toggle,
    chart_type_radio,
    axis_dropdown,
    color_picker,
    comparison_toggle,
)
from utils.file_utils import list_available_datasets


MAIN_CONTENT_ID = "example-main-content"
SECONDARY_CONTENT_ID = "example-secondary-content"
VIEW_CONTAINER_ID = "example-view-container"


def _comparison_controls():
    return html.Div(
        id="example-comparison-controls",
        className="controls-row",
        children=[
            html.Div(
                className="control-card",
                children=[html.Strong("Compare View"), view_type_radio("example-view-type", value="chart")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("Compare Chart"), chart_type_radio("example-chart-type", value="scatter")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("X Axis"), axis_dropdown("example-compare-x-axis")],
            ),
            html.Div(
                className="control-card",
                children=[html.Strong("Y Axis"), axis_dropdown("example-compare-y-axis")],
            ),
            html.Div(
                className="control-card",
                children=[
                    html.Strong("Color By"),
                    axis_dropdown("example-compare-color-column", placeholder="Optional"),
                ],
            ),
            html.Div(
                className="control-card narrow-card",
                children=[html.Strong("Base Color"), color_picker("example-compare-color-picker", "#b95c70")],
            ),
        ],
        style={"display": "none"},
    )


def example_layout():
    dataset_options = list_available_datasets()
    default_value = "example_sales.csv"
    return html.Div(
        className="container",
        children=[
            html.H1("Example Dataset"),
            html.P(
                "This page uses the bundled example dataset. Switch views to see table, summary, or charts.",
            ),
            html.Div(
                className="controls-row",
                children=[
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Dataset"),
                            dataset_dropdown(
                                value=default_value,
                                options=dataset_options,
                            ),
                        ],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("View"), view_type_radio()],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Theme"), theme_toggle()],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Layout"), comparison_toggle("example-comparison-toggle")],
                    ),
                ],
            ),
            html.Div(
                className="controls-row",
                children=[
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Chart Type"), chart_type_radio()],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("X Axis"), axis_dropdown("example-x-axis")],
                    ),
                    html.Div(
                        className="control-card",
                        children=[html.Strong("Y Axis"), axis_dropdown("example-y-axis")],
                    ),
                    html.Div(
                        className="control-card",
                        children=[
                            html.Strong("Color By"),
                            axis_dropdown("example-color-column", placeholder="Optional"),
                        ],
                    ),
                    html.Div(
                        className="control-card narrow-card",
                        children=[html.Strong("Base Color"), color_picker("example-color-picker")],
                    ),
                ],
            ),
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
        ],
    )
