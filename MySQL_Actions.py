import MySQLdb
from MySQLdb import cursors
import settings
class MySQL_Codes:
    #conn = None
    #cur = None
    def __init__(self):
        mysql_username = settings.mysql_username
        mysql_password = settings.mysql_password
        mysql_host = settings.mysql_host
        mysql_port = settings.mysql_port

        self.ID_checker_already_deleted = {}

        self.conn = MySQLdb.connect(user=mysql_username, passwd=mysql_password, host=mysql_host, port=mysql_port,
                               charset="utf8",
                               use_unicode=True, cursorclass=MySQLdb.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.cur._defer_warnings = True

        self.cur.execute("CREATE DATABASE IF NOT EXISTS timorleste")
        self.cur.execute('USE timorleste;')
        self.cur.execute("SET NAMES 'utf8';")
        self.cur.execute("SET CHARACTER SET utf8;")
        self.cur.execute('SET GLOBAL max_allowed_packet=16073741824;')
        '''
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fbGraph.likes (
                object_id TEXT,
                object_from_name TEXT,
                object_from_id TEXT,
                like_from_name TEXT,
                like_from_id TEXT
            );""")
        '''

        self.cur.execute("""    CREATE TABLE IF NOT EXISTS timorleste.status (
                group_or_page_id TEXT,
                status_id TEXT,
                status_message TEXT,
                status_author TEXT,
                link_name TEXT,
                status_type TEXT,
                status_link TEXT,
                status_published TEXT,
                num_reactions TEXT,
                num_comments TEXT,
                num_shares TEXT,
                num_likes TEXT,
                num_loves TEXT,
                num_wows TEXT,
                num_hahas TEXT,
                num_sads TEXT,
                num_angrys TEXT
            );""")

        self.cur.execute("""    CREATE TABLE IF NOT EXISTS timorleste.comments (
                group_or_page_id TEXT,
                comment_id TEXT,
                status_id TEXT,
                parent_id TEXT,
                comment_message TEXT,
                comment_author TEXT,
                comment_published TEXT,
                comment_likes TEXT
            );
            """)

    def get_table_data(self,table_name,group_or_page_id):
        self.cur.execute("SELECT * from {0} where group_or_page_id = '{1}'".format(table_name,group_or_page_id))
        table_data= self.cur.fetchall()
        return table_data

    def save_to_db(self,value_list,table_name,group_or_page_id):
        value_list = list(value_list) #convert tuple to list to insert the page or group id
        value_list.insert(0, group_or_page_id)  # insert id of page or group on the list of values on first position
        try:
            self.execute_insert(value_list,table_name,group_or_page_id)
        except Exception, e:
            formatted_values = self.escape_invalid_unicodes(value_list)
            self.execute_insert(formatted_values, table_name,group_or_page_id)

    def execute_insert(self,value_list,table_name,group_or_page_id):
        placeholders = ','.join('%s' for val in value_list)
        current_ID_previous_data_deleted = self.ID_checker_already_deleted.get('{0}'.format(group_or_page_id),False)
        if not current_ID_previous_data_deleted: #delete previous saved data of target id
            self.cur.execute("DELETE from {0} where group_or_page_id ='{1}'".format(table_name,group_or_page_id))
            self.conn.commit()
            self.ID_checker_already_deleted[group_or_page_id] = True
        self.cur.execute('INSERT INTO {0} VALUES ({1})'.format(table_name,placeholders),value_list)
        self.conn.commit()

    def escape_invalid_unicodes(self,value_list):
        formatted_values = []
        for item_value in value_list:
            try:
                formatted_values.append(str(item_value).encode('unicode-escape'))
            except Exception, e:
                formatted_values.append(unicode(item_value,'utf-8').encode('unicode-escape'))
        return formatted_values

    def close_db_connection(self):
        self.conn.close()