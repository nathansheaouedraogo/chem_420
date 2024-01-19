# plot figures and such
import plotly.express as px  

def visualize_fft(df):
    fig = px.line(
        df, 
        x=df['amplitude'],
        y=df['hz'],
        labels = {
            'time' : 'Amplitude',
            'hz' : 'Frequency (Hz)'
        }
    )
    fig.show()
