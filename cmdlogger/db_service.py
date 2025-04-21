from collections import defaultdict
from multiprocessing import Lock
from queue import Queue
import sqlite3

class DBConnectionPoolService:
    """
    DB connection pool service class for database access
    """
    lock = Lock()

    def __init__(self, max_connections=3):
        self._max_connections = max_connections
        self._pools = defaultdict(Queue)
        self._locks = defaultdict(Lock)

    def get_connection(self, db_path):
        """
        Gets an usable connection to a DB 
        """
        with self.lock:
            if db_path not in self._pools:
                self._pools[db_path] = Queue(self._max_connections)
                for _ in range(self._max_connections):
                    conn = sqlite3.connect(db_path)
                    self._pools[db_path].put(conn)

            db_lock = self._locks[db_path]
            db_pool = self._pools[db_path]

            with db_lock:
                if db_pool.empty():
                    return sqlite3.connect(db_path)
            return db_pool.get()
        
    def release_connection(self, db_path, conn):
        """
        Release prior connection
        """
        with self.lock:
            self._pools[db_path].put(conn)

    def clear_all(self):
        """
        Clear all connections to all DB
        """
        with self.lock:
            for _, pool in self._pools.items():
                while not pool.empty():
                    try:
                        conn = pool.get_nowait()
                        conn.close()
                    except:
                        continue


class DatabaseService:
    """Helper class for database access"""

    def __init__(self, dbconnpoolserv: DBConnectionPoolService):
        self.db_pool_service = dbconnpoolserv

    def create_database(self, db):
        conn = self.db_pool_service.get_connection(db)
        conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS cmd (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       cmd TEXT NOT NULL,
                       date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );

''')
        conn.commit()
        self.db_pool_service.release_connection(conn=conn)

    def delete_database(self, db):
        pass

    def execute_save(self, db, cmd):
        conn = self.db_pool_service.get_connection(db)
        cursor = conn.cursor()

        cursor.execute('''
CREATE TABLE IF NOT EXISTS cmd (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       cmd TEXT NOT NULL,
                       date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );

''')
        cursor.execute('INSERT INTO cmd (cmd) VALUES (?)', (cmd, ))
        conn.close()

    def execute_fetch(self, db, query, params=()):
        pass




