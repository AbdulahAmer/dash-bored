import dash
from dash import Input, Output, State, dcc, html, dash_table

from components.graphs import build_bar, build_histogram, build_scatter
from layouts.example_layout import MAIN_CONTENT_ID as EXAMPLE_CONTENT_ID, example_layout
from layouts.home_layout import MAIN_CONTENT_ID as HOME_CONTENT_ID, home_layout
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


def _build_chart_view(df, chart_type, x_value, y_value):
    if chart_type == "bar":
        return build_bar(df, x_value, y_value)
    if chart_type == "scatter":
        return build_scatter(df, x_value, y_value)
    return build_histogram(df, x_value)


def _render_view(df, view_type, chart_type, x_value, y_value):
    if df.empty:
        return html.Div("No data available for this selection.")
    if view_type == "summary":
        return _build_summary_view(df)
    if view_type == "chart":
        return _build_chart_view(df, chart_type, x_value, y_value)
    return _build_table_view(df)


@app.callback(
    Output("x-axis-column", "options"),
    Output("y-axis-column", "options"),
    Output("x-axis-column", "value"),
    Output("y-axis-column", "value"),
    Input("dataset-dropdown", "value"),
)
def update_axis_options(selected_dataset):
    df = load_dataset(selected_dataset)
    if df.empty:
        return [], [], None, None
    numeric_cols = detect_numeric_columns(df)
    x_default = numeric_cols[0] if numeric_cols else (df.columns[0] if not df.empty else None)
    y_default = numeric_cols[0] if numeric_cols else None

    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [{"label": col, "value": col} for col in numeric_cols]
    return x_options, y_options, x_default, y_default


@app.callback(
    Output(HOME_CONTENT_ID, "children"),
    Input("dataset-dropdown", "value"),
    Input("view-type", "value"),
    Input("chart-type", "value"),
    Input("x-axis-column", "value"),
    Input("y-axis-column", "value"),
)
def update_main_content(selected_dataset, view_type, chart_type, x_value, y_value):
    df = load_dataset(selected_dataset)
    return _render_view(df, view_type, chart_type, x_value, y_value)


@app.callback(
    Output("example-x-axis", "options"),
    Output("example-y-axis", "options"),
    Output("example-x-axis", "value"),
    Output("example-y-axis", "value"),
    Input("dataset-dropdown", "value"),
)
def update_example_axis_options(selected_dataset):
    df = load_dataset(selected_dataset)
    if df.empty:
        return [], [], None, None
    numeric_cols = detect_numeric_columns(df)
    x_default = numeric_cols[0] if numeric_cols else (df.columns[0] if not df.empty else None)
    y_default = numeric_cols[0] if numeric_cols else None

    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [{"label": col, "value": col} for col in numeric_cols]
    return x_options, y_options, x_default, y_default


@app.callback(
    Output(EXAMPLE_CONTENT_ID, "children"),
    Input("dataset-dropdown", "value"),
    Input("view-type", "value"),
    Input("chart-type", "value"),
    Input("example-x-axis", "value"),
    Input("example-y-axis", "value"),
)
def update_example_content(selected_dataset, view_type, chart_type, x_value, y_value):
    df = load_dataset(selected_dataset)
    return _render_view(df, view_type, chart_type, x_value, y_value)


if __name__ == "__main__":
    app.run(debug=True)
