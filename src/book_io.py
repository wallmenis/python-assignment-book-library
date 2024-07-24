import re
import pandas as pd
import matplotlib.pyplot as plt

def make_bar_graph(name_array, array, name_array_title, array_title, plot_title):
    plt.figure(figsize=(12, 8))
    plt.bar(name_array, array, color='red', width=0.4)
    plt.xlabel(name_array_title)
    plt.ylabel(array_title)
    plt.title(plot_title)
    plt.grid(True)
    for i, txt in enumerate(array):
        plt.annotate(txt, (i, array[i]), ha='center')
    plt.show()
    # print(name_array)
    # print(array)
    # plt.close()

def input_list():
    inp = ""
    result = []
    while not re.match("exit", inp.replace(" ",""), re.IGNORECASE):
        inp = input()
        result.append(inp)
    result.pop()
    return result


def print_dataframe(df, df_name = "entries", df_search_term = "IDs", df_title="Search DataFrame" , df_fields = [], interval = 5, use_search = False, multiple = True):
    end = False
    datf = df.copy()
    if df_fields != []:
        datf = datf[df_fields]
    ind = 0
    while not end :
        tmp_df = datf.iloc[ind*interval : (ind+1)*interval]
        print(df_title)
        print(tmp_df)
        print(f"Type /n for the next {interval} {df_name}, /b for the {interval} previous and /e to exit")
        if use_search:
            if multiple:
                print(f"You may also type the {df_search_term} to select specific {df_name} (separated with commas).")
            else:
                print(f"You may also type the {df_search_term} to select the specific {df_name}.")
        inp = input()
        if re.match("/n", inp):
            if ind*interval > datf.shape[0] - interval:
                print(f"No {df_name} left.")
            else:
                ind = ind + 1
        elif re.match("/b", inp):
            if ind == 0:
                print("We are at the start.")
            else:
                ind = ind - 1
        elif re.match("/e", inp):
            end = True
        else:
            if use_search:
                if multiple:
                    return inp.split(',')
                if len(inp.split(','))>1:
                    print("Please insert only one value.")
                else:
                    return inp
            print("Could not Interperate command.")
    return ""
        
def dict_editor(dictionary):
    ndictionary = dictionary
    inp = "Y"
    while inp == "Y":
        print("Editing Below:")
        print(ndictionary)
        
        print("Please select some of the above the values to be edited (comma separated).")
        inp = input()
        
        print(inp)
        inp = inp.split(',')
        for i in inp:
            print(f"Now editing {i}.")
            if type(i) == dict:
                ndictionary[i] = dict_editor(i)
            elif type(i) == list:
                ndictionary[i] = list_editor(i)
            else:
                ndictionary[i] = input()
        print("These are the new changes. Would you like to try again?[Y/N/D]")
        print_dict(ndictionary)
        inp = input()
    if inp != "N":
        print("Changes discarded.")
        return dictionary
    return ndictionary


def dict_editor_custom(dictionary, fields):
    ndictionary = dictionary
    inp="Y"
    while inp == "Y":
        for i in fields:
            print(f"Now editing {i}. Current value \"{ndictionary[i]}\" Press enter to not alter.")
            if type(ndictionary[i]) == dict:
                ndictionary[i] = dict_editor(ndictionary[i])
            elif type(ndictionary[i]) == list:
                ndictionary[i] = list_editor_int(ndictionary[i])
            else:
                inp2 = input()
                if inp2 != "":
                    ndictionary[i] = inp2
        print("These are the new changes. Would you like to try again?[Y/N/D]")
        print_dict(ndictionary)
        inp = input()
    if inp != "N":
        print("Changes discarded.")
        return dictionary
    return ndictionary

def list_editor_int(list_to_edit, list_name = "value", text = True):
    if text:
        print(f"Please enter values (comma separated) for {list_name} list.")
        print("List preview:")
        print(list_to_edit)
    inp = input()
    if inp == "":
        return list_to_edit
    inp = inp.split(',')
    ret = []
    for i in inp:
        ret.append(int(i))
    return ret

def list_editor(list_to_edit, list_name = "value"):
    print(f"Please enter values (comma separated) for {list_name} list.")
    print("List preview:")
    print(list_to_edit)
    inp = input()
    inp = inp.split(',')
    return inp

def print_dict(dictionary):
    for i in dictionary.keys():
        print(f"{i} : {dictionary[i]}")