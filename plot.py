# plot figures and such
import plotly.express as px  

def visualize_fft(df):
    fig = px.line(
        df, 
        x=df['time'],
        y=df['Hz'],
        labels = {
            'time' : 'Time (seconds)',
            'Hz' : 'Frequency (Hz)'
        }
    )
    fig.show
