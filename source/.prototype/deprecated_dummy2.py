
"""Convert a directory tree into dummy files for testing purposes."""
import os
import shutil
import logging
import argparse

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


def run_main(main_path, zip_folder=False, sample_file=False, invisible=False):
    """Run all methods of this module.

    Arguments:
        main_path {str}   - the absolute path of the directory to copy
        zip_folder {bool} - archive the directory after copying.
                            default: False
        sample_file {str} - a sample file if generating "real" dummy files
                            default: False
        invisible {bool}  - if want to include invisible files
                            default: False
    """
    print('Copying in progress... this can take a bit...')
    if zip_folder:
        create_zip(main_path, sample_file, invisible)
    else:
        make_dummy_directory(main_path, sample_file, invisible)
    print('Done!')


def create_zip(main_path, sample_file, invisible):
    """Generate and create archive with Dummy directory."""
    LOGGER.info('Creating zip archive...')
    output_filename = 'SEND_ME'
    directory_to_zip = make_dummy_directory(main_path, sample_file, invisible)
    shutil.make_archive(output_filename, 'zip', directory_to_zip)
    shutil.rmtree(directory_to_zip)


def make_dummy_directory(main_path, sample_file, invisible):
    """Make dummy files from selected directory.

    Shows progress bar if module tqdm is installed.
    """
    # size in bytes
    chunk = 1024

    tmp_name = '.tmp'
    top_folder = os.path.basename(main_path)
    LOGGER.info('Creating new dummy files...')

    if PROGRESS_BAR:
        search_dir = tqdm.tqdm(generate_path(
            main_path, invisible), desc='files copied')
    else:
        search_dir = generate_path(main_path, invisible)

    for directory, files in search_dir:
        os.makedirs(f'{tmp_name}{directory}', exist_ok=True)
        if sample_file:
            shutil.copy(sample_file, f'{tmp_name}/{files}')
        else:
            with open(f'{tmp_name}/{files}', 'wb') as f:
                f.write(bytearray(chunk))

    dummy_name = shutil.move(f'{tmp_name}/{main_path}', f'Dummy_{top_folder}')
    shutil.rmtree(tmp_name)
    return dummy_name


def generate_path(main_path, invisible):
    """Generate directory path from args.path.

    Returns:
        (create_directory_path, create_file_path) {tuple} -- string of
        absolutes paths for folders and files.
    """
    LOGGER.info(f'Copying from Directory: {os.path.basename(main_path)}...')
    for dirpath, dirnames, filenames in os.walk(main_path):
        for filename in filenames:
            if not invisible:
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

    wd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(wd)
    run_main(main_path=args.path, zip_folder=args.zip,
             sample_file=args.file, invisible=args.invisible)
