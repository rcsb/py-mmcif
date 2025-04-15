# File: setup.py
# Date: 17-Dec-2017
#
# Update:  17-Jan-2018 jdw - resolve python virtual env issues with Tox.
#           8-Aug-2018 jdw - add py3.7
#          14-May-2021 jdw - make requirements*.txt authoritative
#
import glob
import os
import platform
import re
import subprocess
import sys
from distutils.version import LooseVersion  # pylint: disable=no-name-in-module,import-error

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir="", sources=None):
        sources = sources if sources else []
        Extension.__init__(self, name, sources=sources)
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake >= 3.4 must be installed to build the following extensions: " + ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmakeVersion = LooseVersion(re.search(r"version\s*([\d.]+)", out.decode()).group(1))
            if cmakeVersion < "3.4.0":
                raise RuntimeError("CMake >= 3.4.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        debug = True
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmakeArgs = ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir, "-DPYTHON_EXECUTABLE=" + sys.executable]

        # We need to help cmake find the correct python for this virtual env -
        # ---
        libPath = None
        lsp = os.path.join(sys.exec_prefix, "lib", "libpython") + "*"
        lpL = glob.glob(lsp)
        if lpL:
            libPath = lpL[0]
        elif hasattr(sys, "base_exec_prefix"):
            lsp = os.path.join(sys.base_exec_prefix, "lib", "libpython") + "*"  # pylint: disable=no-member
            lpL = glob.glob(lsp)
            if lpL:
                libPath = lpL[0]
        if libPath:
            cmakeArgs += ["-DPYTHON_LIBRARY=" + libPath]
        else:
            print("------ WARNING could not locate python library")
        # ---
        inclPath = None
        isp = os.path.join(sys.exec_prefix, "include", "python") + "%s.%s" % (sys.version_info.major, sys.version_info.minor) + "*"
        ipL = glob.glob(isp)
        if ipL:
            inclPath = ipL[0]
        elif hasattr(sys, "base_exec_prefix"):
            isp = os.path.join(sys.base_exec_prefix, "include", "python") + "%s.%s" % (sys.version_info.major, sys.version_info.minor) + "*"  # pylint: disable=no-member
            ipL = glob.glob(isp)
            if ipL:
                inclPath = ipL[0]
        if inclPath:
            cmakeArgs += ["-DPYTHON_INCLUDE_DIR=" + inclPath]
        else:
            print("------ WARNING could not locate python include files")
        # ---
        cfg = "Debug" if self.debug else "Release"
        buildArgs = ["--config", cfg]

        if platform.system() == "Windows":
            cmakeArgs += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)]
            if sys.maxsize > 2 ** 32:
                cmakeArgs += ["-A", "x64"]
            buildArgs += ["--", "/m"]
        else:
            cmakeArgs += ["-DCMAKE_BUILD_TYPE=" + cfg]
            buildArgs += ["--", "-j2"]


        if sys.platform.startswith("darwin"):
            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmakeArgs += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get("CXXFLAGS", ""), self.distribution.get_version())
        env["RUN_FROM_DISUTILS"] = "yes"
        #
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        #
        if debug:
            print("------------- setup.py -----------------")
            print("Extension source path ", ext.sourcedir)
            print("CMAKE_ARGS ", cmakeArgs)
            print("self.build_temp ", self.build_temp)
            print("extdir", extdir)
            print("ext.name", ext.name)
            print("sys.executable", sys.executable)
            print("sys.exec_prefix", sys.exec_prefix)
            print("CXXFLAGS ", env["CXXFLAGS"])

        #
        subprocess.check_call(["cmake", ext.sourcedir] + cmakeArgs, cwd=self.build_temp, env=env)
        subprocess.check_call(["cmake", "--build", "."] + buildArgs, cwd=self.build_temp)


packages = []
thisPackage = "mmcif"

# Load packages from requirements*.txt
with open("requirements.txt", "r") as ifh:
    packagesRequired = [ln.strip() for ln in ifh.readlines()]

with open("requirements-test.txt", "r") as ifh:
    packagesTest = [ln.strip() for ln in ifh.readlines()]

with open("requirements-doc.txt", "r") as ifh:
    packagesDoc = [ln.strip() for ln in ifh.readlines()]

with open("README.md", "r") as ifh:
    longDescription = ifh.read()

with open("mmcif/__init__.py", "r") as ifh:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', ifh.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="mmCIF Core Access Library",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    author="John Westbrook",
    author_email="john.westbrook@rcsb.org",
    url="http://mmcif.wwpdb.org",
    #
    license="Apache 2.0",
    classifiers=[
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    #
    install_requires=packagesRequired,
    tests_require=packagesTest,
    extras_require={"all": packagesRequired + packagesTest + packagesTest, "test": packagesTest, "docs": packagesTest},
    #
    packages=find_packages(exclude=["mmcif.tests", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.h", "*.C", ".c", "*.cpp"]
    },
    test_suite="mmcif.tests",
    #
    ext_modules=[CMakeExtension("mmcif.core.mmciflib")],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "build_dict_cli=mmcif.io.BuildDictionaryExec:main",
        ]
    },
)
