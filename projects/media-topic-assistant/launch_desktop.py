"""Desktop entry point: reuse the local studio or start it, then open the browser."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser


URL = 'http://127.0.0.1:8765/'
ROOT = Path(__file__).resolve().parent
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def ready():
    try:
        with OPENER.open(URL + 'api/studio/weekly', timeout=2) as response:
            data = json.load(response)
            return response.status == 200 and isinstance(data, dict) and {'week_start', 'budget_hours', 'tasks'} <= data.keys()
    except (OSError, urllib.error.URLError, ValueError):
        return False


def port_busy():
    with socket.socket() as connection:
        connection.settimeout(1)
        return connection.connect_ex(('127.0.0.1', 8765)) == 0


def spawn_service(root):
    python = root / '.venv' / 'Scripts' / 'python.exe'
    if not python.is_file():
        raise RuntimeError('尚未安装运行环境，请先运行项目中的 start.cmd 完成初始化。')
    logs = root / 'data' / 'launcher'
    logs.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    executable = str(python)
    options = {}
    if os.name == 'nt':
        # Match Easel: avoid the venv redirector tying the background service
        # to the lifetime of the short-lived launcher window.
        executable = sys._base_executable
        env['__PYVENV_LAUNCHER__'] = str(python)
        options['creationflags'] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    command = [executable, '-m', 'uvicorn', 'app:create_app', '--factory', '--host', '127.0.0.1', '--port', '8765']
    with (logs / 'server.log').open('a', encoding='utf-8') as output, (logs / 'error.log').open('a', encoding='utf-8') as error:
        return subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=output, stderr=error, **options)


def launch(root=ROOT, open_browser=True):
    if not ready():
        if port_busy():
            raise RuntimeError('8765 端口已被旧版服务或其他程序占用。请先关闭旧启动窗口，再双击快捷方式。')
        process = spawn_service(root)
        deadline = time.monotonic() + 45
        while not ready():
            if process.poll() is not None:
                raise RuntimeError(f'启动失败，请查看日志：{root / "data" / "launcher" / "error.log"}')
            if time.monotonic() >= deadline:
                raise RuntimeError(f'启动等待超时，请查看日志后重试：{root / "data" / "launcher" / "error.log"}')
            time.sleep(.3)
    if open_browser:
        webbrowser.open(URL)


if __name__ == '__main__':
    try:
        launch(open_browser='--no-browser' not in sys.argv)
        print('Studio ready: ' + URL)
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
