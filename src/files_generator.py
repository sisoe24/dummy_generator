"""Generate dummy files from a real directory. Can be called from CLI or gui"""
import os
import shutil
import logging
import argparse

LOGGER = logging.getLogger('dummy_gui.generator')

PROGRESS_BAR = False


class DummyGenerator:
    """A Class that generates dummy files from a given path."""

    def __init__(self, main_path, sample_file, invisible_files, zip_after):
        """Initialize the class with all the arguments needed.

        Arguments:
            main_path {str} -- path of the directory to be converted in dummy.
            sample_file {bool} -- use sample file for generating real dummy.
            invisible_files {bool} -- include invisibile files.
            zip_after {bool} -- zip folder after.
        """
        self.main_path = main_path
        self.sample_file = sample_file
        self.invisibile_files = invisible_files

        self.dummy_home = f'{os.path.expanduser("~")}/Dummy_Folder'
        os.makedirs(self.dummy_home, exist_ok=True)

        self.dummy_dest = f'{self.dummy_home}/Dummy_{self._get_top_folder()}'
        self.dummy_archive = f'{self.dummy_home}/SendMe_{self._get_top_folder()}'

        while True:
            if not self._already_exists():
                if zip_after:
                    self.make_zip_dummy_directory()
                else:
                    self.make_dummy_directory()
                break
            else:
                shutil.rmtree(self.dummy_dest)

    def _get_top_folder(self):
        """Get the top folder name of the directory copied."""
        top_folder = os.path.basename(self.main_path)
        return top_folder

    def _already_exists(self):
        """Check if dummy destination already exists."""
        return os.path.exists(self.dummy_dest)

    def make_zip_dummy_directory(self):
        """Generate and create archive with Dummy directory."""
        LOGGER.info('Creating zip archive...')
        directory_to_zip = self.make_dummy_directory()
        output_path = os.path.join(self.dummy_home, self.dummy_archive)
        shutil.make_archive(output_path, 'zip', directory_to_zip)
        shutil.rmtree(directory_to_zip)

    def make_dummy_directory(self, chunk_size=1024):
        """Generate dummy files.

        Shows progress bar if module tqdm is installed.
        Keyword Arguments:
            chunk_size {int} -- size of the files to generate (default: {1024})

        Returns:
            [str] -- the name of the dummy directory generated
        """
        LOGGER.info('Creating new dummy files...')
        if PROGRESS_BAR:
            search_dir = tqdm.tqdm(self._generate_path(), desc='files copied')
        else:
            search_dir = self._generate_path()

        tmp_name = os.path.join(self.dummy_home, '.tmp')
        for directory, files in search_dir:
            os.makedirs(f'{tmp_name}{directory}', exist_ok=True)
            if self.sample_file:
                shutil.copy(self.sample_file, f'{tmp_name}/{files}')
            else:
                with open(f'{tmp_name}/{files}', 'wb') as file:
                    file.write(bytearray(chunk_size))

        move_tmp = tmp_name + self.main_path
        dummy_path = shutil.move(move_tmp, self.dummy_dest)
        shutil.rmtree(tmp_name)
        return dummy_path

    def _generate_path(self):
        """Generate directory path from main path.

        Returns:
            (create_directory_path, create_file_path) {tuple} -- string of
            absolutes path for folders and files.
        """
        LOGGER.info('Copying from Directory: %s...',
                    os.path.basename(self.main_path))
        for dirpath, _, filenames in os.walk(self.main_path):
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
    PARSER = argparse.ArgumentParser(
        description='''Generate Dummy files
                        from given directory path.''')
    PARSER.add_argument('-v', '--verbosity', action='store_true',
                        help='Increase output verbosity')
    PARSER.add_argument('path', type=str,
                        help=''' absolute path of directory to be copied
                        and converted into dummy. by default the files
                        will be 1byte in size and of no type''')
    PARSER.add_argument('-p', '--progress', action='store_true',
                        help='Show progress bar (requires tqdm module)')
    PARSER.add_argument('-f', '--file', type=str,
                        help='''type of sample file to be
                        used as base for generating 'real' dummy files''')
    PARSER.add_argument('-i', '--invisible', action='store_true',
                        help='Include invisibile files. default is False')
    PARSER.add_argument('-z', '--zip', action='store_true',
                        help='archive the created dummy directory')
    ARGS = PARSER.parse_args()

    if not ARGS.verbosity:
        LOGGER.disabled = True
    if ARGS.progress:
        try:
            import tqdm
            PROGRESS_BAR = True
        except ModuleNotFoundError:
            PROGRESS_BAR = False
            LOGGER.warning('module tqdm not found')
    else:
        PROGRESS_BAR = False

    DummyGenerator(main_path=ARGS.path,
                   sample_file=ARGS.file,
                   invisible_files=ARGS.invisible,
                   zip_after=ARGS.zip)
    LOGGER.info('Copying in progress... this could take a moment...')
    LOGGER.info('Done!')
