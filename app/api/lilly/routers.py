from . import lilly_bp
from app.services.lilly_search import LillySearchTool
from flask import request, jsonify

search_tool = LillySearchTool()

@lilly_bp.route('/query', methods=['POST'])
def query_database():
    try:
        data = request.json
        if data is None:
            raise ValueError("请求体中未提供 JSON 数据")

        # 从请求体中提取参数
        user_id = data.get("user_id")
        if not user_id:
            raise ValueError("user_id 是必需的")

        tool_parameters = {
            "query": data.get("query"),
            "database": data.get("database"),
        }

        # 检查所有必需参数是否存在
        for param, value in tool_parameters.items():
            if value is None:
                raise ValueError(f"参数 '{param}' 是必需的")
        print('qqqqq',tool_parameters,user_id)
        # 调用 LillySearchTool 的 _invoke 方法
        result_message = search_tool._invoke(user_id, tool_parameters)
        print('result_message',result_message)
        return jsonify({'result': result_message}), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        return jsonify({'error': '服务器内部错误，请稍后重试'}), 500