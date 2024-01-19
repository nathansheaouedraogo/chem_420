# plot figures and such
import plotly.express as px  

def visualize_fft(df):
    fig = px.line(
        df, 
        x=df['amplitude'],
        y=df['frequency'],
        labels = {
            'time' : 'Amplitude',
            'frequency' : 'Frequency (Hz)'
        }
    )
    fig.show()
