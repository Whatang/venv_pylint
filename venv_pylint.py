'''venv_pylint wraps the right pylint for the current virtualenv.

Using virtualenv is great for isolating your python environment for the current
application. Pylint + PyDev is a great way of automatically analysing your
source code for mistakes. But PyDev does not play very well with virtualenv
when it comes to running pylint: only a single, global instance of pylint can
be specified, rather than being able to specify each pylint instance
per-project.

This causes problems when developing an application in a virtualenv, as you
might do for django for example. PyDev will run pylint with whichever
interpreter you specify for a given project, but it will only run the globally
specified instance of pylint. If your project has its own Python interpreter in
the virtualenv, then running a pylint installed in a different interpreter will
fail.

This script wraps pylint so that it automatically finds for the right version
of pylint to run for the Python interpreter which is running it.

To use this script with PyDev, make sure that you have pylint installed in each
of the interpreters that you have configured in PyDev. Then simply put
the venv_pylint.py file somewhere, and enter its location in the
PyDev > PyLint preferences section, in the "Location of the pylint executable"
box. Runnning pylint from pydev will now pick up the appropriate install of
pylint for each interpreter.

You can also run this script directly with any python interpreter, and it will
find and run the correct version of pylint (assuming it is installed).

It is sometimes helpful to have a per-project pylint rcfile. You can achieve
this by having a file named pylintrc in the project root, and no --rcfile
option specified. When run from PyDev, pylint will pick this up since the
project root is the working directory where pylint is run from, and pylint
looks for a file named pylintrc in its working directory.
'''
import sys
import os
import glob

def get_capitalized_filename(name):
    """Windows filenames are case-insensitive. Find the right case for a path.

    Some filenames are returned by some functions as all lower-case (e.g. the
    inspect module). Functions from other modules (e.g. lint), expect that
    filenames are case-sensitive, and therefore do not match these filenames
    correctly. It is therefore important to get the correct capitalization of
    a filename for passing to lint.

    This function is taken from user xvorsx's answer on StackOverflow at:

    http://stackoverflow.com/questions/3692261/in-python-how-can-i-get-the-correctly-cased-path-for-a-file/14742779#14742779
    """
    dirs = name.split('\\')
    # disk letter
    test_name = [dirs[0].upper()]
    for this_dir in dirs[1:]:
        test_name += ["%s[%s]" % (this_dir[:-1], this_dir[-1])]
    res = glob.glob('\\'.join(test_name))
    if not res:
        # File not found
        return None
    return res[0]

def get_lint_path():
    """Find the path to lint.py

    We find lint.py by importing the pylint module, and looking at where it is
    loaded from. The lint.py script should be in the same directory.
    """
    try:
        import pylint
        import inspect
    except ImportError:
        return ""
    pylint_dir = os.path.dirname(inspect.getfile(pylint))
    pylint_file = os.path.join(pylint_dir, "lint.py")
    return get_capitalized_filename(pylint_file)

def main():
    """Wrap pylint: run the right version for the current interpreter.

    1. Find the right version of pylint.
    2. Run pylint with the interpreter, piping stdout/stderr appropriately.
    """
    lint_path = get_lint_path()
    if not lint_path:
        print "Could not find pylint!"
        sys.exit(1)
    print "PyLint is at " + lint_path
    import subprocess
    args = [get_capitalized_filename(sys.executable), lint_path] + sys.argv[1:]
    print " ".join(args)
    subprocess.call(args = args,
                    stdout = sys.stdout, stderr = sys.stderr)

if __name__ == '__main__':
    main()
