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

class SaveDatabase:

    def __init__(self, table_name, df):
        self.table_name = table_name
        self.df = df
        
    def verify_if_not_exists_dupe_values(self):
        
        meta = MetaData()
        table = Table(self.table_name, meta, autoload=True, autoload_with=engine)
        primary_key = table.primary_key.columns.values()[0].name
        engine_table = pd.read_sql_query(f'SELECT {primary_key} from {self.table_name};', engine)
        
        try:
            mask = engine_table[primary_key].isin(self.df[primary_key])
            if engine_table[primary_key].loc[mask].shape[0] != 0:
                for i in engine_table[primary_key].loc[mask]:
                    statement = 'DELETE FROM {} WHERE {} = {};'.format(self.table_name, primary_key, i) # Query sintax to exclude values
                    engine.connect().execute(statement)
                print('DUPLICATED PRIMARY KEY VALUES WERE EXCLUDED')
            return 1
        except Exception as ex:
            print("OCCOUR EXCEPTIOM :( => {}".format(ex))
            return 0
        
    def save_in_table(self):
        if self.verify_if_not_exists_dupe_values == 1: 
            try:
                columns = engine.connect().execute('''
                                            SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}';
                                            '''.format(self.table_name)
                                            )
                
                if self.table_name is not None:
                    if any(columns) == any(self.df.columns):
                        self.df.to_sql(self.table_name, engine, if_exists = "append", index=False)
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
        else:
            return "is not possible save this values in database"