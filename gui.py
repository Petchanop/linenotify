import tkinter as tk
import tkinter.messagebox as messagebox
import os
import subprocess
from tkinter import ttk
from tkinter import filedialog, PhotoImage
import module.line_notify as notify
import module.file_monitoring as monitor
import requests

url = 'https://notify-api.line.me/api/notify'

def create_env(name, line_token, file_path):
    if not os.path.exists(".env"):
        file = open(".env", "w", encoding="utf-8")
        token_line = f"{name}={line_token}\n"
        file_path_line = f"file_path={file_path}\n"
        file.write(token_line+file_path_line)
    else:
        file = open(".env", "a", encoding="utf-8")
        token_line = f"{name}={line_token}\n"
        file_path_line = f"file_path={file_path}\n"
        file.write(token_line+file_path_line)
    file.close()

def check_input(name, line_token, file_path):
    if os.path.exists(".env"):
        file = open(".env", "r", encoding="utf-8")
        text = file.readlines()
        file.close()
        for i in range(len(text)):
            if line_token in text[i] and i < len(text) - 1:
                if file_path in text[i + 1]:
                    return False
    return True

def process_status(process_name):
    try:
        subprocess.check_output(["pgrep", "-f", process_name])
        return True
    except subprocess.CalledProcessError:
        return False
 
def run_process(name, lineToken, folderPath, isSelected):
    if not name:
        messagebox.showwarning("Error", message="please input name.")
        return
    if not lineToken:
       messagebox.showwarning("Error", message="please input line token.")
       return 
    if not folderPath:
        messagebox.showwarning("Error", message="please input folder for monitor.")
        return
    if not isSelected:
        if not check_input(name, lineToken, folderPath):
            messagebox.showwarning("Error", message="Duplicate token and file path.")
            return
        if not check_token(lineToken):
            messagebox.showwarning("Error", message="Not a valid token.")
            return
        create_env(name, lineToken, folderPath)
    print(f"username : {name}")
    print(f"token : {lineToken}")
    print(f"monitoring: {folderPath}")
    subprocess.Popen(['python','module\\run_process.py', lineToken, folderPath, name])
        

