import threading
import time
import webbrowser

import dash
from dash import Input, Output, State, dcc, html, dash_table

from components.graphs import (
    build_area,
    build_bar,
    build_box,
    build_histogram,
    build_line,
    build_scatter,
)
from layouts.example_layout import (
    MAIN_CONTENT_ID as EXAMPLE_CONTENT_ID,
    SECONDARY_CONTENT_ID as EXAMPLE_SECONDARY_CONTENT_ID,
    VIEW_CONTAINER_ID as EXAMPLE_VIEW_CONTAINER_ID,
    example_layout,
)
from layouts.home_layout import (
    MAIN_CONTENT_ID as HOME_CONTENT_ID,
    SECONDARY_CONTENT_ID as HOME_SECONDARY_CONTENT_ID,
    VIEW_CONTAINER_ID as HOME_VIEW_CONTAINER_ID,
    home_layout,
)
from utils.data_loader import build_summary, detect_numeric_columns, load_dataset
from utils.file_utils import ensure_data_dirs_exist, list_available_datasets, save_uploaded_file

ensure_data_dirs_exist()

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(
    id="app-root",
    className="theme-light",
    children=[dcc.Location(id="url"), html.Div(id="page-content")],
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/example":
        return example_layout()
    return home_layout()


@app.callback(Output("app-root", "className"), Input("theme-toggle", "value"))
def toggle_theme(theme_value):
    if theme_value == "dark":
        return "theme-dark"
    return "theme-light"


@app.callback(
    Output("dataset-dropdown", "options"),
    Output("dataset-dropdown", "value"),
    Output("last-uploaded-filename", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
)
def handle_file_upload(contents, filename):
    if not contents or not filename:
        return dash.no_update, dash.no_update, dash.no_update

    saved_value = save_uploaded_file(contents, filename)
    options = list_available_datasets()
    status = f"Last uploaded file: {filename}"
    return options, saved_value, status


def _build_table_view(df):
    return html.Div(
        className="table-container",
        children=[
            dash_table.DataTable(
                data=df.head(50).to_dict("records"),
                columns=[{"name": col, "id": col} for col in df.columns],
                page_action="none",
                style_table={"overflowX": "auto"},
            )
        ],
    )


def _build_summary_view(df):
    summary = build_summary(df)
    numeric_summary = summary.get("numeric_summary", {})
    cards = [
        html.Div(className="summary-card", children=[html.H4("Rows"), html.P(summary["n_rows"])]),
        html.Div(className="summary-card", children=[html.H4("Columns"), html.P(summary["n_columns"])]),
        html.Div(
            className="summary-card",
            children=[html.H4("Column Names"), html.P(", ".join(summary["columns"]))],
        ),
    ]

    if numeric_summary:
        metrics = ["mean", "min", "max"]
        stats_rows = []
        for metric in metrics:
            row = {"metric": metric}
            for col, stats in numeric_summary.items():
                if metric in stats:
                    row[col] = stats[metric]
            stats_rows.append(row)

        cards.append(
            html.Div(
                className="summary-card",
                children=[
                    html.H4("Numeric Summary"),
                    dash_table.DataTable(
                        data=stats_rows,
                        columns=[{"name": "Metric", "id": "metric"}]
                        + [{"name": col, "id": col} for col in numeric_summary],
                        style_table={"overflowX": "auto"},
                    ),
                ],
            )
        )

    return html.Div(className="summary-grid", children=cards)


def _build_chart_view(df, chart_type, x_value, y_value, color_column, color_value):
    if chart_type == "bar":
        return build_bar(df, x_value, y_value, color_column, color_value)
    if chart_type == "scatter":
        return build_scatter(df, x_value, y_value, color_column, color_value)
    if chart_type == "line":
        return build_line(df, x_value, y_value, color_column, color_value)
    if chart_type == "area":
        return build_area(df, x_value, y_value, color_column, color_value)
    if chart_type == "box":
        return build_box(df, x_value, y_value, color_column, color_value)
    return build_histogram(df, x_value, color_column, color_value)


def _render_view(df, view_type, chart_type, x_value, y_value, color_column=None, color_value=None):
    if df.empty:
        return html.Div("No data available for this selection.")
    if view_type == "summary":
        return _build_summary_view(df)
    if view_type == "chart":
        return _build_chart_view(df, chart_type, x_value, y_value, color_column, color_value)
    return _build_table_view(df)


@app.callback(
    Output("x-axis-column", "options"),
    Output("y-axis-column", "options"),
    Output("x-axis-column", "value"),
    Output("y-axis-column", "value"),
    Output("color-column", "options"),
    Output("color-column", "value"),
    Input("dataset-dropdown", "value"),
)
def update_axis_options(selected_dataset):
    df = load_dataset(selected_dataset)
    if df.empty:
        return [], [], None, None, [], None
    numeric_cols = detect_numeric_columns(df)
    x_default = numeric_cols[0] if numeric_cols else (df.columns[0] if not df.empty else None)
    y_default = numeric_cols[0] if numeric_cols else None

    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [{"label": col, "value": col} for col in numeric_cols]
    color_options = [{"label": col, "value": col} for col in df.columns]
    return x_options, y_options, x_default, y_default, color_options, None


@app.callback(
    Output("compare-x-axis", "options"),
    Output("compare-y-axis", "options"),
    Output("compare-x-axis", "value"),
    Output("compare-y-axis", "value"),
    Output("compare-color-column", "options"),
    Output("compare-color-column", "value"),
    Input("dataset-dropdown", "value"),
)
def update_compare_axis_options(selected_dataset):
    df = load_dataset(selected_dataset)
    if df.empty:
        return [], [], None, None, [], None
    numeric_cols = detect_numeric_columns(df)
    x_default = numeric_cols[0] if numeric_cols else (df.columns[0] if not df.empty else None)
    y_default = numeric_cols[0] if numeric_cols else None

    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [{"label": col, "value": col} for col in numeric_cols]
    color_options = [{"label": col, "value": col} for col in df.columns]
    return x_options, y_options, x_default, y_default, color_options, None


@app.callback(
    Output(HOME_CONTENT_ID, "children"),
    Output(HOME_SECONDARY_CONTENT_ID, "children"),
    Output(HOME_VIEW_CONTAINER_ID, "className"),
    Output("comparison-controls", "style"),
    Input("dataset-dropdown", "value"),
    Input("view-type", "value"),
    Input("chart-type", "value"),
    Input("x-axis-column", "value"),
    Input("y-axis-column", "value"),
    Input("color-column", "value"),
    Input("color-picker", "value"),
    Input("comparison-toggle", "value"),
    Input("compare-view-type", "value"),
    Input("compare-chart-type", "value"),
    Input("compare-x-axis", "value"),
    Input("compare-y-axis", "value"),
    Input("compare-color-column", "value"),
    Input("compare-color-picker", "value"),
)
def update_main_content(
    selected_dataset,
    view_type,
    chart_type,
    x_value,
    y_value,
    color_column,
    color_value,
    comparison_toggle,
    compare_view_type,
    compare_chart_type,
    compare_x_value,
    compare_y_value,
    compare_color_column,
    compare_color_value,
):
    df = load_dataset(selected_dataset)
    primary_view = _render_view(df, view_type, chart_type, x_value, y_value, color_column, color_value)

    show_comparison = comparison_toggle and "enabled" in comparison_toggle
    comparison_style = {"display": "flex"} if show_comparison else {"display": "none"}
    container_class = "view-grid" if show_comparison else "view-single"

    if not show_comparison:
        return primary_view, html.Div(className="view-placeholder"), container_class, comparison_style

    comparison_view = _render_view(
        df,
        compare_view_type,
        compare_chart_type,
        compare_x_value,
        compare_y_value,
        compare_color_column,
        compare_color_value,
    )
    return primary_view, comparison_view, container_class, comparison_style


@app.callback(
    Output("example-x-axis", "options"),
    Output("example-y-axis", "options"),
    Output("example-x-axis", "value"),
    Output("example-y-axis", "value"),
    Output("example-color-column", "options"),
    Output("example-color-column", "value"),
    Input("dataset-dropdown", "value"),
)
def update_example_axis_options(selected_dataset):
    df = load_dataset(selected_dataset)
    if df.empty:
        return [], [], None, None, [], None
    numeric_cols = detect_numeric_columns(df)
    x_default = numeric_cols[0] if numeric_cols else (df.columns[0] if not df.empty else None)
    y_default = numeric_cols[0] if numeric_cols else None

    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [{"label": col, "value": col} for col in numeric_cols]
    color_options = [{"label": col, "value": col} for col in df.columns]
    return x_options, y_options, x_default, y_default, color_options, None


@app.callback(
    Output(EXAMPLE_CONTENT_ID, "children"),
    Output(EXAMPLE_SECONDARY_CONTENT_ID, "children"),
    Output(EXAMPLE_VIEW_CONTAINER_ID, "className"),
    Output("example-comparison-controls", "style"),
    Input("dataset-dropdown", "value"),
    Input("view-type", "value"),
    Input("chart-type", "value"),
    Input("example-x-axis", "value"),
    Input("example-y-axis", "value"),
    Input("example-color-column", "value"),
    Input("example-color-picker", "value"),
    Input("example-comparison-toggle", "value"),
    Input("example-view-type", "value"),
    Input("example-chart-type", "value"),
    Input("example-compare-x-axis", "value"),
    Input("example-compare-y-axis", "value"),
    Input("example-compare-color-column", "value"),
    Input("example-compare-color-picker", "value"),
)
def update_example_content(
    selected_dataset,
    view_type,
    chart_type,
    x_value,
    y_value,
    color_column,
    color_value,
    comparison_toggle,
    compare_view_type,
    compare_chart_type,
    compare_x_value,
    compare_y_value,
    compare_color_column,
    compare_color_value,
):
    df = load_dataset(selected_dataset)
    primary_view = _render_view(df, view_type, chart_type, x_value, y_value, color_column, color_value)

    show_comparison = comparison_toggle and "enabled" in comparison_toggle
    comparison_style = {"display": "flex"} if show_comparison else {"display": "none"}
    container_class = "view-grid" if show_comparison else "view-single"

    if not show_comparison:
        return primary_view, html.Div(className="view-placeholder"), container_class, comparison_style

    comparison_view = _render_view(
        df,
        compare_view_type,
        compare_chart_type,
        compare_x_value,
        compare_y_value,
        compare_color_column,
        compare_color_value,
    )
    return primary_view, comparison_view, container_class, comparison_style


if __name__ == "__main__":
    def _open_browser():
        time.sleep(1)
        webbrowser.open_new("http://127.0.0.1:8050")

    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(debug=True)
