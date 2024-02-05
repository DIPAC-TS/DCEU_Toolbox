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
    
def __rename_file(myroot:str, key:str, value:str="", prefix="", suffix="", sep=" "):
    """
    This method rename a file based the original name (key) and the reference name (value), addittionally you
    can add a prefix before the new name and a suffix after.
    
    arguments:
    ----------
    myroot - string with the directory root of the file to change the name
    key - string with original file of the file
    value - string with the new name of the file (if empty the new name is the key)
    prefix - string with the new prefix to use before the new file name
    suffix - string with the new suffix to use after the new file name
    sep - string with the separator pattern to know how to classify the common patterns in file
    """
    if len(value) == 0:
        value = key
    # If prefix exists, it will add the separator pattern after the value
    if len(prefix) != 0:
        prefix += sep
    # If suffix exists, it will add the separator pattern before the value
    if len(suffix) != 0:
        suffix = sep + suffix
    # The value will be added after the prefix but if there are an extension (.ext), then it will be added the suffix before
    # the extension
    if len(value.split(".")) > 1:
        prefix = prefix + "".join(value.split(".")[:-1])
        suffix = suffix + "." + value.split(".")[-1]
    else:
        prefix = prefix + value
    os.rename(myroot + key, myroot + prefix + suffix)

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
        __rename_file(myroot=myroot, key=key, value=value, prefix=prefix, suffix=suffix, sep=sep)

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
        __rename_file(myroot=myroot, key=i, prefix=prefix, suffix=suffix, sep=sep)