def check_token(linetoken):
    header = {'content-type':'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + linetoken}
    payload = {'message':'test'}
    res = requests.post(url, headers=header, data=payload)
    if res.status_code != 200:
        return False
    return True

def choose_folder(folderPath):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folderPath.set(folder_selected)
        return folder_selected
    return None

def edit_file():
    subprocess.Popen(['notepad', '.env'])
    return 

def stop_process(name, path):
    taskPath = path.split("/")
    if len(taskPath) > 1:
        joinPath = '@'.join([taskPath[-2], taskPath[-1]])
    else:
        joinPath = '@'.join(taskPath)
    process = name + joinPath
    taskPath = f"{os.getcwd()[2:]}\\module"
    cmd = f"powershell Stop-ScheduledTask -TaskPath \"{taskPath}\" -TaskName \"{process}\" &"
    print(f"Stop Scheduled Task {process} in {taskPath}")
    subprocess.run(cmd, shell=True)
    cmd = f"powershell Disable-ScheduledTask -TaskPath \"{taskPath}\" -TaskName \"{process}\" &"
    print(f"Disable Scheduled Task {process} in {taskPath}")
    subprocess.run(cmd, shell=True)
    cmd = f"powershell Write-output Y | powershell Unregister-ScheduledTask -TaskName \"{process}\" &"
    print(f"Unregister Scheduled Task {process} in {taskPath}")
    subprocess.run(cmd, shell=True)
    return 

class LineNotifyFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
    
        self.name = tk.StringVar() 
        self.lineToken = tk.StringVar()
        self.folderPath = tk.StringVar()
        self.selectFromFile = False
       
        #exit button
        ttk.Button(self,text='Exit',command=lambda: [self.destroy(), exit()]).grid()
        
    def create_name_frame(self):
         #name label
        self.nameLabel = ttk.Label(self, text='Name', font=("Helvetica", 16), width=9)
        self.nameLabel.grid(column=0, row=0, padx=10, pady=5)
        
        self.nameEntry = ttk.Entry(self, textvariable=self.name, font=("Helvetica", 16), width=25)
        self.nameEntry.grid(column=1, row=0, pady=5)
        
    def create_linetoken_frame(self):
         #line token label 
        self.tokenLabel = ttk.Label(self, text='Line token', font=("Helvetica", 16), width=9)
        self.tokenLabel.grid(column=0, row=1, padx=10)
        
        #line token input
        self.tokenEntry = ttk.Entry(self, textvariable=self.lineToken, font=("Helvetica", 16), width=25)
        self.tokenEntry.focus()
        self.tokenEntry.grid(column=1, row=1)
        
        #get line token from previous session
        #<a href="https://www.flaticon.com/free-icons/automatic" title="automatic icons">Automatic icons created by Freepik - Flaticon</a>
        folder_image = PhotoImage(file="image/auto1.png")
        resize_image = folder_image.subsample(1, 1)

         #edit name
        edit_image = PhotoImage(file="image/icons8-edit-50.png")
        edit_resize_image = edit_image.subsample(2, 2)
        self.editButton = ttk.Button(self, image=edit_resize_image, command=lambda: edit_file(), width=4)
        self.editButton.image = edit_resize_image
        self.editButton.grid(column=2, row=0, padx=10, pady=5)
        
        self.autoSelect = ttk.Button(self, image=resize_image, command=lambda: select_name_token(self), width=4)
        self.autoSelect.image = resize_image
        self.autoSelect.grid(column=2, row=1, padx=10, pady=5)
                        
        def select_name_token(container):
            try:
                file = open(".env", "r", encoding="utf-8")
            except:
                file = open(".env", "x", encoding="utf-8")
            text = file.readlines()
            file.close()
            
            #create dict for new frame listbox
            name_list = {}
            for line in text:
                if "file_path" not in line:
                    line_split = line.split("=")
                    if len(line_split) != 2:
                        continue
                    name_list.update(dict({line_split[0]:line_split[1].replace("\n", "")}))
            new_frame = tk.Tk()
            new_frame.title("Select name")
            window_width = 250
            window_height = 200
             # get the screen dimension
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # find the center point
            center_x = int(screen_width / 2 - window_width / 2) + 250
            center_y = int(screen_height / 2 - window_height / 2) - 150
            
            new_frame.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
            new_frame.resizable(False, False)
            
            #insert name to listbox 
            box = tk.Listbox(new_frame, font=("Times", 16), selectmode=tk.BROWSE)
            for name in name_list.keys():
                box.insert(tk.END, name)
            
            box.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
            
            #add a scrollbar to the listbox 
            scrollbar = ttk.Scrollbar(new_frame, orient=tk.VERTICAL, command=box.yview)
            box['yscrollcommand'] = scrollbar.set

            scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)
            
            #select name from listbox by mouse double click event 
            def select_name(event):
                selected_item = box.curselection()
                if selected_item:
                    name = box.get(selected_item)
                    container.name.set(name)
                    container.lineToken.set(name_list[name])
                    container.selectFromFile = True
            
            #bind double click event to listbox 
            box.bind('<Double-Button-1>', select_name)
            ttk.Button(new_frame, text="Close Tkinter Window", command=[new_frame.quit()]).pack()
            new_frame.mainloop()
    
    def create_folder_frame(self):
        #folder path lavbel
        self.folderLabel = ttk.Label(self, text='Path',font=("Helvetica", 16), width=9)
        self.folderLabel.grid(column=0, row=2, padx=10)

        #folder path input
        self.folderEntry = ttk.Entry(self, textvariable=self.folderPath, font=("Helvetica", 16), width=25)
        self.folderEntry.grid(column=1, row=2)
       
        #select folder button 
        folder_image = PhotoImage(file="image/icons8-folder-48.png")
        resize_image = folder_image.subsample(2, 2)
        
        self.selectFolder = ttk.Button(self, image=resize_image, command=lambda: choose_folder(self.folderPath), width=5)
        self.selectFolder.image = resize_image
        self.selectFolder.grid(column=2, row=2, padx=10, pady=5)
        
    def create_button_frame(self):
       
        #start button
        self.button_frame = ttk.Frame(self)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.start_button = ttk.Button(self.button_frame,text='Start',command=lambda: run_process(self.nameEntry.get(), self.tokenEntry.get(), self.folderEntry.get(), self.selectFromFile))
        self.start_button.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        
        #stop button
        self.stop_button = ttk.Button(self.button_frame,text='Stop',command=lambda: stop_process(self.nameEntry.get(), self.folderPath.get()))
        self.stop_button.grid(column=1, row=2, pady=5)
        
        #help button
        self.help_button = ttk.Button(self.button_frame,text='Help', command=print("help"))
        self.help_button.grid(column=2, row=2, padx=5, pady=5)
        
        self.button_frame.grid(column=0, row=3, columnspan=3, pady=5)
       
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Line notify")
        
        window_width = 500
        window_height = 200

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.__create_widgets()
        
    def __create_widgets(self):
        frame = LineNotifyFrame(self)
        frame.create_name_frame()
        frame.create_linetoken_frame()
        frame.create_folder_frame()
        frame.create_button_frame()
        frame.grid(row=0, column=0, pady=10)

if __name__ == "__main__":
    if sys.prefix != sys.base_prefix:
        cmd = f"python -m venv ."
        subprocess.run(cmd, shell=True)
        print("Activate python enviroment.")
    # app = App()
    # app.mainloop()


# pyinstaller --onefile 'C:\Users\nop_h\OneDrive\Desktop\lineNotifyForWindows11\gui.py' --add-data='C:\Users\nop_h\OneDrive\Desktop\lineNotifyForWindows11\module\line_notify.py:module' --add-data='C:\Users\nop_h\OneDrive\Desktop\lineNotifyForWindows11\module\file_monitoring.py:module' --add-data='C:\Users\nop_h\OneDrive\Desktop\lineNotifyForWindows11\module\run_process.py:module' --add-data='C:\Users\nop_h\OneDrive\Desktop\lineNotifyForWindows11\AutoConfig.ps1:script'

