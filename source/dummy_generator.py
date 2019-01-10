import os
import shutil
import logging
import argparse


wd = os.path.abspath(os.path.dirname(__file__))
os.chdir(wd)
# --------------------------------- #
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter(
    '[%(levelname)s] - %(message)s')

PRINT_TERMINAL = logging.StreamHandler()
PRINT_TERMINAL.setLevel(logging.INFO)
PRINT_TERMINAL.setFormatter(FORMATTER)
LOGGER.addHandler(PRINT_TERMINAL)
# --------------------------------- #

PROGRESS_BAR = False


class DummyGenerator(object):
    """A Class that generates dummy files from a given path."""

    def __init__(self, main_path, sample_file, invisible_files):
        """Initialize the class with all the arguments needed.

        Arguments:
            main_path {str} -- path of the directory to be converted in dummy
            sample_file {bool} -- use sample file for generating real dummy
            invisible_files {bool} -- include invisibile files
        """
        self.main_path = main_path
        self.sample_file = sample_file
        self.invisibile_files = invisible_files

    def make_zip_dummy_directory(self):
        """Generate and create archive with Dummy directory."""
        LOGGER.info('Creating zip archive...')
        output_filename = 'SEND_ME'
        directory_to_zip = self.make_dummy_directory()
        shutil.make_archive(output_filename, 'zip', directory_to_zip)
        shutil.rmtree(directory_to_zip)

    def make_dummy_directory(self, chunk_size=1024):
        """Generate dummy files.

        Shows progress bar if module tqdm is installed.
        Keyword Arguments:
            chunk_size {int} -- size of the files to generate (default: {1024})

        Returns:
            [str] -- the name of the dummy directory generated
        """
        tmp_name = '.tmp'
        top_folder = os.path.basename(self.main_path)
        LOGGER.info('Creating new dummy files...')

        if PROGRESS_BAR:
            search_dir = tqdm.tqdm(self.generate_path(), desc='files copied')
        else:
            search_dir = self.generate_path()

        for directory, files in search_dir:
            os.makedirs(f'{tmp_name}{directory}', exist_ok=True)
            if self.sample_file:
                shutil.copy(self.sample_file, f'{tmp_name}/{files}')
            else:
                with open(f'{tmp_name}/{files}', 'wb') as f:
                    f.write(bytearray(chunk_size))

        dummy_name = shutil.move(f'{tmp_name}/{self.main_path}',
                                 f'Dummy_{top_folder}')
        shutil.rmtree(tmp_name)
        return dummy_name

    def generate_path(self):
        """Generate directory path from main path.

        Returns:
            (create_directory_path, create_file_path) {tuple} -- string of
            absolutes path for folders and files.
        """
        LOGGER.info(
            f'Copying from Directory: {os.path.basename(self.main_path)}...')
        for dirpath, dirnames, filenames in os.walk(self.main_path):
            for filename in filenames:
                if not self.invisibile_files:
                    if not filename.startswith('.'):
                        file_path = os.path.join(dirpath, filename)
                        yield dirpath, file_path
                else:
                    file_path = os.path.join(dirpath, filename)
                    yield dirpath, file_path
        LOGGER.info('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Generate Dummy files
                        from given directory path.''')
    parser.add_argument('-v', '--verbosity', action='store_true',
                        help='Increase output verbosity')
    parser.add_argument('path', type=str,
                        help=''' absolute path of directory to be copied
                        and converted into dummy. by default the files
                        will be 1byte in size and of no type''')
    parser.add_argument('-p', '--progress', action='store_true',
                        help='Show progress bar (requires tqdm module)')
    parser.add_argument('-f', '--file', type=str,
                        help='''type of sample file to be
                        used as base for generating 'real' dummy files''')
    parser.add_argument('-i', '--invisible', action='store_true',
                        help='Include invisibile files. default is False')
    parser.add_argument('-z', '--zip', action='store_true',
                        help='archive the created dummy directory')
    args = parser.parse_args()

    if not args.verbosity:
        LOGGER.disabled = True
    if args.progress:
        try:
            import tqdm
            PROGRESS_BAR = True
        except ModuleNotFoundError:
            PROGRESS_BAR = False
    else:
        PROGRESS_BAR = False

    dummy = DummyGenerator(main_path=args.path,
                           sample_file=args.file,
                           invisible_files=args.invisible)
    print('Copying in progress... this could take a moment...')
    if args.zip:
        dummy.make_zip_dummy_directory()
    else:
        dummy.make_dummy_directory()
    print('Done!')
