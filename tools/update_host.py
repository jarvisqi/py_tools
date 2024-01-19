
import subprocess
import requests
from datetime import datetime  

url="https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts?ref_type=heads";
tmp_host="/tmp/host.txt";
host_path="/etc/hosts"

def update():
    res= requests.get(url)
    if res.status_code==200:
        file = open(tmp_host, "w")
        # 将内容写入文件
        file.write(res.text)
        # 关闭文件
        file.close()

        # 删除第11行及以下的所有内容  
        with open(host_path, 'r') as original_file:  
            original_lines = original_file.readlines()  
            # 删除第二行及以下的所有内容  
            new_lines = original_lines[:11] + [''] * (len(original_lines) - 11)  
            original_file.close()

            with open(tmp_host, 'r') as tmp_file:  
                lines = tmp_file.readlines()  
                end=len(lines)
                update_data=lines[2:end]
                string_data = str(update_data)
                for k in update_data:
                    new_lines.append(k)
                tmp_file.close()

            # 写回到文件  
            with open(host_path, 'w') as new_file:  
                for item in new_lines:
                    new_file.write(item)  
                new_file.close()

    print("host已经更新",datetime.now(),"\n")

    try:  
        subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"])  
        print("DNS缓存已刷新")  
    except subprocess.CalledProcessError:  
        print("刷新DNS缓存失败")  

if __name__ == '__main__':
    # main()
    update()