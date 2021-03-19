import pandas as pd
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy import create_engine
import os
import glob

engine = create_engine("postgresql://{user}:{pswd}@{host}/{database}".format( #+psycopg2
    host = 'localhost',
    user = 'teamvendas',
    pswd = '1q2w3e4r',
    database = 'ecommerce'
))

def handler(event, context):


    print(f"CONNECTED TO {creds['dbname']} DATABASE")
        
    s3_client.Bucket(bucket).download_file(key, download_path)

    print(f"DOWNLOADED  {tmpkey} FILE")

    # Unzip
    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    print("UNZIPED FILE")

    # Open CSV and get a newest file in folder
    list_of_files = glob.glob(extract_path+'/*') # * means all if need specific format then *.csv
    print(f'LIST OF FILES {list_of_files}')
    
    try:   
        file_name = max(list_of_files, key=os.path.getctime)
        df = pd.read_csv(file_name) # Create a dataframe by unziped csv
        df.columns = df.columns.str.strip().str.lower()
    except Exception as ex:
        print('Error in READ file to create a dataframe')
    # Discover table name
    table_name = None
    try:      
        for key in SERVICES.keys():
            if file_name.find(key) != -1:
                table_name = SERVICES[key]
        # Get primary key name and create pandas data frame by sql table
        print('TABLE NAME: ', table_name)
        meta = MetaData()
        table = Table(table_name, meta, autoload=True, autoload_with=engine)
        primary_key = table.primary_key.columns.values()[0].name
        engine_table = pd.read_sql_query(f'SELECT {primary_key} from {table_name};', engine)
    
        columns = engine.connect().execute('''
                                       SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}';
                                       '''.format(table_name))
    except:
        print('Error to find a table to this file!')
        publish_message('Error to find a table to this file!')
    else:
        print(f"IDENTIFIED TABLE DESTINATION AS {table_name}")
        print('PRIMARY KEY IS: {}'.format(primary_key))
    
    # Verify if have a register for primary key
    try:
        mask = engine_table[primary_key].isin(df[primary_key])
        if engine_table[primary_key].loc[mask].shape[0] != 0 and table_name != 'payment_slip':
            for i in engine_table[primary_key].loc[mask]:
                statement = 'DELETE FROM {} WHERE {} = {};'.format(table_name, primary_key, i) # Query sintax to exclude values
                engine.connect().execute(statement)
            print('DUPLICATED PRIMARY KEY VALUES WERE EXCLUDED')
        elif engine_table[primary_key].loc[mask].shape[0] != 0 and table_name == 'payment_slip':  
            for j in engine_table[primary_key].loc[mask]:
                statement = '''
                            DELETE FROM {} WHERE {} = '{}';
                            '''.format(table_name, primary_key, j) # Query sintax to exclude values
                engine.connect().execute(statement)
            print('DUPLICATED PRIMARY KEY VALUES WERE EXCLUDED')
    except Exception as ex:
        print("OCCOUR EXCEPTIOM :( => {}".format(ex))
        publish_message(ex)
    else:
        print('NOT HAVE DUPLICATED PRIMARY KEY VALUES')

    # Insert into database
    # TODO: create a table to insert the duplicate lines
    try:
        if table_name is not None:
            if any(columns) == any(df.columns):
                df.to_sql(table_name, engine, if_exists = "append", index=False)
                print(f"Inserted {file_name} into {table_name}")
                everythingWorks = 1 
    except ValueError as ex:
        print('EXCEPTION (ValueError) {}'.format(ex))
        publish_message(ex)
    except IntegrityError as ex:
        print('ERROR TO INSERT IN TABLE (IntegrityError) {}'.format(ex))
        dupe_field = str(ex.orig).split('(')
        print('PRIMARY KEY VALUE: {}'.format(dupe_field[2].split(')')[0]))
        publish_message(ex)
    except Exception as e:
        publish_message(e)
        print(e)
    except ProgrammingError as ex:
        print('(ProgrammingError) {}'.format(ex))