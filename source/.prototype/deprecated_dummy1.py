"""Convert a directory tree into dummy files for testing purposes."""
import os
import shutil
import logging
import argparse
import subprocess

try:
    import tqdm
except ModuleNotFoundError:
    pass

pwd = os.path.abspath(os.path.dirname(__file__))
os.chdir(pwd)


def run_main():
    """Run all methods of this module."""
    print('Copying in progress... this can take a bit...')
    # make_dummy_dir()
    make_dummy_file()
    extract_path()
    delete_empty_path()
    if args.file:
        convert_files()
    else:
        logger.warning('No sample file was given..')
    if args.zip:
        create_zip()
        delete_after_zip()
    print('Done!')


def make_dummy_dir():
    """Copy and create directories/sub directory from selected directory."""
    logger.info('Creating new folders path...')
    for directory, files in generate_path():
        os.makedirs(directory, exist_ok=True)
    logger.info('Done.')


def make_dummy_file():
    """Make dummy files from selected directory.

    Shows progress bar if module tqdm is installed.
    """
    logger.info('Creating new dummy files...')
    chunck = 1024
    try:
        for directory, files in tqdm.tqdm(generate_path(),
                                          desc='files copied'):
            with open(f'tmp/{files}', 'wb') as f:
                f.write(bytearray(chunck))
            # subprocess.run(['mkfile', '1', f'tmp/{files}'])
    except NameError:
        for directory, files in generate_path():
            os.makedirs(directory, exist_ok=True)
            with open(f'tmp/{files}', 'wb') as f:
                f.write(bytearray(chunck))
            # subprocess.run(['mkfile', '1', f'tmp/{files}'])
    logger.info('Done.')


def convert_files():
    """Convert the dummy files into real files.

    Dont always needed but can be necessary if you need test some application.
    """
    logger.info('Converting dummy files...')
    for directory, files in generate_path():
        # TODO: if file path begins with / then it wont work
        shutil.copy(args.file, f'tmp/{files}')
    logger.info('Done.')


def extract_path():
    """Extract the top level folder from the directory path created."""
    shutil.move(f'tmp/{args.path}', f'Dummy {args.path.split("/")[-1]}')


def delete_empty_path():
    """Delete the empty path created from the dummy generator."""
    shutil.rmtree('tmp')


def search_dummy_dir():
    """Search for the generated Dummy directory."""
    logger.info('Search for folder to archive...')
    for directory in os.scandir():
        if directory.is_dir() and directory.name.startswith('Dummy'):
            return directory.name


def create_zip():
    """Create Archive from the Dummy directory."""
    logger.info('Creating zip archive...')
    output_filename = 'SEND_ME'
    shutil.make_archive(output_filename, 'zip', search_dummy_dir())


def delete_after_zip():
    """Delete the Dummy folder after only if has been already archived."""
    # TODO: this action should be optional
    logger.info('Deleting folder..')
    shutil.rmtree(search_dummy_dir())
    logger.info('Done.')


def generate_path():
    """Generate directory path from args.path.

    Returns:
        (create_directory_path, create_file_path) {tuple} -- string of
        absolutes paths for folders and files.
    """
    logger.info(f'Copying from Directory: {os.path.basename(args.path)}...')
    for dirpath, dirnames, filenames in os.walk(args.path):
        create_directory_path = f'tmp{dirpath}'
        for filename in filenames:
            if not filename.startswith('.'):
                create_file_path = os.path.join(dirpath, filename)
                yield create_directory_path, create_file_path
    logger.info('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Generate Dummy files
                        from given directory path.''')
    parser.add_argument('-v', '--verbosity', action='store_true',
                        help='Increase output verbosity')
    parser.add_argument('path', type=str,
                        help='''path for directory to be copied
                        and converted into dummy files. by default the files
                        will be 1byte in size and of no extension''')
    parser.add_argument('-f', '--file', type=str,
                        help='''type of sample file to be
                        used as base for generating 'real' dummy files''')
    parser.add_argument('-i', '--invisible', action='store_true',
                        help='Include invisibile files. default is False')
    parser.add_argument('-z', '--zip', action='store_true',
                        help='archive the created dummy directory')
    args = parser.parse_args()
    # --------------------------------- #
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(funcName)-16s[%(levelname)s] - %(message)s')

    print_terminal = logging.StreamHandler()
    print_terminal.setLevel(logging.INFO)
    print_terminal.setFormatter(formatter)
    logger.addHandler(print_terminal)
    # --------------------------------- #

    if not args.verbosity:
        logger.disabled = True
    else:
        pass
    run_main()
