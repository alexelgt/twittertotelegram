# twittertotelegram
# Copyright (C) 2022 Alexelgt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import MySQLdb

from twittertotelegram.config import SQL_USER, SQL_PASSWORD, SQL_DATABASE

def get_since_id(screen_name):
    db = MySQLdb.connect("localhost", SQL_USER, SQL_PASSWORD, SQL_DATABASE)
    c= db.cursor()

    try:
        sql_query = "SELECT since_id FROM twitter_info WHERE screen_name = %s"
        c.execute(sql_query, (screen_name, ))
        result = c.fetchall()
    except:
        db.rollback()
        result = []

    c.close()
    db.close()

    if len(result) == 0:
        return None

    return result[0][0]

def update_since_id(screen_name, since_id):
    db = MySQLdb.connect("localhost", SQL_USER, SQL_PASSWORD, SQL_DATABASE)
    c= db.cursor()

    try:
        sql_query = "INSERT INTO twitter_info (`screen_name`, `since_id`) VALUES (%s, %s);"
        c.execute(sql_query, (screen_name, since_id))
        db.commit()
    except:
        db.rollback()

        try:
            sql_query = "UPDATE twitter_info SET since_id = %s WHERE screen_name = %s"
            c.execute(sql_query, (since_id, screen_name))
            db.commit()
        except:
            db.rollback()

    c.close()
    db.close()