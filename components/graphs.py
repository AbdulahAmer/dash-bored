import plotly.express as px
from dash import dcc, html


def _missing_columns_message():
    return html.Div("Please select valid columns to build this chart.")


def build_histogram(df, x_column):
    if not x_column or x_column not in df.columns:
        return _missing_columns_message()
    fig = px.histogram(df, x=x_column, title=f"Histogram of {x_column}")
    return dcc.Graph(figure=fig)


def build_bar(df, x_column, y_column):
    if not x_column or not y_column or x_column not in df.columns or y_column not in df.columns:
        return _missing_columns_message()
    fig = px.bar(df, x=x_column, y=y_column, title=f"Bar chart of {y_column} by {x_column}")
    return dcc.Graph(figure=fig)


def build_scatter(df, x_column, y_column):
    if not x_column or not y_column or x_column not in df.columns or y_column not in df.columns:
        return _missing_columns_message()
    fig = px.scatter(df, x=x_column, y=y_column, title=f"Scatter plot of {y_column} vs {x_column}")
    return dcc.Graph(figure=fig)
