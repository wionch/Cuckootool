# -*- coding:utf-8 -*-
import pymysql, sqlite3, os, pydblite, telethon, pickle
import wio.func as func


# Mysql 类 ================================================================================================================================================================
class mysql(object):
    def __init__(self, user):
        self.user = user

    def con(self):
        if self.user == 'openresty_online':
            host = '89.35.39.202'
            user = 'root'
            password = '@Wionch777'
            database = 'openresty'
        elif self.user == 'openresty_test':
            host = '207.244.243.8'
            user = 'root'
            password = '@Wionch777'
            database = 'openresty'
        elif self.user == 'localhost':
            host = '127.0.0.1'
            user = 'root'
            password = '@Wionch777'
            database = 'openresty'
        elif self.user == 'contabo_win':
            host = '62.171.152.216'
            user = 'root'
            password = '@Wionch777'
            database = 'zen'
        db = pymysql.connect(host, user, password, database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        return db

    def select(self, query):
        data = None
        db = self.con()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        try:
            # 使用 execute()  方法执行 SQL 查询
            cursor.execute(query)
            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchall()
            # print ( str(data))
        except:
            print("Error: unable to fetch data")
        finally:
            cursor.close()
            # 关闭数据库连接
            db.close()
        return data

    def ui(self, query):
        db = self.con()
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(query)
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        finally:
            cursor.close()
            db.close()

    # 调用存储过程
    def call_proc(self, proc, args):
        db = self.con()
        # 使用 cursor() 方法创建一个游标对象 cursor
        # print(db_name,proc,args)
        # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        try:
            cursor.callproc(proc, args)
            db.commit()
            data = cursor.fetchall()
            # print(data)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()
        return data


# Mysql ================================================================================================================================================================
# host='localhost'
host = "62.171.152.216"  # contabo-win
# host="127.0.0.1" #contabo-win
user = 'root'
password = 'wionch777'
database = 'zen'
charset = 'utf8mb4'
cusror_type = pymysql.cursors.DictCursor


def Con(name):
    if name == 'localhost' or name == 'local':
        db = pymysql.connect('127.0.0.1', 'root', '@Wionch777', 'zen', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    elif name == 'contabo-win':
        db = pymysql.connect('62.171.152.216', 'root', 'wionch777', 'zen', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    elif name == 'contabo-win-local':
        db = pymysql.connect('127.0.0.1', 'root', 'wionch777', 'zen', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    elif name == 'openresty':
        db = pymysql.connect('207.244.254.178', 'root', '@Wionch777', 'openresty', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    elif name == 'openresty-test':
        db = pymysql.connect('207.244.243.8', 'root', '@Wionch777', 'openresty', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return db


# 数据库查询
def Select(query, con='local'):
    data = None
    # if db is None:
    #    db = pymysql.connect(host, user, password, database, charset=charset,cursorclass=cusror_type )
    db = Con(con)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(query)
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        # print ( str(data))
    except:
        print("Error: unable to fetch data")
    finally:
        cursor.close()
        # 关闭数据库连接
        db.close()
    return data


# 数据库增删改
def UI(query, con='local'):
    # if db is None:
    #    db = pymysql.connect(host, user, password, database, charset=charset )
    db = Con(con)
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(query)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    finally:
        cursor.close()
        db.close()


# 调用存储过程
def CallProc(db_name, proc, args, con='local'):
    # data=None
    # if db is None:
    #    # db = pymysql.connect(host, user, password, database, charset=charset )
    #    db=Con('contabo-win')
    db = Con(con)
    # 使用 cursor() 方法创建一个游标对象 cursor
    # print(db_name,proc,args)
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    try:
        cursor.callproc(proc, args)
        db.commit()
        data = cursor.fetchall()
        # print(data)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
    return data


# 查询config表 [config_key : 查询key值 . config_task: 查询任务 . select_sql: 查询条件语句 .注意select_sql最后一定是和value组合, 如id>value 等]
def Config(config_key, config_task, select_sql, con='local'):
    # 插入默认数据 , 已存在则忽略
    insert_sql = "insert ignore into zen.`config` (`status`,`key`,`value`,`task`) values (1,'%s','%s','%s')" % (
        config_key, "0", config_task)
    UI(insert_sql, con=con)
    '''
    并发处理 : 先查询config中对应key,task的id, 同时更新status为2 , 如果查询不到数据, 则直接返回None ; 获取到数据则在完成查询后, 将status更新为1
    '''
    # 根据value查询数据 , 注意select_sql最后一定是和value组合, 如id>value 等
    sel_sql = select_sql + " and id>(" + "select `value` from zen.`config` where `key`='%s' and `task`='%s' limit 1" % (
        config_key, config_task) + ") limit 1;"
    sel_data2 = Select(sel_sql, con=con)
    if len(sel_data2) > 0:
        # 查到数据 , 更新id到config
        sql_id = sel_data2[0]['id']
        sq = "update zen.`config` set `value`='%s' where `key`='%s' and `task`='%s' limit 1" % (
            sql_id, config_key, config_task)
        UI(sq, con=con)
        return sel_data2
    else:
        # 无数据 , 更新config为0
        up_sql = "update zen.`config` set `value`='0' where `key`='%s' and `task`='%s' limit 1" % (
            config_key, config_task)
        UI(up_sql, con=con)


# [推荐]存储过程, 查询config数据
def CallSelCofig(config_key, config_task, db_name, tb, where_sql, con='local'):
    # 插入默认数据 , 已存在则忽略
    insert_sql = "insert ignore into zen.`config` (`status`,`key`,`value`,`task`) values (1,'%s','%s','%s')" % (
        config_key, "0", config_task)
    UI(insert_sql, con=con)
    call_data = CallProc('zen', 'SelConfig', (config_key, config_task, db_name, tb, where_sql), con=con)
    if call_data:
        return call_data


# mysql 字符转义
def StrZY(string):
    if string and type(string) == str:
        string = string.replace(r"\\", r"\\\\")
        string = string.replace(r"'", r"\'")
    return string


# Sqlite ================================================================================================================================================================

# 初始化sqlite, 新建db文件, 新建config,log表

def InitSqlite(dbfile):
    create_dict = func.sql_dict('init_db')

    if not os.path.exists(dbfile):  # 文件不存在, 全部重新建立
        conn = sqlite3.connect(dbfile)
        try:
            for _, sql in create_dict.items():
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                c.close()
        finally:
            conn.close()
    else:  # db文件存在, 则判断表是否存在,不存在则创建
        sql = "select name from sqlite_master where type='table'"
        sql_data = SqliteSelect(sql, dbfile)
        if sql_data:
            tb_list = []
            for d in sql_data:
                tb_list.append(d['name'])
            if tb_list:
                conn = sqlite3.connect(dbfile)
                try:
                    for tbname, sql in create_dict.items():
                        if tbname not in tb_list:
                            c = conn.cursor()
                            c.execute(sql)
                            conn.commit()
                            c.close()
                finally:
                    conn.close()


# 新建采集库 用于采集
def CreateCDB(dbfile):
    create_dict = func.sql_dict('creat_cdb')

    conn = sqlite3.connect(dbfile)
    try:
        for _, sql in create_dict.items():
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            c.close()
    finally:
        conn.close()


def InitDataDB(dbfile):
    InitSqlite(dbfile)


def SqliteUI(sql, dbfile):
    try:
        conn = sqlite3.connect(dbfile, timeout=10)
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            result = conn.total_changes
            c.close()
        except Exception as e:
            func.err_log("SqliteUI:" + str(e))
        finally:
            conn.close()
        return result
    except Exception as e:
        func.err_log("SqliteUI:" + str(e))


# 插入数据, 返回最后一条数据id

def SqliteInsert(sql, dbfile):
    try:
        result = None
        conn = sqlite3.connect(dbfile, timeout=10)
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            result = c.lastrowid
            c.close()
        except Exception as e:
            func.err_log("SqliteInsertIn:" + str(e))
        finally:
            conn.close()
        return result
    except Exception as e:
        func.err_log("SqliteInsertOut:" + str(e))


def SqliteSelect(sql, dbfile):
    #  dbfile=dbname+'.db'
    try:
        conn = sqlite3.connect(dbfile)

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        conn.row_factory = dict_factory
        try:
            c = conn.cursor()
            cursor = c.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        finally:
            conn.close()
    except Exception as e:
        func.err_log("SqliteSelect:" + str(e))


def SqliteInitTable(table_name='task', dbfile=None):
    try:
        sql = "update sqlite_sequence set seq = 0 where name = '%s'" % table_name
        SqliteUI(sql, dbfile)
        sql = "delete from sqlite_sequence where name = '%s'" % table_name
        SqliteUI(sql, dbfile)
        sql = "delete from %s" % table_name
        SqliteUI(sql, dbfile)
    except Exception as e:
        func.err_log("SqliteInitTable:" + str(e))


# 初始化数据库和表
def clear_table(dbfile):
    '''初始化数据库和表'''
    try:
        if os.path.exists(dbfile):
            os.remove(dbfile)  # 删除原来的db文件
    except:
        pass
    InitSqlite(dbfile)
    # 自动清空task表
    SqliteInitTable('task', dbfile)
    SqliteInitTable('account', dbfile)
    SqliteInitTable('target', dbfile)
    SqliteInitTable('proxy', dbfile)
    SqliteInitTable('content', dbfile)
    SqliteInitTable('collection', dbfile)
    SqliteInitTable('log', dbfile)


class MysqlLite3(object):
    """快速模型: 先生成conn, 方法必须传入conn, 全部执行完成后, 需要conn.commit提交保存
    此模型sql执行效率高很多.
    """
    def __init__(self):
        pass

    def get_conn(self, dbfile):
        conn = sqlite3.connect(dbfile, check_same_thread=False)  # 允许多线程调用
        conn.text_factory = str
        if os.path.exists(dbfile) and os.path.isfile(dbfile):
            # print('硬盘上面:[{}]'.format(self.dbfile))
            return conn
        return conn

    def get_cursor(self, conn):
        cur = conn.cursor()
        return cur

    def select(self, sql, conn):
        """
        查询所有数据
        """
        try:
            r = None
            if sql is not None and sql != '':
                conn.row_factory = self.dict_factory
                cu = self.get_cursor(conn)
                cu.execute(sql)
                r = cu.fetchall()

            else:
                print('the [{}] is empty or equal None!'.format(sql))
        finally:
            cu.close()
            return r

    def select_by_str(self, val, tb, where_str, conn):
        """
        查询所有数据
        """
        try:
            conn.row_factory = self.dict_factory
            cu = self.get_cursor(conn)
            sql = """select {} from `{}` where {}""".format(val, tb, where_str)
            cu.execute(sql)
            r = cu.fetchall()
        finally:
            cu.close()
            return r


    def insert(self, sql, conn, commit=True):
        try:
            r = None
            cu = self.get_cursor(conn)
            cu.execute(sql)
            if commit:
                conn.commit()
            r = cu.lastrowid
        except Exception as e:
            func.err_log("{}:{}".format(str(e), sql))
        finally:
            cu.close()
            return r

    def insert_by_dict(self, conn, tb, insert_dict, commit=True):
        try:
            r = None
            cu = self.get_cursor(conn)
            keys = ','.join(insert_dict.keys())
            wh = []
            for key in insert_dict.keys():
                wh.append(':{}'.format(key))
            wh = ','.join(wh)
            sql = """insert into `{}` ({}) values ({})""".format(tb, keys, wh)
            cu.execute(sql, insert_dict)
            if commit:
                conn.commit()
            r = cu.lastrowid
        except Exception as e:
            func.err_log("{}:{}".format(str(e), sql))
        finally:
            cu.close()
            return r

    def ui(self, sql, conn, commit=True):
        try:
            r = None
            cu = self.get_cursor(conn)
            cu.execute(sql)
            if commit:
                conn.commit()
            r = cu.rowcount
        except Exception as e:
            func.err_log("{}:{}".format(str(e), sql))
        finally:
            cu.close()
            return r

    def update_by_id(self, tb, key, val, sql_id, conn, commit=True):
        try:
            r = None
            cu = self.get_cursor(conn)
            sql = "update `{}` set `{}`=? where id=?".format(tb, key)
            cu.execute(sql, (val, sql_id))
            if commit:
                conn.commit()
            r = cu.rowcount
        except Exception as e:
            func.err_log("update_by_id:{}".format(str(e)))
        finally:
            cu.close()
            return r

    def update_by_str(self, tb, set_str, where_str, conn, commit=True):
        try:
            r = None
            cu = self.get_cursor(conn)
            sql = "update `{}` set {} where {}".format(tb, set_str, where_str)
            cu.execute(sql)
            if commit:
                conn.commit()
            r = cu.rowcount
        except Exception as e:
            func.err_log(str(e))
        finally:
            cu.close()
            return r

    def delete_by_str(self, tb, where_str, conn, commit=True):
        try:
            cu = self.get_cursor(conn)
            sql = "delete from `{}` where {}".format(tb, where_str)
            cu.execute(sql)
            if commit:
                conn.commit()
        except Exception as e:
            func.err_log(str(e))
        finally:
            cu.close()
            return


    def uiSession(self, session_info, conn, commit=True, iskey=True):
        try:
            if iskey:
                dc_id, server_address, port, auth_key = session_info['dc_id'], session_info['server_address'], \
                                                        session_info['port'], session_info['auth_key'].key
            else:
                dc_id, server_address, port, auth_key = session_info['dc_id'], session_info['server_address'], \
                                                        session_info['port'], session_info['auth_key']
            r = None
            cu = self.get_cursor(conn)
            cu.execute('insert or replace into sessions values (?,?,?,?,?)', (
                dc_id,
                server_address,
                port,
                auth_key,
                None
            ))
            if commit:
                conn.commit()
            r = cu.lastrowid

        except Exception as e:
            # print(str(e))
            func.err_log(str(e))
        finally:
            cu.close()
            return r

    # 初始化session文件,建文件和表
    def initSessionDb(self, conn, commit=True):
        create_dict = func.sql_dict('creat_session_db')
        try:
            for tb, sql in create_dict.items():
                cu = self.get_cursor(conn)
                cu.execute(sql)
                if commit:
                    conn.commit()

            self.insert("insert into version values (7)")
        finally:
            cu.close()

    def init_db(self, conn, commit=True):
        create_dict = func.sql_dict('init_db')
        try:
            for tb, sql in create_dict.items():
                cu = self.get_cursor(conn)
                cu.execute(sql)
                if commit:
                    conn.commit()
        finally:
            cu.close()

    def creat_cdb(self, conn, commit=True):
        create_dict = func.sql_dict('creat_cdb')
        try:
            for _, sql in create_dict.items():
                cu = self.get_cursor(conn)
                cu.execute(sql)
                if commit:
                    conn.commit()
        except Exception as e:
            func.err_log('creat_cdb:{}'.format(str(e)))
        finally:
            cu.close()

    def create_log_db(self, conn, commit=True):
        try:
            sql = func.sql_dict('init_db')['log']
            cu = self.get_cursor(conn)
            cu.execute(sql)
            if commit:
                conn.commit()
        finally:
            cu.close

    def init_table(self, table_name, conn):
        sql = "update sqlite_sequence set seq = 0 where name = '%s'" % table_name
        self.ui(sql, conn)
        sql = "delete from sqlite_sequence where name = '%s'" % table_name
        self.ui(sql, conn)
        sql = "delete from %s" % table_name
        self.ui(sql, conn)


class MySqlite(object):
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def get_conn(self):
        """
        获取数据库连接
        """
        try:
            conn = sqlite3.connect(self.dbfile)

            """
            该参数是为了解决一下错误：
            ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str).
            It is highly recommended that you instead just switch your application to Unicode strings.
            """
            # conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
            conn.text_factory = str
            if os.path.exists(self.dbfile) and os.path.isfile(self.dbfile):
                # print('硬盘上面:[{}]'.format(self.dbfile))
                return conn
        except sqlite3.OperationalError as e:
            print(str(e))

    def get_cursor(self, conn):
        """
        该方法是获取数据库的游标对象，参数为数据库的连接对象
        """
        if conn is not None:
            return conn.cursor()
        else:
            return self.get_conn().cursor()

    def close_all(self, conn, cu):
        """
        关闭数据库游标对象和数据库连接对象
        """
        try:
            cu.close()
            conn.close()
        except sqlite3.OperationalError as e:
            # print(str(e))
            func.err_log("db_close_all:{}".format(str(e)))
            pass

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def select(self, sql):
        """
        查询所有数据
        """
        try:
            r = None
            if sql is not None and sql != '':
                conn = self.get_conn()
                conn.row_factory = self.dict_factory
                cu = self.get_cursor(conn)
                cu.execute(sql)
                r = cu.fetchall()
            else:
                print('the [{}] is empty or equal None!'.format(sql))
        finally:
            self.close_all(conn, cu)
            return r

    def select_by_str(self, val, tb, where_str=None):
        """
        查询所有数据
        """
        try:
            r = None
            conn = self.get_conn()
            conn.row_factory = self.dict_factory
            cu = self.get_cursor(conn)
            if where_str:
                where = 'where {}'.format(where_str)
            else:
                where = ''
            sql = """select {} from `{}` {}""".format(val, tb, where)
            cu.execute(sql)
            r = cu.fetchall()
        finally:
            self.close_all(conn, cu)
            return r

    def insert(self, sql):
        try:
            r = None
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            cu.execute(sql)
            conn.commit()
            r = cu.lastrowid
        except Exception as e:
            func.err_log("{}:{}".format(str(e), sql))
        finally:
            self.close_all(conn, cu)
            return r

    def insert_by_dict(self, tb, insert_dict):
        try:
            r = None
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            keys = ','.join(insert_dict.keys())
            wh = []
            for key in insert_dict.keys():
                wh.append(':{}'.format(key))
            wh = ','.join(wh)
            sql = """insert into `{}` ({}) values ({})""".format(tb, keys, wh)
            cu.execute(sql, insert_dict)
            conn.commit()
            r = cu.lastrowid
        except Exception as e:
            func.err_log("{}:{}".format(str(e), sql))
        finally:
            self.close_all(conn, cu)
            return r

    def ui(self, sql):
        try:
            r = None
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            cu.execute(sql)
            conn.commit()
            r = cu.rowcount
        except Exception as e:
            # print(str(e))
            func.err_log("{}:{}".format(str(e), sql))
        finally:
            self.close_all(conn, cu)
            return r

    def update_by_id(self, tb, key, val, sql_id):
        try:
            r = None
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            sql = "update `{}` set `{}`=? where id=?".format(tb, key)
            cu.execute(sql, (val, sql_id))
            conn.commit()
            r = cu.rowcount
        except Exception as e:
            func.err_log("update_by_id:{}".format(str(e)))
        finally:
            self.close_all(conn, cu)
            return r

    def update_by_str(self, tb, set_str, where_str=None):
        try:
            r = None
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            if where_str:
                where = 'where {}'.format(where_str)
            else:
                where = ''
            sql = "update `{}` set {} {}".format(tb, set_str, where)
            cu.execute(sql)
            conn.commit()
            r = cu.rowcount
        except Exception as e:
            func.err_log(str(e))
        finally:
            self.close_all(conn, cu)
            return r

    def delete_by_str(self, tb, where_str):
        try:
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            sql = "delete from `{}` where {}".format(tb, where_str)
            cu.execute(sql)
            conn.commit()
        except Exception as e:
            func.err_log(str(e))
        finally:
            self.close_all(conn, cu)
            return

    def uiSession(self, session_info, iskey=True):
        try:
            if iskey:
                dc_id, server_address, port, auth_key = session_info['dc_id'], session_info['server_address'], \
                                                        session_info['port'], session_info['auth_key'].key
            else:
                dc_id, server_address, port, auth_key = session_info['dc_id'], session_info['server_address'], \
                                                        session_info['port'], session_info['auth_key']
            r = None
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            cu.execute('insert or replace into sessions values (?,?,?,?,?)', (
                dc_id,
                server_address,
                port,
                auth_key,
                None
            ))
            conn.commit()
            r = cu.lastrowid

        except Exception as e:
            # print(str(e))
            func.err_log(str(e))
        finally:
            self.close_all(conn, cu)
            return r

    # 初始化session文件,建文件和表
    def initSessionDb(self):
        create_dict = func.sql_dict('creat_session_db')
        try:
            for tb, sql in create_dict.items():
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                cu.execute(sql)
                conn.commit()
            self.insert("insert into version values (7)")
        finally:
            self.close_all(conn, cu)

    def init_db(self):
        create_dict = func.sql_dict('init_db')
        try:
            conn = self.get_conn()
            for tb, sql in create_dict.items():
                cu = self.get_cursor(conn)
                cu.execute(sql)
            conn.commit()
            self.close_all(conn, cu)
        finally:
            pass
            # conn.close()

    def creat_cdb(self):
        create_dict = func.sql_dict('creat_cdb')
        try:
            for _, sql in create_dict.items():
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                cu.execute(sql)
                conn.commit()
                self.close_all(conn, cu)
        except Exception as e:
            func.err_log("creat_cdb:{}".format(str(e)))
        finally:
            pass


    def create_log_db(self):
        try:
            sql = func.sql_dict('init_db')['log']
            conn = self.get_conn()
            cu = self.get_cursor(conn)
            cu.execute(sql)
            conn.commit()
        finally:
            self.close_all(conn, cu)

    def init_table(self, table_name):
        sql = "update sqlite_sequence set seq = 0 where name = '%s'" % table_name
        self.ui(sql)
        sql = "delete from sqlite_sequence where name = '%s'" % table_name
        self.ui(sql)
        sql = "delete from %s" % table_name
        self.ui(sql)


class ClientDbLite(object):
    """pydblie: telethon client专属内存数据库类"""
    def __init__(self, db_file='clt'):
        self.db = pydblite.Base(db_file)
        # 如果存在, 则连接
        if self.db.exists():
            print('connect db')
            self.db.open()
        else:
            print('db not exist')

    def create(self):
        if not self.db.exists():
            print('create db')
            self.db.create('status', 'phone', 'client', 'use_num', 'latest_time')

    def insert(self, indict, commit=True):
        r = self.db.insert(**indict)
        if commit:
            self.db.commit()
        return r

    def select(self):
        for r in self.db:
            print(r)


def make_insert(table, dic):
    if table and dic:
        keys = values = ''
        for k, v in dic.items():
            k = '`{}`'.format(k)
            if not keys:
                keys = k
            else:
                keys = keys + ',{}'.format(k)
            if not v:
                v = '""'
            else:
                if type(v) == int:
                    v = str(v)
                else:
                    v = str(v).replace('"', '""')
                    v = '"{}"'.format(v)

            if not values:
                values = v
            else:
                values = values + ',' + str(v)

        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(table, keys, values)
        return sql


def get_db_data(dbfile):
    """获取数据库数据"""
    try:
        db_data = {}
        account_sql = 'select * from `account`'
        target_sql = 'select * from `target`'
        user_sql = 'select * from `user`'
        my = MySqlite(dbfile)
        db_data['account'] = my.select(account_sql) or []
        db_data['target'] = my.select(target_sql) or []
        db_data['user'] = my.select(user_sql) or []
        return db_data
    except Exception as e:
        func.err_log('get_db_data:{}'.format(str(e)))
