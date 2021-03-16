# Manipulating time-series

Time-series are a key element when assessing solar resource data. In this section, we present several examples to learn how to deal with different formats in the data and few common tasks to prepare our time-series for later analysis, such as down and up-sampling data when we need different temporal resolution than that initially available or interpolating missing values in the data. 

The dataset used in the examples of this section is an extract of the dataset from the Technical University of Denmark used in the previous section on Quality Assessment with 1-minute GHI, DHI and DNI measurements, which has been customised by adding columns with time-related data and sliced to take the data from 2019 to perform the examples. The dataset used in this section is available for download in csv format [here](https://www.dropbox.com/s/0wnz5b7454mit8o/solar_irradiance_dtu_2018_2020.csv?dl=0).

In this section, we cover:

- [Time-series handling](#timeseries_handling)
- [Down and up-sampling time-series data](#timeseries_downup_sampling)
- [Interpolating time-series data](#timeseries_interpolation)
- [Visualizating time-series data](#timeseries_visualization)

## Time-series handling <a id='timeseries_handling'></a>
Datasets often come in different formats depending on the source. Those formats sometimes cannot be used straightaway to build a time-series and may require additional processing steps before building the time-series. For example: 
- **What if date and time are in different columns?**
- **What if the year, month, day and time are in separate columns?**
- **How to the define the timestamp format for a particular dataset?**
- **How to deal with timestamp issues, local vs. universal (UTC) time?**

This subsection presents several examples to deal with different formats in which time-series data could come and shows how to build a time-series or *datetime series*, as known in Python, for later analysis. The processing steps to build time-series are based on [pandas library](https://pandas.pydata.org/).

Let's load the data and start!

# Importing the needed libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Let's first load the data into a DataFrame and inspect it
data_path = 'https://www.dropbox.com/s/qd8aw2ug8s7dq4u/solar_irradiance_dtu_2019_extended.csv?dl=1'
df = pd.read_csv(data_path, sep=',', header=0)

# Let's check the dimensions of the DataFrame
df.shape

A quite large DataFrame with 525,600 rows and 14 columns. Let's have a look to the columns and visualize the first and last rows in the dataframe:

df.columns

# First 3 rows in the dataframe
df.head(3)

# Last 3 rows in the dataframe
df.tail(3)

Now that we know better the characteristics of our data: 1-minute irradiance measurements for 2019, we can start build the timeseries in different ways.

### Time-series when timestamps are available:

When timestamps are available, the most straightforward way to build the DataFrame with a datetime index is to provide the columns where the index and the timestamps are located with the arguments *index_col* and *parse_dates*, respectively.

Let's see how!

# Load data with available timestamps
df = pd.read_csv(data_path, sep=',', header=0, index_col=[0], parse_dates=[0])
# See the first 3 rows
df.head(3)

The timestamps can be localized to a particular time zone in several ways. Universal Time Coordinated (UTC) is usually provided for many solar radiation data networks and platforms like the BSRN, SoDa, PVGIS, NSRDB, etc. However, data can be also reported in local time. 

Below, we have 2 examples on how to **localize the time-series**. The first way (for data in UTC) passes the argument *date_parser* when loading the csv file.

# Localize the time-series when loading the file (for data in UTC)
df = pd.read_csv(data_path, sep=',', header=0, index_col=[0], parse_dates=[0],
                date_parser=lambda col: pd.to_datetime(col, utc=True))
# See the first 3 rows
df.head(3)

Alternatively, the function *tz_localize* can be used to localize the values in a timezone-naive series. For other timezones, you can find the options for valid timezone strings in this [link](https://pvlib-python.readthedocs.io/en/stable/timetimezones.html).

# Load the data
df = pd.read_csv(data_path, sep=',', header=0, index_col=[0], parse_dates=[0])
# Localize the index of the dataframe using 'tz_localize'
df.index = df.index.tz_localize('UTC')
# See the first 3 rows
df.head(3)

We see how both examples, with *date_parser* and *tz_localize*, return the same DataFrame.

### Time-series when date and time are available:

When date and time are available in separate columns, a timestamp can be created in a new column and then the new column can be set as index and localized. Let's have a look how to do that:


# Load the data
df = pd.read_csv(data_path, sep=',', header=0)
# New column with the date and the time 
df['datetime'] = df['date'] + 'T' + df['time']
# Convert the new column into datetime as we pass the format as in a string as an argument
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%dT%H:%M:%S', utc=True)
# Set the column 'datetime' as index
df = df.set_index(df['datetime'])
# See the first 3 rows 
df.head(3)

### Time-series when the time data is split in multiple columns:

If time-related data are split across multiple columns, a timestamp can be created in a new column similarly than in the previous case. Let's imagine our dataset would have the year, month, day, hour, and minute in separate columns. In that case, we could build our time-series as follows:



# Load the data
df = pd.read_csv(data_path, sep=',', header=0)
# Let's reduce the code lines and define the new string within the 'to_datetime' function
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']], 
                                format = '%Y-%m-%d%H:%M')
# Set the column 'datetime' as index
df = df.set_index(df['datetime']) 
# Localize the datetime series
df.index = df.index.tz_localize('UTC') 
# See the first 3 rows 
df.head(3)

### Time-series when the timestamp is given as epoch (Unix Time)

If the dataset has epoch timestamps, the data could be loaded and can be converted to a datetime series as follows:

# Load the data
df = pd.read_csv(data_path, sep=',', header=0)
# Convert epoch timestamps to datetime format and localized to UTC
df['datetime'] = pd.to_datetime(df['epoch'], unit='s', utc=True)
# Set datetime as index
df = df.set_index(df['datetime']) 
# See the results
df.head(3)

We have seen how the same DataFrame with *datetimeindex* can be obtained regardless of the format of time-related data.


## Down and up-sampling time-series data<a id='timeseries_downup_sampling'></a>

When assessing solar resource, you may need a different time-resolution than your data for a particular part of the analysis. In those cases, it is possible to **down-sample and up-sample the data at different temporal resolutions** using two different methods within [pandas library](https://pandas.pydata.org/) called *resample* and *asfreq*. Depending on your needs, you will opt for one or the other. Regardless of the method, both of them require a DataFrame with *datetimeindex* either time-aware (localized) or time-naive (not localized). 

### asfreq vs. resample
Let's first create a new DataFrame with only the columns with solar data and see the differences between both methods with examples.

# New DataFrame with 1-minute data and solar data
df_1min = df[['GHI', 'DHI', 'DNI', 'zenith', 'azimuth']]
# See our new DataFrame
df_1min.head(3)

Let's try to obtain a DataFrame down-sampled with the maximum monthly data with both methods and see the differences. With *asfreq*, it would be the following:

df_1min.asfreq("1M").max()

With *resample* the result would be:

df_1min.resample("1M").max()

It is obvious that the outputs are not the same and that is because the methods work differently. *asfreq* takes the value at the simultaneous stamps given by the frequency argument. See below:

df_1min.asfreq("1M")

Then *.max()* has returned the maximum of each of the columns. 

In contrast, *resample* does return the maximum value within the period of time at the specified frequency. *resample* method requires a mathematical operation to perform in the resampled data (the maximum value in our case). Otherwise, it would return a *DatetimeIndexResampler* object without showing any data. See below:

df_1min.resample("1M")

The *resample* method accepts multiple **mathematical and statistical operations**. For example: maximum (max), minimum (min), arithmetic mean (mean), standard deviation (std), median (median), mode (mode), addition (sum), among others. 

Both methods allow for multiple **frequencies options**, the available frequency tags within Python can be found [here](https://stackoverflow.com/questions/35339139/where-is-the-documentation-on-pandas-freq-tags).

### Down-sampling the data in a time-series

Down-sampling permits turning more frequent values into less frequent. In the context of solar resource and considering our 1-minute resolution dataset, down-sampling can be used for:
- Producing a timeseries of hourly/daily average irradiance.
- Producing a timeseries of maximum daily irradiance.
- Estimating the hourly/daily/monthly sums of irradiation.
- And many more!

Let's implement some of these listed examples!

#### Producing hourly average irradiance from minutely observations

# Resampling to hourly mean values
df_hourly = df_1min.resample('1h').mean()
# Showing the shape of the new DataFrame
df_hourly.shape # returns Rows, Columns

There are 8760 hours in a year. Yet, we can have a look to the first few rows of the DataFrame:

df_hourly.head(12)

A time-series with the maximum irradiance would be similar replacing *'mean()'* with *'max()'*.

##### Producing time-series of monthly total GHI, DHI, DNI irradiation from minutely observations

# Resampling to monthly aggregated values
monthly_energy = df_1min[['GHI', 'DHI', 'DNI']].resample('1M').sum()*(1/60)
# See the results expressed in kWh·sqm
monthly_energy/1000

It could be done in similar way for other resolutions (e.g. daily or annual irradiation).

### Up-sampling the data in a time-series

Up-sampling permits obtaining more frequent values from less frequent. For solar data, depending on the application up to sub-minutely data could be required and up-sampling is a technique that provides a manner to increase the temporal resolution to adapt it to our needs. For example, turning an hourly time-series into a half-hourly. Let's see an example using both *resample* and *asfreq*.

#### Producing half-hourly irradiance series from hourly observations
Using the DataFrame *df_hourly* created previously, it can be up-sample as follows:

# Using 'resample' method:
df_hourly.resample('30min').mean().head(10)

# Using 'asfreq' method:
df_hourly.asfreq('30min').head(10)

Contrary to the case of down-sampling, both *asfreq* and *resample* provide similar results when up-sampling. However, *asfreq* provides additional functionalities to treat the new timestamps without data, i.e. NaN values.

By passing the argument *'method'* with the string *'backfill'* or *'bfill'* uses the next valid observation to fill the NaN value (back filling). If instead, the string *'pad'* or *'ffill'* is given, the method assigns the last valid observation forward to the next valid (forward filling). 

Let's see the same example adding this argument:

# Half-hourly up-sample with back filling function
df_hourly.asfreq('30min', method='bfill').head(10)

We see that the DataFrame now contains the next valid hourly value in the newly obtained half-hourly timestamps of the previous hour. It would take the previous valid hourly value if we used forward filling. For example:

# Half-hourly up-sample with forward-filling function
df_hourly.asfreq('30min', method='ffill').head(10)

The forward filling option provides the same value for o'clock and half past timestamps within the same hour. In addition to these two ways to complete the NaN values, the method *asfreq* can replace the NaN values with a constant. See below:

# Half-hourly up-sample filling the new timestamps with a constant
df_hourly.asfreq('30min', fill_value=0).head(10)

The use of the methods *asfreq* or *resample* will depend on your dataset and the analysis you aim to undertake.

## Interpolating time-series data<a id='timeseries_interpolation'></a>

When up-sampling the data series, it can happen that back-filling, forward-filling and constant replacement does not necessarily work for your analysis/application. An alternative approach is interpolating the replacing the NaN values with an interpolated result. Interpolation in Pandas DataFrames with *DatetimeIndex* is done with the *interpolate* method.

The mathematical interpolation method in *interpolate* is defined with the argument called *'method'*. Pandas permits several interpolation methods, such as 'linear', 'cubic', 'quadratic', 'spline', 'polynomial' and others. All the interpolation options can be found in the [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html) of the *interpolate* method. 

Following the previous example, let's implement interpolation in the missing values of the half-hourly timestamps using 'linear', 'cubic' and 'polynomial' methods:

# Up-sample using the 'asfreq' method
df_30min = df_hourly.asfreq('30min')
# Interpolate missing values (NaN) with linear interpolation
df_linear = df_30min.interpolate(method='linear')
# See the results:
df_linear.head(10)

Similarly, it can be implemented to other methods:

# Interpolate missing values (NaN) with cubic interpolation
df_cubic = df_30min.interpolate(method='cubic')
# See the results:
df_cubic.head(10)

With polynomial interpolation, the degree or order of the polynomial function needs to be defined as an argument:

# Interpolate missing values (NaN) with polynomial interpolation
df_polynomial = df_30min.interpolate(method='polynomial', order=5)
# See the results:
df_polynomial.head(10)

The interpolation of NaN values when up-sampling time-series data can help overcome the issues of using back or forward filling, specially if you aim to up-sample at higher frequencies than the example shown (e.g. 1-hour to 15-minute resolution series). The mathematical methods available for interpolation within Pandas are diverse and cover beyond the most common interpolation functions.

## Visualizing time-series data<a id='timeseries_visualization'></a>

It is often useful to visualize the data to grasp insighs and observe trends about the data. This section shows few examples to visualize time-series data.

**Plotting a time-series for a day of interest:**

Below there is an example to visualize a single day of interest. With DataFrames using *DatetimeIndex* it is easy to select a particular day and Pandas interacts with Matplotlib.Pyplot library to plot straight-away.

# Plotting GHI for a given day in the time-series
df_1min.loc['2019-06-01', 'GHI'].plot(label='GHI')
plt.ylabel('Irradiance [W/m$^2$]')
plt.xlabel('UTC Time [HH:MM]')
plt.legend(loc='best')
plt.show()  # Not necsessary in Jupyter Notebooks but usually required in other IDEs.

We can visualize the effect of using average (*resample*) vs. instantaneous (*asfreq*) measurements when down-sampling our data.

# Plotting GHI for a given day in the time-series
df_1min['2019-06-01']['GHI'].plot(label='1-min data', alpha=0.4) # Reference data
df_1min.asfreq('30min')['2019-06-01']['GHI'].plot(label='30-min instant.') # Instantaneous 30-min values
df_1min.resample('30Min').mean()['2019-06-01']['GHI'].plot(label='30-min average') # Average 30-min values
plt.title('Average vs. Actual GHI Measurements') # title of the figure
plt.ylabel('Irradiance [W/m$^2$]') # y-axis label
plt.xlabel('UTC Time [HH:MM]') # x-axis label
plt.legend(loc='upper left') # insert legend
plt.show() # Not needed in Jupyter Notebooks but usually required in other IDEs.

**Plotting a time-series for a few consecutive days of interest**

Below there is an example to visualize a few consecutive days (e.g. 5 days) of interest. By using ['start date']:['end date'] it is possible to select time ranges easily with a DataFrame having a *DatetimeIndex*.

# Variables to plot
vars = ['GHI', 'DNI', 'DHI'] 
# Create 3 subplots, with shared X and Y axis
fig, axs = plt.subplots(3, sharex=True, sharey=True, figsize=(9,6))
# Add title to the plot
fig.suptitle('Average Hourly Solar Radiation Observations', fontsize=14)

for i in range(3):
    axs[i].plot(df_1min.resample('1H').mean()['2019-06-01':'2019-06-05'][vars[i]], label='Average') # Average hourly
    axs[i].plot(df_1min.resample('1H').max()['2019-06-01':'2019-06-05'][vars[i]], label='Maximum') # Max. hourly
    axs[i].plot(df_1min.resample('1H').min()['2019-06-01':'2019-06-05'][vars[i]], label='Minimum') # Min. hourly
    axs[i].set_title(vars[i]) # Title for each subplot
fig.subplots_adjust(hspace=0.3) # Adjust the white space between the subplots titles
fig.text(0.04, 0.5, 'Irradiance [W/m$^2$]', va='center', rotation='vertical', fontsize=12) # Common Y Axis
fig.text(0.51, 0.04, 'UTC Time', ha='center', fontsize=12) # Common X Axis
plt.legend(loc='upper right', ncol=1) # Legend for the last subplot or 'axs[i].legend()' in the loop to a legend to each.
plt.show()

**Plotting a time-series for a few non-consecutive days of interest**

Below there is an example to visualize a few non-consecutive days of interest, which could be the case when we would like to observe several days scattered throughout the year a single plot. In order to do this, we need to select the day of interest from the DataFrame and then reset its *DatetimeIndex*. For example:

# List of days of interest
days = ['2019-01-01', '2019-03-01', '2019-06-01', '2019-09-01']
# Iterate over the days and plot each of them
for day in days: 
    df_day = df_1min.resample('1h').mean()[day]['GHI'].to_frame()  # average hourly of GHI for current day
    df_day = df_day.reset_index(drop=True) # reset its Index to numeric (i.e. 0,1,2,3...)
    plt.plot(df_day, label=day) # plot the current day
plt.title('Average Hourly GHI Measurements for Days of Interest') # title of the figure
plt.xticks(np.arange(0, 25, 3), np.arange(0, 25, 3)) # set labels positions and names
plt.ylabel('Irradiance [W/m$^2$]') # y-axis label
plt.xlabel('UTC Time') # x-axis label
plt.legend(loc='best') # insert legend
plt.show()

**Daily insolation throughout the year**

With time-series data, the hourly/daily/monthly insolation (i.e. the sum of accumulated energy) can also be analysed throughout the year with time-series data. For example, below an example to visualize the daily insolation is shown:

# Calculate the daily insolation expressed in kWh·sqm from GHI measurements
daily_energy = (df_1min['GHI'].resample('1D').sum()*(1/60))/1000 # selecting only GHI returns a Pandas Series

# Create time-series plot
daily_energy.plot(figsize=(9,6), legend=False) # plot timeseries 
plt.title('Time-series of Daily Insolation')  # add title
plt.ylabel('Energy [kWh/m$^2$]') # add Y-axis label
plt.xlabel('Time') # add X-axis label
plt.show()

Time-series data can also be visualized in other ways, for instance, as a heat map.

# Prepare the data for heat map of hourly insolation
energy_array = pd.DataFrame() # empty DataFrame for the results
for i in range(1,13): # iterate over months
    # select the data in the month and eliminate the datetimeindex
    df_month = daily_energy[daily_energy.index.month==i].reset_index(drop=True) 
    # rename the column with the number of the month
    df_month.columns = [str(i)]
    # Append results to the DataFrame
    energy_array = pd.concat([energy_array, df_month], axis=1)
# Transpose to have months in y-axis and days in x-axis
energy_array = energy_array.transpose()
# Rename the columns of the days 
energy_array.columns = np.arange(1, 32)

# Plot heat map of daily insolation
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', # month labels
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.figure(figsize=(10, 5))
ax = sns.heatmap(energy_array, cmap='CMRmap', linewidths=0.2, # plot heatmap with Seaborn (sns) library 
                xticklabels=2, annot=False,
                cbar_kws={'label': 'Daily Energy [kWh/m$^2$]'})
ax.set_title('Heat Map of Daily Insolation') # add title
ax.set_yticklabels(months,rotation=0) # add the months as tick-labels for the y-axis
ax.set_xticklabels(ax.get_xticklabels(),rotation=0) # add the days as tick-labels for the x-axis
ax.set_xlabel('Day of the Month')
plt.show()

## Section summary

This section has shown how to build and work with a time-series in Python with multiple examples:
- We have seen how to prepare a DataFrame with *DatatimeIndex* to be used as a time-series when the timestamps are given in multiple formats. 
- Changes in the temporal resolution of the data can be applied by down and up-sampling the data and the differences between 2 available methods (*asfreq* and *resample*) have been shown with examples and different sampling frequencies. 
- The interpolation of missing data in time-series can be used to up-sample the resolution of the data and examples with some methods have been shown.
- Finally, several ideas to visualize data have been presented. 

Overall, the possibilities with time-series of solar resource are many. The most useful and suitable analysis and visualizations will be determined by the application and scope of the study. 