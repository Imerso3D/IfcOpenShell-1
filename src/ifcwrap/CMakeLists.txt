################################################################################
#                                                                              #
# This file is part of IfcOpenShell.                                           #
#                                                                              #
# IfcOpenShell is free software: you can redistribute it and/or modify         #
# it under the terms of the Lesser GNU General Public License as published by  #
# the Free Software Foundation, either version 3.0 of the License, or          #
# (at your option) any later version.                                          #
#                                                                              #
# IfcOpenShell is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 #
# Lesser GNU General Public License for more details.                          #
#                                                                              #
# You should have received a copy of the Lesser GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.         #
#                                                                              #
################################################################################

FIND_PACKAGE(SWIG)
IF(NOT SWIG_FOUND)
	MESSAGE(FATAL_ERROR "BUILD_IFCPYTHON enabled, but unable to find SWIG. Disable BUILD_IFCPYTHON or fix SWIG paths to proceed.")
ENDIF()

INCLUDE(${SWIG_USE_FILE})

IF(NOT "$ENV{PYTHON_INCLUDE_DIR}" STREQUAL "")
	SET(PYTHON_INCLUDE_DIR $ENV{PYTHON_INCLUDE_DIR} CACHE FILEPATH "Python header files")
	MESSAGE(STATUS "Looking for Python header files in: ${PYTHON_INCLUDE_DIR}")
ENDIF()
IF(NOT "$ENV{PYTHON_LIBRARY}" STREQUAL "")
	SET(PYTHON_LIBRARY $ENV{PYTHON_LIBRARY} CACHE FILEPATH "Python library file")
	MESSAGE(STATUS "Looking for Python library file in: ${PYTHON_LIBRARY}")
ENDIF()

find_package (Python COMPONENTS Interpreter Development)
IF(NOT Python_FOUND)
	MESSAGE(FATAL_ERROR "BUILD_IFCPYTHON enabled, but unable to find Python lib or header. Disable BUILD_IFCPYTHON or fix Python paths to proceed.")
ENDIF()

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

SET(CMAKE_SWIG_FLAGS "")
# NOTE Workaround for most likely missing debug Python libraries on Windows (requires Python built from the source).
# Python 3.5 intaller and onwards will have an option to install the debug libraries too.
# NOTE PYTHON_DEBUG_LIBRARIES appears to be a deprecated variable
IF (WIN32 AND NOT PYTHON_DEBUG_LIBRARIES)
	MESSAGE(STATUS "PYTHON_DEBUG_LIBRARIES not found, defining SWIG_PYTHON_INTERPRETER_NO_DEBUG workaround for IfcWrap.")
	ADD_DEFINITIONS(-DSWIG_PYTHON_INTERPRETER_NO_DEBUG)
ENDIF()

SET_SOURCE_FILES_PROPERTIES(IfcPython.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(ifcopenshell_wrapper python IfcPython.i)
if("$ENV{LDFLAGS}" MATCHES ".undefined.suppress")
# On osx there is some state in the python dylib. With `-Wl,undefined,suppress` we can ignore the missing symbols at compile time.
SWIG_LINK_LIBRARIES(ifcopenshell_wrapper ${IFCOPENSHELL_LIBRARIES} CONAN_PKG::opencascade
    CONAN_PKG::icu CONAN_PKG::boost)
else()
SWIG_LINK_LIBRARIES(ifcopenshell_wrapper ${IFCOPENSHELL_LIBRARIES} Python::Python CONAN_PKG::opencascade
    CONAN_PKG::icu CONAN_PKG::boost)
endif()

INSTALL(FILES 
        "${CMAKE_BINARY_DIR}/ifcwrap/ifcopenshell_wrapper.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/__init__.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/entity_instance.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/file.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/guid.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/main.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/template.py"
    DESTINATION "ifcopenshell")
INSTALL(FILES
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/geom/__init__.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/geom/app.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/geom/code_editor_pane.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/geom/main.py"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ifcopenshell-python/ifcopenshell/geom/occ_utils.py"
        DESTINATION "ifcopenshell/geom")
INSTALL(TARGETS _ifcopenshell_wrapper DESTINATION "ifcopenshell")
