import mysql.connector
import pandas as pd
from sqlalchemy import types, create_engine


def get_sql_data(taglist, tablename):   
    """Takes a list of strings with tags and a tablename, 
    returns a pandas dataframe with the tag timeseries"""

    tagstring = taglist[0]
    for nr in range(1, len(taglist)):
        tagstring = tagstring + ', ' + taglist[nr]
    
    
    conn = mysql.connector.connect(user='root', 
                                  password='pugliawijnislekker',
                                  host='127.0.0.1',
                                  database='Teijin_2019')
    
      
    sqlcommand = 'SELECT Datetime, ' + tagstring + ' FROM ' + tablename
    df = pd.read_sql(sqlcommand, con=conn)
    df = df.set_index(pd.to_datetime(df['Datetime']), drop=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(0)
    df = df.drop(['Datetime'], axis=1)
#    df2 = pd.read_sql('SELECT Datetime, 82T23 FROM PPD', con = conn)
    
    # drop duplicates of one row to prevent create additional rows (from summertime to wintertime a double time stamp is created, 
    # merging two dataframes with double timestamps creates 4 timestamps instead of 2)
#    df4 = df2.drop_duplicates(subset='Datetime')
    
    
#    df = df3.merge(df4, left_on='Datetime', right_on='Datetime')
    return df






def store_dataframe(df, tablename):
    
    # MySQL Connection
    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
                            .format(user="root",
                                    pw="pugliawijnislekker",
                                    db="teijin_2019"))
     
    

    
    # Store dataframe to SQL
    df.to_sql(name=tablename.lower(), con=engine, if_exists = 'replace', chunksize = 1000)


