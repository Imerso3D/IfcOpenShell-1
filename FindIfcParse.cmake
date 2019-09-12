# Exported target: IfcOpenShell::Parse

include(FindPackageHandleStandardArgs)
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)

if(${CMAKE_HOST_UNIX})
  find_path(IfcParse_INCLUDE_DIR
            NAMES ifcparse/IfcParse.h
            PATHS ${_IMPORT_PREFIX}/include
            NO_DEFAULT_PATH
            DOC "The directory where IfcParse.h resides")

  find_library(IfcParse_LIBRARY
               NAMES IfcParse
               PATHS ${_IMPORT_PREFIX}/lib
               NO_DEFAULT_PATH
               DOC "The IfcParse library")
endif()

mark_as_advanced(IfcParse_INCLUDE_DIR IfcParse_LLIBRARY)

find_package_handle_standard_args(IfcParse
                                  DEFAULT_MSG
                                  IfcParse_INCLUDE_DIR
                                  IfcParse_LIBRARY)

if(IfcParse_FOUND AND NOT TARGET IfcOpenShell::Parse)
  add_library(IfcOpenShell::Parse UNKNOWN IMPORTED)

  set_target_properties(IfcOpenShell::Parse
                        PROPERTIES IMPORTED_LINK_INTERFACE_LANGUAGES
                                   "CXX"
                                   IMPORTED_LOCATION
                                   "${IfcParse_LIBRARY}"
                                   INTERFACE_INCLUDE_DIRECTORIES
                                   "${IfcParse_INCLUDE_DIR}"
                                   IMPORTED_LINK_INTERFACE_LIBRARIES
                                   "CONAN_PKG::icu;CONAN_PKG::boost")
endif()
