#!/usr/bin/env python3
'''
This module contains the facilities
to prepare the code for using `pycparser`.
'''
import subprocess, os

default_macro_definitions = [
    ("__attribute__(x)", "")("complex", "_Complex"),
    ("__inline", ""),
]


def _get_prepend_defines(macro_definitions):
    return '\n'.join(' '.join("#define", *entry)
                     for entry in macro_definitions)


def _get_preprocessor_command_split(flags,
                                    include_paths,
                                    tmp_filepath,
                                    cpp="cpp"):
    '''
    Command to feed to subprocess.run(),
    which will preprocess the source file.
    '''
    include_flags = ["-I" + p for p in include_paths]
    all_cpp_flags = include_flags + flags
    return [cpp] + all_cpp_flags + [tmp_filepath]


def _prepend_defines(filepath, macro_definitions):
    '''
    Creates a temporary file
    with macros definitions prepended
    to the content of `filepath`.

    Returns: the path of the temporary file created.
    '''
    text = ''
    text += _get_prepend_defines(macro_definitions)
    with open(filepath, "r") as f:
        text += f.read()

    tmp_filepath = filepath + "_cpptmp.c"
    with open(tmp_filepath, "w") as f:
        f.write(text)
    return tmp_filepath


def get_preprocessed_source(
        filepath,
        flags,
        include_paths,
        additional_macro_definitions=default_macro_definitions):

    tmp_filepath = _prepend_defines(filepath, additional_macro_definitions)
    preprocessor_command_split = _get_preprocessor_command_split(
        flags, include_paths, tmp_filepath)
    output = subprocess.run(preprocessor_command_split, capture_output=True)
    stderr = output.stderr.decode("UTF-8")
    if stderr:
        print("STDERR:", stderr)
    os.remove(tmp_filepath)
    return output.stdout.decode("UTF-8")
