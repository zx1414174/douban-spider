from App.Mysql.MysqlTool import MysqlTool


class Book(MysqlTool):
    """
    书籍
    """
    _table = 'db_book'
