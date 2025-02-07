import tkinter as tk
from tkinter import messagebox
import os
import json
from cryptography.fernet import Fernet

# 生成新的 Fernet 密鑰
new_key = Fernet.generate_key()
print(new_key.decode())

# 設定加密密鑰，確保每次執行時相同
SECRET_KEY = b'生成的密鑰'  # 確保是32字節
cipher = Fernet(SECRET_KEY)

# 儲存檔案名稱
DATA_FILE = "hosts.json"

# 初始化儲存資料
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# 加密與解密函式
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# 介面主程式
class RDSManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows RDS 遠端桌面管理器")
        self.root.geometry("500x400")

        # 主機列表
        self.hosts = self.load_hosts()

        # 元件
        self.name_label = tk.Label(root, text="主機名稱：")
        self.name_label.grid(row=0, column=0, pady=5, sticky="e")
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        self.ip_label = tk.Label(root, text="IP 位址：")
        self.ip_label.grid(row=1, column=0, pady=5, sticky="e")
        self.ip_entry = tk.Entry(root, width=30)
        self.ip_entry.grid(row=1, column=1, pady=5)

        self.password_label = tk.Label(root, text="密碼：")
        self.password_label.grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        self.add_button = tk.Button(root, text="新增主機", command=self.add_host)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.list_label = tk.Label(root, text="已儲存的主機：")
        self.list_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.host_listbox = tk.Listbox(root, width=60, height=10)
        self.host_listbox.grid(row=5, column=0, columnspan=2)
        self.host_listbox.bind("<Double-1>", self.connect_host)

        self.load_listbox()

    def load_hosts(self):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def save_hosts(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.hosts, f)

    def add_host(self):
        name = self.name_entry.get()
        ip = self.ip_entry.get()
        password = self.password_entry.get()

        if not name or not ip or not password:
            messagebox.showerror("錯誤", "請填寫所有欄位！")
            return

        encrypted_password = encrypt_password(password)

        # 儲存主機
        self.hosts.append({"name": name, "ip": ip, "password": encrypted_password})
        self.save_hosts()

        # 更新列表
        self.load_listbox()

        # 清空輸入框
        self.name_entry.delete(0, tk.END)
        self.ip_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "主機已新增！")

    def load_listbox(self):
        self.host_listbox.delete(0, tk.END)
        for host in self.hosts:
            self.host_listbox.insert(tk.END, f"{host['name']} ({host['ip']})")

    def connect_host(self, event):
        selected_index = self.host_listbox.curselection()
        if not selected_index:
            return

        selected_host = self.hosts[selected_index[0]]
        password = decrypt_password(selected_host["password"])

        # 使用 mstsc 啟動遠端桌面
        command = f"cmd /c mstsc /v:{selected_host['ip']} /prompt"
        os.system(command)

# 主程式執行
if __name__ == "__main__":
    root = tk.Tk()
    app = RDSManager(root)
    root.mainloop()