class FileSystem: 
    def __init__(self, total_space=64*1024, block_size=512): 
        self.total_space = total_space 
        self.block_size = block_size 
        self.total_blocks = total_space // block_size 
        self.free_blocks = self.total_blocks 
        self.blocks_map = [0] * self.total_blocks
        self.file_data = "files_data.txt"
        self.current_directory = Folder("/", [""])
        self.root = self.current_directory

    def check_path(self, path_dirs):
        current_dir = self.root
        for i in range(len(path_dirs)-1):      
            if current_dir.to_dir(path_dirs[i+1]) == -1: 
                print("There is no such way")
                return False                
            current_dir = current_dir.to_dir(path_dirs[i+1])
        return True

    def to_path(self, path_dirs):
        current_dir = self.root
        if path_dirs == ["", ""]:
            return self.root
        for i in range(len(path_dirs)-1):            
            if current_dir.to_dir(path_dirs[i+1]) == -1: 
                print("There is no such way")
                return False
            current_dir = current_dir.to_dir(path_dirs[i+1])
        return current_dir

    def display_file_system(self, subfolder="cur"):
        folder = self.current_directory
        if subfolder != "cur":
            folder = subfolder
        print(f"total space {self.total_blocks*self.block_size//1024} Kb / free space {self.free_blocks*self.block_size//1024} Kb")
        print(f"total blocks {self.total_blocks} / free blocks {self.free_blocks}")
        print("Current Directory: ", folder.name) 
        print("Files: ")
        for file in folder.files:
            print("- File Name: " + file.name + ", Size: " + str(file.size))
        print("Directories: ")
        for subfolder in folder.folders:
            print("- Folder Name: " + subfolder.name)
            #self.display_file_system(subfolder)

    def display_blocks_map(self):         
        print(f"total_blocks {self.total_blocks} / free_blocks {self.free_blocks}")   
        print("-"*32, end="")       
        for i, block in enumerate(self.blocks_map):            
            if i % 16 == 0:
                print()
            print('X' if block == 1 else '.', end=' ')        
        print()
        print("-"*32)
        
    def allocate_blocks(self, file):
        num_blocks_needed = file.size // self.block_size        
        if file.size % self.block_size != 0:
            num_blocks_needed += 1      
        for i in range(self.total_blocks):
            if num_blocks_needed == 0:                
                break
            if self.blocks_map[i] == 0:                    
                num_blocks_needed -= 1
                self.blocks_map[i] = 1
                file.ind.append(i) 
        self.free_blocks -= len(file.ind)
        
    def add_file(self, file_name, size, path="cur"):   
        folder = self.current_directory
        if path != "cur":
            if self.check_path(path):
                folder = self.to_path(path)   
            else:
                return
        if self.free_blocks * self.block_size < size:            
            print("Not enough space to create the file")   
            return 
        if  folder.parent != None:
            if any(file.name == file_name for file in folder.files):
                print("File with the same name already exists")                
                return        
        folder.add_file(file_name, size)
        self.allocate_blocks(folder.files[-1])        
        #print(f"Total {self.total_blocks}, Free {self.free_blocks}")
        print("File {} created successfully".format(file_name))

    def add_folder(self, folder_name, path="cur"):   
        folder = self.current_directory  
        if path != "cur":
            if self.check_path(path):
                folder = self.to_path(path)
        if any(fol.name == folder_name for fol in folder.folders):
            print("folder with the same name already exists")                
            return
        folder.add_folder(folder_name)

    def remove_file(self, file_name, path="cur"):
        folder = self.current_directory
        if path != "cur":
            if self.check_path(path):
                folder = self.to_path(path)
        names_files = list(map(lambda i: i.name, folder.files))
        if file_name not in names_files:
            print("File not found")            
            return 
        for i in range(len(folder.files)):
            if folder.files[i].name == file_name:
                file = folder.files[i]
        for i in range(len(file.ind)):
            self.blocks_map[file.ind[i]] = 0    
            self.free_blocks += 1
        print("File {} deleted successfully".format(file_name))
        folder.remove_file(file_name)

    def remove_folder(self, folder_name, path="cur"):
        folder = self.current_directory
        if path != "cur":
           if self.check_path(path):
                folder = self.to_path(path)
        names_dirs = list(map(lambda i: i.name, folder.folders))
        if folder_name not in names_dirs:
            print("Folder not found")            
            return 
        folder_to_remove = None
        for dir in folder.folders:
            if dir.name == folder_name:
                folder_to_remove = dir
                break
        for file in folder_to_remove.files:
            self.remove_file(file.name, path=folder_to_remove.full_path)
        for dir in folder_to_remove.folders:            
            self.remove_folder(dir.name, path=folder_to_remove.full_path)
        folder_to_remove.parent.remove_folder(folder_name)

    def to(self, folder_name):
        for folder in self.current_directory.folders:
            if folder.name == folder_name:
                self.current_directory = folder
                self.cur()
                return
        print("Folder not found")

    def back(self):
        if self.current_directory.name != "/":            
            self.current_directory = self.current_directory.parent
            pass

    def cur(self):
        print("/".join(self.current_directory.full_path))

    def rename(self, name, type):
        if type == "f":
            names_files = list(map(lambda i: i.name, self.current_directory.files))
            if file_name not in names_files:
                print("File not found")            
                return 
            for i in range(len(self.current_directory.files)):
                if self.current_directory.files[i].name == name:
                    new_name = input("Enter a new file name: ")
                    self.current_directory.files[i].name = new_name
        elif type == "d":
            names_folders = list(map(lambda i: i.name, self.current_directory.folders))
            if file_name not in names_folders:
                print("Folder not found")            
                return 
            for i in range(len(self.current_directory.folders)):
                if self.current_directory.folders[i].name == name:
                    new_name = input("Enter a new folder name: ")
                    self.current_directory.folders[i].name = new_name

    def move_file(self, file_name, path="cur"):
        folder = self.current_directory
        if path != "cur":
            if self.check_path(path):
                folder = self.to_path(path)  
        path_to = input("Enter the path to move file: ")
        to_folder = self.to_path(path_to.split('/'))
        if to_folder == -1:
            return
        for file in folder.files:
            if file.name == file_name:     
                self.add_file(file.name, file.size, to_folder.full_path) 
                self.remove_file(file.name, folder.full_path)
                return
            else:
                print("File not found")

    def copy_file(self, file_name, path="cur"):
        folder = self.current_directory
        if path != "cur":
            if self.check_path(path):
                folder = self.to_path(path)  
        path_to = input("Enter the path to copy file: ")
        to_folder = self.to_path(path_to.split('/'))
        if to_folder == False:
            return
        for file in folder.files:
            if file.name == file_name:
                if file.size > self.free_blocks*self.block_size:
                    print("Not enough space")
                else:
                    self.add_file(file.name, file.size, to_folder.full_path) 
            else:
                print("File not found")

