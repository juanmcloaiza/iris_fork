#!/usr/bin/env python

##################################################
#                                                #
#  For this program to run, you need to acrivate #
#  the pipistrello environment. You do this by   #
#  entering the following command in the shell:  #
#                                                #
#        $ source activate pipistrello           #
#                                                #
##################################################

#Import modules:
import sys
import argparse
from importlib.machinery import SourceFileLoader
import os, errno

#The following line should be replaced by "import iris"
#import iris
#iris = SourceFileLoader("iris", "/home/juan/MHPC-Thesis/iris/lib/iris/__init__.py").load_module()
iris = SourceFileLoader("iris", "../lib/iris/__init__.py").load_module()
iris.FUTURE.netcdf_promote = True

def silentremove(filename):
    try:
        os.remove(filename)
#        print("\t {} removed".format(filename))
    except OSError as e:
        if e.errno == errno.EISDIR: 
            for f in os.listdir(filename):
                silentremove(filename+"/"+f)
            os.rmdir(filename)
#            print("\t {} removed".format(filename))
        elif e.errno == errno.ENOENT: # errno.ENOENT = no such file or directory
            print("{}: No such file or directory.".format(filename))
        else:
            raise
def print_usage():
    print("\n\tUsage: {} {}\n".format(sys.argv[0],' <filename1> <filename2> <filename3> ... [--restriction <restriction 1> <restriction 2> ...]'))
    return

def command_line_load():
    #Clean compiled files:
    print("Cleaning up compiled files...")
    silentremove('compiled_krb')
    silentremove('__pycache__')

    #parse for command line arguments
    parser = argparse.ArgumentParser(description='Loads cubes from files')
    parser.add_argument('filenames', metavar='path/to/NEtCDF_file',type=str,  nargs='+')
    parser.add_argument('--restriction',required=False,type=str, nargs='+')

    args = parser.parse_args()
    filenames=args.filenames
    restriction = args.restriction

    #Load cubes from file:
    try:
        cubes = iris.load(filenames,constraints=restriction)
    except IOError:
        print('Cannot open one or more files in {}.'.format(filenames)+
          ' Please make sure that all files exist.')
        print_usage()
        sys.exit()
    except ValueError:
        print('Cannot open one or more files in {}.'.format(filenames)+
          ' Please make sure that all files are '
          'compatible with Iris.')
        print_usage()
        sys.exit()


    #print loaded cubes:
    print('\n\n')
    print("{} cubes generated from {} files (restricted to {}):".format(len(cubes),len(filenames),restriction) )
    print(cubes)
    if(len(cubes) == 0):
        cubes_avail = iris.load(filenames)
        print("Available cubes: ")
        print(cubes_avail)
    return cubes


def cleanup_and_finish():
    #Clean compiled files:
    print("Cleaning up compiled files...")
    silentremove('compiled_krb')
    silentremove('__pycache__')

    #If everything ran smoothly, one should see this:
    print("------------------")
    print("Finished execution")

