from crypto_file import CryptoFile
import argparse
from os import walk, makedirs
from shutil import rmtree


class ArgParse:
    def __init__(self):
        self.parse = argparse.ArgumentParser()
        self.parse.add_argument('directory', help='Directory name')
        self.parse.add_argument(
            '-m',
            '--mode',
            help='Select mode',
            choices=['encrypt', 'decrypt']
        )
        self.args = self.parse.parse_args()
        self.mode = self.args.mode
        self.directory = self.args.directory


class Tree:
    def __init__(self, selected_directory, mode):
        self.selected_directory = selected_directory

        self.mode = mode
        self.new_directory = self.mode + 'ed_' + self.selected_directory.split('_')[-1]

    def copy_tree(self):
        password = input('Enter Password -> ')
        makedirs(name=self.new_directory, exist_ok=True)

        for path, directories, files in walk(self.selected_directory):
            new = path.split(sep='/')
            new[0] = self.new_directory
            makedirs('/'.join(new), exist_ok=True)
            if files:
                for file in files:
                    with CryptoFile(
                            file=path + '/' + file,
                            mode=self.mode,
                            password=password,
                            new_file='/'.join(new) + '/' + file
                                    ) as cf:
                        mode_mapper = {'encrypt': cf.encrypt_mode, 'decrypt': cf.decrypt_mode}
                        func = mode_mapper.get(self.mode)
                        func()

    def remove_old_tree(self):
        rmtree(self.selected_directory)


def main():
    arg_parse = ArgParse()
    tree = Tree(arg_parse.directory, arg_parse.mode)
    tree.copy_tree()
    tree.remove_old_tree()


if __name__ == '__main__':
    main()
