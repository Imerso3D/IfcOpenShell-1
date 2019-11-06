#!/usr/bin/env python3

import os

from conans import CMake, tools
from conans.model.conan_file import ConanFile


class IfcOpenShell(ConanFile):
    name = "ifcopenshell"
    license = "LGPL-3.0"
    description = "IfcOpenShell is an open source (LGPL) software library that helps users and software developers to work with the IFC file format."
    generators = "cmake"
    homepage = "http://ifcopenshell.org/"
    exports_sources = (
        "*",
        "!build",
        "!*-build-*",
        "!conan*",
        "!test_package",
        "!graph_info.json",
        "!imerso_library.cmake",
        "!.idea",
        "!test",
        "!examples",
        "!template_instantiation_tool",
    )
    _src_dir = "./"
    settings = "os", "compiler", "build_type", "arch", "python_version"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}

    requires = (
        "opencascade/7.3.0@imerso/master",
        "boost/1.68.0@conan/stable",
        "icu/62.1@bincrafters/stable",
        "libxml2/2.9.9@bincrafters/stable",
        "swig_installer/3.0.12@imerso/master",
        "zlib/1.2.11@conan/stable",  # Fix for unspecific dependency zlib/1.2.11 in libxml2/2.9.9@bincrafters/stable
    )

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure_cmake(self):
        cmake = CMake(self)

        # Configure CMake library build:
        cmake.definitions["ENABLE_BUILD_OPTIMIZATIONS"] = (
            self.settings.build_type == "Release"
        )
        cmake.definitions["IFCCONVERT_DOUBLE_PRECISION"] = True
        cmake.definitions["USE_VLD"] = False
        cmake.definitions["USE_MMAP"] = False
        cmake.definitions["USE_IFC4"] = False
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["BUILD_IFCMAX"] = False
        cmake.definitions["BUILD_IFCPYTHON"] = True
        cmake.definitions["COLLADA_SUPPORT"] = False
        cmake.definitions["UNICODE_SUPPORT"] = True
        cmake.definitions["BUILD_GEOMSERVER"] = False
        cmake.definitions["BUILD_CONVERT"] = True

        cmake.definitions["PYTHON_EXECUTABLE:FILEPATH"] = os.environ[
            "Python%s_EXECUTABLE" % self.settings.python_version.value.replace(".", "")
        ]

        # RPATH fix:
        cmake.definitions["CMAKE_SKIP_BUILD_RPATH"] = True

        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        if "CCACHE" in os.environ:
            cmake.definitions["CMAKE_CXX_COMPILER_LAUNCHER"] = os.environ["CCACHE"]

        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.configure(source_folder=f"{self._src_dir}/cmake")
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

        self.copy("FindIfcParse.cmake", src=".", dst=".")
        self.copy("FindIfcGeom.cmake", src=".", dst=".")

        self.copy("COPYING", "licenses", self._src_dir)
        self.copy("COPYING.LESSER", "licenses", self._src_dir)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]

        self.cpp_info.includedirs = ["include"]

        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["rt", "dl"])

            if self.settings.compiler == "gcc":
                self.cpp_info.libs.append("m")

        self.env_info.PYTHONPATH.append(self.package_folder)
