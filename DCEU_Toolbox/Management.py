from scipy import stats as stat
import numpy as np
import os

def __get_pattern(file_list:list, sep:str = " "):
    """
    This private function analyze a file list to evaluate the mode of a pattern based on a separator specified
    arguments:
    ----------
    file_list : list with the string of each file name to analyze
    sep : string with keyword to split the file name 

    returns:
    --------
    tupple with the pattern most frequent found and the count with how many the pattern was found
    """
    patterns = np.array([])
    for myfile in file_list:
        patterns = np.append(patterns, myfile.split(sep)[0])
    return stat.mode(patterns).mode[0], stat.mode(patterns).count[0]

def __get_filelist(directory:str = ""):
    """
    This private function save the file list and the root of the specified directory
    arguments:
    ----------
    directory - string with location root of the directory where the files are

    returns:
    --------
    tupple with string of file list and the directory root
    """
    if len(directory) > 0:
        return os.listdir(directory), directory + "/"
    else:
        return os.listdir(), ""

def purge_filenames(sep:str = " ", directory:str = "", prefix:str="", suffix:str="", clones:int=1):
    """
    This method reduce the filename string to eliminate common pattern based on a separator specified,
    after identify the filenames to change, it allows add a new suffix and prefix to the new name.

    arguments:
    ----------
    sep - string with the separator pattern to know how to classify the common patterns in file
    directory - string with location root of the directory where the files are
    prefix - string with the new prefix to use before the new file name
    suffix - string with the new suffix to use after the new file name
    clones - copies allowed with the same pattern without modifying
    """
    file_list, myroot = __get_filelist(directory)
    pattern, count = __get_pattern(file_list)
    files_to_edit = {}
    while count > clones and pattern != "":
        for myfile in file_list:
            if pattern in myfile.split(sep)[0]:
                files_to_edit[myfile] = myfile
        for key, value in files_to_edit.items():
            if pattern in value.split(sep)[0]:
                newfilename = sep.join(value.split(sep)[1:])
                files_to_edit[key] = newfilename
        pattern, count = __get_pattern(files_to_edit.values())     
    for key, value in files_to_edit.items():
        os.rename(myroot + key, myroot + prefix + sep + value + sep + suffix)

def add_to_filenames(directory:str = "", prefix:str = "", suffix:str = "", sep:str = ""):
    """
    This method add keywords before (prefix) and after (suffix) of all file names in a specified directory

    arguments:
    ----------
    directory - string with location root of the directory where the files are
    prefix - string with the new prefix to use before the new file name
    suffix - string with the new suffix to use after the new file name
    sep - string with keyword to separate suffix and prefix of initial filename
    """
    file_list, myroot = __get_filelist(directory)
    for i in file_list:
        os.rename(myroot + i, myroot + prefix + sep + i + sep + suffix)
