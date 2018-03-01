from App.Mysql.MysqlTool import MysqlTool


class BookTag(MysqlTool):
    """
    书籍热门标签
    """
    _table = 'db_book_tag'
