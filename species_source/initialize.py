from __future__ import print_function
import pathlib
import argparse
import exodus3 as exodus
import sys
import operator
import numpy as np
import scipy.interpolate

a = 0.1
b = 0.9
eps = 0.1

def u_init(x,y,z):
    u0 = a+b
    u = u0 + eps*np.random.random_sample(np.shape(x))*u0
    return u


def v_init(x,y,z):
    v0 = b / ((a+b)**2)
    v = v0 + eps*np.random.random_sample(np.shape(x))*v0
    return v

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize level set function")
    parser.add_argument("input_mesh", metavar="Input_Mesh", type=str, help="mesh")

    parser.add_argument(
        "output_mesh", metavar="Output_Mesh", type=str, help="output mesh"
    )
    args = parser.parse_args()

    try:
        input_mesh = exodus.exodus(args.input_mesh)
        file_to_rem = pathlib.Path(args.output_mesh)
        file_to_rem.unlink(True)
        output_mesh = input_mesh.copy(args.output_mesh)
    except Exception as e:
        print(e)
        print("Could not open exodus file", file=sys.stderr)
        sys.exit(-1)

    x, y, z = input_mesh.get_coords()

    output_mesh.set_node_variable_number(2)
    output_mesh.put_time(1, 0)

    var = "Y0"
    output_mesh.put_node_variable_name(var, 1)

    output_mesh_values = u_init(x, y, z)

    output_mesh.put_node_variable_values(var, 1, output_mesh_values)

    var = "Y1"
    output_mesh.put_node_variable_name(var, 2)

    output_mesh_values = v_init(x, y, z)

    output_mesh.put_node_variable_values(var, 1, output_mesh_values)

    input_mesh.close()
    output_mesh.close()
