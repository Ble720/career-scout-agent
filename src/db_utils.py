import os
from psycopg_pool import ConnectionPool

def bootstrap_database(db_pool: ConnectionPool) -> None:
    """
    Decoupled database migration engine.
    Reads 'init.sql' dynamically and executes it as an atomic transaction.
    """
    print("Verifying database tables and pgvector schemas...")
    
    with db_pool.connection() as conn:
        try:
            sql_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "init.sql")
            
            if not os.path.exists(sql_filepath):
                sql_filepath = "init.sql"
                
            with open(sql_filepath, "r") as f:
                sql_script = f.read()
                
            with conn.cursor() as cur:
                cur.execute(sql_script)
            
            print("PostgreSQL and pgvector initialized successfully.")
            
        except Exception as e:
            print(f"Critical Migration Failure: Could not bootstrap database: {e}")
            raise e
