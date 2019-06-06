# File: setup.py
# Date: 17-Dec-2017
#
# Update:  17-Jan-2018 jdw - resolve python virtual env issues with Tox.
#           8-Aug-2018 jdw - add py3.7
#
import glob
import os
import platform
import re
import subprocess
import sys
from distutils.version import LooseVersion

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir="", sources=[]):
        Extension.__init__(self, name, sources=sources)
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " + ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r"version\s*([\d.]+)", out.decode()).group(1))
            if cmake_version < "3.1.0":
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):

        #
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir, "-DPYTHON_EXECUTABLE=" + sys.executable]

        # we need to help cmake find the correct python for this virtual env -
        if hasattr(sys, "real_prefix"):
            lsp = os.path.join(sys.real_prefix, "lib", "libpython") + "*"
            isp = os.path.join(sys.real_prefix, "include", "python") + "%s.%s" % (sys.version_info.major, sys.version_info.minor) + "*"
        else:
            lsp = os.path.join(sys.exec_prefix, "lib", "libpython") + "*"
            isp = os.path.join(sys.exec_prefix, "include", "python") + "%s.%s" % (sys.version_info.major, sys.version_info.minor) + "*"
        #
        lpL = glob.glob(lsp)
        if len(lpL):
            lp = lpL[0]
            cmake_args += ["-DPYTHON_LIBRARY=" + lp]

        ipL = glob.glob(isp)
        if len(ipL):
            ip = ipL[0]
            cmake_args += ["-DPYTHON_INCLUDE_DIR=" + ip]
        #
        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get("CXXFLAGS", ""), self.distribution.get_version())
        env["RUN_FROM_DISUTILS"] = "yes"
        #
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        #
        if False:
            print("------------------------------")
            print("Extension source path ", ext.sourcedir)
            print("CMAKE_ARGS ", cmake_args)
            print("self.build_temp ", self.build_temp)
            print("extdir", extdir)
            print("ext.name", ext.name)
            print("sys.executable", sys.executable)
            print("sys.exec_prefix", sys.exec_prefix)
            print("CXXFLAGS ", env["CXXFLAGS"])

        #
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=self.build_temp)


packages = []
thisPackage = "mmcif"
requires = ["future", "six"]


with open("mmcif/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="mmCIF Core Access Library",
    long_description="See:  README.md",
    author="John Westbrook",
    author_email="john.westbrook@rcsb.org",
    url="http://mmcif.wwpdb.org",
    #
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    # entry_points={
    #    'console_scripts': [
    #        'onedep_validate_cli=onedep.cli.validate_cli:run',
    #    ]
    # },
    #
    install_requires=["future", "six"],
    packages=find_packages(exclude=["mmcif.tests", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.h", "*.C", ".c", "*.cpp"]
    },
    #
    #
    test_suite="mmcif.tests",
    tests_require=["tox"],
    #
    # Not configured ...
    extras_require={"dev": ["check-manifest"], "test": ["coverage"]},
    # Added for
    command_options={"build_sphinx": {"project": ("setup.py", thisPackage), "version": ("setup.py", version), "release": ("setup.py", version)}},
    ext_modules=[CMakeExtension("mmcif.core.mmciflib")],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
