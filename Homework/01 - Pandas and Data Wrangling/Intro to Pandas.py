
# coding: utf-8

# # Table of Contents
#  <p><div class="lev1"><a href="#Introduction-to-Pandas"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction to Pandas</a></div><div class="lev2"><a href="#Pandas-Data-Structures"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Pandas Data Structures</a></div><div class="lev3"><a href="#Series"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Series</a></div><div class="lev3"><a href="#DataFrame"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>DataFrame</a></div><div class="lev3"><a href="#Exercise-1"><span class="toc-item-num">1.1.3&nbsp;&nbsp;</span>Exercise 1</a></div><div class="lev3"><a href="#Exercise-2"><span class="toc-item-num">1.1.4&nbsp;&nbsp;</span>Exercise 2</a></div><div class="lev2"><a href="#Importing-data"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Importing data</a></div><div class="lev3"><a href="#Microsoft-Excel"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Microsoft Excel</a></div><div class="lev2"><a href="#Pandas-Fundamentals"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Pandas Fundamentals</a></div><div class="lev3"><a href="#Manipulating-indices"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Manipulating indices</a></div><div class="lev2"><a href="#Indexing-and-Selection"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Indexing and Selection</a></div><div class="lev3"><a href="#Exercise-3"><span class="toc-item-num">1.4.1&nbsp;&nbsp;</span>Exercise 3</a></div><div class="lev2"><a href="#Operations"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Operations</a></div><div class="lev2"><a href="#Sorting-and-Ranking"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Sorting and Ranking</a></div><div class="lev3"><a href="#Exercise-4"><span class="toc-item-num">1.6.1&nbsp;&nbsp;</span>Exercise 4</a></div><div class="lev2"><a href="#Hierarchical-indexing"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Hierarchical indexing</a></div><div class="lev2"><a href="#Missing-data"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>Missing data</a></div><div class="lev3"><a href="#Exercise-5"><span class="toc-item-num">1.8.1&nbsp;&nbsp;</span>Exercise 5</a></div><div class="lev2"><a href="#Data-summarization"><span class="toc-item-num">1.9&nbsp;&nbsp;</span>Data summarization</a></div><div class="lev2"><a href="#Writing-Data-to-Files"><span class="toc-item-num">1.10&nbsp;&nbsp;</span>Writing Data to Files</a></div><div class="lev3"><a href="#Advanced-Exercise:-Compiling-Ebola-Data"><span class="toc-item-num">1.10.1&nbsp;&nbsp;</span>Advanced Exercise: Compiling Ebola Data</a></div><div class="lev2"><a href="#References"><span class="toc-item-num">1.11&nbsp;&nbsp;</span>References</a></div>

# # Introduction to Pandas
# 
# **pandas** is a Python package providing fast, flexible, and expressive data structures designed to work with *relational* or *labeled* data both. It is a fundamental high-level building block for doing practical, real world data analysis in Python. 
# 
# pandas is well suited for:
# 
# - Tabular data with heterogeneously-typed columns, as in an SQL table or Excel spreadsheet
# - Ordered and unordered (not necessarily fixed-frequency) time series data.
# - Arbitrary matrix data (homogeneously typed or heterogeneous) with row and column labels
# - Any other form of observational / statistical data sets. The data actually need not be labeled at all to be placed into a pandas data structure
# 
# 
# Key features:
#     
# - Easy handling of **missing data**
# - **Size mutability**: columns can be inserted and deleted from DataFrame and higher dimensional objects
# - Automatic and explicit **data alignment**: objects can be explicitly aligned to a set of labels, or the data can be aligned automatically
# - Powerful, flexible **group by functionality** to perform split-apply-combine operations on data sets
# - Intelligent label-based **slicing, fancy indexing, and subsetting** of large data sets
# - Intuitive **merging and joining** data sets
# - Flexible **reshaping and pivoting** of data sets
# - **Hierarchical labeling** of axes
# - Robust **IO tools** for loading data from flat files, Excel files, databases, and HDF5
# - **Time series functionality**: date range generation and frequency conversion, moving window statistics, moving window linear regressions, date shifting and lagging, etc.

# In[49]:

import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


# ## Pandas Data Structures

# ### Series
# 
# A **Series** is a single vector of data (like a NumPy array) with an *index* that labels each element in the vector.

# In[50]:

counts = pd.Series([632, 1638, 569, 115])
counts


# If an index is not specified, a default sequence of integers is assigned as the index. A NumPy array comprises the values of the `Series`, while the index is a pandas `Index` object.

# In[51]:

counts.values


# In[52]:

counts.index


# We can assign meaningful labels to the index, if they are available:

# In[53]:

bacteria = pd.Series([632, 1638, 569, 115], 
    index=['Firmicutes', 'Proteobacteria', 'Actinobacteria', 'Bacteroidetes'])

