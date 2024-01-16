import subprocess
import os
from .config import WEB_RUN_SHELL_PATH, WEB_TOOL_DIR, ANALYSIS_MUTATION_SCORE_PY_PATH
import importlib.util

def execShell(run_dir_path, run_case_num):

    # 定义要执行的 shell 命令
    shell_command = "cd " + WEB_TOOL_DIR + "; " \
                    + "bash " +  WEB_RUN_SHELL_PATH + " " + run_dir_path + " " + str(run_case_num)
    print("exec: " + shell_command)
    # 使用 subprocess.run 执行 shell 命令
    # result = subprocess.run(shell_command, shell=True, capture_output=True, text=True)
    result = subprocess.run(shell_command, shell=True)

    # 打印命令执行结果
    print("Exit code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)

def getActualRunCaseNum(run_dir_path):
    log_dir = os.path.join(run_dir_path, "log")
    log_file_ran_path = os.path.join(log_dir, "ran")

    actual_run_case_num = os.path.getsize(log_file_ran_path)
    print(log_file_ran_path)
    print(actual_run_case_num)
    return actual_run_case_num

def getMutOutputFilesForCase(case_dir):
    mutOutputFilesForCase = {}
    contents = os.listdir(case_dir)
    contents.sort()
    file_need_check = []
    for content in contents:
        if content.startswith("mut_output-0-"):
            file_name = content.split("mut_output-0-")[1]
            mutOutputFilesForCase[file_name] = []
            file_need_check.append(file_name)
    
    for content in contents:
        if content.startswith("mut_output-"):
            for file_name in file_need_check:
                if content.endswith(file_name):
                    fileJson = {}
                    fileJson['name'] = content
                    fileJson['path'] = os.path.join(case_dir, content)
                    mutOutputFilesForCase[file_name].append(fileJson)
    return mutOutputFilesForCase



def getMutOutputFilesForRun(run_dir_path):
    run_case_mutOutputFiles = {}

    log_dir = os.path.join(run_dir_path, "log")
    log_run_dir = os.path.join(log_dir, "run")

    items = os.listdir(log_run_dir)
    items.sort()
    for item in items:
        item_path = os.path.join(log_run_dir, item)
        assert os.path.isdir(item_path) and f"{item_path} not a case dir!\n"
        
        run_case_mutOutputFiles[item] = {}
        run_case_mutOutputFiles[item]['case_dir'] = item_path
        run_case_mutOutputFiles[item]['mutOutputFiles'] = getMutOutputFilesForCase(item_path)
    return run_case_mutOutputFiles


def import_mutation_score_py():
    # 构建文件路径
    file_path = ANALYSIS_MUTATION_SCORE_PY_PATH

    # 使用 importlib.util 来创建一个模块规范
    spec = importlib.util.spec_from_file_location("mutation_score", file_path)

    # 使用模块规范来加载模块
    module = importlib.util.module_from_spec(spec)

    # 执行加载模块的动作
    spec.loader.exec_module(module)

    return module

def getRunStat(run_dir_path):
    ms_module = import_mutation_score_py()
    run = ms_module.Run(run_dir_path)
    print(run.getRunStat())
    return run.getRunStatJson()

