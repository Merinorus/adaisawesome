
# coding: utf-8

# # Table of Contents
#  <p><div class="lev1"><a href="#Data-Wrangling-with-Pandas"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data Wrangling with Pandas</a></div><div class="lev2"><a href="#Date/Time-data-handling"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Date/Time data handling</a></div><div class="lev2"><a href="#Merging-and-joining-DataFrame-objects"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Merging and joining DataFrame objects</a></div><div class="lev2"><a href="#Concatenation"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Concatenation</a></div><div class="lev2"><a href="#Exercise-1"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Exercise 1</a></div><div class="lev2"><a href="#Reshaping-DataFrame-objects"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Reshaping DataFrame objects</a></div><div class="lev2"><a href="#Pivoting"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Pivoting</a></div><div class="lev2"><a href="#Data-transformation"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Data transformation</a></div><div class="lev3"><a href="#Dealing-with-duplicates"><span class="toc-item-num">1.7.1&nbsp;&nbsp;</span>Dealing with duplicates</a></div><div class="lev3"><a href="#Value-replacement"><span class="toc-item-num">1.7.2&nbsp;&nbsp;</span>Value replacement</a></div><div class="lev3"><a href="#Inidcator-variables"><span class="toc-item-num">1.7.3&nbsp;&nbsp;</span>Inidcator variables</a></div><div class="lev2"><a href="#Categorical-Data"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>Categorical Data</a></div><div class="lev3"><a href="#Discretization"><span class="toc-item-num">1.8.1&nbsp;&nbsp;</span>Discretization</a></div><div class="lev3"><a href="#Permutation-and-sampling"><span class="toc-item-num">1.8.2&nbsp;&nbsp;</span>Permutation and sampling</a></div><div class="lev2"><a href="#Data-aggregation-and-GroupBy-operations"><span class="toc-item-num">1.9&nbsp;&nbsp;</span>Data aggregation and GroupBy operations</a></div><div class="lev3"><a href="#Apply"><span class="toc-item-num">1.9.1&nbsp;&nbsp;</span>Apply</a></div><div class="lev2"><a href="#Exercise-2"><span class="toc-item-num">1.10&nbsp;&nbsp;</span>Exercise 2</a></div><div class="lev2"><a href="#References"><span class="toc-item-num">1.11&nbsp;&nbsp;</span>References</a></div>

# # Data Wrangling with Pandas
# 
# Now that we have been exposed to the basic functionality of Pandas, lets explore some more advanced features that will be useful when addressing more complex data management tasks.
# 
# As most statisticians/data analysts will admit, often the lion's share of the time spent implementing an analysis is devoted to preparing the data itself, rather than to coding or running a particular model that uses the data. This is where Pandas and  Python's standard library are beneficial, providing high-level, flexible, and efficient tools for manipulating your data as needed.
# 

# In[2]:

