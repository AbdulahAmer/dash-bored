import plotly.express as px
from dash import dcc, html


def _missing_columns_message():
    return html.Div("Please select valid columns to build this chart.")


def _color_kwargs(color_column, color_value):
    kwargs = {}
    if color_column:
        kwargs["color"] = color_column
    if color_value:
        kwargs["color_discrete_sequence"] = [color_value]
    return kwargs


def build_histogram(df, x_column, color_column=None, color_value=None):
    if not x_column or x_column not in df.columns:
        return _missing_columns_message()
    fig = px.histogram(
        df, x=x_column, title=f"Histogram of {x_column}", **_color_kwargs(color_column, color_value)
    )
    return dcc.Graph(figure=fig)


def build_bar(df, x_column, y_column, color_column=None, color_value=None):
    if not x_column or not y_column or x_column not in df.columns or y_column not in df.columns:
        return _missing_columns_message()
    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=f"Bar chart of {y_column} by {x_column}",
        **_color_kwargs(color_column, color_value),
    )
    return dcc.Graph(figure=fig)


def build_scatter(df, x_column, y_column, color_column=None, color_value=None):
    if not x_column or not y_column or x_column not in df.columns or y_column not in df.columns:
        return _missing_columns_message()
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"Scatter plot of {y_column} vs {x_column}",
        **_color_kwargs(color_column, color_value),
    )
    fig.update_traces(marker={"size": 10})
    return dcc.Graph(figure=fig)


def build_line(df, x_column, y_column, color_column=None, color_value=None):
    if not x_column or not y_column or x_column not in df.columns or y_column not in df.columns:
        return _missing_columns_message()
    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        markers=True,
        title=f"Line chart of {y_column} over {x_column}",
        **_color_kwargs(color_column, color_value),
    )
    return dcc.Graph(figure=fig)


def build_area(df, x_column, y_column, color_column=None, color_value=None):
    if not x_column or not y_column or x_column not in df.columns or y_column not in df.columns:
        return _missing_columns_message()
    fig = px.area(
        df,
        x=x_column,
        y=y_column,
        title=f"Area chart of {y_column} over {x_column}",
        **_color_kwargs(color_column, color_value),
    )
    return dcc.Graph(figure=fig)


def build_box(df, x_column, y_column, color_column=None, color_value=None):
    if not x_column or x_column not in df.columns or (y_column and y_column not in df.columns):
        return _missing_columns_message()
    fig = px.box(
        df,
        x=x_column,
        y=y_column,
        points="all",
        title="Box plot",
        **_color_kwargs(color_column, color_value),
    )
    return dcc.Graph(figure=fig)
