from django.db import connection
from django.core import serializers



def test_custom_sql():
    with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM test_table WHERE baz = %s", [self.baz])
        cursor.execute("SELECT shop_asst_name,shop_asst_desc FROM test_table")
        row = cursor.fetchall()
        json_data = serializers.serialize('json', row)
    return row

# CREATE TABLE test_table (
#  cus_id         TEXT,
#  shop_id        TEXT,
#  product_id     TEXT,
#  trx_id         TEXT,
#  shop_asst_name TEXT,
#  shop_asst_desc TEXT
# );
