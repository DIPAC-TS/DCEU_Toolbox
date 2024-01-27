from scipy import stats as stat
import numpy as np
import os

def __get_pattern(file_list:list, sep:str = " "):
    patterns = np.array([])
    for myfile in file_list:
        patterns = np.append(patterns, myfile.split(sep)[0])
    return stat.mode(patterns).mode[0], stat.mode(patterns).count[0]

def __get_filelist(directory:str = ""):
    if len(directory) > 0:
        return os.listdir(directory), directory + "/"
    else:
        return os.listdir(), ""

def purge_filenames(directory:str = "", sep:str = " ", prefix:str="", suffix:str=""):
    file_list, myroot = __get_filelist(directory)
    pattern, count = __get_pattern(file_list)
    files_to_edit = {}
    if count > 1:
        for myfile in file_list:
            if pattern in myfile:
                files_to_edit[myfile] = myfile
    while count > 1 and pattern != "":
        for key, value in files_to_edit.items():
            newfilename = sep.join(value.split(sep)[1:])
            files_to_edit[key] = newfilename
        pattern, count = __get_pattern(files_to_edit.values())
     
    for key, value in files_to_edit.items():
        os.rename(myroot + key, myroot + prefix + sep + value + sep + suffix)

def add_to_filenames(prefix:str = "", suffix:str = "", directory:str = "", sep:str = ""):
    file_list, myroot = __get_filelist(directory)
    for i in file_list:
        os.rename(myroot + i, myroot + prefix + sep + i + sep + suffix)
