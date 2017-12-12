# Perform the Exploratory Analysis of Titanic Dataset
# and generate various reports and plots for analysing the Data.
import pandas as pd
import os
import sys
import datetime
import warnings
import seaborn as sns
import matplotlib
import numpy as np
import pandasql as pdsql
import pylab as pl
import matplotlib.pyplot as plt


matplotlib.pyplot.switch_backend('agg')
warnings.filterwarnings('ignore')


# Identiy catagorial values based on some treshould.
# Here I set the treshould as .25
treshold_for_category = 0.25

# Replace the String values in Catagory attribute to an integer.
replace_string_catagories = {"Sex": {"male": 0, "female": 1},
                             "Embarked": {"S": 1, "C": 2, "Q": 3}
                             }


# Mention the name of the columns that you are intrested.
# Ensure the plotting applis only for numerical vlaues,
# since we get min/max for ploting.
intrested_columns = ['Fare']

# If there are many unique values then the plot will have plots
# overlapped with values. To avoid it, we can set the attributes
# that do not need to display the unique values.
do_notShow_unique_values_in_plot = ['Fare']


def data_analysis(datasetName, df, targetAttribute, outDirectory):

    """
    Function will take the dataset and perform some analysis about the data

    Parameters
    ----------
    datasetName: Name of the dataset.
    df: DataFrame for Test data
    targetAttribute: Target Attribute
    outDirectory: directory where the reports and plot images generated
    """

    file = "1_initial_data_analysis.txt"

    print("\n\nWritting the analysis report to - ", outDirectory)

    print("\n\nWriting the overview of data to " + outDirectory + "/" + file)

    # Create a directory to write the output and report.
    os.system("mkdir " + outDirectory)

    # Output will be written to initial_data_analysis.txt
    report = open(outDirectory + "/" + file, 'w+')

    # Write the dataset name, date the report generted
    # into initial_data_analysis.txt
    print('\n=============================================' +
          '===============================================',
          file=report)
    print('Dataset : ', datasetName, file=report)
    now = str(datetime.datetime.now())
    print('Date : ', now, file=report)
    print('\n=============================================' +
          '===============================================\n',
          file=report)

    # Write the attribute name/count, row count of the dataset to report file
    instance_count, attr_count = df.shape
    attr_name = list(df)
    print('Instance Count : ', instance_count, file=report)
    print('Attribute count (X,y) : ', attr_count, file=report)
    print('Attribute Names (X,y) : ', attr_name, file=report)

    # Identify the attributes that have numeric and String values
    # and write it to initial_data_analysis.txt
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print('\n', file=report)
    print('Attribute with Numeric Type : ', numeric_cols, file=report)
    item_list = list(df)
    item_list = [e for e in item_list if e not in numeric_cols]
    print('Attribute with String Type : ', item_list, file=report)
    print('\n=============================================' +
          '===============================================\n',
          file=report)

    # Write sample data to initial_data_analysis.txt
    print('Sample data : ', file=report)
    print(df.head(5), file=report)
    print('\n=============================================' +
          '===============================================\n',
          file=report)

    # describe data to initial_data_analysis.txt
    des = df.describe()
    print('Describe Attributes : ', file=report)
    print('\n', file=report)
    print(des, file=report)
    print('\n=============================================' +
          '===============================================\n',
          file=report)

    # Write attributes that have missing values to initial_data_analysis.txt
    missCol = pd.isnull(df).any()
    print('Attributes that have Missing Values : ', file=report)
    print('\n', file=report)
    print(missCol, file=report)
    print('\n=============================================' +
          '===============================================\n',
          file=report)

    # Write sum of attributes that have missing values
    # to initial_data_analysis.txt
    sumCol = pd.isnull(df).sum()
    print('Sum of Missing Values for each attributes : ', file=report)
    print('\n', file=report)
    print(sumCol, file=report)
    print('\n=============================================' +
          '===============================================\n',
          file=report)

    mostly_cat = {}
    category_column_list = list()
    for var in df.columns:
            mostly_cat[var] = 1.*df[var].nunique()/df[var].count() < \
                                treshold_for_category
    for key, value in mostly_cat.items():
        if value:
            category_column_list.append(key)
    print('Most likely cataegorial values : ', file=report)
    print(category_column_list, file=report)

    non_category_column_list = [e for e in attr_name
                                if e not in
                                category_column_list]
    print('\n\nMost likely **Non cataegorial values : ', file=report)
    print(non_category_column_list, file=report)

    print('\n=============================================' +
          '===============================================\n',
          file=report)

    # display the unique values for catagorial attributes
    for col in category_column_list:
        print('Unique values for cataegorial column : ', col, file=report)
        print(df[col].unique(), file=report)
        print('\n ', file=report)

    report.close()

    return category_column_list


