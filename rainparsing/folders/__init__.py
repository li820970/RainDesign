from rainparsing import utils
from rainparsing import files
import os
from rainparsing import envs

class SkinFolder:

    def __init__(self, path, env):
        self.env = env
        self.resources = {}
        self.name = path.split('\\')[-1]
        self.path = path
        self.subfolders, skin_filenames, var_filenames,resource_filenames = utils.scan_files_in_dir(self.path)
        self.subfolders = {name:ResourceFolder(self.path + '\\' + name, env = self.env.clone()) for name in self.subfolders}
        self.skin_files = {file:files.SkinFile(self.path + '\\' + file, self.env.clone()) for file in skin_filenames}
        self.var_files = {file:files.VarFile(self.path + '\\' + file, self.env.clone()) for file in var_filenames}
        self.resources = {file:files.ResourceFile(self.path + '\\' + file) for file in resource_filenames}


    def get_all_subfolders(self):
        return self.subfolders.values()
    def get_all_skinfiles(self):
        return self.skin_files.values()
    def get_all_varfiles(self):
        return self.var_files.values()
    def get_all_resourcefiles(self):
        return self.resources.values()
    def __str__(self):
        return self.name
    def __getitem__(self, item):
        if item in self.subfolders:
            return self.subfolders[item]
        if item in self.skin_files:
            return self.skin_files[item]
        elif item in self.var_files:
            return self.var_files[item]


class ResourceFolder:
    def __init__(self, path, env):
        self.env = env
        self.path = path
        self.name = path.split('\\')[-1]
        self.subfolders, skin_filenames, var_filenames, self.resource_files = utils.scan_files_in_dir(self.path)

        self.importables = {file:files.VarFile(self.path + '\\' + file, self.env.clone()) for file in skin_filenames + var_filenames}
        self.subfolders = {name:ResourceFolder(self.path + '\\' + name, env = self.env.clone()) for name in self.subfolders}
        self.resource_files = {name:files.ResourceFile(self.path + '\\' + name) for name in self.resource_files}

    def get_all_subfolders(self):
        return self.subfolders.values()
    def get_all_importables(self):
        return self.importables.values()
    def get_all_resource_files(self):
        return self.resource_files.values()
    def __str__(self):
        return self.name
    def __getitem__(self, item):
        if item in self.subfolders:
            return self.subfolders[item]
        if item in self.importables:
            return self.importables[item]
        elif item in self.resource_files:
            return self.resource_files[item]
class CollectionFolder:
    def __init__(self, path, env = None):

        self.skin_folders = {}
        self.resources = {}
        self.path = path
        self.name = path.split('\\')[-1]
        if env is None:
            self.env = envs.local_env(resources_path=self.path + '\\@Resources')
        names = os.listdir(path)
        for name in names:
            if os.path.isdir(self.path + '\\' + name):
                if name.startswith('@'):
                    self.resources[name] = ResourceFolder(self.path + '\\' + name, env = self.env.clone())
                else:
                    self.skin_folders[name] = SkinFolder(path + '\\' + name, env = self.env.clone())
        if env is None:
            self.env = envs.local_env(resources_path=self.path + '\\@Resources')
    def __getitem__(self, item):
        if item in self.skin_folders:
            return self.skin_folders[item]
        if item in self.resources:
            return self.resources[item]
    def __str__(self):
        return self.name

    def get_all_skin_folders(self):
        return self.skin_folders.values()
    def get_all_resources(self):
        return self.resources.values()

class root_folder:
    def __init__(self, path):
        self.path = path