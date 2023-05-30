import psycopg2
from local_tasks.utils import PostgresCreds


# Program Purpose: pull state and city info from NIH surveys
# STEPS:
# 1. connect to NIH survey database
# 2. select state and city columns
# 3. convert to 

# database connection setup
pgc = PostgresCreds()
conn = psycopg2.connect(database=pgc.db,
                        user=pgc.user,
                        password=pgc.pw,
                        host=pgc.host,
                        port=pgc.port)
curs = conn.cursor()
conn.close()