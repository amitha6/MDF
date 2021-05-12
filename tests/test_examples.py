"""
Runs and tests everything in the examples folder.
"""

import pytest
import glob
import runpy
import os
import sys

from distutils.dir_util import copy_tree

example_scripts = glob.glob("examples/**/*.py", recursive=True)


@pytest.fixture(autouse=True)
def chdir_back_to_root():
    """
    This fixture sets up and tears down state before each example is run. Certain examples
    require that they are run from the local directory in which they reside. This changes
    directory and adds the local directory to sys.path. It reverses this after the test
    finishes.
    """

    # Get the current directory before running the test
    cwd = os.getcwd()
    sys.path.append(".")

    yield

    # We need chdir back to root of the repo
    os.chdir(cwd)
    sys.path.pop()


@pytest.mark.parametrize("script", example_scripts)
def test_example(script, tmpdir):
    """
    Run the examples/MDF
    """
    # Get the full path for the script
    script = os.path.abspath(script)

    # Some of the scripts in examples/MDF import from the local directory. So lets run from the scripts
    # local directory.
    dir_path = os.path.dirname(os.path.realpath(script))

    # Copy the contents of this directory to a tmpdir (so any files generated by the example will get cleaned up when
    # we run it)
    copy_tree(dir_path, tmpdir.strpath)

    os.chdir(tmpdir)

    runpy.run_path(os.path.basename(script), run_name="__main__")