bacteria


# These labels can be used to refer to the values in the `Series`.

# In[54]:

bacteria['Actinobacteria']


# In[55]:

bacteria


# In[56]:

bacteria[[name.endswith('bacteria') for name in bacteria.index]]


# In[57]:

[name.endswith('bacteria') for name in bacteria.index]


# Notice that the indexing operation preserved the association between the values and the corresponding indices.
# 
# We can still use positional indexing if we wish.

# In[58]:

bacteria[0]


# We can give both the array of values and the index meaningful labels themselves:

# In[59]:

bacteria.name = 'counts'
bacteria.index.name = 'phylum'
bacteria


# NumPy's math functions and other operations can be applied to Series without losing the data structure.

# In[60]:

np.log(bacteria)


# We can also filter according to the values in the `Series`:

# In[61]:

bacteria[bacteria>1000]


# A `Series` can be thought of as an ordered key-value store. In fact, we can create one from a `dict`:

# In[62]:

bacteria_dict = {'Firmicutes': 632, 'Proteobacteria': 1638, 'Actinobacteria': 569,
                 'Bacteroidetes': 115}
pd.Series(bacteria_dict)


# Notice that the `Series` is created in key-sorted order.
# 
# If we pass a custom index to `Series`, it will select the corresponding values from the dict, and treat indices without corrsponding values as missing. Pandas uses the `NaN` (not a number) type for missing values.

# In[63]:

bacteria2 = pd.Series(bacteria_dict, 
                      index=['Cyanobacteria','Firmicutes',
                             'Proteobacteria','Actinobacteria'])
bacteria2


# In[64]:

bacteria2.isnull()


# Critically, the labels are used to **align data** when used in operations with other Series objects:

# In[65]:

bacteria + bacteria2


# Contrast this with NumPy arrays, where arrays of the same length will combine values element-wise; adding Series combined values with the same label in the resulting series. Notice also that the missing values were propogated by addition.

# ### DataFrame
# 
# Inevitably, we want to be able to store, view and manipulate data that is *multivariate*, where for every index there are multiple fields or columns of data, often of varying data type.
# 
# A `DataFrame` is a tabular data structure, encapsulating multiple series like columns in a spreadsheet. Data are stored internally as a 2-dimensional object, but the `DataFrame` allows us to represent and manipulate higher-dimensional data.

# In[66]:

data = pd.DataFrame({'value':[623, 1638, 569, 115, 433, 1130, 754, 555],
                     'patient':[1, 1, 1, 1, 2, 2, 2, 2],
                     'phylum':['Firmicutes', 'Proteobacteria', 'Actinobacteria', 
    'Bacteroidetes', 'Firmicutes', 'Proteobacteria', 'Actinobacteria', 'Bacteroidetes']})
data


# Notice the `DataFrame` is sorted by column name. We can change the order by indexing them in the order we desire:

# In[67]:

data[['phylum','value','patient']]


# A `DataFrame` has a second index, representing the columns:

# In[68]:

data.columns


# The `dtypes` attribute reveals the data type for each column in our DataFrame. 
# 
# - `int64` is numeric integer values 
# - `object` strings (letters and numbers)
# - `float64` floating-point values

# In[69]:

data.dtypes


# If we wish to access columns, we can do so either by dict-like indexing or by attribute:

# In[70]:

data['patient']


# In[71]:

data.patient


# In[72]:

type(data.value)


# In[73]:

data[['value']]


# Notice this is different than with `Series`, where dict-like indexing retrieved a particular element (row). 
# 
# If we want access to a row in a `DataFrame`, we index its `loc` attribute.

# In[74]:

data.loc[0]


# ### Exercise 1
# 
# Try out these commands to see what they return:
# 
# - `data.head()`
# - `data.tail(3)`
# - `data.shape`

# In[75]:

data.head()


# data.head shows all of the data up to a certain number, if it is indicated in the parantheses

# In[76]:

data.tail(3)


# this shows the last 3 rows of data of the data row

# In[77]:

data.shape


# this gives you the number of rows of data (8) and columns (3)

# An alternative way of initializing a `DataFrame` is with a list of dicts:

# In[78]:

data = pd.DataFrame([{'patient': 1, 'phylum': 'Firmicutes', 'value': 632},
                    {'patient': 1, 'phylum': 'Proteobacteria', 'value': 1638},
                    {'patient': 1, 'phylum': 'Actinobacteria', 'value': 569},
                    {'patient': 1, 'phylum': 'Bacteroidetes', 'value': 115},
                    {'patient': 2, 'phylum': 'Firmicutes', 'value': 433},
                    {'patient': 2, 'phylum': 'Proteobacteria', 'value': 1130},
                    {'patient': 2, 'phylum': 'Actinobacteria', 'value': 754},
                    {'patient': 2, 'phylum': 'Bacteroidetes', 'value': 555}])


