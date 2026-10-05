cmake_minimum_required(VERSION 3.16)
project(haiku-kdecoration VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 6.6 REQUIRED COMPONENTS Core Gui)
find_package(KDecoration3 REQUIRED)
find_package(KF6CoreAddons REQUIRED)

add_library(haikudecoration MODULE
    src/haikudecoration.cpp
    src/haikudecoration.h
    src/haikupainter.cpp
    src/haikupainter.h
)
target_link_libraries(haikudecoration PRIVATE Qt6::Core Qt6::Gui KDecoration3::KDecoration KF6::CoreAddons)
target_link_options(haikudecoration PRIVATE "LINKER:--no-undefined")
set_target_properties(haikudecoration PROPERTIES OUTPUT_NAME "org.haiku.decoration" PREFIX "")

if(NOT DEFINED HAIKU_QT_PLUGIN_DIR)
    get_target_property(_qmake Qt6::qmake IMPORTED_LOCATION)
    execute_process(COMMAND ${_qmake} -query QT_INSTALL_PLUGINS
                    OUTPUT_VARIABLE HAIKU_QT_PLUGIN_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)
endif()
if(NOT KDECORATION_PLUGIN_DIR)
    set(KDECORATION_PLUGIN_DIR "org.kde.kdecoration3")
endif()
message(STATUS "Decoration plugin will be installed to ${HAIKU_QT_PLUGIN_DIR}/${KDECORATION_PLUGIN_DIR}")
install(TARGETS haikudecoration DESTINATION ${HAIKU_QT_PLUGIN_DIR}/${KDECORATION_PLUGIN_DIR})
