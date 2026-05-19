import os
import time
import platform
import shutil
import subprocess
import requests
import tempfile
from datetime import datetime

hosts_url = "https://hosts.gitcdn.top/hosts.txt"


def get_hosts_path():
    """根据操作系统返回hosts文件路径"""
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system == "Darwin":  # macOS
        return "/etc/hosts"
    else:
        raise OSError(f"不支持的操作系统: {system}")


def backup_hosts(hosts_path):
    """备份hosts文件"""
    backup_path = f"{hosts_path}.backup.{time.strftime('%Y%m%d%H%M%S')}"
    try:
        shutil.copy2(hosts_path, backup_path)
        print(f"已备份原有hosts文件到: {backup_path}")
        return True
    except Exception as e:
        print(f"备份hosts文件失败: {str(e)}")
        return False


def download_hosts_tempfile(url):
    """下载hosts文件到临时目录，返回文件路径"""
    try:
        # 将Gitee的blob地址转换为raw地址
        raw_url = url.replace("blob", "raw")
        print(f"正在从原始地址下载: {raw_url}")

        response = requests.get(raw_url, timeout=10)
        response.raise_for_status()

        # 创建临时文件
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, suffix=".hosts"
        ) as temp_file:
            temp_file.write(response.text.strip())
            temp_path = temp_file.name
            print(f"临时文件已保存到: {temp_path}")

        return temp_path

    except Exception as e:
        print(f"下载hosts失败: {str(e)}")
        return None


def read_temp_hosts(temp_path):
    """读取临时hosts文件内容"""
    try:
        with open(temp_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取临时文件失败: {str(e)}")
        return None


def delete_temp_file(temp_path):
    """删除临时文件"""
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"临时文件已删除: {temp_path}")
    except Exception as e:
        print(f"删除临时文件失败: {str(e)}")


def update_hosts(hosts_path, new_content):
    """用新内容覆盖hosts文件"""
    try:
        with open(hosts_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"hosts文件更新成功")
        return True
    except PermissionError:
        print("权限不足，请以管理员身份运行脚本（Windows）或使用sudo（macOS）")
        return False
    except Exception as e:
        print(f"更新hosts文件失败: {str(e)}")
        return False


def flush_dns(system):
    if system == "Windows":
        # Windows 刷新 DNS 缓存命令
        subprocess.run(["ipconfig", "/flushdns"], check=True)
        print("Windows DNS 缓存已刷新")
    elif system == "Darwin":  # macOS
        # macOS 刷新 DNS 缓存命令
        subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=True)
        print("macOS DNS 缓存已刷新")
    else:
        print(f"不支持的操作系统: {system}")


def main():
    print(f"准备从以下URL更新hosts: {hosts_url}")

    # 下载到临时文件
    temp_path = download_hosts_tempfile(hosts_url)
    if not temp_path:
        print("获取hosts内容失败，更新中止")
        return

    # 读取临时文件内容
    new_hosts_content = read_temp_hosts(temp_path)
    if not new_hosts_content:
        delete_temp_file(temp_path)
        return
    system_name = platform.system()
    # 获取系统信息和hosts路径
    try:
        print(f"检测到操作系统: {system_name}")
        hosts_path = get_hosts_path()
        print(f"hosts文件路径: {hosts_path}")
    except OSError as e:
        print(e)
        delete_temp_file(temp_path)
        return

    # 备份原有hosts文件
    if not backup_hosts(hosts_path):
        print("备份失败，是否继续更新？(y/n)")
        if input().lower() != "y":
            delete_temp_file(temp_path)
            return

    # 更新hosts文件
    update_success = update_hosts(hosts_path, new_hosts_content)

    # 无论成功与否都删除临时文件
    delete_temp_file(temp_path)

    # 更新成功后刷新DNS
    if update_success:
        flush_dns(system_name)


if __name__ == "__main__":
    main()
