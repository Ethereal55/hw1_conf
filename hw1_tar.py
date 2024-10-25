import tkinter as tk
import tarfile

def emu():
    global path
    com = input_area.get("1.0", tk.END).strip()[2:]  # Удаляем лишние пробелы
    
    # Открываем tar-архив
    with tarfile.open("files.tar", "r") as mytar:
        # Получаем список всех путей в архиве
        members = mytar.getmembers()
        
        # Выводим содержимое архива для отладки
        print("Members in tar:", [member.name for member in members])  # Отладочный вывод

        # Обработка команды ls
        if com == "ls":
            output_area.insert(tk.END, "/".join(path) + ":\n")
            for member in members:
                dir_structure = member.name.lstrip('/.').split('/')
                if dir_structure[:-1] == path:
                    output_area.insert(tk.END, dir_structure[-1] + " ")
            output_area.insert(tk.END, "\n")
        
        # Обработка команды exit
        elif com == "exit":
            root.quit()
        
        # Обработка команды cd
        elif com.startswith("cd "):
            new_path = com.split(" ")[1].strip()
            
            if new_path == "/":
                path.clear()  # Переход в корневую директорию
            
            elif new_path == "..":
                if path:       # Переход на уровень вверх
                    path.pop()
            
            else:
                temp_path = path + [p for p in new_path.split("/") if p]
                
                # Проверка, существует ли путь в архиве
                path_exists = any(
                    member.name.lstrip('/.').split('/')[:len(temp_path)] == temp_path for member in members
                )
                
                if path_exists:
                    path = temp_path  # Обновляем путь, если существует
                else:
                    output_area.insert(tk.END, f"cd: {new_path}: No such directory\n")
        
        # Обработка команды cat
        elif com.startswith("cat "):
            file_name = com.split(" ")[1].strip()
            full_path = "/".join(path + [file_name])
            
            # Отладочные выводы
            print("Current path:", "/".join(path))
            print("Full path to file:", full_path)

            try:
                member = mytar.getmember(full_path)  # Получаем член архива
                print("Found member:", member.name)  # Отладочный вывод
                with mytar.extractfile(member) as file:
                    if file:  # Проверяем, что файл существует
                        output_area.insert(tk.END, file.read().decode('utf-8') + "\n")
            except (KeyError, FileNotFoundError):
                output_area.insert(tk.END, f"cat: {file_name}: No such file\n")
        
        # Обработка команды wc
        elif com.startswith("wc "):
            file_name = com.split(" ")[1].strip()
            full_path = "/".join(path + [file_name])
            
            # Отладочные выводы
            print("Current path:", "/".join(path))
            print("Full path to file:", full_path)

            try:
                member = mytar.getmember(full_path)  # Получаем член архива
                print("Found member:", member.name)  # Отладочный вывод
                with mytar.extractfile(member) as file:
                    if file:  # Проверяем, что файл существует
                        content = file.read().decode('utf-8')
                        line_count = content.count('\n') + 1
                        word_count = len(content.split())
                        byte_count = len(content.encode('utf-8'))
                        output_area.insert(tk.END, f"количество строк: {line_count} количество слов: {word_count} количество символов: {byte_count} имя: {file_name} \n")
            except (KeyError, FileNotFoundError):
                output_area.insert(tk.END, f"wc: {file_name}: No such file\n")
        
    # Очищаем и обновляем приглашение
    input_area.delete("1.0", tk.END)
    input_area.insert(tk.END, "$ ")

# Инициализация GUI
path = []
root = tk.Tk()
root.title("Shell Emulator")
output_area = tk.Text(root, height=20, width=100)
output_area.pack(pady=10)
input_area = tk.Text(root, height=2, width=100)
input_area.pack(pady=10)
execute_button = tk.Button(root, text="Enter", command=emu)
execute_button.pack(pady=5)
input_area.insert(tk.END, "$ ")
root.mainloop()