# In[79]:

data


# Its important to note that the Series returned when a DataFrame is indexted is merely a **view** on the DataFrame, and not a copy of the data itself. So you must be cautious when manipulating this data:

# In[80]:

vals = data.value
vals


# In[81]:

vals[5] = 0
vals


# If we plan on modifying an extracted Series, its a good idea to make a copy.

# In[82]:

vals = data.value.copy()
vals[5] = 1000
vals


# We can create or modify columns by assignment:

# In[83]:

data.value[3,4,5,6] = [14, 21, 1130,5]
data
type(data)


# In[84]:

data['year'] = 2013
data


# But note, we cannot use the attribute indexing method to add a new column:

# In[85]:

data.treatment = 1
data


# In[86]:

data.treatment


# ### Exercise 2
# 
# From the `data` table above, create an index to return all rows for which the phylum name ends in "bacteria" and the value is greater than 1000.

# In[87]:

# get all of the values from the data where the phylum name ends with bacteria
data[[phylum.endswith('bacteria') for phylum in data.phylum]]
# take all of the rows where the value which are above 1000
data[data.value>1000]


# In[88]:

data
data.phylum


# Specifying a `Series` as a new columns cause its values to be added according to the `DataFrame`'s index:

# In[89]:

treatment = pd.Series([0]*4 + [1]*2)
treatment


# In[90]:

data['treatment'] = treatment
data


# Other Python data structures (ones without an index) need to be the same length as the `DataFrame`:

# In[91]:

month = ['Jan', 'Feb', 'Mar', 'Apr']
data['month'] = month


# In[ ]:

data['month'] = ['Jan']*len(data)
data


# We can use the `drop` method to remove rows or columns, which by default drops rows. We can be explicit by using the `axis` argument:

# In[ ]:

data_nomonth = data.drop('month', axis=1)
data_nomonth


# We can extract the underlying data as a simple `ndarray` by accessing the `values` attribute:

# In[ ]:

data.values


# Notice that because of the mix of string and integer (and `NaN`) values, the dtype of the array is `object`. The dtype will automatically be chosen to be as general as needed to accomodate all the columns.

# In[ ]:

df = pd.DataFrame({'foo': [1,2,3], 'bar':[0.4, -1.0, 4.5]})
df.values


# Pandas uses a custom data structure to represent the indices of Series and DataFrames.

# In[ ]:

data.index


# Index objects are immutable:

# In[ ]:

data.index[0] = 15


# This is so that Index objects can be shared between data structures without fear that they will be changed.

# In[ ]:

bacteria2.index = bacteria.index


# In[ ]:

bacteria2


# ## Importing data

# A key, but often under-appreciated, step in data analysis is importing the data that we wish to analyze. Though it is easy to load basic data structures into Python using built-in tools or those provided by packages like NumPy, it is non-trivial to import structured data well, and to easily convert this input into a robust data structure:
# 
#     genes = np.loadtxt("genes.csv", delimiter=",", dtype=[('gene', '|S10'), ('value', '<f4')])
# 
# Pandas provides a convenient set of functions for importing tabular data in a number of formats directly into a `DataFrame` object. These functions include a slew of options to perform type inference, indexing, parsing, iterating and cleaning automatically as data are imported.

# Let's start with some more bacteria data, stored in csv format.

# In[ ]:

get_ipython().system('cat Data/microbiome.csv')


# This table can be read into a DataFrame using `read_csv`:

# In[ ]:

mb = pd.read_csv("data/microbiome.csv")
mb


# Notice that `read_csv` automatically considered the first row in the file to be a header row.
# 
# We can override default behavior by customizing some the arguments, like `header`, `names` or `index_col`.

# In[ ]:

pd.read_csv("Data/microbiome.csv", header=None).head()


# `read_csv` is just a convenience function for `read_table`, since csv is such a common format:

# In[ ]:

mb = pd.read_table("Data/microbiome.csv", sep=',')


# The `sep` argument can be customized as needed to accomodate arbitrary separators. For example, we can use a regular expression to define a variable amount of whitespace, which is unfortunately very common in some data formats: 
#     
#     sep='\s+'

# For a more useful index, we can specify the first two columns, which together provide a unique index to the data.

# In[ ]:

mb = pd.read_csv("Data/microbiome.csv", index_col=['Patient','Taxon'])
mb.head(5)


# This is called a *hierarchical* index, which we will revisit later in the section.

# If we have sections of data that we do not wish to import (for example, known bad data), we can populate the `skiprows` argument:

# In[ ]:

pd.read_csv("Data/microbiome.csv", skiprows=[3,4,6]).head()


