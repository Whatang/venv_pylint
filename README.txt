venv_pylint Copyright (C) 2014 Michael Thomas

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
  
LICENSING INFORMATION

venv_pylint is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

See the file COPYING for details of the GNU GPL.

Contact details: venv_pylint@whatang.org
