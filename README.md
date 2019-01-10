# Dummy Generator

## Description

_Dummy Generator_ will copy a _directory tree_ of given path and generate a new version with dummy files.
~~Dummy files are generate using the **bash command line**: `mkfile 1 filename`.~~

A _dummy file_ has no attributes, meaning that it won't work with some applications or with specific tasks/workflow. When I first wrote this script I needed all files to be wav because of a special metadata working only with audio files, so if needed,
Dummy Generator, can also convert all the generated files into "real" ones from a given sample file.

---

### Using Dummy Generator

> All the examples from now on, are assuming that you are in the same directory where the dummy_generator.py is.
> If not then you need to supply the full path of the script.
> You always drag and drop folders or files inside the terminal for a quick path!
> ![Alt Text](https://media.giphy.com/media/1BFWhNVg0ALAt4i8pB/giphy.gif)

### Required Parameters

### UPDATE:

#### GUI:
Dummy generator now can also be launched using the standard python GUI framework Tkinter.
You need to have tkinter on your computer. If you are on MacOS, tkinter comes already in your python package while if you are on linux you probably need to install it manually.

    sudo apt-get install python3-tk

To launch the GUI version
To start using the Dummy Generator, is as simple as launching the script inside the terminal and
providing the path of the source directory you want to copy.

    $ python3 dummy_generator.py /users/etc/documents/Music
    Start copying...
    Done!
    $ ..

This will copy and generate the dummy files inside the directory where `dummy_generator.py` is.

    Dummy\ Generator/
    ├── Dummy\ Music  <- the dummy directory generated
    ├── dummy_generator.py
    └── sample.wav

---

### Optional parameters

There are a few optional parameters that can add some extra options:

> You can always bring them up with `-h` or `--help`

    -f FILE, --file FILE  Sample file to be used as base for generating
                          'real' dummy files.
    -v, --verbosity       Increase output verbosity.
    -z, --zip             Archive the created dummy directory.

#### Usage examples

- `-v` or `--verbosity` adds an extra level of information that the script will output to the screen.

        $ python3 dummy_generator.py -v /users/etc/copy_123\
        Start copying...
        copy_tree       [INFO] - Copying Directory tree Copy_123:
        copy_tree       [INFO] - Done
        ...

- `-f` or `--file` takes an existing file and converts all the dummy files into that type of file.

  > _Example_: if you need to write BWF metadata(broadcasting wave format) will you need a real .wav file otherwise you won't have any metadata fields.
  > Its important to remember however, that the size of the given sample file matters, so if you want to copy large directory keep that in mind.

        $ python3 dummy_generator.py -v -f sample.wav /users/etc/music
        ...
        convert_files      [INFO] - Converting dummy files...
        convert_files      [INFO] - Done.
        ...

- `-z` or `--zip` will automatically create a zip archive of the directory generated.

        $ python3 dummy_generator.py -v -z /users/etc/music
        ...
        make_zip        [INFO] - Creating zip archive...
        make_zip        [INFO] - Done.
        Done!
        $ tree -L 1
        .
        ├── SEND_ME.zip <- the new archive generated from the dummy directory
        ├── Dummy music/
        ├── dummy_generator.py
        └── sample.wav