import plotly.graph_objects as go


# Function to create the Plotly chart
def create_plot(x_time, y_data, title, y_axis_label):
    fig = go.Figure(
        data=[go.Scatter(x=x_time, y=y_data, mode='lines', name="V52")],
        layout=go.Layout(
            title=dict(text=title),
            xaxis=dict(title='Date'),
            yaxis=dict(title=y_axis_label)
        )
    )
    return fig
