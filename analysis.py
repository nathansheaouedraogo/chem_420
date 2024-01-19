# get data frames and such; reverse fft!
import plot
import fft_df
import cwd

df = fft_df.fft_df()
df.to_csv(cwd.file_path('df'), index=False)
print(df)
# plot.visualize_fft(fft_df.fft_df())