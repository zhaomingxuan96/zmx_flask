import os
import sys
from typing import Any, Union

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool
import psycopg2

class LillySearchTool(BuiltinTool):
    def _invoke(self, 
                user_id: str,
               tool_parameters: dict[str, Any], 
        ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        query = tool_parameters['query']
        host = tool_parameters['host']
        database = tool_parameters['database']
        dbuser = tool_parameters['dbuser']
        dbpassword = tool_parameters['dbpassword']
        dbschema = tool_parameters['dbschema']
        # TODO:  filter sql format,can only be 'select'
        if not query:
            return self.create_text_message('Please input query')
        # api_key = self.runtime.credentials['serpapi_api_key']
        result = self.GetData(query,host,database,dbuser,dbpassword,dbschema)
        return self.create_text_message(text=result)
    
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