def updateMissingOrStringCatagorialValues(df):
    print("\n\nUpdating the missing Values and Replace" +
          " the catagorial string values to integer")

    # Fill the missing Age values to median
    df['Age'].fillna(df['Age'].median(), inplace=True)

    # Fill the missing values for Cabin as missing
    df['Cabin'].fillna('Missing', inplace=True)

    # Fill the missing values for Embarked as  S = Southampton
    # since it has the highest no# of people embarked.
    df['Embarked'].fillna('S', inplace=True)

    # Replace the String values in Catagory attribute to an integer.
    # "Sex": {"male": 0, "female": 1}
    # "Embarked": {"S": 1, "C": 2, "Q": 3}
    df.replace(replace_string_catagories, inplace=True)

    return df


def plot(df, category_column_list, targetAttribute, outDirectory):

    instance_count, attr_count = df.shape
    sumCol = pd.isnull(df).sum()

    for rows in range(1, 6):
        size = rows * 5
        if size >= attr_count:
            break

    # Do a ploting of Histogram to get the count
    pl.rcParams.update({'font.size': 18})
    df.hist()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(30, 15)
    # fig.savefig('test2png.png', dpi=100)
    fig.savefig(outDirectory + "/2_Histogram_plot.png", dpi=100)
    pl.rcParams.update({'font.size': 10})

    # Create the box plot for categorial values
    pl.rcParams.update({'font.size': 18})
    df.plot(kind='box', subplots=True, layout=(rows, 5), sharex=False)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(30, 15)
    fig.savefig(outDirectory + "/3_Box_plot.png", tight_layout=True)
    pl.rcParams.update({'font.size': 10})

    for col in category_column_list:
        bar_density_plot(outDirectory, df, col, replace_string_catagories,
                         do_notShow_unique_values_in_plot, sumCol,
                         category_column_list, treshold_for_category)

    for col in intrested_columns:
        bar_density_plot(outDirectory, df, col, replace_string_catagories,
                         do_notShow_unique_values_in_plot, sumCol,
                         category_column_list, treshold_for_category)

    for col in category_column_list:
        histogram(df, col, targetAttribute, df[col].nunique(), col,
                  'Frequency', 'Distribution of ' + col + ' with respect to ' +
                  targetAttribute, outDirectory + "/5_" + col + "_GroupBy_" +
                  targetAttribute + "_Histogram_plot.png")

    # Plot the pairwise plotting with respect to Target attribute
    pl.rcParams.update({'font.size': 18})
    df1 = pd.DataFrame(df, columns=category_column_list)
    plt.figure()
    sns.pairplot(data=df1, hue=targetAttribute)
    plt.savefig(outDirectory + "/6_pairwise_plot.png")
    pl.rcParams.update({'font.size': 10})


def generalizeAttribute(df):

    df['Age_group'] = pd.cut(df['Age'], [0, 10, 20, 30,
                                         40, 50, 60, 70,
                                         80, 90],
                             labels=['0-10', '10-20',
                                     '20-30', '30-40',
                                     '40-50', '50-60',
                                     '60-70', '70-80',
                                     '80-90'])

    cabin_dict = {'A': 'A_Cabin', 'B': 'B_Cabin', 'C': 'C_Cabin',
                  'D': 'D_Cabin', 'E': 'E_Cabin', 'F': 'F_Cabin',
                  'G': 'G_Cabin', 'T': 'T_Cabin', 'M': 'Missing'}

    df['Cabin_group'] = df.Cabin.str[:1].apply(lambda val: cabin_dict[val])

    # Fare starts from 0.0 so we need to put -1 when we cut it
    df['Fare_group'] = pd.cut(df['Fare'], [-1, 50, 100, 150, 200,
                              250, 300, 350, 400,
                              450, 500, 550],
                              labels=['0-50', '50-100', '100-150',
                                      '150-200', '200-250',
                                      '250-300', '300-350',
                                      '350-400', '400-450',
                                      '450-500', '500-550'])

    return df