# If we only want to import a small number of rows from, say, a very large data file we can use `nrows`:

# In[ ]:

pd.read_csv("Data/microbiome.csv", nrows=4)


# Alternately, if we want to process our data in reasonable chunks, the `chunksize` argument will return an iterable object that can be employed in a data processing loop. For example, our microbiome data are organized by bacterial phylum, with 14 patients represented in each:

# In[ ]:

pd.read_csv("Data/microbiome.csv", chunksize=14)


# In[ ]:

data_chunks = pd.read_csv("Data/microbiome.csv", chunksize=14)

mean_tissue = pd.Series({chunk.Taxon[0]: chunk.Tissue.mean() for chunk in data_chunks})
    
mean_tissue


# Most real-world data is incomplete, with values missing due to incomplete observation, data entry or transcription error, or other reasons. Pandas will automatically recognize and parse common missing data indicators, including `NA` and `NULL`.

# In[ ]:

get_ipython().system('cat Data/microbiome_missing.csv')


# In[ ]:

pd.read_csv("Data/microbiome_missing.csv").head(20)


# Above, Pandas recognized `NA` and an empty field as missing data.

# In[ ]:

pd.isnull(pd.read_csv("Data/microbiome_missing.csv")).head(20)


# Unfortunately, there will sometimes be inconsistency with the conventions for missing data. In this example, there is a question mark "?" and a large negative number where there should have been a positive integer. We can specify additional symbols with the `na_values` argument:
#    

# In[ ]:

pd.read_csv("Data/microbiome_missing.csv", na_values=['?', -99999]).head(20)


# These can be specified on a column-wise basis using an appropriate dict as the argument for `na_values`.

# ### Microsoft Excel
# 
# Since so much financial and scientific data ends up in Excel spreadsheets (regrettably), Pandas' ability to directly import Excel spreadsheets is valuable. This support is contingent on having one or two dependencies (depending on what version of Excel file is being imported) installed: `xlrd` and `openpyxl` (these may be installed with either `pip` or `easy_install`).
# 
# The read_excel convenience function in pandas imports a specific sheet from an Excel file

# In[ ]:

mb = pd.read_excel('Data/microbiome/MID2.xls', sheetname='Sheet 1', header=None)
mb.head()


# There are several other data formats that can be imported into Python and converted into DataFrames, with the help of buitl-in or third-party libraries. These include JSON, XML, HDF5, relational and non-relational databases, and various web APIs. These are beyond the scope of this tutorial, but are covered in [Python for Data Analysis](http://shop.oreilly.com/product/0636920023784.do).

# ## Pandas Fundamentals

# This section introduces the new user to the key functionality of Pandas that is required to use the software effectively.
# 
# For some variety, we will leave our digestive tract bacteria behind and employ some baseball data.

# In[93]:

baseball = pd.read_csv("Data/baseball.csv", index_col='id')
baseball.head()


# In[ ]:




# Notice that we specified the `id` column as the index, since it appears to be a unique identifier. We could try to create a unique index ourselves by combining `player` and `year`:

# In[94]:

player_id = baseball.player + baseball.year.astype(str)
baseball_newind = baseball.copy()
baseball_newind.index = player_id
baseball_newind.head()


# This looks okay, but let's check:

# In[95]:

baseball_newind.index.is_unique


# So, indices need not be unique. Our choice is not unique because some players change teams within years.

# In[96]:

pd.Series(baseball_newind.index).value_counts()


# The most important consequence of a non-unique index is that indexing by label will return multiple values for some labels:

# In[97]:

baseball_newind.loc['wickmbo012007']


# We will learn more about indexing below.

# We can create a truly unique index by combining `player`, `team` and `year`:

# In[98]:

player_unique = baseball.player + baseball.team + baseball.year.astype(str)
baseball_newind = baseball.copy()
baseball_newind.index = player_unique
baseball_newind.head()


# In[ ]:

baseball_newind.index.is_unique


# We can create meaningful indices more easily using a hierarchical index; for now, we will stick with the numeric `id` field as our index.

# ### Manipulating indices
# 
# **Reindexing** allows users to manipulate the data labels in a DataFrame. It forces a DataFrame to conform to the new index, and optionally, fill in missing data if requested.
# 
# A simple use of `reindex` is to alter the order of the rows:

# In[ ]:

baseball.reindex(baseball.index[::-1]).head()


# Notice that the `id` index is not sequential. Say we wanted to populate the table with every `id` value. We could specify and index that is a sequence from the first to the last `id` numbers in the database, and Pandas would fill in the missing data with `NaN` values:

# In[ ]:

id_range = range(baseball.index.values.min(), baseball.index.values.max())
baseball.reindex(id_range).head()


