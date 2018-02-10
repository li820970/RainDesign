import os
from rainparsing import files, envs




def scan_files_in_dir(path):
    """
given a path to a folder, return all .ini, .inc and folders in it as 3 lists
    :param path: str path to folder
    :return: (foldernames, .ini names, .inc names)
    """
    if not os.path.isdir(path):
        return None
    names = os.listdir(path)
    subfolders = []
    skin_files = []
    var_files = []
    other_files = []
    for name in names:
        if os.path.isdir(path + name):
            subfolders.append(name)
        else:
            if name.endswith('.ini'):
                skin_files.append(name)
            elif name.endswith('.inc'):
                var_files.append(name)
            else:
                other_files.append(name)
    return subfolders, skin_files, var_files, other_files

def find_section_props(section_lines):
    """
Given a string representing the lines in a section, return its properties as a dictionary of {key:value}
In the even of identical keys, later entries will override earlier ones
Since the placement of the meterstyle prop matters, we may restructure this as a list later
    :param section_lines:
    :return:
    """
    prop_dict = {} #this is still good for quick lookups
    comments = []
    for line in section_lines:
        line = line.strip()
        if line.startswith(';'):
            comments.append(line)
        else:
            try:
                a, b = line.split('=')
                a = a.strip()
                b = b.strip()
                prop_dict[a] = b
            except:
                continue
    prop_dict[';'] = comments
    return prop_dict



def path_from_widgetitem(item):
    """

    :type item: QTreeWidgetItem
    """
    path = [item.text(0)]
    while item.parent() is not None:
        path.insert(0, item.parent().text(0))
        item = item.parent()
    return path

def resolve_path(path, env):
    """

    :type env: envs.local_env
    """
    path = path.replace('#@#', env.resources_path)
    path = path.replace('/', '\\')

    return path
def dict_list_update(original_dict, new_dict):
    # print(original_dict,'\n---\n', new_dict)
    for key, value in new_dict.items():
        if key in original_dict:
            new_list = original_dict[key] + value
            original_dict[key ]= new_list
        else:
            original_dict[key] = value
    # print('^^^^\n',original_dict)
    # print('==================================')
def list_to_args(args):
    if isinstance(args, list):
        return str(list).replace('[','').replace(']', '').replace(',', '|')
    else:
        return args