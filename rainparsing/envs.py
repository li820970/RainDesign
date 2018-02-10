import files, folders, sections

class local_env:
    def __init__(self, resources_path = None, vars = None, var_file = None):
        """

        :type var_file: rainparsing.SkinFile
        :type vars: rainparsing.Variables
        """
        self.resources_path = resources_path
        self.measures = {}
        self.meterstyles = {}
        self.variables = {}
        if vars is not None:
            self.variables = vars.props

        if var_file is not None:
            self.measures = var_file.measures
            self.meterstyles = var_file.meterstyles
            self.variables.update(var_file.variables)

    def clone(self):
        new = local_env(resources_path=self.resources_path)
        new.measures = self.measures.copy()
        new.variables = self.variables.copy()
        new.meterstyles = self.meterstyles.copy()
        # print(new.variables, self.variables)
        return new
    def add_from_file(self, file_obj):
        """

        :type file_obj: rainparsing.SkinFile
        """
        self.add_vars(file_obj.variables)
        self.add_meterstyles(file_obj.get_all_meterstyles())
        self.add_measures(file_obj.get_all_measures())
    def add_vars(self, section):
        """

        :type section: rainparsing.Variables
        """
        for var, val in section.props.items():
            if var != ';':
                self.variables[var] = val

    def add_meterstyles(self, meterstyles):
        """

        :type meterstyles: list
        """
        for meterstyle in meterstyles:
            self.meterstyles[meterstyle.name] = meterstyle
    def add_measures(self, measures):
        """

        :type measures: list
        """
        for measure in measures:
            self.measures[measure.name] = measure

    def __getitem__(self, item):
        if item in self.variables:
            return self.variables[item]
        elif item in self.meterstyles:
            return self. meterstyles[item]
        elif item in self.measures:
            return self.measures[item]
        else:
            return None
