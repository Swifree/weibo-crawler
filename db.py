import sqlite3


def prepare_table(db_name):
    conn = sqlite3.connect(db_name)
    sql = '''create table if not exists published_articles (
            id integer primary key ,
            content text)'''

    conn.cursor().execute(sql)
    # 提交事务
    conn.commit()
    # 关闭数据库连接
    conn.close()


prepare_table("articles.db")


def connect_to_db(db_name):
    # 连接到数据库并创建游标对象
    conn = sqlite3.connect(db_name)
    return conn.cursor(), conn


def check_published_article(cur, article_id):
    # 查询文章是否已发布
    cur.execute("SELECT id FROM published_articles WHERE id=?", (article_id,))
    row = cur.fetchone()
    return True if row is not None else False


def insert_article(cur, conn, article_id, content):
    # 插入新文章
    cur.execute("INSERT INTO published_articles (id, content) VALUES (?, ?)", (article_id, content))
    # 提交更改
    conn.commit()