def generalizedAttributePlot(df, targetAttribute, outDirectory):

    generalizedAttributeList = ['Age_group', 'Cabin_group', 'Fare_group']

    for col in generalizedAttributeList:
        histogram(df[col], None, None,
                  df[col].nunique(), col,
                  'Frequency', 'Distribution of ' + col,
                  outDirectory + "/7_Count_" + col + "_GroupedValues_plot.png")

    for col in generalizedAttributeList:
        histogram(df, col, targetAttribute, df[col].nunique(), col,
                  'Frequency', 'Distribution of ' + col + ' with respect to ' +
                  targetAttribute, outDirectory + "/8_" + col + "_GroupBy_" +
                  targetAttribute + "_Histogram_plot.png")


def groupByData(df, category_column_list, targetAttribute, outDirectory):
    file = "9_GroupBy_Attribute_based_on_Target.txt"

    # Output will be written to initial_data_analysis.txt
    report = open(outDirectory + "/" + file, 'w+')

    print("\n\nWriting Group By Attribute data based on Target Attribute " +
          outDirectory + "/" + file)

    attributes_for_sql_analysis = list()
    attributes_for_sql_analysis.extend(category_column_list)
    attributes_for_sql_analysis.extend(intrested_columns)
    attributes_for_sql_analysis.append('Age_group')
    attributes_for_sql_analysis.append('Cabin_group')
    attributes_for_sql_analysis.append('Fare_group')
    attributes_for_sql_analysis.remove(targetAttribute)

    print('Groupby on attribute values with respect to target attribute : ',
          file=report)
    print('\n', file=report)

    for col in attributes_for_sql_analysis:
        # pysql = lambda q: pdsql.sqldf(q, locals())
        queryStr = "select " + col + ", count(" + col + ") as Count, " + \
                    targetAttribute + " from df group by " + col + \
                    ", " + targetAttribute + " order by " + col + ";"

        df1 = pdsql.sqldf(queryStr.lower(), locals())

        # Do a groupby on attribute values with respect to target attribute
        print('Group by on Attribute : ' + col, file=report)

        if col in replace_string_catagories:
            print('Dictionary Mapping : ' +
                  str(replace_string_catagories[col]) + '\n', file=report)

        print(df1.to_string(), file=report)
        print('\n ', file=report)
        print('\n ', file=report)

    print('\n=============================================' +
          '===============================================',
          file=report)
    print('\n ', file=report)

    report.close()


def cross_attribute_analysis(df, intrestedCrossAttributeList, targetAttribute,
                             doNormalise, outDirectory, inpFile):

    print("\n\nWritting the Cross Attribute Analysis report to - ",
          outDirectory)

    print("\n\nWriting the overview of data to " + outDirectory +
          "/" + inpFile)

    # Create a directory to write the output and report.
    os.system("mkdir " + outDirectory)

    # Output will be written to initial_data_analysis.txt
    report = open(outDirectory + "/" + inpFile, 'w+')

    crossAttributeList = list()
    index = 0
    attributeListLength = len(intrestedCrossAttributeList)
    for i in range(0, attributeListLength):
        counter = i + 1

        for j in range(counter, attributeListLength):
            crossAttributeList.append([])
            crossAttributeList[index].append(intrestedCrossAttributeList[i])
            crossAttributeList[index].append(intrestedCrossAttributeList[j])
            index = index + 1

    index = 1
    length = len(crossAttributeList)
    print("\nTotal Cross Attribute No# - " + str(length) + "\n")
    for item in crossAttributeList:
        print("Processing the cross attribute ( " + item[0] + " & " +
              item[1] + " ) " + str(index) + " out of " + str(length))

        file = outDirectory + "/" + "2_CrossAttribute_" + item[0] + "_" + \
                              item[1] + "_Count.png"

        groupBucket = df.groupby(item)

        groupCount = groupBucket[targetAttribute].count()

        # Write the dataset name, date the report generted
        # into initial_data_analysis.txt
        print('\n=============================================' +
              '===============================================',
              file=report)
        print('Group By - ' + item[0] + " & " + item[1] + '\n', file=report)

        content = ""
        if item[0] in replace_string_catagories:
            content = content + 'Dictionary Mapping : ' + \
                      str(replace_string_catagories[item[0]]) + '\n'

        if item[1] in replace_string_catagories:
            content = content + 'Dictionary Mapping : ' + \
                      str(replace_string_catagories[item[1]]) + '\n'

        print(content, file=report)

        print(groupCount.to_string(), file=report)
        print('\n=============================================' +
              '===============================================\n',
              file=report)
        groupCountUnstack = groupCount.unstack()

        pl.rcParams.update({'font.size': 18})

        groupCountUnstack.plot(kind='bar', title='Grouped by - ' +
                               item[0] + " & " + item[1] + "\n" + content)
        plt.xlabel(item[0])
        plt.ylabel("frequency")
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(30, 15)
        fig.savefig(file)
        pl.rcParams.update({'font.size': 10})
        index = index + 1

    report.close()


