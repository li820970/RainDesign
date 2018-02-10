import unittest
import os, sys
import rainparsing
import widget_generators
class TestBasicParsing(unittest.TestCase):


    path = os.getcwd()
    illustro_collection = rainparsing.CollectionFolder(path + '\\illustro')

    def test_skin_folders(self):
        self.assertSetEqual(set(['Clock', 'Disk', 'Google', 'Network', 'Recycle Bin', 'System', 'Welcome']), set([folder for folder in self.illustro_collection.skin_folders] ))
    def test_sections(self):
        clock = self.illustro_collection.skin_folders['Clock']
        self.assertEqual('1000', clock.skin_files['Clock.ini'].header.props['update'])
        self.assertEqual('Displays the current date and time.', clock.skin_files['Clock.ini'].metadata.props['information'])
        self.assertEqual('Trebuchet MS', clock.skin_files['Clock.ini'].variables.props['fontName'])#this is important because the N should have retained its caps
        self.assertEqual('Time', clock.skin_files['Clock.ini'].measures['measureTime'].props['measure'])
        self.assertEqual('Shadow', clock.skin_files['Clock.ini'].meterstyles['styleLeftText'].props['stringeffect'])

    def test_bracket_ops(self):
        clock = self.illustro_collection['Clock']
        self.assertEqual('1000', clock['Clock.ini']['rainmeter']['update'])
        self.assertEqual('Displays the current date and time.', clock['Clock.ini']['metadata']['information'])
        self.assertEqual('Trebuchet MS', clock['Clock.ini']['variables']['fontName'])#this is important because the N should have retained its caps
        self.assertEqual('Time', clock.skin_files['Clock.ini']['measureTime']['measure'])
        self.assertEqual('Shadow', clock.skin_files['Clock.ini']['styleLeftText']['stringeffect'])

    def test_getters_and_str(self):
        self.assertEqual(set(['Clock', 'Disk', 'Google', 'Network', 'Recycle Bin', 'System', 'Welcome']), set([str(f) for f in self.illustro_collection.get_all_skin_folders()]))
        self.assertEqual(set(['[styleRightText]','[styleTitle]','[styleLeftText]','[styleBar]']) , set([str(f) for f in self.illustro_collection['System']['System.ini'].get_all_meterstyles()]))
        self.assertEqual(set(['[measureCPU]','[measureSWAP]','[measureRAM]']) , set([str(f) for f in self.illustro_collection['System']['System.ini'].get_all_measures()]))
        self.assertEqual(set(['[meterLabelCPU]','[meterBarCPU]','[meterValueCPU]','[meterBarSWAP]','[meterValueRAM]','[meterLabelRAM]','[meterBarRAM]','[meterTitle]','[meterLabelSWAP]','[meterValueSWAP]']) ,
                         set([str(f) for f in self.illustro_collection['System']['System.ini'].get_all_meters()]))

    def test_env_no_imports(self):
        clock = self.illustro_collection['Clock']['Clock.ini']

        self.assertEqual('Trebuchet MS', clock.env['fontName'])
        self.assertEqual(self.illustro_collection.env.resources_path,clock.env.resources_path )
        self.assertEqual(self.illustro_collection.env['@Resources'],clock.env['@Resources'] )

    def test_env_imports(self):
        welcome = self.illustro_collection['Welcome']['Welcome.ini']

        self.assertEqual('includedVar', welcome.env['includedVar1'])
        self.assertEqual('[includedMeasure1]', str(welcome.env['includedMeasure1']))
        self.assertEqual('[includedMeasure1]', str(welcome.env['includedMeasure1']))
    def test_groups(self):
        two_disk = self.illustro_collection['Disk']['2 Disks.ini']
        self.assertEqual(['skinGroup1'], two_disk.header.groups)
        self.assertEqual(['measuregroup1'], two_disk['measureUsedDisk1'].groups)
        self.assertEqual(['measuregroup2'], two_disk['measureTotalDisk2'].groups)
        self.assertEqual(['metergroup1', 'metergroup2'], two_disk['meterTitle'].groups)
        self.assertEqual(['[meterTitle]', '[meterLabelDisk1]', '[meterValueDisk1]'], [str(measure) for measure in two_disk.get_all_in_group('metergroup2')])
    def test_import_tracking(self):
        welcome = self.illustro_collection['Welcome']['Welcome.ini']
        path = 'E:\\Documents\\Dropbox\\fa 17\\242\\RainDesign\\unittesting\\illustro\\@Resources\\includefile.inc'
        self.assertTrue( path in welcome.dependencies)
if __name__ == '__main__':
    unittest.main()