class Folder(FileSystem): 
    def __init__(self, name, parent): 
        self.name = name 
        self.files = [] 
        self.folders = []
        self.parent = parent
        if parent != ['']:
            self.full_path = parent.full_path+[self.name]
        else:
            self.full_path = ['']
        
    def add_file(self, file_name, size):
        self.files.append(File(file_name, size))

    def add_file_obj(self, file):
        self.files.append(file)

    def add_folder(self, folder_name):
        self.folders.append(Folder(folder_name, self))

    def remove_file(self, file_name):
        for file in self.files:
            if file.name == file_name:
                self.files.remove(file)

    def remove_file_obj(self, file):
        self.files.remove(file)

    def remove_folder(self, folder_name):
        for folder in self.folders:
            if folder.name == folder_name:
                self.folders.remove(folder)

    def find_dir(self, folder_name):
        for i in range(len(self.folders)):
            if self.folders[i].name == folder_name:
                return i
        print("Folder not found")  
        return -1
    
    def to_dir(self, folder_name):
        i = self.find_dir(folder_name)
        if i != -1:
            return self.folders[i]
        return -1

class File(Folder): 
    def __init__(self, name, size):         
        self.name = name 
        self.size = size
        self.ind = []
        

fs = FileSystem() 
print("Enter the command: \n--- file - adding a file \n--- dir - adding a folder\n--- del_f- deleting a file \n--- del_d - deleting a folder \n--- show - displaying occupied space \n---map - displaying memory partitions\n--- info - view commands \n--- move - move \n---copy - copy \n--- end - completion ")
while True:   
    inp = input(">> ").split()
    if inp != []:
        command = inp[0]
    options = ""
    if len(inp) > 1:
        options = inp[1]
    if command == "file": 
        size = input("Enter the file size (in bytes): ") 
        if size.isdigit():
            filename = input("Enter the file name: ") 
            if options == "":
                path = "cur"
            else:
                path = options.split("/")
            fs.add_file(filename, int(size), path) 
        else: 
            print("It's not a number.") 
    elif command == "dir": 
        dirname = input("Enter the name of the catalog: ") 
        if options == "":
            path = "cur"
        else:
            path = options.split("/")
        fs.add_folder(dirname, path) 
    elif command == "info":
        print("Enter the command: \n--- file - adding a file \n--- dir - adding a folder\n--- del_f- deleting a file \n--- del_d - deleting a folder \n--- show - displaying occupied space \n---map - displaying memory partitions\n--- info - view commands \n--- move - move \n---copy - copy \n--- end - completion ")
    elif command == "show": 
        fs.display_file_system() 
    elif command == "map":
        fs.display_blocks_map()
    elif command == "del_f": 
        filename = input("Enter the file name: ") 
        if options == "":
            path = "cur"
        else:
            path = options.split("/")
        fs.remove_file(filename, path) 
    elif command == "del_d": 
        dirname = input("Enter the folder name: ") 
        if options == "":
            path = "cur"
        else:
            path = options.split("/")
        fs.remove_folder(dirname, path) 
    elif command == "to": 
        folder_name = input("Enter the folder name: ") 
        fs.to(folder_name) 
    elif command == "back": 
        fs.back() 
    elif command == "cur": 
        fs.cur() 
    elif command == "rename_f": 
        file_name = input("Enter the file name: ") 
        fs.rename(file_name, "f") 
    elif command == "rename_d": 
        folder_name = input("Enter the folder name: ") 
        fs.rename(folder_name, "d") 
    elif command == "check":
        path = input("Enter the path: ") 
        fs.check_path(path.split("/")[1:]) 
    elif command == "move_f": 
        dirname = input("Enter the file name: ") 
        if options == "":
            path = "cur"
        else:
            path = options.split("/")
        fs.move_file(dirname, path) 
    elif command == "copy_f": 
        dirname = input("Enter the file name: ") 
        if options == "":
            path = "cur"
        else:
            path = options.split("/")
        fs.copy_file(dirname, path) 
    elif command == "end": 
        break 
    else: 
        print("ERROR")
print("The program has ended")