get_ipython().magic('matplotlib inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('notebook')


# ## Date/Time data handling
# 
# Date and time data are inherently problematic. There are an unequal number of days in every month, an unequal number of days in a year (due to leap years), and time zones that vary over space. Yet information about time is essential in many analyses, particularly in the case of time series analysis.

# The `datetime` built-in library handles temporal information down to the nanosecond.

# In[51]:

from datetime import datetime


# In[52]:

now = datetime.now()
now


# In[53]:

now.day


# In[5]:

now.weekday()


# In addition to `datetime` there are simpler objects for date and time information only, respectively.

# In[54]:

from datetime import date, time


# In[7]:

time(3, 24)


# In[8]:

date(1970, 9, 3)


# Having a custom data type for dates and times is convenient because we can perform operations on them easily. For example, we may want to calculate the difference between two times:

# In[9]:

my_age = now - datetime(1970, 1, 1)
my_age


# In[55]:

print(type(my_age))
my_age.days/365


# In this section, we will manipulate data collected from ocean-going vessels on the eastern seaboard. Vessel operations are monitored using the Automatic Identification System (AIS), a safety at sea navigation technology which vessels are required to maintain and that uses transponders to transmit very high frequency (VHF) radio signals containing static information including ship name, call sign, and country of origin, as well as dynamic information unique to a particular voyage such as vessel location, heading, and speed. 
# 
# The International Maritime Organization’s (IMO) International Convention for the Safety of Life at Sea requires functioning AIS capabilities on all vessels 300 gross tons or greater and the US Coast Guard requires AIS on nearly all vessels sailing in U.S. waters. The Coast Guard has established a national network of AIS receivers that provides coverage of nearly all U.S. waters. AIS signals are transmitted several times each minute and the network is capable of handling thousands of reports per minute and updates as often as every two seconds. Therefore, a typical voyage in our study might include the transmission of hundreds or thousands of AIS encoded signals. This provides a rich source of spatial data that includes both spatial and temporal information.
# 
# For our purposes, we will use summarized data that describes the transit of a given vessel through a particular administrative area. The data includes the start and end time of the transit segment, as well as information about the speed of the vessel, how far it travelled, etc.

# In[56]:

segments = pd.read_csv("Data/AIS/transit_segments.csv")
segments.head()


# For example, we might be interested in the distribution of transit lengths, so we can plot them as a histogram:

# In[57]:

segments.seg_length.hist(bins=500)


# Though most of the transits appear to be short, there are a few longer distances that make the plot difficult to read. This is where a transformation is useful:

# In[58]:

segments.seg_length.apply(np.log).hist(bins=500)


# We can see that although there are date/time fields in the dataset, they are not in any specialized format, such as `datetime`.

# In[59]:

segments.st_time.dtype


# Our first order of business will be to convert these data to `datetime`. The `strptime` method parses a string representation of a date and/or time field, according to the expected format of this information.

# In[ ]:

datetime.strptime(segments.st_time.ix[0], '%m/%d/%y %H:%M')


# The `dateutil` package includes a parser that attempts to detect the format of the date strings, and convert them automatically.

# In[ ]:

from dateutil.parser import parse


# In[ ]:

parse(segments.st_time.ix[0])


# We can convert all the dates in a particular column by using the `apply` method.

# In[ ]:

segments.st_time.apply(lambda d: datetime.strptime(d, '%m/%d/%y %H:%M'))


# As a convenience, Pandas has a `to_datetime` method that will parse and convert an entire Series of formatted strings into `datetime` objects.

# In[ ]:

pd.to_datetime(segments.st_time[:10])


# Pandas also has a custom NA value for missing datetime objects, `NaT`.

# In[ ]:

pd.to_datetime([None])


# Also, if `to_datetime()` has problems parsing any particular date/time format, you can pass the spec in using the `format=` argument.

# The `read_*` functions now have an optional `parse_dates` argument that try to convert any columns passed to it into `datetime` format upon import:

# In[ ]:

segments = pd.read_csv("Data/AIS/transit_segments.csv", parse_dates=['st_time', 'end_time'])


# In[ ]:

segments.dtypes


# Columns of the `datetime` type have an **accessor** to easily extract properties of the data type. This will return a `Series`, with the same row index as the `DataFrame`. For example:

# In[ ]:

segments.st_time.dt.month.head()


# In[ ]:

segments.st_time.dt.hour.head()


# This can be used to easily filter rows by particular temporal attributes:

# In[ ]:

segments[segments.st_time.dt.month==2].head()


# In addition, time zone information can be applied:

# In[ ]:

segments.st_time.dt.tz_localize('UTC').head()


# In[ ]:

segments.st_time.dt.tz_localize('UTC').dt.tz_convert('US/Eastern').head()


# ## Merging and joining DataFrame objects

# Now that we have the vessel transit information as we need it, we may want a little more information regarding the vessels themselves. In the `data/AIS` folder there is a second table that contains information about each of the ships that traveled the segments in the `segments` table.

# In[ ]:

vessels = pd.read_csv("Data/AIS/vessel_information.csv", index_col='mmsi')
vessels.head()


# In[ ]:

[v for v in vessels.type.unique() if v.find('/')==-1]


# In[ ]:

vessels.type.value_counts()


# The challenge, however, is that several ships have travelled multiple segments, so there is not a one-to-one relationship between the rows of the two tables. The table of vessel information has a *one-to-many* relationship with the segments.
# 
# In Pandas, we can combine tables according to the value of one or more *keys* that are used to identify rows, much like an index. Using a trivial example:

# In[ ]:

df1 = pd.DataFrame(dict(id=range(4), age=np.random.randint(18, 31, size=4)))
df2 = pd.DataFrame(dict(id=list(range(3))+list(range(3)), 
                        score=np.random.random(size=6)))

df1


# In[ ]:

df2


# In[ ]:

pd.merge(df1, df2)


# Notice that without any information about which column to use as a key, Pandas did the right thing and used the `id` column in both tables. Unless specified otherwise, `merge` will used any common column names as keys for merging the tables. 
# 
# Notice also that `id=3` from `df1` was omitted from the merged table. This is because, by default, `merge` performs an **inner join** on the tables, meaning that the merged table represents an intersection of the two tables.

# In[ ]:

pd.merge(df1, df2, how='outer')


# The **outer join** above yields the union of the two tables, so all rows are represented, with missing values inserted as appropriate. One can also perform **right** and **left** joins to include all rows of the right or left table (*i.e.* first or second argument to `merge`), but not necessarily the other.

# Looking at the two datasets that we wish to merge:

# In[ ]:

segments.head(1)


# In[ ]:

vessels.head(1)


# we see that there is a `mmsi` value (a vessel identifier) in each table, but it is used as an index for the `vessels` table. In this case, we have to specify to join on the index for this table, and on the `mmsi` column for the other.

# In[ ]:

segments_merged = pd.merge(vessels, segments, left_index=True, right_on='mmsi')


# In[ ]:

segments_merged.head()


# In this case, the default inner join is suitable; we are not interested in observations from either table that do not have corresponding entries in the other. 
# 
# Notice that `mmsi` field that was an index on the `vessels` table is no longer an index on the merged table.

# Here, we used the `merge` function to perform the merge; we could also have used the `merge` *method* for either of the tables:

# In[ ]:

vessels.merge(segments, left_index=True, right_on='mmsi').head()


# Occasionally, there will be fields with the same in both tables that we do not wish to use to join the tables; they may contain different information, despite having the same name. In this case, Pandas will by default append suffixes `_x` and `_y` to the columns to uniquely identify them.

# In[ ]:

segments['type'] = 'foo'
pd.merge(vessels, segments, left_index=True, right_on='mmsi').head()


# This behavior can be overridden by specifying a `suffixes` argument, containing a list of the suffixes to be used for the columns of the left and right columns, respectively.

# ## Concatenation
# 
# A common data manipulation is appending rows or columns to a dataset that already conform to the dimensions of the exsiting rows or colums, respectively. In NumPy, this is done either with `concatenate` or the convenience "functions" `c_` and `r_`:

# In[ ]:

np.concatenate([np.random.random(5), np.random.random(5)])


# In[ ]:

np.r_[np.random.random(5), np.random.random(5)]


# In[ ]:

np.c_[np.random.random(5), np.random.random(5)]


# > Notice that `c_` and `r_` are not really functions at all, since it is performing some sort of indexing operation, rather than being called. They are actually *class instances*, but they are here behaving mostly like functions. Don't think about this too hard; just know that they are there.

# This operation is also called *binding* or *stacking*.
# 
# With Pandas' indexed data structures, there are additional considerations as the overlap in index values between two data structures affects how they are concatenate.
# 
# Lets import two microbiome datasets, each consisting of counts of microorganiams from a particular patient. We will use the first column of each dataset as the index.

# In[28]:

mb1 = pd.read_excel('Data/microbiome/MID1.xls', 'Sheet 1', index_col=0, header=None)
mb2 = pd.read_excel('Data/microbiome/MID2.xls', 'Sheet 1', index_col=0, header=None)
mb1.shape, mb2.shape


# In[29]:

mb1.head()


# Let's give the index and columns meaningful labels:

# In[30]:

mb1.columns = mb2.columns = ['Count']


# In[31]:

mb1.index.name = mb2.index.name = 'Taxon'


# In[32]:

mb1.head()


# The index of these data is the unique biological classification of each organism, beginning with *domain*, *phylum*, *class*, and for some organisms, going all the way down to the genus level.
# 
# ![classification](http://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Biological_classification_L_Pengo_vflip.svg/150px-Biological_classification_L_Pengo_vflip.svg.png)

# In[ ]:

mb1.index[:3]


# In[ ]:

mb1.index.is_unique


# If we concatenate along `axis=0` (the default), we will obtain another data frame with the the rows concatenated:

# In[ ]:

pd.concat([mb1, mb2], axis=0).shape


# However, the index is no longer unique, due to overlap between the two DataFrames.

# In[ ]:

pd.concat([mb1, mb2], axis=0).index.is_unique


# Concatenating along `axis=1` will concatenate column-wise, but respecting the indices of the two DataFrames.

# In[ ]:

pd.concat([mb1, mb2], axis=1).shape


# In[ ]:

pd.concat([mb1, mb2], axis=1).head()


# If we are only interested in taxa that are included in both DataFrames, we can specify a `join=inner` argument.

# In[ ]:

pd.concat([mb1, mb2], axis=1, join='inner').head()


# If we wanted to use the second table to *fill values* absent from the first table, we could use `combine_first`.

# In[ ]:

mb1.combine_first(mb2).head()


# We can also create a hierarchical index based on keys identifying the original tables.

# In[ ]:

pd.concat([mb1, mb2], keys=['patient1', 'patient2']).head()


# In[ ]:

pd.concat([mb1, mb2], keys=['patient1', 'patient2']).index.is_unique


# Alternatively, you can pass keys to the concatenation by supplying the DataFrames (or Series) as a dict, resulting in a "wide" format table.

# In[ ]:

pd.concat(dict(patient1=mb1, patient2=mb2), axis=1).head()


# If you want `concat` to work like `numpy.concatanate`, you may provide the `ignore_index=True` argument.

# ## Exercise 1
# 
# In the *data/microbiome* subdirectory, there are 9 spreadsheets of microbiome data that was acquired from high-throughput RNA sequencing procedures, along with a 10th file that describes the content of each. Write code that imports each of the data spreadsheets and combines them into a single `DataFrame`, adding the identifying information from the metadata spreadsheet as columns in the combined `DataFrame`.

# In[43]:

# Loading all the .xls files one by one
mb1 = pd.read_excel('Data/microbiome/MID1.xls', 'Sheet 1', index_col=0, header=None)
mb2 = pd.read_excel('Data/microbiome/MID2.xls', 'Sheet 1', index_col=0, header=None)
mb3 = pd.read_excel('Data/microbiome/MID3.xls', 'Sheet 1', index_col=0, header=None)
mb4 = pd.read_excel('Data/microbiome/MID4.xls', 'Sheet 1', index_col=0, header=None)
mb5 = pd.read_excel('Data/microbiome/MID5.xls', 'Sheet 1', index_col=0, header=None)
mb6 = pd.read_excel('Data/microbiome/MID6.xls', 'Sheet 1', index_col=0, header=None)
mb7 = pd.read_excel('Data/microbiome/MID7.xls', 'Sheet 1', index_col=0, header=None)
mb8 = pd.read_excel('Data/microbiome/MID8.xls', 'Sheet 1', index_col=0, header=None)
mb9 = pd.read_excel('Data/microbiome/MID9.xls', 'Sheet 1', index_col=0, header=None)
# Each of these files contain two column : the name of the taxon and a counter. So we name the second column as "count" to keep the same meaning.
mb1.columns = mb2.columns = mb3.columns = mb4.columns = mb5.columns = mb6.columns = mb7.columns = mb8.columns = mb9.columns = ['Count']
# Same here for the first column by adding the name of the taxon.
mb1.index.name = mb2.index.name = mb3.index.name = mb4.index.name = mb5.index.name = mb6.index.name = mb7.index.name = mb8.index.name = mb9.index.name = 'Taxon'
# Now we'll add three columns which are defined in the metadata file : the barcode, the group and the sample type of each excel file.
dataframe = pd.concat([mb1, mb2, mb3, mb4, mb5, mb6, mb7, mb8, mb9], axis=0)
dataframe['Barcode']=['MID1']*len(mb1) + ['MID2']*len(mb2) + ['MID3']*len(mb3) + ['MID4']*len(mb4)+ ['MID5']*len(mb5)+ ['MID6']*len(mb6)+ ['MID7']*len(mb7)+ ['MID8']*len(mb8)+ ['MID9']*len(mb9) 
dataframe['Group']=['Extraction Control']*len(mb1) + ['NEC 1']*len(mb2) + ['Control 1']*len(mb3) + ['NEC 2']*len(mb4)+ ['Control 2']*len(mb5)+ ['NEC 1']*len(mb6)+ ['Control 1']*len(mb7)+ ['NEC 2']*len(mb8)+ ['Control 2']*len(mb9) 
dataframe['Sample']=['NA']*len(mb1) + ['tissue']*len(mb2) + ['tissue']*len(mb3) + ['tissue']*len(mb4)+ ['tissue']*len(mb5)+ ['stool']*len(mb6)+ ['stool']*len(mb7)+ ['stool']*len(mb8)+ ['stool']*len(mb9) 
dataframe.tail()


# In[42]:

type(dataset)


# ## Reshaping DataFrame objects
# 
# In the context of a single DataFrame, we are often interested in re-arranging the layout of our data. 

# This dataset is from Table 6.9 of [Statistical Methods for the Analysis of Repeated Measurements](http://www.amazon.com/Statistical-Methods-Analysis-Repeated-Measurements/dp/0387953701) by Charles S. Davis, pp. 161-163 (Springer, 2002). These data are from a multicenter, randomized controlled trial of botulinum toxin type B (BotB) in patients with cervical dystonia from nine U.S. sites.
# 
# * Randomized to placebo (N=36), 5000 units of BotB (N=36), 10,000 units of BotB (N=37)
# * Response variable: total score on Toronto Western Spasmodic Torticollis Rating Scale (TWSTRS), measuring severity, pain, and disability of cervical dystonia (high scores mean more impairment)
# * TWSTRS measured at baseline (week 0) and weeks 2, 4, 8, 12, 16 after treatment began

# In[ ]:

cdystonia = pd.read_csv("Data/cdystonia.csv", index_col=None)
cdystonia.head()


# This dataset includes repeated measurements of the same individuals (longitudinal data). Its possible to present such information in (at least) two ways: showing each repeated measurement in their own row, or in multiple columns representing multiple measurements.
# 

# The `stack` method rotates the data frame so that columns are represented in rows:

# In[ ]:

stacked = cdystonia.stack()
stacked


# To complement this, `unstack` pivots from rows back to columns.

# In[ ]:

stacked.unstack().head()


# For this dataset, it makes sense to create a hierarchical index based on the patient and observation:

# In[ ]:

cdystonia2 = cdystonia.set_index(['patient','obs'])
cdystonia2.head()


# In[ ]:

cdystonia2.index.is_unique


# If we want to transform this data so that repeated measurements are in columns, we can `unstack` the `twstrs` measurements according to `obs`.

# In[ ]:

twstrs_wide = cdystonia2['twstrs'].unstack('obs')
twstrs_wide.head()


# In[ ]:

cdystonia_wide = (cdystonia[['patient','site','id','treat','age','sex']]
                  .drop_duplicates()
                  .merge(twstrs_wide, right_index=True, left_on='patient', how='inner')
                  .head())
cdystonia_wide


# A slightly cleaner way of doing this is to set the patient-level information as an index before unstacking:

# In[ ]:

(cdystonia.set_index(['patient','site','id','treat','age','sex','week'])['twstrs']
     .unstack('week').head())


# To convert our "wide" format back to long, we can use the `melt` function, appropriately parameterized. This function is useful for `DataFrame`s where one
# or more columns are identifier variables (`id_vars`), with the remaining columns being measured variables (`value_vars`). The measured variables are "unpivoted" to
# the row axis, leaving just two non-identifier columns, a *variable* and its corresponding *value*, which can both be renamed using optional arguments.

# In[ ]:

pd.melt(cdystonia_wide, id_vars=['patient','site','id','treat','age','sex'], 
        var_name='obs', value_name='twsters').head()


# This illustrates the two formats for longitudinal data: **long** and **wide** formats. Its typically better to store data in long format because additional data can be included as additional rows in the database, while wide format requires that the entire database schema be altered by adding columns to every row as data are collected.
# 
# The preferable format for analysis depends entirely on what is planned for the data, so it is imporant to be able to move easily between them.

# ## Pivoting
# 
# The `pivot` method allows a DataFrame to be transformed easily between long and wide formats in the same way as a pivot table is created in a spreadsheet. It takes three arguments: `index`, `columns` and `values`, corresponding to the DataFrame index (the row headers), columns and cell values, respectively.
# 
# For example, we may want the `twstrs` variable (the response variable) in wide format according to patient, as we saw with the unstacking method above:

# In[ ]:

cdystonia.pivot(index='patient', columns='obs', values='twstrs').head()


# If we omit the `values` argument, we get a `DataFrame` with hierarchical columns, just as when we applied `unstack` to the hierarchically-indexed table:

# In[ ]:

cdystonia.pivot('patient', 'obs')


# A related method, `pivot_table`, creates a spreadsheet-like table with a hierarchical index, and allows the values of the table to be populated using an arbitrary aggregation function.

# In[ ]:

cdystonia.pivot_table(index=['site', 'treat'], columns='week', values='twstrs', 
                      aggfunc=max).head(20)


# For a simple cross-tabulation of group frequencies, the `crosstab` function (not a method) aggregates counts of data according to factors in rows and columns. The factors may be hierarchical if desired.

# In[ ]:

pd.crosstab(cdystonia.sex, cdystonia.site)


# ## Data transformation
# 
# There are a slew of additional operations for DataFrames that we would collectively refer to as "transformations" which include tasks such as removing duplicate values, replacing values, and grouping values.

# ### Dealing with duplicates
# 
# We can easily identify and remove duplicate values from `DataFrame` objects. For example, say we want to removed ships from our `vessels` dataset that have the same name:

# In[ ]:

vessels.duplicated(subset='names')


# In[ ]:

vessels.drop_duplicates(['names'])


# ### Value replacement
# 
# Frequently, we get data columns that are encoded as strings that we wish to represent numerically for the purposes of including it in a quantitative analysis. For example, consider the treatment variable in the cervical dystonia dataset:

# In[ ]:

cdystonia.treat.value_counts()


# A logical way to specify these numerically is to change them to integer values, perhaps using "Placebo" as a baseline value. If we create a dict with the original values as keys and the replacements as values, we can pass it to the `map` method to implement the changes.

# In[ ]:

treatment_map = {'Placebo': 0, '5000U': 1, '10000U': 2}


# In[ ]:

cdystonia['treatment'] = cdystonia.treat.map(treatment_map)
cdystonia.treatment


# Alternately, if we simply want to replace particular values in a `Series` or `DataFrame`, we can use the `replace` method. 
# 
# An example where replacement is useful is dealing with zeros in certain transformations. For example, if we try to take the log of a set of values:

# In[ ]:

vals = pd.Series([float(i)**10 for i in range(10)])
vals


# In[ ]:

np.log(vals)


# In such situations, we can replace the zero with a value so small that it makes no difference to the ensuing analysis. We can do this with `replace`.

# In[ ]:

vals = vals.replace(0, 1e-6)
np.log(vals)


# We can also perform the same replacement that we used `map` for with `replace`:

# In[ ]:

cdystonia2.treat.replace({'Placebo': 0, '5000U': 1, '10000U': 2})


# ### Inidcator variables
# 
# For some statistical analyses (*e.g.* regression models or analyses of variance), categorical or group variables need to be converted into columns of indicators--zeros and ones--to create a so-called **design matrix**. The Pandas function `get_dummies` (indicator variables are also known as *dummy variables*) makes this transformation straightforward.
# 
# Let's consider the DataFrame containing the ships corresponding to the transit segments on the eastern seaboard. The `type` variable denotes the class of vessel; we can create a matrix of indicators for this. For simplicity, lets filter out the 5 most common types of ships:
# 

# In[ ]:

top5 = vessels.type.isin(vessels.type.value_counts().index[:5])
top5.head(10)


# In[ ]:

vessels5 = vessels[top5]


# In[ ]:

pd.get_dummies(vessels5.type).head(10)


# ## Categorical Data
# 
# Pandas provides a convenient `dtype` for reprsenting categorical (factor) data, called `category`. 
# 
# For example, the `treat` column in the cervical dystonia dataset represents three treatment levels in a clinical trial, and is imported by default as an `object` type, since it is a mixture of string characters.

# In[ ]:

cdystonia.treat.head()


# We can convert this to a `category` type either by the `Categorical` constructor, or casting the column using `astype`:

# In[ ]:

pd.Categorical(cdystonia.treat)


# In[ ]:

cdystonia['treat'] = cdystonia.treat.astype('category')


# In[ ]:

cdystonia.treat.describe()


# By default the Categorical type represents an unordered categorical.

# In[ ]:

cdystonia.treat.cat.categories


# However, an ordering can be imposed. The order is lexical by default, but will assume the order of the listed categories to be the desired order.

# In[ ]:

cdystonia.treat.cat.categories = ['Placebo', '5000U', '10000U']


# In[ ]:

cdystonia.treat.cat.as_ordered().head()


# The important difference between the `category` type and the `object` type is that `category` is represented by an underlying array of integers, which is then mapped to character labels.

# In[ ]:

cdystonia.treat.cat.codes


# Notice that these are 8-bit integers, which are essentially single bytes of data, making memory usage lower.
# 
# There is also a performance benefit. Consider an operation such as calculating the total segment lengths for each ship in the `segments` table (this is also a preview of pandas' `groupby` operation!):

# In[ ]:

get_ipython().magic('time segments.groupby(segments.name).seg_length.sum().sort_values(ascending=False, inplace=False).head()')


# In[ ]:

segments['name'] = segments.name.astype('category')


# In[ ]:

get_ipython().magic('time segments.groupby(segments.name).seg_length.sum().sort_values(ascending=False, inplace=False).head()')


# Hence, we get a considerable speedup simply by using the appropriate `dtype` for our data.

# ### Discretization
# 
# Pandas' `cut` function can be used to group continuous or countable data in to bins. Discretization is generally a very **bad idea** for statistical analysis, so use this function responsibly!
# 
# Lets say we want to bin the ages of the cervical dystonia patients into a smaller number of groups:

# In[ ]:

cdystonia.age.describe()


# Let's transform these data into decades, beginnnig with individuals in their 20's and ending with those in their 80's:

# In[ ]:

pd.cut(cdystonia.age, [20,30,40,50,60,70,80,90])[:30]


# The parentheses indicate an open interval, meaning that the interval includes values up to but *not including* the endpoint, whereas the square bracket is a closed interval, where the endpoint is included in the interval. We can switch the closure to the left side by setting the `right` flag to `False`:

# In[ ]:

pd.cut(cdystonia.age, [20,30,40,50,60,70,80,90], right=False)[:30]


# Since the data are now **ordinal**, rather than numeric, we can give them labels:

# In[ ]:

pd.cut(cdystonia.age, [20,40,60,80,90], labels=['young','middle-aged','old','really old'])[:30]


# A related function `qcut` uses empirical quantiles to divide the data. If, for example, we want the quartiles -- (0-25%], (25-50%], (50-70%], (75-100%] -- we can just specify 4 intervals, which will be equally-spaced by default:

# In[ ]:

pd.qcut(cdystonia.age, 4)[:30]


# Alternatively, one can specify custom quantiles to act as cut points:

# In[ ]:

quantiles = pd.qcut(segments.seg_length, [0, 0.01, 0.05, 0.95, 0.99, 1])
quantiles[:30]


# Note that you can easily combine discretiztion with the generation of indicator variables shown above:

# In[ ]:

pd.get_dummies(quantiles).head(10)


# ### Permutation and sampling
# 
# For some data analysis tasks, such as simulation, we need to be able to randomly reorder our data, or draw random values from it. Calling NumPy's `permutation` function with the length of the sequence you want to permute generates an array with a permuted sequence of integers, which can be used to re-order the sequence.

# In[ ]:

new_order = np.random.permutation(len(segments))
new_order[:30]


# Using this sequence as an argument to the `take` method results in a reordered DataFrame:

# In[ ]:

segments.take(new_order).head()


# Compare this ordering with the original:

# In[ ]:

segments.head()


# For random sampling, `DataFrame` and `Series` objects have a `sample` method that can be used to draw samples, with or without replacement:

# In[ ]:

vessels.sample(n=10)


# In[ ]:

vessels.sample(n=10, replace=True)


# ## Data aggregation and GroupBy operations
# 
# One of the most powerful features of Pandas is its **GroupBy** functionality. On occasion we may want to perform operations on *groups* of observations within a dataset. For exmaple:
# 
# * **aggregation**, such as computing the sum of mean of each group, which involves applying a function to each group and returning the aggregated results
# * **slicing** the DataFrame into groups and then doing something with the resulting slices (*e.g.* plotting)
# * group-wise **transformation**, such as standardization/normalization

# In[45]:

cdystonia_grouped = cdystonia.groupby(cdystonia.patient)


# This *grouped* dataset is hard to visualize
# 
# 

# In[ ]:

cdystonia_grouped


# However, the grouping is only an intermediate step; for example, we may want to **iterate** over each of the patient groups:

# In[ ]:

for patient, group in cdystonia_grouped:
    print('patient', patient)
    print('group', group)


# A common data analysis procedure is the **split-apply-combine** operation, which groups subsets of data together, applies a function to each of the groups, then recombines them into a new data table.
# 
# For example, we may want to aggregate our data with with some function.
# 
# ![split-apply-combine](http://f.cl.ly/items/0s0Z252j0X0c3k3P1M47/Screen%20Shot%202013-06-02%20at%203.04.04%20PM.png)
# 
# <div align="right">*(figure taken from "Python for Data Analysis", p.251)*</div>

# We can aggregate in Pandas using the `aggregate` (or `agg`, for short) method:

# In[ ]:

cdystonia_grouped.agg(np.mean).head()


# Notice that the `treat` and `sex` variables are not included in the aggregation. Since it does not make sense to aggregate non-string variables, these columns are simply ignored by the method.
# 
# Some aggregation functions are so common that Pandas has a convenience method for them, such as `mean`:

# In[ ]:

cdystonia_grouped.mean().head()


# The `add_prefix` and `add_suffix` methods can be used to give the columns of the resulting table labels that reflect the transformation:

# In[ ]:

cdystonia_grouped.mean().add_suffix('_mean').head()


# In[ ]:

# The median of the `twstrs` variable
cdystonia_grouped['twstrs'].quantile(0.5)


# If we wish, we can easily aggregate according to multiple keys:

# In[ ]:

cdystonia.groupby(['week','site']).mean().head()


# Alternately, we can **transform** the data, using a function of our choice with the `transform` method:

# In[ ]:

normalize = lambda x: (x - x.mean())/x.std()

cdystonia_grouped.transform(normalize).head()


# It is easy to do column selection within `groupby` operations, if we are only interested split-apply-combine operations on a subset of columns:

# In[ ]:

cdystonia_grouped['twstrs'].mean().head()


# In[ ]:

# This gives the same result as a DataFrame
cdystonia_grouped[['twstrs']].mean().head()


# If you simply want to divide your DataFrame into chunks for later use, its easy to convert them into a dict so that they can be easily indexed out as needed:

# In[ ]:

chunks = dict(list(cdystonia_grouped))


# In[ ]:

chunks[4]


# By default, `groupby` groups by row, but we can specify the `axis` argument to change this. For example, we can group our columns by `dtype` this way:

# In[ ]:

grouped_by_type = cdystonia.groupby(cdystonia.dtypes, axis=1)
{g:grouped_by_type.get_group(g) for g in grouped_by_type.groups}


# Its also possible to group by one or more levels of a hierarchical index. Recall `cdystonia2`, which we created with a hierarchical index:

# In[ ]:

cdystonia2.head(10)


# In[ ]:

cdystonia2.groupby(level='obs', axis=0)['twstrs'].mean()


# ### Apply
# 
# We can generalize the split-apply-combine methodology by using `apply` function. This allows us to invoke any function we wish on a grouped dataset and recombine them into a DataFrame.

# The function below takes a DataFrame and a column name, sorts by the column, and takes the `n` largest values of that column. We can use this with `apply` to return the largest values from every group in a DataFrame in a single call. 

# In[ ]:

def top(df, column, n=5):
    return df.sort_values(by=column, ascending=False)[:n]


# To see this in action, consider the vessel transit segments dataset (which we merged with the vessel information to yield `segments_merged`). Say we wanted to return the 3 longest segments travelled by each ship:

# In[ ]:

top3segments = segments_merged.groupby('mmsi').apply(top, column='seg_length', n=3)[['names', 'seg_length']]
top3segments.head(15)


# Notice that additional arguments for the applied function can be passed via `apply` after the function name. It assumes that the DataFrame is the first argument.

# Recall the microbiome data sets that we used previously for the concatenation example. Suppose that we wish to aggregate the data at a higher biological classification than genus. For example, we can identify samples down to *class*, which is the 3rd level of organization in each index.

# In[ ]:

mb1.index[:3]


# Using the string methods `split` and `join` we can create an index that just uses the first three classifications: domain, phylum and class.

# In[ ]:

class_index = mb1.index.map(lambda x: ' '.join(x.split(' ')[:3]))


# In[ ]:

mb_class = mb1.copy()
mb_class.index = class_index


# However, since there are multiple taxonomic units with the same class, our index is no longer unique:

# In[ ]:

mb_class.head()


# We can re-establish a unique index by summing all rows with the same class, using `groupby`:

# In[ ]:

mb_class.groupby(level=0).sum().head(10)


# ## Exercise 2
# 
# Load the dataset in `titanic.xls`. It contains data on all the passengers that travelled on the Titanic.

# In[44]:

from IPython.core.display import HTML
HTML(filename='Data/titanic.html')


# In[125]:

#import titanic data file
titanic = pd.read_excel("Data/titanic.xls", index_col=None)
titanic.head()


# In[126]:

# turn "sex" attribute into numerical attribute
# 0 = male ; 1= female

sex_map = {'male': 0, 'female': 1}
titanic['sex'] = titanic.sex.map(sex_map)
titanic.head()


# In[127]:

# clean duplicate values
titanic_2 = titanic.drop_duplicates(['name'])


# In[128]:

# convert attributes to categorical data
pd.Categorical(titanic_2.pclass)
pd.Categorical(titanic_2.survived)
pd.Categorical(titanic_2.sex)
pd.Categorical(titanic_2.age)
pd.Categorical(titanic_2.sibsp)
pd.Categorical(titanic_2.parch)
pd.Categorical(titanic_2.ticket)
pd.Categorical(titanic_2.fare)
pd.Categorical(titanic_2.cabin)
pd.Categorical(titanic_2.embarked)
pd.Categorical(titanic_2.boat)
pd.Categorical(titanic_2.body)


# In[129]:

titanic_2


# In[114]:

# describe passenger class
pclasses = titanic_2.pclass.value_counts()
class1 = (pclasses[1]/1307)*100
class2 = (pclasses[2]/1307)*100
class3 = (pclasses[3]/1307)*100
d = {'1st Class' : class1, '2nd Class' : class2, '3rdclass' : class3}
pd.Series(d)
#24% of passengers travelled 1st class, 21% travelled in 2nd class and 54% travelled in 3rd class


# In[130]:

# plot classes 1 = 1st 2 = 2nd and 3 = 3rd
pclasses.plot.pie() 


# In[131]:

# describe passenger survival
survivals = titanic_2.survived.value_counts()
survived = (survivals[1]/1307)*100
survived
# 38.25% of passengers survived


# In[132]:

# plot survivals 0 = death & 1 = survival
survivals.plot.pie() 


# In[133]:

# describe passenger sex
sex = titanic_2.sex.value_counts()
sex
male_ratio = (sex[1]/1307)*100
male_ratio
# results show that 35% of passengers are male and 65% are female


# In[134]:

# plot gender distribution 0 = male & 1 = female
sex.plot.pie() 


# In[135]:

# calculate proportions of port of embarcation S = Southtampton & C = Cherbourg & Q = Queenstown
port = titanic_2.embarked.value_counts()
S = (port[0]/1307)*100
C = (port[1]/1307)*100
Q = (port[2]/1307)*100
d = {'S' : S, 'C' : C, 'Q' : Q}
pd.Series(d)
# 20.6% of passengers boarded in C, 9.4% boarded in Q and 69.7% boarded in S.


# In[136]:

# plot gender distribution 0 = male & 1 = female
port.plot.pie() 


# In[141]:

# describe passenger age
# assumption - dropping all NaN values and including values of estimated ages
titanic_2age = titanic_2.age.dropna()
titanic_2age.describe()
# results show that mean age was 29.86 y.o. 
# min age was 0.16y.o. and max was 80 y.o. 
# 25% of passengers under 21, 50% under 28, 75% under 39 y.o.


# In[143]:

# show distribution of ages on board
titanic_2age.plot.hist(bins=50) 


# In[144]:

# describe passenger fare
# assumption - dropping all NaN values 
titanic_2fare = titanic_2.fare.dropna()
titanic_2fare.describe()
# results show that mean fare was  33 
# min fare was 0 and max was 512 
# 25% of passengers paid under 7.9, 50% under 14.5, 75% under 31.27


# In[148]:

# show distribution of fares on board
titanic_2fare.plot.hist(bins=50) 
# majority of fares under 100 with few outliers 


# In[149]:

# description of statistics on # of siblings and spouses on board
# assumption - dropping all NaN values and include values which are 0
titanic_2sibsp = titanic_2.sibsp.dropna()
titanic_2sibsp.describe()
# results show that mean # of sibsp was 0.49 siblings or spouses aboard 
# min number of siblings or spouses was 0 and max was 8 
# 75% of passengers had less than 1 sibling or spouse aboard, indicating outliers above 1


# In[150]:

# show distribution of # of siblings and spouses on board
titanic_2sibsp.plot.hist(bins=50) 


# In[151]:

# description of statistics on # of parents and children on board
# assumption - dropping all NaN values and include values which are 0
titanic_2parch = titanic_2.parch.dropna()
titanic_2parch.describe()
# results show that mean # of parch was 0.38 parents or children aboard 
# min number of parents or children was 0 and max was 9
# 75% of passengers had less or equal to 0 parents or children aboard, indicating many outliers in the data


# In[152]:

# show distribution of # of siblings and spouses on board
titanic_2parch.plot.hist(bins=50) 


# Women and children first?
# 
# 1. Describe each attribute, both with basic statistics and plots. State clearly your assumptions and discuss your findings.
# 2. Use the `groupby` method to calculate the proportion of passengers that survived by sex.
# 3. Calculate the same proportion, but by class and sex.
# 4. Create age categories: children (under 14 years), adolescents (14-20), adult (21-64), and senior(65+), and calculate survival proportions by age category, class and sex.

# In[160]:

# Part 2
# Using Groupby to find ratio of survival by sex
sex_survival = titanic.groupby(titanic.survived).sex.value_counts()
sex_survival


# In[161]:

# survivers gender profile calculation
surv_tot = sex_survival[1].sum() # calculate total number of survivors
fem_surv = (sex_survival[1,1]/surv_tot)*100 # calculate proportion of survived females
male_surv = (sex_survival[1,0]/surv_tot)*100 # calculate proportion of survived males
out2 = {'Male Survivors' : male_surv , 'Female Survivors' : fem_surv,} # display outputs simultaneously
pd.Series(out2)
# 67.8% of survivors were female and 32.2% were male


# In[201]:

# Part 3
# Using Groupby to find ratio of survival by sex and class
# table outputs raw numbers, but not proportions
sex_class = titanic_2.groupby(['survived','sex']).pclass.value_counts()
sex_class


# In[249]:

# survivers gender + class profile calculation
data = pd.DataFrame(sex_class) # turn into data set
surv_tot = sex_class[1].sum() # calculate total number of survivors
data['proportion of survived'] = (data/nsurv_tot)*100 #add column of proportion of survivors
# this column refers to the percentage of people that survived/ did not survived that belong to each category (e.g. percntage of non survivors that were females in second class)
data.loc[1]
# the table below only shows proportions of different categories of people among survivors


# In[219]:

# Part 4
# Create Age Categories
# Assumption: Dropped all NaNs
age_group = pd.cut(titanic_2.age, [0,14,20,64,100], labels=['children','adolescents','adult','seniors']) # create age categories
titanic_2['age_group'] = age_group #add column of age group to main dataframe
sex_class_age = titanic_2.groupby(['survived','sex', 'pclass']).age_group.value_counts() #find counts for different combinations of age group, sex and class
sex_class_age


# In[251]:

# survivers gender + class + age group profile calculation
data = pd.DataFrame(sex_class_age) # turn into data set
surv_tot = sex_class_age[1].sum() # calculate total number of survivors
data['proportion of survivors'] = (data/surv_tot)*100 #add column of proportion
# this column refers to the percentage of people that survived/ did not survive that belong to each category (e.g. percntage of survivors that were old males in first class
data.loc[1]
# the table below shows proportions of survivals belonging to different categories


# ## References
# 
# [Python for Data Analysis](http://shop.oreilly.com/product/0636920023784.do) Wes McKinney
