# get data frames and such; reverse fft!
import plot
import fft_df

# load df
df = fft_df.fft_df()

## DEBUG df##
# # import cwd
# # save to cwd
# df.to_csv(cwd.file_path('fft_df.dat'), index=False)

# plot df (NOTE: launches interactive plot in browser)
plot.visualize_fft(df)
