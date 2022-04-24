import os
import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route("/hook", methods=["POST"])
def hook():
    repo_dict = {
        "mtb": {
            "folder": r"C:\code",
            "install": "npm install"
        },
        "city": {
            "folder": r"C:\code",
            "install": "pip3.9 install -r requirements.txt"
        }
    }
    # 项目名称：mtb  city
    repo_name = request.json['project']['path']
    print(repo_name)
    # 放在服务器的那个目录？
    local_info = repo_dict.get(repo_name)
    if not local_info:
        return "error"
    # 项目的父级
    parent_folder_path = local_info['folder']
    install_command = local_info['install']

    # 项目的目录
    project_file_path = os.path.join(parent_folder_path, repo_name)

    # git仓库地址 https://gitee.com/wupeiqi/mtb.git
    git_http_url = request.json['project']['git_http_url']

    # 项目目录是否存在
    if not os.path.exists(project_file_path):
        # cd c:\code
        # git clone https://gitee.com/wupeiqi/mtb.git
        subprocess.check_call('git clone {}'.format(git_http_url), shell=True, cwd=parent_folder_path)
    else:
        # cd c:\code\mtb
        # git pull origin master
        subprocess.check_call('git pull origin master', shell=True, cwd=project_file_path)

    # 安装依赖包
    # cd c:\code\mtb
    # pip3.9 install -r requirements.txt
    subprocess.check_call(install_command, shell=True, cwd=project_file_path)
    return "success"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)