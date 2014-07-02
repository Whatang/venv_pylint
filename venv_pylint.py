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

Additionally, it is sometimes helpful to have different versions of the pylint
rc file for different projects, in order to specify different types of code
cehcking. A Django project may have different requirements from a PyQt one.
Again, PyDev gives no way to specify different per-project Pylint setups.

This script wraps pylint so that it automatically finds for the right version
of pylint to run for the Python interpreter which is running it. It can also
be configured to search for and use a project-specific pylint rc file.

To use this script with PyDev, make sure that you have pylint installed in each
of the interpreters that you have configured in PyDev. Then simply put
the venv_pylint.py file somewhere, and enter its location in the
PyDev > PyLint preferences section, in the "Location of the pylint executable"
box. Runnning pylint from pydev will now pick up the appropriate install of
pylint for each interpreter.

You can also run this script directly with any python interpreter, and it will
find and run the correct version of pylint (assuming it is installed).

If no --rcfile option is specified, then venv_pylint will look for
a file called lint.rc in the directory containing the first target file
specified, i.e. the first file which pylint will analyse. If no such lint.rc
file is found, then the parent directory will be searched, then the next
directory up, and so on, until a lint.rcis found or the file system root is
reached. If any such lint.rc file is found it will be passed to pylint as an
argument and used to configure for the code analysis.

There are some additional options you can give to this script which will
help specify the right pylint rcfile to use:

--override-rc
  If this option is given then the rcfile searching described above is
  performed even if a --rcfile option is given. If a lint.rc is found, then
  it will replace the --rcfile specified on the command line. Otherwise, the
  existing --rcfile given will be used. This allows a default rcfile to be
  specified, while allowing projects to override it with their own if
  necessary.

--rc-name=RC_NAME
  Specify a different file name to search for as the per-project rcfile,
  instead of the default "lint.rc".
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

def find_venv_rcfile(args, lint_name):
    """Find a project-specific pylint rcfile.

    1. Find the first pylint target given.
    2. Look in the directory containing that target, and all parent dirs
       until a file matching lint_name is found.
    """
    for arg in args:
        if not arg.startswith("-"):
            if os.path.isdir(arg):
                current_dir = arg
            else:
                current_dir = os.path.dirname(arg)
            break
    else:
        return None
    last_dir = None
    while last_dir != current_dir:
        potential_rc_file = os.path.join(current_dir, lint_name)
        if os.path.exists(potential_rc_file):
            return get_capitalized_filename(potential_rc_file)
        last_dir = current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def process_arguments():
    """Process/remove venv_pylint specific arguments before passing to pylint.

    This function takes the arguments specified on the command line and
    processes them to remove the venv_pylint specific options and to update/add
    the --rcfile option as necessary.
    """
    override_arg = "--override-rc"
    rcfile_arg = "--rcfile"
    rc_name_arg = "--rc-name"
    lint_file_name = "lint.rc"
    args = sys.argv[1:]
    print "Initial pylint arguments are:"
    print " ".join(args)
    has_override = any(x == override_arg for x in args)
    if has_override:
        args.remove(override_arg)
    has_rcfile = any(x.startswith(rcfile_arg) for x in args)
    if any(x.startswith(rc_name_arg) for x in args):
        lint_args = set()
        for arg in args:
            if arg.startswith(rc_name_arg):
                if '=' not in arg:
                    continue
                lint_file_name = arg.split('=', 1)[1]
                lint_file_name = lint_file_name.strip()
                lint_args.add(arg)
        for arg in lint_args:
            args.remove(arg)
    venv_rcfile = find_venv_rcfile(args, lint_file_name)
    new_rcfile_arg = (rcfile_arg + "=")
    if venv_rcfile is not None:
        new_rcfile_arg += venv_rcfile
    if has_override and has_rcfile and venv_rcfile is not None:
        for index, arg in enumerate(args):
            if arg.startswith(rcfile_arg):
                print "Using rc file " + venv_rcfile
                args[index] = new_rcfile_arg
    elif not has_rcfile and venv_rcfile is not None:
        print "Using rc file " + venv_rcfile
        args.insert(0, new_rcfile_arg)
    print "Final pylint arguments are:"
    print " ".join(args)
    return args

def main():
    """Wrap pylint: run the right version with the correct rcfile.

    1. Find the right version of pylint.
    2. Update the arguments to remove venv_pylint specific options and set the
       --rcfile option correctly.
    3. Run pylint with the new arguments, piping stdout/stderr appropriately.
    """
    lint_path = get_lint_path()
    if not lint_path:
        print "Could not find pylint!"
        sys.exit(1)
    print "PyLint is at " + lint_path
    import subprocess
    args = [get_capitalized_filename(sys.executable),
            lint_path] + process_arguments()
    print " ".join(args)
    subprocess.call(args = args,
                    stdout = sys.stdout, stderr = sys.stderr)

if __name__ == '__main__':
    main()
