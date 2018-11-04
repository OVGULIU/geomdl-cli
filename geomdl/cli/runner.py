"""

    geomdl-cli - Run NURBS-Python (geomdl) from the command line
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
from . import __version__
from . import __usage__
from . import helpers_yaml
from . import helpers_nurbs


def command_help(**kwargs):
    """\
HELP: Displays GEOMDL-CLI help\
    """
    print(__usage__)


def command_version(**kwargs):
    """\
VERSION: Displays GEOMDL-CLI version\
    """
    print("GEOMDL-CLI version", __version__)


def command_plot(yaml_file, **kwargs):
    """\
PLOT: Plots single or multi NURBS curves or surfaces

"geomdl plot" command takes a YAML file as the input. The YAML file can contain single or multiple shapes. \
The YAML file format is described in the GEOMDL-CLI documentation.

Alternatively, NURBS-Python library may be used to export curves and surfaces as YAML files. \
Please see "geomdl.exchange.export_yaml" documentation for details.

Usage:

    geomdl plot {yaml file}                             plots the shape defined in the YAML file
    geomdl plot {yaml file} --delta=0.1                 plots the shape using the evaluation delta of 0.1
    geomdl plot {yaml file} --index=2                   plots the 2nd shape defined in the YAML file
    geomdl plot {yaml file} --index=1 --delta=0.025     plots the 1st shape using the evaluation delta of 0.025

Available parameters:
    --help      displays this message
    --index=n   plots n-th curve or surface in the YAML file (works only for multi shapes)
    --delta=d   allows customization of the pre-defined evaluation delta in the YAML file. 0.0 < d < 1.0

Please see GEOMDL-CLI documentation for details.\
    """
    # Get keyword arguments
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)

    # Process YAML file
    yaml_data = helpers_yaml.read_yaml_file(yaml_file)
    nurbs_data = yaml_data['shape']
    try:
        vis_data = yaml_data['visualization']
    except KeyError:
        vis_data = {}

    # Detect NURBS shape building function
    shape_types = dict(
        curve=dict(
            single=helpers_nurbs.build_curve_single,
            multi=helpers_nurbs.build_curve_multi,
        ),
        surface=dict(
            single=helpers_nurbs.build_surface_single,
            multi=helpers_nurbs.build_surface_multi,
        ),
    )

    try:
        build_func = shape_types[str(nurbs_data['type'])]
    except KeyError:
        print("Unsupported shape type: ", str(nurbs_data['type']), "\n")
        types_str = ", ".join([k for k in shape_types.keys()])
        print("Possible values are:", types_str)
        sys.exit(1)

    # Plot the NURBS object
    try:
        ns = helpers_nurbs.build_nurbs_shape(data=nurbs_data['data'], build_func=build_func,
                                             shape_delta=shape_delta, shape_idx=shape_idx)
        helpers_nurbs.build_vis(obj=ns, data=vis_data)
        ns.render()
    except KeyError as e:
        print("Problem with the YAML file. The following key does not exist: {}".format(e.args[-1]))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)