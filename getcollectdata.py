from flask import Flask
from flask import jsonify, request
from flask_cors import CORS

import getconfigdata

'''
Flask - Web 框架

'''

app = Flask(__name__)
cors = CORS(app, resources={r"/api/get_page_collect_data": {"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/get_page_collect_data', methods=['GET', 'POST'])
def get_page_collect_data():
    # 通过 args 属性访问 URL 中提交的请求参数（?key=value）
    args = request.args  # dict 类型
    data_type = args['type']
    msg = ''
    new_datas = []
    # 读取收集到的 打印数据
    try:
        # 这里可换成配置文件中的路径名
        datas = getconfigdata.get_collect_json_data('./file/app.txt')
            

        if datas and len(datas) > 0:
            # 筛选出其中合理的数据，也即是能正常打开的Activity
            new_datas = getconfigdata.get_collect_page_valid(datas)

            # 对列表按照 ThisTime 排序
            new_datas.sort(key=lambda item: int(item['ThisTime']))
            # 筛选出大于250的数据
            # 列表生成式效率更高： [item for item in new_datas if int(item['ThisTime']) >= 200]
            # new_datas = list(filter(lambda item: int(item['ThisTime']) >= 200, new_datas))
        # print(new_datas)

    except ValueError as e:
        msg = 'Unfortunately, catch error !'
        print('catch error:', e)
    # 注意：这里构造的数据必须有对应的类型，
    response = {
        'type': data_type,
        'total': len(new_datas),
        'data': new_datas,
        'msg': msg,
    }

    # 响应json串
    return jsonify(response)


if __name__ == '__main__':
    app.run()
    # app.run(host='your ip')

