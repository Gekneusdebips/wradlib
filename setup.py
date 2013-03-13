# distribute_setup module will automatically download a matching version
#   of setuptools from PyPI, if it isn't present on the target system.
import distribute_setup
distribute_setup.use_setuptools()


import os
import sys
import site

### BEFORE importing distutils, remove MANIFEST. distutils doesn't
### properly update it when the contents of directories change.
##if os.path.exists('MANIFEST'): os.remove('MANIFEST')

##from distutils.core import setup
from setuptools import setup
from distutils.sysconfig import get_python_lib

import subprocess as sub

MAJOR               = 0
MINOR               = 1
MICRO               = 1
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

bufr_dir = "wradlib/bufr_3.1"

##from distutils.command.build_py import build_py
from setuptools.command.build_py import build_py
class build_bufr(build_py):
    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            #---------------------------------------------------------------------------
            # START: BUFR COMPILATION
            # This is the TEMPORARY solution for compiling and installing the BUFR library
            # It is simply a call to a makefile for gcc (Windows: mingw gcc) in the BUFR library directory
            # For this purpose, MinGW (or on Linux: gcc) needs to be installed
            os.chdir(bufr_dir)
            if os.sys.platform=="win32":
                # Test functionality of MinGW
                retval = sub.call("mingw32-make --version")
                if not retval==0:
                    print "Please check your MinGW installation."
                    print "Apparently MinGW is not properly installed on your machine."
                    print "You need MinGW to properly install the wradlib bufr module."
                    print "Normally, MinGW comes with Python(x,y)"
                else:
                    retval = sub.call("mingw32-make -f makefile_mingw.gcc clean")
                    retval = sub.call("mingw32-make -f makefile_mingw.gcc decbufr")
        ##        # This should be used if the shared BUFR library is functional
        ##        sub.call("mingw32-make -f makefile_mingw.gcc dll")
            elif "linux" in os.sys.platform:
                retval = sub.call(["make", "-f", "makefile.gcc", "clean"])
                retval = sub.call(["make", "-f", "makefile.gcc", "decbufr"])
        ##        # This should be used if the shared BUFR library is functional
        ##        sub.call("make -f makefile.gcc shlib")
            else:
                print "ATTENTION: wradlib BUFR module not yet available to OS: %s" % os.sys.platform
                print "You have to compile the BUFR software for your OS."
            os.chdir('../..')
            # END: BUFR COMPILATION
            #---------------------------------------------------------------------------


        # distutils uses old-style classes, so no super()
        build_py.run(self)


if __name__ == '__main__':

##    #---------------------------------------------------------------------------
##    # START: BUFR COMPILATION
##    # This is the TEMPORARY solution for compiling and installing the BUFR library
##    # It is simply a call to a makefile for gcc (Windows: mingw gcc) in the BUFR library directory
##    # For this purpose, MinGW (or on Linux: gcc) needs to be installed
##    os.chdir(bufr_dir)
##    if os.sys.platform=="win32":
##        # Test functionality of MinGW
##        retval = sub.call("mingw32-make --version")
##        if not retval==0:
##            print "Please check your MinGW installation."
##            print "Apparently MinGW is not properly installed on your machine."
##            print "You need MinGW to properly install the wradlib bufr module."
##            print "Normally, MinGW comes with Python(x,y)"
##        else:
##            retval = sub.call("mingw32-make -f makefile_mingw.gcc clean")
##            retval = sub.call("mingw32-make -f makefile_mingw.gcc decbufr")
####        # This should be used if the shared BUFR library is functional
####        sub.call("mingw32-make -f makefile_mingw.gcc dll")
##    elif "linux" in os.sys.platform:
##        retval = sub.call(["make", "-f", "makefile.gcc", "clean"])
##        retval = sub.call(["make", "-f", "makefile.gcc", "decbufr"])
####        # This should be used if the shared BUFR library is functional
####        sub.call("make -f makefile.gcc shlib")
##    else:
##        print "ATTENTION: wradlib BUFR module not yet available to OS: %s" % os.sys.platform
##        print "You have to compile the BUFR software for your OS."
##    os.chdir('../..')
##    # END: BUFR COMPILATION
##    #---------------------------------------------------------------------------


    # targets and List of files which need to be copied to the site packages installation directory
    if "--user" in sys.argv:
        sitepackdir = site.USER_SITE
    else:
        sitepackdir = get_python_lib()
    # BUFR
    bufr_trg_dir = os.path.join(sitepackdir, bufr_dir)
    bufr_files = []
##    for f in os.listdir(bufr_dir):
##        if ( f.endswith(".csv") ) or ( f=="decbufr.exe") or ( f=="decbufr") or \
##        ( f=="decbufr.a") or ( f=="decbufr.dll") or ("zdll" in f) or ("zlib" in f):
##            bufr_files.append(os.path.join(bufr_dir, f))
    for f in os.listdir(bufr_dir):
        if f.endswith(".exe"):
            bufr_files.append(os.path.join(bufr_dir, f))
##    # EXAMPLES
##    example_trg_dir = os.path.join(sitepackdir, "wradlib/examples")
##    example_files = []
##    for f in os.listdir("examples"):
##        if os.path.isfile(f):
##            example_files.append(os.path.join("examples", f))
##    # EXAMPLE DATA
##    data_trg_dir = os.path.join(sitepackdir, "wradlib/examples/data")
##    data_files = [ os.path.join("examples/data", f) for f in os.listdir("examples/data") ]
##    # TESTS
##    tests_trg_dir = os.path.join(sitepackdir, "wradlib/tests")
##    tests_files = [ os.path.join("wradlib/tests", f) for f in os.listdir("wradlib/tests") ]


    setup(name='wradlib',
          version=VERSION,
          description='Open Source Library for Weather Radar Data Processing',
          long_description = """\
wradlib - An Open Source Library for Weather Radar Data Processing
==================================================================

wradlib is designed to assist you in the most important steps of
processing weather radar data. These may include: reading common data
formats, georeferencing, converting reflectivity to rainfall
intensity, identifying and correcting typical error sources (such as
clutter or attenuation) and visualising the data.

""",
          license='BSD',
          url='http://wradlib.bitbucket.org/',
          download_url='https://bitbucket.org/wradlib/wradlib',
          packages=['wradlib'],
          include_package_data=True, # see MAINFEST.in
          data_files=[(bufr_trg_dir, ["wradlib/bufr_3.1/decbufr.exe"])],#, (example_trg_dir, example_files),
##            (data_trg_dir, data_files), (tests_trg_dir, tests_files)],
          cmdclass={'build_py': build_bufr},
          classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          ],
          install_requires=["numpydoc >= 0.3", "pyproj >= 1.9"]
          )

