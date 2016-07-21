#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    query = "select content, time from posts order by time desc"
    # posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    # posts.sort(key=lambda row: row['time'], reverse=True)
    cursor.execute(query)
    posts = cursor.fetchall()
    #
    # update_query = "delete from posts where content like '%marquee%'"
    # cursor.execute(update_query)
    # db.commit()
    db.close()
    dicted_posts = [{'content': str(bleach.clean(str(row[1]))),
                     'time': str(row[0])} for row in posts]
    return dicted_posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # t = time.strftime('%c', time.localtime())
    # DB.append((t, content))
    bleached_content = bleach.clean(content)
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    cursor.execute("insert into posts values (%s)", (str(bleached_content),))
    db.commit()
    db.close()
