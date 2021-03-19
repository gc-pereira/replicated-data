from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://{user}:{pswd}@{host}/{database}".format( #+psycopg2
    host = 'localhost',
    user = 'teamvendas',
    pswd = '1q2w3e4r',
    database = 'ecommerce'
))

table_name = 'vendedor'
engine_table = pd.read_sql_table

def save_in_sales_table(df):

    meta = MetaData()
    table = Table(table_name, meta, autoload=True, autoload_with=engine)
    primary_key = table.primary_key.columns.values()[0].name
    engine_table = pd.read_sql_query(f'SELECT {primary_key} from {table_name};', engine)
    
    columns = engine.connect().execute('''
                                       SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}';
                                       '''.format(table_name)
                                       )
    
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
    else:
        print('NOT HAVE DUPLICATED PRIMARY KEY VALUES')
    
    try:
        if table_name is not None:
            if any(columns) == any(df.columns):
                df.to_sql(table_name, engine, if_exists = "append", index=False)
    except ValueError as ex:
        print('EXCEPTION (ValueError) {}'.format(ex))
    except IntegrityError as ex:
        print('ERROR TO INSERT IN TABLE (IntegrityError) {}'.format(ex))
        dupe_field = str(ex.orig).split('(')
        print('PRIMARY KEY VALUE: {}'.format(dupe_field[2].split(')')[0]))
    except Exception as e:
        print(e)
    except ProgrammingError as ex:
        print('(ProgrammingError) {}'.format(ex))