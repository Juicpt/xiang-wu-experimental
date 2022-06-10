import os

import snowflake.connector as sf_conn

_SNOWFLAKE_CONTEXT = None


def snowflake_run_query(sql):
    global _SNOWFLAKE_CONTEXT
    if _SNOWFLAKE_CONTEXT is None:
        _SNOWFLAKE_CONTEXT = sf_conn.connect(
            user="xiang_wu",
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account="opensea.us-east-1",
        )

    cs = _SNOWFLAKE_CONTEXT.cursor()
    cs.execute(sql)
    return cs.fetch_pandas_all()