# Missing values can be filled as desired, either with selected values, or by rule:

# In[ ]:

baseball.reindex(id_range, method='ffill', columns=['player','year']).head()


# In[ ]:

baseball.reindex(id_range, fill_value='charliebrown', columns=['player']).head()


# Keep in mind that `reindex` does not work if we pass a non-unique index series.

# We can remove rows or columns via the `drop` method:

# In[ ]:

baseball.shape


# In[ ]:

baseball.drop([89525, 89526])


# In[99]:

baseball.drop(['ibb','hbp'], axis=1)


# ## Indexing and Selection
# 
# Indexing works analogously to indexing in NumPy arrays, except we can use the labels in the `Index` object to extract values in addition to arrays of integers.

# In[100]:

# Sample Series object
hits = baseball_newind.h
hits


# In[ ]:

# Numpy-style indexing
hits[:3]


# In[ ]:

# Indexing by label
hits[['womacto01CHN2006','schilcu01BOS2006']]


# We can also slice with data labels, since they have an intrinsic order within the Index:

# In[ ]:

hits['womacto01CHN2006':'gonzalu01ARI2006']


# In[ ]:

hits['womacto01CHN2006':'gonzalu01ARI2006'] = 5
hits


# In a `DataFrame` we can slice along either or both axes:

# In[ ]:

baseball_newind[['h','ab']]


# In[ ]:

baseball_newind[baseball_newind.ab>500]


# For a more concise (and readable) syntax, we can use the new `query` method to perform selection on a `DataFrame`. Instead of having to type the fully-specified column, we can simply pass a string that describes what to select. The query above is then simply:

# In[ ]:

baseball_newind.query('ab > 500')


# The `DataFrame.index` and `DataFrame.columns` are placed in the query namespace by default. If you want to refer to a variable in the current namespace, you can prefix the variable with `@`:

# In[ ]:

min_ab = 450


# In[ ]:

baseball_newind.query('ab > @min_ab')


# The indexing field `loc` allows us to select subsets of rows and columns in an intuitive way:

# In[ ]:

baseball_newind.loc['gonzalu01ARI2006', ['h','X2b', 'X3b', 'hr']]


# In[ ]:

baseball_newind.loc[:'myersmi01NYA2006', 'hr']


# In addition to using `loc` to select rows and columns by **label**, pandas also allows indexing by **position** using the `iloc` attribute.
# 
# So, we can query rows and columns by absolute position, rather than by name:

# In[ ]:

baseball_newind.iloc[:5, 5:8]


# ### Exercise 3
# 
# You can use the `isin` method query a DataFrame based upon a list of values as follows: 
# 
#     data['phylum'].isin(['Firmacutes', 'Bacteroidetes'])
# 
# Use `isin` to find all players that played for the Los Angeles Dodgers (LAN) or the San Francisco Giants (SFN). How many records contain these values?

# In[101]:

baseball_newind[baseball_newind['team'].isin(['LAN','SFN'])]
#there are 15 players who are either LAN or SFN


# ## Operations
# 
# `DataFrame` and `Series` objects allow for several operations to take place either on a single object, or between two or more objects.
# 
# For example, we can perform arithmetic on the elements of two objects, such as combining baseball statistics across years. First, let's (artificially) construct two Series, consisting of home runs hit in years 2006 and 2007, respectively:

# In[102]:

hr2006 = baseball.loc[baseball.year==2006, 'hr']
hr2006.index = baseball.player[baseball.year==2006]

hr2007 = baseball.loc[baseball.year==2007, 'hr']
hr2007.index = baseball.player[baseball.year==2007]


# In[103]:

hr2007


# Now, let's add them together, in hopes of getting 2-year home run totals:

# In[104]:

hr_total = hr2006 + hr2007
hr_total


# Pandas' data alignment places `NaN` values for labels that do not overlap in the two Series. In fact, there are only 6 players that occur in both years.

# In[105]:

hr_total[hr_total.notnull()]


# While we do want the operation to honor the data labels in this way, we probably do not want the missing values to be filled with `NaN`. We can use the `add` method to calculate player home run totals by using the `fill_value` argument to insert a zero for home runs where labels do not overlap:

# In[106]:

hr2007.add(hr2006, fill_value=0)


# Operations can also be **broadcast** between rows or columns.
# 
# For example, if we subtract the maximum number of home runs hit from the `hr` column, we get how many fewer than the maximum were hit by each player:

# In[107]:

baseball.hr - baseball.hr.max()


# Or, looking at things row-wise, we can see how a particular player compares with the rest of the group with respect to important statistics

# In[108]:

baseball.loc[89521, "player"]


# In[109]:

stats = baseball[['h','X2b', 'X3b', 'hr']]
diff = stats - stats.loc[89521]
diff[:10]