def cross_attribute_with_target_analysis(df, intrestedCrossAttributeList,
                                         targetAttribute, doNormalise,
                                         outDirectory, inpFile):

    print("\n\nWritting the Cross Attribute Analysis with target report to - ",
          outDirectory)

    print("\n\nWriting the overview of data to " +
          outDirectory + "/" + inpFile)

    # Create a directory to write the output and report.
    os.system("mkdir " + outDirectory)

    # Output will be written to initial_data_analysis.txt
    report = open(outDirectory + "/" + inpFile, 'w+')

    crossAttributeList = list()
    index = 0
    attributeListLength = len(intrestedCrossAttributeList)
    for i in range(0, attributeListLength):
        counter = i + 1

        for j in range(counter, attributeListLength):
            crossAttributeList.append([])
            crossAttributeList[index].append(intrestedCrossAttributeList[i])
            crossAttributeList[index].append(intrestedCrossAttributeList[j])
            index = index + 1

    index = 1
    length = len(crossAttributeList)
    print("\nTotal Cross Attribute No# - " + str(length) + "\n")
    for item in crossAttributeList:
        print("Processing the cross attribute ( " + item[0] + " & " +
              item[1] + " & " + targetAttribute + " ) " + str(index) +
              " out of " + str(length))

        file = outDirectory + "/" + "2_CrossAttribute_" + item[0] + "_" + \
                              item[1] + "_" + targetAttribute + ".png"

        item.append(targetAttribute)
        groupBucket = df.groupby(item)
        groupCount = groupBucket[targetAttribute].count()

        # Write the dataset name, date the report generted
        # into initial_data_analysis.txt
        print('\n=============================================' +
              '===============================================',
              file=report)
        print('Group By - ' + item[0] + " & " + item[1] + " & " +
              targetAttribute + '\n', file=report)

        content = ""
        if item[0] in replace_string_catagories:
            content = content + 'Dictionary Mapping : ' + \
                      str(replace_string_catagories[item[0]]) + '\n'

        if item[1] in replace_string_catagories:
            content = content + 'Dictionary Mapping : ' + \
                      str(replace_string_catagories[item[1]]) + \
                      '\n'

        print(content, file=report)

        print(groupCount.to_string(), file=report)
        print('\n=============================================' +
              '===============================================\n',
              file=report)
        groupCountUnstack = groupCount.unstack()
        pl.rcParams.update({'font.size': 15})
        groupCountUnstack.plot(kind='bar', title='Grouped by - ' +
                               item[0] + " & " + item[1] + " & " +
                               targetAttribute + "\n" + content)
        plt.xlabel(item[0] + " & " + item[1])
        plt.ylabel("frequency")
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(30, 15)
        fig.savefig(file)
        pl.rcParams.update({'font.size': 10})
        index = index + 1

    report.close()


