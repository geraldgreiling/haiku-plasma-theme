cmake_minimum_required(VERSION 3.16)
project(haiku-qt-style VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 6.4 REQUIRED COMPONENTS Core Gui Widgets)

option(BUILD_GALLERY "Build the widget gallery test program" OFF)

add_library(haikustyle MODULE
    src/haikustyle.cpp
    src/haikustyle.h
    src/haikustyleplugin.cpp
)
target_link_libraries(haikustyle PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
# fail at build time instead of silently producing a plugin Qt cannot load
target_link_options(haikustyle PRIVATE "LINKER:--no-undefined")

# Install into Qt's plugin directory (…/qt6/plugins/styles)
if(NOT DEFINED HAIKU_QT_PLUGIN_DIR)
    get_target_property(_qmake Qt6::qmake IMPORTED_LOCATION)
    execute_process(COMMAND ${_qmake} -query QT_INSTALL_PLUGINS
                    OUTPUT_VARIABLE HAIKU_QT_PLUGIN_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)
endif()
message(STATUS "Style plugin will be installed to ${HAIKU_QT_PLUGIN_DIR}/styles")
install(TARGETS haikustyle LIBRARY DESTINATION ${HAIKU_QT_PLUGIN_DIR}/styles)

if(BUILD_GALLERY)
    add_executable(haiku-gallery test/gallery.cpp src/haikustyle.cpp src/haikustyle.h)
    target_include_directories(haiku-gallery PRIVATE src)
    target_link_libraries(haiku-gallery PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
endif()
