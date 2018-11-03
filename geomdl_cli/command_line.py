"""

    geomdl_runner - Run NURBS-Python (geomdl) from the command line
    Copyright (c) 2018 Onur Rauf Bingol <orbingol@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

import sys
from . import runner

# Default commands
GEOMDL_DEFAULT_COMMANDS = dict(
    help=dict(
        command=runner.command_help,
        num_arguments=0,
    ),
    version=dict(
        command=runner.command_version,
        num_arguments=0,
    ),
    plot=dict(
        command=runner.command_plot,
        num_arguments=1,
    ),
)


def main():
    # Get number of command line arguments
    argc = len(sys.argv)

    # Show help if there are no command line arguments
    if argc < 2:
        runner.command_help()
        sys.exit(0)

    # Command execution
    command = sys.argv[1]
    try:
        current_command = GEOMDL_DEFAULT_COMMANDS[command]
        try:
            if current_command['num_arguments'] > 0:
                if argc - 2 < current_command['num_arguments']:
                    print("To execute", str(command).upper(), "command", str(current_command['num_arguments']), "command line argument(s) required.")
                    sys.exit(1)
                current_command['command'](*sys.argv[2:])
            else:
                current_command['command']()
        except KeyError:
            print("Problem executing", str(command).upper(), "command. Please see the documentation for details.")
            sys.exit(1)
        except Exception as e:
            print("An error occurred: {}".format(e.args[-1]))
            sys.exit(1)
    except KeyError:
        print("The command", str(command).upper(), "does not exist. Please run 'geomdl help' for command reference.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)

    # Command execution completed
    sys.exit(0)