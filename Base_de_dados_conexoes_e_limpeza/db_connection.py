import pandas  as pd
import pyodbc
'''
INSTRUÇÕES PARA TRANSFORMAR EM CSV

importar módulo

cnxn = db_connect.Conexao.create_connection()
cursor = cnxn.cursor()
df = db_connect.Conexao.create_df(tablename, cursor) -> tabelas disponíveis abaixo, retorna pd.DataFrame

'''

class Conexao:
    """Métodos necessários para a conexão com servidor SQl"""

    server = 'tcp:fgv-db-server.database.windows.net,1433'
    database = 'fgv-db'
    username = 'student'
    password = '@dsInf123'

    @classmethod
    def create_connection(cls, server:str=None, database:str=None, username:str=None, password:str=None) -> pyodbc.Connection:
        """Cria uma conexão com uma base de dados online

        Parameters
        ----------
        server : str
            String no formato 'tcp:[link],[port]'
        database : str
            Nome da base de dados
        username : str
            Nome de usuário
        password : str
            Senha

        Returns
        -------
        pyodbc.Connection

        Raises
        ------
        TypeError
            Quando os parâmetros não são Strings
        invalid_server_string_format
            Quando a string não obedece o padrão 'tcp:**nome do banco**, **número da porta do servidor**'
        invalid_server_port_value
            Quando a porta do servidor não está compatível com servidor
        """
    
        if server is None:
            server = cls.server
        if database is None:
            database = cls.database
        if username is None:
            username = cls.username
        if password is None:
            password = cls.password

        if not (type(server)==str and type(server)==type(database) and type(server)==type(username) and type(username)==type(password)):
            raise TypeError('Todos os parametros devem ser no formato str()')
        if server[0:3]!='tcp' or server[-5] != ',':
            raise invalid_server_string_format
        if not(server[-4:].isnumeric()):
            raise invalid_server_port_value

        cnxn_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};'
        cnxn = pyodbc.connect(cnxn_string)
        return cnxn

    @classmethod
    def create_df(cls, tablename:str, cursor:pyodbc.Cursor)->pd.DataFrame:
        """A partir de um cursor e o nome de um tabela acessável por esse cursor retorna um pd.DataFrame

        Parameters
        ----------
        tablename : str
            Nome da tabela presente no banco
        
        cursor : pyodbc.Cursor
            Cursor obtido a partir da conexão com o server

        Returns
        -------
        pd.DataFrame
            DataFrame com dados do banco
            
        Raises
        ------
        TypeError
            Quando os parâmetros não correspondem aos tipos especificados
        """

        if type(tablename)!=str:
            raise TypeError('type(tablename)!=str:')
        if type(cursor) != pyodbc.Cursor:
            raise TypeError('type(cursor) != pyodbc.Cursor:')

        table_names = [str(name[1])+'.'+str(name[2]) for name in cursor.tables(tableType='Table').fetchall()]

        if not(tablename in table_names):
            raise invalid_table_name

        query = f'SELECT * FROM {tablename};'
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [t[0] for t in rows[0].cursor_description]
        values = [list(rows[i]) for i in range(len(rows))]
        df = pd.DataFrame(values, columns=cols)
        return df

    @classmethod
    def save_df_csv(cls, df:pd.DataFrame, name:str):
        """Salva .csv a partir de um DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame para gerar o arquivo .csv

        name : str
            Nome do que será atribuido ao arquivo .csv

        Raises
        ------
        TypeError
            Quando os parâmetros não correspondem aos tipos especificados

        """
        if type(df)!=pd.DataFrame or type(name)!= str:
            raise TypeError

        df.to_csv(name + '.csv')



### AVAILABLE TABLES:

    # covid.covid_impact_on_airport_traffic
    # fifa.fifa_players
    # real_state.real_state_values
    # ufc.ufc_master
    # ufc.ufc_most_recent_event
    # ufc.ufc_upcoming_event

### USEFUL COMMANDS:

    # cur = cnxn.cursor()

    # INFO ABOUT ROW:
        # pyodbc.Row.cursor_description

        # IN ORDER:

            # column name (or alias, if specified in the SQL)
            # type code
            # display size (pyodbc does not set this value)
            # internal size (in bytes)
            # precision
            # scale
            # nullable (True/False)


    # INFO ABOUT TABLES
    # cur.tables -> tables -> pyodbc.Row objects
        # cur.tables.table_name
        # result = [table for table in cur.tables]
        # result[0].cursor_description

    # INFO ABOUT COLUMNS
    # result = cursor.columns(table='fifa_players') -> pyodbc.Row object
    # result = iter(result)
    # col = next(result)

### TAKING VALUES INTO PANDAS

    # cursor.execute(query)
    # rows = cursor.fetchmany(10)
    # cols = [t[0] for t in rows.cursor_description]
    # values = [list(rows[i]) for i in range(len(rows))] -> list of lists
    # df = pd.DataFrame(values, columns=cols)
class invalid_server_string_format(ValueError):
    """Exceção levantada quando a string com informações do server não está no formato adequado"""

    pass


class invalid_server_port_value(ValueError):
    """Exceção levantada quando o valor para porta do server não é numérica"""

    pass

class invalid_table_name(ValueError):
    """Exceção levantada quando é requisitada uma tabela que não existe no banco"""

    pass


