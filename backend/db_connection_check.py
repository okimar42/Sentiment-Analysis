import sys
from django.db import connections
from django.db.utils import OperationalError

try:
    db_conn = connections['default']
    db_conn.cursor()
    sys.exit(0)
except OperationalError:
    sys.exit(1) 