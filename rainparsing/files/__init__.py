from builtins import isinstance

from rainparsing import utils
from rainparsing import sections
from rainparsing import envs
class SkinFile:
    def __init__(self, path, env):
        """
given a filepath to a rainmeter.ini, initialize a skin_file object
header -> [rainmeter]
metadata -> [metadata]
variables -> [variables]
in a proper file, there should only be one instance of each of these three. if there's more than one, they are merged together, with duplicate keys resolving to the latter
meterstyles/meters/measures -> each is a dict of {name: obj}. Names should be unique in a properly formatted file.
        :type env: envs.local_env
        :type path: str
        :param path: str path to .ini
        """
        self.header = sections.Header(props={})
        self.metadata = sections.Metadata(props={})
        self.variables = sections.Variables(props={})
        self.meterstyles = {}
        self.meters = {}
        self.measures = {}
        self.env =env
        self.dependencies = set()

        self.name = path.split('\\')[-1]
        self.path = path
        self.components_raw = self.find_skin_sections(path)
        for section_name in self.components_raw:
            prop_dict = utils.find_section_props(self.components_raw[section_name])
            if section_name.lower() == 'rainmeter':
                self.header.update_props(prop_dict)
            elif section_name.lower() == 'variables':
                self.variables.update_props(prop_dict)
            elif section_name.lower() == 'metadata':
                self.metadata.update_props(prop_dict)
            elif 'measure' in [key.lower() for key in prop_dict]:
                self.measures[section_name] = sections.Measure(section_name, prop_dict)
            elif 'meter' in [key.lower() for key in prop_dict]:
                self.meters[section_name] = sections.Meter(section_name, prop_dict)
            else:
                self.meterstyles[section_name] =sections.MeterStyle(section_name, prop_dict)
        self.env.add_from_file(self)
        self.groups = self.header.groups


    def find_skin_sections(self, path = None):
        """
    given a path to a rainmeter file, return a list of strings, each string corresponding to a section, ie '[sectionName]\n meter=string \n font = Arial'
        :param filepath: str path to file
        :return: list of str
        """
        components = {}
        if path is None:
            path = self.path
        with open(path) as f:
            current_name = None
            current_prop_list = []
            include_queue = []
            for line in f:
                line = line.strip()

                if line.startswith('[') and line.endswith(']'):
                    if current_name is not None:
                        components[current_name] = current_prop_list
                    current_name = line.strip('[]')
                    current_prop_list = []
                    if len(include_queue) > 0:
                        for include_line in include_queue:
                            try:
                                (include_name, filepath) = [token.strip() for token in include_line.split('=')]
                                include_name = include_name[8:]
                                filepath = utils.resolve_path(filepath, self.env)
                                included_sections = self.find_skin_sections(path = filepath)
                                if include_name == '':
                                    utils.dict_list_update(components, included_sections)
                                else:
                                    utils.dict_list_update(components, {include_name:included_sections[include_name]})
                                self.dependencies.add(filepath)
                            except:
                                continue
                        include_queue = []
                else:
                    current_prop_list.append(line)
                    if line.lower().startswith('@include') :
                        include_queue.append(line)

            components[current_name] = current_prop_list
            if len(include_queue) > 0:
                for include_line in include_queue:
                    try:
                        (include_name, filepath) = [token.strip() for token in include_line.split('=')]
                        include_name = include_name[8:]
                        filepath = utils.resolve_path(filepath, self.env)
                        included_sections = self.find_skin_sections(path=filepath)
                        if include_name == '':
                            utils.dict_list_update(components, included_sections)
                        else:
                            utils.dict_list_update(components, {include_name: included_sections[include_name]})
                        print(components['Variables'])
                    except:
                        continue
                include_queue = []

        return components



    def get_all_meterstyles(self):
        return self.meterstyles.values()
    def get_all_measures(self):
        return self.measures.values()
    def get_all_meters(self):
        return self.meters.values()
    def get_all_in_group(self, groupname):
        ret = []
        for section in self:
            if groupname in section.groups:
                ret.append(section)
        return ret
    def export(self):
        """
converts this file object back into a the file that it would look like on disk.
        :return: string - file contents
        """
        output = ''
        for section_type in [self.header, self.metadata, self.variables, self.meterstyles, self.measures, self.meters]:
            for section in section_type:
                output = output + section.export()
        return output
    def __str__(self):
        return self.name
    def __getitem__(self, item):
        try:
            if item.lower() == 'rainmeter':
                return self.header
            elif item.lower() == 'metadata':
                return self.metadata
            elif item.lower() == 'variables':
                return self.variables
            elif item in self.meterstyles:
                return self.meterstyles[item]
            elif item in self.meters:
                return self.meters[item]
            elif item in self.measures:
                return self.measures[item]
        except:
            return None

    def __iter__(self):
        ret = [self.header, self.metadata, self.variables]
        ret.extend(self.meterstyles.values())
        ret.extend(self.measures.values())
        ret.extend(self.meters.values())
        return iter(ret)


class VarFile(SkinFile):
    def __init__(self, path, env):
        """
Same structure as a skin file, but with .inc extension and specifically used as an import. As such, no meters should exist.
        :param path: string path to .inc file
        """
        SkinFile.__init__(self, path, env)

class ResourceFile:
    def __init__(self, path):
        self.name = path.split('\\')[-1]
        self.path = path

