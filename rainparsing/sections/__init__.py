from rainparsing import utils

class Section():
    def __init__(self,name,  props, lower = True):
        """

        :type lower: bool
        :type name: str
        :type props: dict
        """
        self.props = props
        self.name = name
        self.lowercase_props = lower
        if lower:
            self.lower_props()
            self.update_groups()

    def add_group(self, groupname):
        self.groups.append(groupname)
    def export(self):
        output = '[' + self.name + ']\n'
        for prop in self.props:
            output = output + prop + ' = '+ utils.list_to_args(self.props[prop]) + '\n'
        return output
    def __str__(self):
        return '['+self.name + ']'
    def update_props(self, other):
        """

        :type other: dict
        """
        self.props.update(other)
        self.update_groups()
    def update_groups(self):
        if 'group' in self.props:
            self.groups = [groupname.strip() for groupname in self.props['group'].split('|') ]
        else:
            self.groups = []

        if self.lowercase_props:
            self.lower_props()
    def lower_props(self):
        lowerprops = {}
        for key, value in self.props.items():
            lowerprops[key.lower()] = value
        self.props = lowerprops
    def __getitem__(self, item):
        if self.lowercase_props:
            try:
                item = item.lower()
            except:
                return None
        if item in self.props:
            return self.props[item]
class Meter(Section):
    def __init__(self,name, props):
        Section.__init__(self, name, props)

class Measure(Section):
    def __init__(self,name, props):
        Section.__init__(self, name, props)

class Header(Section):
    def __init__(self, props):
        Section.__init__(self, 'Rainmeter', props)



class MeterStyle(Section):
    def __init__(self, name,props):
        Section.__init__(self, name, props)

class Metadata(Section):
    def __init__(self, props):
        Section.__init__(self, 'MetaData', props)

class Variables(Section):
    def __init__(self, props):
        Section.__init__(self, 'Variables', props, lower = False)