# We can also apply functions to each column or row of a `DataFrame`

# In[110]:

stats.apply(np.median)


# In[111]:

def range_calc(x):
    return x.max() - x.min()


# In[112]:

stat_range = lambda x: x.max() - x.min()
stats.apply(stat_range)


# Lets use apply to calculate a meaningful baseball statistics, [slugging percentage](https://en.wikipedia.org/wiki/Slugging_percentage):
# 
# $$SLG = \frac{1B + (2 \times 2B) + (3 \times 3B) + (4 \times HR)}{AB}$$
# 
# And just for fun, we will format the resulting estimate.

# In[113]:

def slugging(x): 
    bases = x['h']-x['X2b']-x['X3b']-x['hr'] + 2*x['X2b'] + 3*x['X3b'] + 4*x['hr']
    ab = x['ab']+1e-6
    
    return bases/ab

baseball.apply(slugging, axis=1).round(3)


# ## Sorting and Ranking
# 
# Pandas objects include methods for re-ordering data.

# In[ ]:

baseball_newind.sort_index().head()


# In[ ]:

baseball_newind.sort_index(ascending=False).head()


# Try sorting the **columns** instead of the rows, in ascending order:

# In[ ]:

baseball_newind.sort_index(axis=1).head()


# We can also use `sort_values` to sort a `Series` by value, rather than by label.

# In[ ]:

baseball.hr.sort_values()


# For a `DataFrame`, we can sort according to the values of one or more columns using the `by` argument of `sort_values`:

# In[ ]:

baseball[['player','sb','cs']].sort_values(ascending=[False,True], 
                                           by=['sb', 'cs']).head(10)


# **Ranking** does not re-arrange data, but instead returns an index that ranks each value relative to others in the Series.

# In[114]:

baseball.hr.rank()


# Ties are assigned the mean value of the tied ranks, which may result in decimal values.

# In[ ]:

pd.Series([100,100]).rank()


# Alternatively, you can break ties via one of several methods, such as by the order in which they occur in the dataset:

# In[ ]:

baseball.hr.rank(method='first')


# Calling the `DataFrame`'s `rank` method results in the ranks of all columns:

# In[ ]:

baseball.rank(ascending=False).head()


# In[ ]:

baseball[['r','h','hr']].rank(ascending=False).head()


# ### Exercise 4
# 
# Calculate **on base percentage** for each player, and return the ordered series of estimates.
# 
# $$OBP = \frac{H + BB + HBP}{AB + BB + HBP + SF}$$

# In[116]:

def onbasepercent(x):
    onbases = x['h'] + x['bb'] + x['hbp']
    basetotal = x['ab'] + x['bb'] + x['hbp'] + x['sf']+1e-6
    
    return onbases/basetotal

baseball.apply(onbasepercent, axis=1).round(3)


# ## Hierarchical indexing
# 
# In the baseball example, I was forced to combine 3 fields to obtain a unique index that was not simply an integer value. A more elegant way to have done this would be to create a hierarchical index from the three fields.

# In[117]:

baseball_h = baseball.set_index(['year', 'team', 'player'])
baseball_h.head(10)


# This index is a `MultiIndex` object that consists of a sequence of tuples, the elements of which is some combination of the three columns used to create the index. Where there are multiple repeated values, Pandas does not print the repeats, making it easy to identify groups of values.

# In[118]:

baseball_h.index[:10]


# In[209]:

baseball_h.index.is_unique


# Try using this hierarchical index to retrieve Julio Franco (`francju01`), who played for the Atlanta Braves (`ATL`) in 2007:

# In[210]:

baseball_h.loc[(2007, 'ATL', 'francju01')]


# Recall earlier we imported some microbiome data using two index columns. This created a 2-level hierarchical index:

# In[211]:

mb = pd.read_csv("Data/microbiome.csv", index_col=['Taxon','Patient'])


# In[212]:

mb.head(10)


# With a hierachical index, we can select subsets of the data based on a *partial* index:

# In[213]:

mb.loc['Proteobacteria']


# Hierarchical indices can be created on either or both axes. Here is a trivial example:

# In[214]:

frame = pd.DataFrame(np.arange(12).reshape(( 4, 3)), 
                  index =[['a', 'a', 'b', 'b'], [1, 2, 1, 2]], 
                  columns =[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])

frame


# If you want to get fancy, both the row and column indices themselves can be given names:

# In[215]:

frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
frame


# With this, we can do all sorts of custom indexing:

# In[267]:

frame.loc['a', 'Ohio']


# Try retrieving the value corresponding to `b2` in `Colorado`:

# In[264]:

# Write your answer here
frame.loc['b','2','Colorado']


# Additionally, the order of the set of indices in a hierarchical `MultiIndex` can be changed by swapping them pairwise:

