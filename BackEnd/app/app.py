from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import time
import os
from datetime import datetime
from utils import create_rundir, create_makefile, get_demo_src, exec_shell, config

app = Flask(__name__)
CORS(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/api/get_file_content', methods=['POST'])
def get_file_content():
    # 获取前端传递的文件路径
    file_path = request.json['file_path']  # 假设前端以JSON格式传递文件路径

    # 读取文件内容
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        print(file_path)
        print(file_content)
        return {'content': file_content}
    except FileNotFoundError:
        return {'error': 'File not found'}, 404

@app.route('/api/web_run', methods=['POST'])
def web_run():
    ret = {}
    run_case_list = request.json    # [{'file': 'quick_sort', 'argv': '11 22 33 44 55 66'}, {'file': 'quick_sort', 'argv': '11 22 33 44 55 66'}]
    
    # timestamp = int(time.time())
    # run_dir_name = str(timestamp)

    run_dir_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    run_dir_path = create_rundir.createRunDir(run_dir_name)
    if run_dir_path:
        ret["rundir"] = True
        create_makefile.generateMakefile(run_dir_path, run_case_list)
        run_case_num = len(run_case_list)
        exec_shell.execShell(run_dir_path, run_case_num)

        # check run case 
        actual_run_case_num = exec_shell.getActualRunCaseNum(run_dir_path)
        ret['runcase'] = f"{actual_run_case_num}/{run_case_num}"
        if actual_run_case_num != run_case_num:
            return jsonify(ret)
        
        # build ret: OUTPUT file 
        ret['mutOutputFilesForRun'] = exec_shell.getMutOutputFilesForRun(run_dir_path)
        ret['runStat'] = exec_shell.getRunStat(os.path.join(run_dir_path, "log", "run"))


    else:
        ret['rundir'] = False
    return jsonify(ret)

@app.route('/api/testGetMutOutputFiles')
def test_get_mutoutput_file():
    ret = {}
    ret['data'] = exec_shell.getMutOutputFilesForRun("/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05")
    return jsonify(ret)

@app.route('/api/testGetRunStatJson')
def test_get_runstat_json():
    ret = {}
    ret['data'] = exec_shell.getRunStat("/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/new-subjects/result/tests/AccMutNo-2024-01-15-23-31-32/run")
    return jsonify(ret)

@app.route('/api/get_demo_src')
def app_get_demo_src():
    ret = {}
    ret['data'] = get_demo_src.getDemoSrc()
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True)
