import rainparsing

illustro_root = rainparsing.CollectionFolder('E:\\Documents\\Dropbox\\fa 17\\242\RainDesign\\unittesting\illustro')

print('skin_folder names: ' + str([folder for folder in illustro_root.skin_folders]) )
for folder_name, folder_obj in illustro_root.skin_folders.items():
    print(folder_name)
    print(' skin_files: ')
    for skin_file in folder_obj.skin_files:
        print('   ' + skin_file)
    print(' var_files: ')
    for skin_file in folder_obj.var_files:
        print('   ' + skin_file)