# In[250]:

mb.swaplevel('Patient', 'Taxon').head()


# Data can also be sorted by any index level, using `sortlevel`:

# In[251]:

mb.sortlevel('Patient', ascending=False).head()


# ## Missing data
# 
# The occurence of missing data is so prevalent that it pays to use tools like Pandas, which seamlessly integrates missing data handling so that it can be dealt with easily, and in the manner required by the analysis at hand.
# 
# Missing data are represented in `Series` and `DataFrame` objects by the `NaN` floating point value. However, `None` is also treated as missing, since it is commonly used as such in other contexts (*e.g.* NumPy).

# In[252]:

foo = pd.Series([np.nan, -3, None, 'foobar'])
foo


# In[253]:

foo.isnull()


# Missing values may be dropped or indexed out:

# In[254]:

bacteria2


# In[255]:

bacteria2.dropna()


# In[256]:

bacteria2.isnull()


# In[257]:

bacteria2[bacteria2.notnull()]


# By default, `dropna` drops entire rows in which one or more values are missing.

# In[258]:

data.dropna()


# This can be overridden by passing the `how='all'` argument, which only drops a row when every field is a missing value.

# In[259]:

data.dropna(how='all')


# This can be customized further by specifying how many values need to be present before a row is dropped via the `thresh` argument.

# In[260]:

data.loc[7, 'year'] = np.nan
data


# In[261]:

data.dropna(thresh=5)


# This is typically used in time series applications, where there are repeated measurements that are incomplete for some subjects.

# ### Exercise 5
# 
# Try using the `axis` argument to drop columns with missing values:

# In[119]:

# Write your answer here
data.dropna(axis=1)


# Rather than omitting missing data from an analysis, in some cases it may be suitable to fill the missing value in, either with a default value (such as zero) or a value that is either imputed or carried forward/backward from similar data points. We can do this programmatically in Pandas with the `fillna` argument.

# In[269]:

bacteria2.fillna(0)


# In[270]:

data.fillna({'year': 2013, 'treatment':2})


# Notice that `fillna` by default returns a new object with the desired filling behavior, rather than changing the `Series` or  `DataFrame` in place (**in general, we like to do this, by the way!**).

# We can alter values in-place using `inplace=True`.

# In[271]:

data.year.fillna(2013, inplace=True)
data


# Missing values can also be interpolated, using any one of a variety of methods:

# In[272]:

bacteria2.fillna(method='bfill')


# ## Data summarization
# 
# We often wish to summarize data in `Series` or `DataFrame` objects, so that they can more easily be understood or compared with similar data. The NumPy package contains several functions that are useful here, but several summarization or reduction methods are built into Pandas data structures.

# In[273]:

baseball.sum()


# Clearly, `sum` is more meaningful for some columns than others. For methods like `mean` for which application to string variables is not just meaningless, but impossible, these columns are automatically exculded:

# In[274]:

baseball.mean()


# The important difference between NumPy's functions and Pandas' methods is that the latter have built-in support for handling missing data.

# In[275]:

bacteria2


# In[276]:

bacteria2.mean()


# Sometimes we may not want to ignore missing values, and allow the `nan` to propagate.

# In[277]:

bacteria2.mean(skipna=False)


# Passing `axis=1` will summarize over rows instead of columns, which only makes sense in certain situations.

# In[278]:

extra_bases = baseball[['X2b','X3b','hr']].sum(axis=1)
extra_bases.sort_values(ascending=False)


# A useful summarization that gives a quick snapshot of multiple statistics for a `Series` or `DataFrame` is `describe`:

# In[279]:

baseball.describe()


# `describe` can detect non-numeric data and sometimes yield useful information about it.

# In[280]:

baseball.player.describe()


# We can also calculate summary statistics *across* multiple columns, for example, correlation and covariance.
# 
# $$cov(x,y) = \sum_i (x_i - \bar{x})(y_i - \bar{y})$$

# In[281]:

baseball.hr.cov(baseball.X2b)


# $$corr(x,y) = \frac{cov(x,y)}{(n-1)s_x s_y} = \frac{\sum_i (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_i (x_i - \bar{x})^2 \sum_i (y_i - \bar{y})^2}}$$

# In[282]:

baseball.hr.corr(baseball.X2b)


# In[283]:

baseball.ab.corr(baseball.h)


# Try running `corr` on the entire `baseball` DataFrame to see what is returned:

# In[285]:

# Write answer here
baseball.corr()


# If we have a `DataFrame` with a hierarchical index (or indices), summary statistics can be applied with respect to any of the index levels:

# In[286]:

mb.head()


# In[287]:

mb.sum(level='Taxon')


# ## Writing Data to Files
# 
# As well as being able to read several data input formats, Pandas can also export data to a variety of storage formats. We will bring your attention to just a couple of these.

