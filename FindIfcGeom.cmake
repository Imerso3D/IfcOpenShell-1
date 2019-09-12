# Exports target: IfcOpenShell::Geom

include(FindPackageHandleStandardArgs)
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)

if(${CMAKE_HOST_UNIX})
  find_path(IfcGeom_INCLUDE_DIR
            NAMES ifcgeom/IfcGeom.h
            PATHS ${_IMPORT_PREFIX}/include
            NO_DEFAULT_PATH
            DOC "The directory where IfcGeom.h resides")

  find_library(IfcGeom_LIBRARY
               NAMES IfcGeom
               PATHS ${_IMPORT_PREFIX}/lib
               NO_DEFAULT_PATH
               DOC "The IfcGeom library")
endif()

mark_as_advanced(IfcGeom_INCLUDE_DIR IfcGeom_LLIBRARY)

find_package_handle_standard_args(IfcGeom
                                  DEFAULT_MSG
                                  IfcGeom_INCLUDE_DIR
                                  IfcGeom_LIBRARY)

if(IfcGeom_FOUND AND NOT TARGET IfcOpenShell::Geom)
  add_library(IfcOpenShell::Geom UNKNOWN IMPORTED)

  set_target_properties(IfcOpenShell::Geom
                        PROPERTIES IMPORTED_LINK_INTERFACE_LANGUAGES
                                   "CXX"
                                   IMPORTED_LOCATION
                                   "${IfcGeom_LIBRARY}"
                                   INTERFACE_INCLUDE_DIRECTORIES
                                   "${IfcGeom_INCLUDE_DIR}")
endif()
