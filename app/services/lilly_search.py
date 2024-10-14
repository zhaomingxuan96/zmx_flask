import os
import sys
from typing import Any, Union
from dotenv import load_dotenv
import psycopg2

load_dotenv() # load .env file

DATABASES = {
    "DATABASE1": {
        "HOST": os.getenv('DATABASE1_HOST'),
        "PORT": os.getenv('DATABASE1_PORT'),
        "USERNAME": os.getenv('DATABASE1_USERNAME'),
        "PASSWORD": os.getenv('DATABASE1_PASSWORD'),
        "DATABASE": os.getenv('DATABASE1_DATABASE'),
        "DBSCHEMA": os.getenv('DATABASE1_DBSCHEMA')
    },
    "DATABASE2": {
        "HOST": os.getenv('DATABASE2_HOST'),
        "PORT": os.getenv('DATABASE2_PORT'),
        "USERNAME": os.getenv('DATABASE2_USERNAME'),
        "PASSWORD": os.getenv('DATABASE2_PASSWORD'),
        "DATABASE": os.getenv('DATABASE2_DATABASE'),
        "DBSCHEMA": os.getenv('DATABASE2_DBSCHEMA')
    },
    "DATABASE3": {
        "HOST": os.getenv('DATABASE3_HOST'),
        "PORT": os.getenv('DATABASE3_PORT'),
        "USERNAME": os.getenv('DATABASE3_USERNAME'),
        "PASSWORD": os.getenv('DATABASE3_PASSWORD'),
        "DATABASE": os.getenv('DATABASE3_DATABASE'),
        "DBSCHEMA": os.getenv('DATABASE3_DBSCHEMA')
    }
}

class LillySearchTool():
    def _invoke(self, 
                user_id: str,
               tool_parameters: dict[str, Any], 
        ) :
        """
            invoke tools
        """
        query = tool_parameters['query']
        databasecode = tool_parameters['database']
        host = DATABASES[databasecode]["HOST"]
        dbuser = DATABASES[databasecode]["USERNAME"]
        database = DATABASES[databasecode]["DATABASE"]
        dbpassword = DATABASES[databasecode]["PASSWORD"]
        dbschema = DATABASES[databasecode]["DBSCHEMA"]
        # TODO:  filter sql format,can only be 'select'
        if not query:
            return 'Please input query'
        # api_key = self.runtime.credentials['serpapi_api_key']
        result = self.GetData(query,host,database,dbuser,dbpassword,dbschema)
        return result
    
    def GetData(self,
                sql: any,
                host: str,
                database: str,
                dbuser: str,
                dbpassword: str,
                dbschema: str):
        """
          获取数据
        """
        conn = None
        cur = None
        result =""
        if not dbschema:
            dbschema = "public"
        try:
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=dbuser,
                password=dbpassword
            )
            cur = conn.cursor()
            # 设置搜索路径（schema）
            cur.execute("SET search_path TO %s", (dbschema,))
            cur.execute(sql)
            rows = cur.fetchall()

            # 检查行数是否大于0
            if len(rows) > 0:
                # 获取列名
                columns = [desc[0] for desc in cur.description]

                # 构建Markdown表格
                result = "| " + " | ".join(columns) + " |\n"
                result += "| " + " | ".join(["---"] * len(columns)) + " |\n"
                for row in rows:
                    result += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        except (Exception, psycopg2.Error) as error:
            result = "ERROR:" + str(error)
        finally:
            # 关闭游标和连接
            if cur:
                cur.close()
            if conn:
                conn.close()
        return result