# In[288]:

mb.to_csv("mb.csv")


# The `to_csv` method writes a `DataFrame` to a comma-separated values (csv) file. You can specify custom delimiters (via `sep` argument), how missing values are written (via `na_rep` argument), whether the index is writen (via `index` argument), whether the header is included (via `header` argument), among other options.

# An efficient way of storing data to disk is in binary format. Pandas supports this using Python’s built-in pickle serialization.

# In[289]:

baseball.to_pickle("baseball_pickle")


# The complement to `to_pickle` is the `read_pickle` function, which restores the pickle to a `DataFrame` or `Series`:

# In[290]:

pd.read_pickle("baseball_pickle")


# As Wes warns in his book, it is recommended that binary storage of data via pickle only be used as a temporary storage format, in situations where speed is relevant. This is because there is no guarantee that the pickle format will not change with future versions of Python.

# ### Advanced Exercise: Compiling Ebola Data
# 
# The `Data/ebola` folder contains summarized reports of Ebola cases from three countries during the recent outbreak of the disease in West Africa. For each country, there are daily reports that contain various information about the outbreak in several cities in each country.
# 
# From these data files, use pandas to import them and create a single data frame that includes the daily totals of new cases and deaths for each country.

# In[186]:

# from http://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
import glob

# Guinea
path ='Data/ebola/guinea_data' # file path
allFiles = glob.glob(path + "/*.csv")
guinea_frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
guinea_frame = pd.concat(list_)

# Liberia
path ='Data/ebola/liberia_data' # file path
allFiles = glob.glob(path + "/*.csv")
liberia_frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
liberia_frame = pd.concat(list_)

# Sierra Leone
path ='Data/ebola/sl_data' # file path
allFiles = glob.glob(path + "/*.csv")
sl_frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
sl_frame = pd.concat(list_)



# In[187]:

#do isin to get only New cases of confirmed and New deaths registered for each country
guinea_frame_column = guinea_frame[guinea_frame['Description'].isin(['New cases of confirmed', 'New deaths registered'])]
guinea_frame_column.head()


# In[188]:

#select only the relevant columns for us - date, description, totals
guinea_frame_new= guinea_frame_column[['Date', 'Description', 'Totals']]
guinea_frame_new.head()


# ## References
# 
# [Python for Data Analysis](http://shop.oreilly.com/product/0636920023784.do) Wes McKinney

# In[175]:

#do isin to get only New cases of confirmed and New deaths registered for each country
liberia_frame_column = liberia_frame[liberia_frame['Variable'].isin(['New case/s (confirmed)', 'Newly reported deaths'])]
liberia_frame_column.head()


# In[176]:

#select only the relevant columns for us - date, variable, national
liberia_frame_new= liberia_frame_column[['Date', 'Variable', 'National']]
liberia_frame_new.head()


# In[180]:

#do isin to get only New cases of confirmed and New deaths registered for each country
sl_frame_column = sl_frame[sl_frame['variable'].isin(['new_confirmed', 'death_confirmed'])]
sl_frame_column.head()


# In[181]:

#select only the relevant columns for us - date, variable, national
sl_frame_new= sl_frame_column[['date', 'variable', 'National']]
sl_frame_new.head()


# In[231]:

#for each country
#made the dates the index and drop the date column
#add a column with the Country name at the end
guinea_frame_new.index = guinea_frame_new.Date
guinea_drop = guinea_frame_new.drop('Date', axis=1)
guinea_drop['Country']=['Guinea']*len(guinea_drop)
guinea_drop.head()


# In[208]:

liberia_frame_new.index = liberia_frame_new.Date
liberia_drop = liberia_frame_new.drop('Date', axis=1)
liberia_drop['Country']=['Liberia']*len(liberia_drop)
#liberia_drop['Date'] = liberia_drop['Date'].astype('datetime64[ns]')
liberia_drop.head()


# In[210]:

sl_frame_new.index = sl_frame_new.date
sl_drop = sl_frame_new.drop('date', axis=1)
sl_drop['Country']=['Sierra Leone']*len(sl_drop)
sl_drop['Country']=['Sierra Leone']
#sl_drop['date'] = sl_drop['date'].astype('datetime64[ns]')
sl_drop.head()


# In[233]:

#Change the names of the columns to the same
guinea_drop.columns = liberia_drop.columns = sl_drop.columns = ['Description', 'National Total', 'Country']
#Change the names of the date column to the same
guinea_drop.index.name = liberia_drop.index.name = sl_drop.index.name = ['Date']


# In[240]:

#Merge the files
dataframe = pd.concat([liberia_drop,guinea_drop,sl_drop])
dataframe[['Country','Description','National Total']]


# In[ ]:



