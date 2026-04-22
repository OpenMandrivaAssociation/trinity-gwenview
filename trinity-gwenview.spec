%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg gwenview
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Version:		1.4.2
Release:		%{?tde_version:%{tde_version}_}3
Summary:		Gwenview is an image viewer for TDE.
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/graphics/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:	  cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	trinity-%{_lib}kipi-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# EXIV2 support
BuildRequires:  pkgconfig(exiv2)

# MNG support
BuildRequires:  pkgconfig(libmng)

BuildRequires:  pkgconfig(xcursor)

%if "%{?tde_prefix}" == "/usr"
Conflicts: kdegraphics
%endif


%description
Gwenview is a fast and easy to use image viewer/browser for TDE.
All common image formats are supported, such as PNG(including transparency),
JPEG(including EXIF tags and lossless transformations), GIF, XCF (Gimp
image format), BMP, XPM and others. Standard features include slideshow,
fullscreen view, image thumbnails, drag'n'drop, image zoom, full network
transparency using the KIO framework, including basic file operations and
browsing in compressed archives, non-blocking GUI with adjustable views.
Gwenview also provides image and directory KParts components for use e.g. in
Konqueror. Additional features, such as image renaming, comparing,
converting, and batch processing, HTML gallery and others are provided by the
KIPI image framework.



%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
# Removes useless files (-devel ?)
%__rm -f %{?buildroot}%{tde_prefix}/%{_lib}/libgwenviewcore.so

# Remove unwanted files
%__rm -rf "%{?buildroot}%{tde_prefix}/share/pixmaps"


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_prefix}/bin/gwenview
%{tde_prefix}/%{_lib}/libgwenviewcore.la
%{tde_prefix}/%{_lib}/libgwenviewcore.so.1
%{tde_prefix}/%{_lib}/libgwenviewcore.so.1.0.0
%{tde_prefix}/%{_lib}/libtdeinit_gwenview.la
%{tde_prefix}/%{_lib}/libtdeinit_gwenview.so
%{tde_prefix}/%{_lib}/trinity/gwenview.la
%{tde_prefix}/%{_lib}/trinity/gwenview.so
%{tde_prefix}/%{_lib}/trinity/libgvdirpart.la
%{tde_prefix}/%{_lib}/trinity/libgvdirpart.so
%{tde_prefix}/%{_lib}/trinity/libgvimagepart.la
%{tde_prefix}/%{_lib}/trinity/libgvimagepart.so
%{tde_prefix}/share/applications/tde/gwenview.desktop
%{tde_prefix}/share/apps/gwenview/
%dir %{tde_prefix}/share/apps/gvdirpart
%{tde_prefix}/share/apps/gvdirpart/gvdirpart.rc
%dir %{tde_prefix}/share/apps/gvimagepart
%{tde_prefix}/share/apps/gvimagepart/gvimagepart.rc
%{tde_prefix}/share/apps/gvimagepart/gvimagepartpopup.rc
%{tde_prefix}/share/apps/tdeconf_update/gwenview_1.4_osdformat.sh
%{tde_prefix}/share/apps/tdeconf_update/gwenview_1.4_osdformat.upd
%{tde_prefix}/share/apps/tdeconf_update/gwenview_thumbnail_size.sh
%{tde_prefix}/share/apps/tdeconf_update/gwenview_thumbnail_size.upd
%{tde_prefix}/share/apps/konqueror/servicemenus/konqgwenview.desktop
%{tde_prefix}/share/config.kcfg/fileoperationconfig.kcfg
%{tde_prefix}/share/config.kcfg/fileviewconfig.kcfg
%{tde_prefix}/share/config.kcfg/fullscreenconfig.kcfg
%{tde_prefix}/share/config.kcfg/gvdirpartconfig.kcfg
%{tde_prefix}/share/config.kcfg/imageviewconfig.kcfg
%{tde_prefix}/share/config.kcfg/miscconfig.kcfg
%{tde_prefix}/share/config.kcfg/slideshowconfig.kcfg
%{tde_prefix}/share/icons/crystalsvg/*/apps/gvdirpart.png
%{tde_prefix}/share/icons/crystalsvg/scalable/apps/gvdirpart.svg
%{tde_prefix}/share/icons/hicolor/*/apps/gwenview.png
%{tde_prefix}/share/icons/hicolor/*/apps/gvdirpart.png
%{tde_prefix}/share/icons/hicolor/scalable/apps/gvdirpart.svg
%{tde_prefix}/share/icons/hicolor/scalable/apps/gwenview.svgz
%{tde_prefix}/share/man/man1/gwenview.1*
%{tde_prefix}/share/services/gvdirpart.desktop
%{tde_prefix}/share/services/gvimagepart.desktop
%lang(en) %{tde_prefix}/share/doc/tde/HTML/en/gwenview/