def exploratory_analysis(datasetName, df, targetAttribute, outDirectory):

    """
    Function will take the dataset and perform some analysis
    and generate the reports to visualize the data and to
    identify the outliners.

    Parameters
    ----------
    datasetName: Name of the dataset.
    df: DataFrame for Test data
    targetAttribute: Target Attribute
    outDirectory: directory where the reports and plot images generated
    """

    instance_count, attr_count = df.shape
    sumCol = pd.isnull(df).sum()

    category_column_list = data_analysis(datasetName, df,
                                         targetAttribute,
                                         outDirectory)

    df = updateMissingOrStringCatagorialValues(df)

    plot(df, category_column_list, targetAttribute, outDirectory)

    df = generalizeAttribute(df)

    generalizedAttributePlot(df, targetAttribute, outDirectory)

    groupByData(df, category_column_list, targetAttribute, outDirectory)

    intrestedCrossAttributeList = ['Pclass', 'Sex', 'Age_group', 'SibSp',
                                   'Parch', 'Fare_group', 'Cabin_group',
                                   'Embarked']
    doNormalise = True
    crossDirectory = outDirectory + "/" + "10_CrossAttributeAnalysis"
    inpFile = "1_CrossAttribute_data_analysis.txt"

    cross_attribute_analysis(df, intrestedCrossAttributeList, targetAttribute,
                             doNormalise, crossDirectory, inpFile)

    crossDirectory = outDirectory + "/" + "11_CrossAttributeWithTargetAnalysis"
    inpFile = "1_CrossAttribute_Target_data_analysis.txt"
    print(intrestedCrossAttributeList)
    cross_attribute_with_target_analysis(df, intrestedCrossAttributeList,
                                         targetAttribute, doNormalise,
                                         crossDirectory, inpFile)


def histogram(df, col, targetAttribute, bin, xLabel, yLabel, title, file):
    if col is not None and col == targetAttribute:
        return

    if targetAttribute is not None:
        pl.rcParams.update({'font.size': 18})

        df[col].hist(by=df[targetAttribute], bins=df[col].nunique())

        title = 'Attribute Name: ' + col + \
                ' grouped by Target Attribute : ' + \
                targetAttribute

        if col in replace_string_catagories:
            title = title + "\n\n Dictionary Mapping :" + \
                    str(replace_string_catagories[col])

        pl.suptitle(title)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(30, 15)
        fig.savefig(file)
        pl.rcParams.update({'font.size': 10})
    else:
        plt.figure()
        f, ax = plt.subplots(figsize=(30, 15))
        ax.hist(df, bins=bin)
        ax.set_ylabel(yLabel)
        ax.set_xlabel(xLabel)
        ax.set_title(title)

        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(20)

        plt.savefig(file)


def bar_density_plot(outDirectory, df, col, replace_string_catagories,
                     do_notShow_unique_values_in_plot, sumCol,
                     category_column_list, treshold_for_category):

    plt.figure(figsize=(10, 8))

    plt.subplot(312)
    plt.xlim(df[col].min(), df[col].max()*1.1)

    ax = df[col].plot(kind='kde')

    plt.subplot(313)
    plt.xlim(df[col].min(), df[col].max()*1.1)
    sns.boxplot(x=df[col])

    title = 'Attribute Name: ' + col

    title = title + '\n\nNo of missing values : ' + str(sumCol[col])

    if col in category_column_list:
        title = title + "\n\n Mostly categorial value based on treshold " + \
                str(treshold_for_category) + " ,nrows: " + \
                str(df[col].count()) + " ,unique values: " + \
                str(df[col].nunique())
    else:
        title = title + "\n\n Mostly **NOT** a categorial value" + \
                " based on treshold " + str(treshold_for_category) + \
                " ,nrows: " + str(df[col].count()) + \
                " ,unique values: " + str(df[col].nunique())

    if col not in do_notShow_unique_values_in_plot:
        title = title + '\n\nUnique values : ' + \
                np.array_str(np.sort(df[col].unique()))

    if col in replace_string_catagories:
        title = title + "\n\n Dictionary Mapping :" + \
                str(replace_string_catagories[col])

    plt.suptitle(title)

    plt.savefig(outDirectory + "/4_" + col + "_density_box_plot.png")


def main():

    """
    Function will take the dataset and perform some analysis
    and generate the reports to visualize the data and to
    identify the outliners.

    Arguments Passed:
    -----------------
    datasetName: Name of the dataset.
    train_file: Path of the Test data
    targetAttribute: Target Attribute
    outDirectory: directory where the reports and plot images generated

    Arguments Passed:
    -----------------
    python ExploratoryDataAnalysis.py Titanic /opt/PythonConda/ML/titan/train.csv
    Survived /opt/git_projects/Exploratory-Data-Analysis-with-python/output

    """

    datasetName = sys.argv[1]
    train_file = sys.argv[2]
    targetAttribute = sys.argv[3]
    outDirectory = sys.argv[4]

    print("\n\nExploratory Analysis of Dataset")

    df = pd.read_csv(train_file)
    exploratory_analysis(datasetName, df, targetAttribute, outDirectory)

    print("\n\nExploratory Analysis completed \n\n")

if __name__ == '__main__':
    main()
