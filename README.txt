venv_pylint wraps the right pylint for the current virtualenv.

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