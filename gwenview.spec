#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg gwenview
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.4.2
Release:		%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:		Gwenview is an image viewer for TDE.
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/graphics/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	trinity-libkipi-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

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


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

# Warning: GCC visibility causes FTBFS [Bug #1285]
%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DCONFIG_INSTALL_DIR="%{tde_confdir}" \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

# Removes useless files (-devel ?)
%__rm -f %{?buildroot}%{tde_libdir}/libgwenviewcore.so

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file gwenview RasterGraphics Viewer
%endif

# Remove unwanted files
%__rm -rf "%{?buildroot}%{tde_datadir}/pixmaps"


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/gwenview
%{tde_libdir}/libgwenviewcore.la
%{tde_libdir}/libgwenviewcore.so.1
%{tde_libdir}/libgwenviewcore.so.1.0.0
%{tde_libdir}/libtdeinit_gwenview.la
%{tde_libdir}/libtdeinit_gwenview.so
%{tde_tdelibdir}/gwenview.la
%{tde_tdelibdir}/gwenview.so
%{tde_tdelibdir}/libgvdirpart.la
%{tde_tdelibdir}/libgvdirpart.so
%{tde_tdelibdir}/libgvimagepart.la
%{tde_tdelibdir}/libgvimagepart.so
%{tde_tdeappdir}/gwenview.desktop
%{tde_datadir}/apps/gwenview/
%dir %{tde_datadir}/apps/gvdirpart
%{tde_datadir}/apps/gvdirpart/gvdirpart.rc
%dir %{tde_datadir}/apps/gvimagepart
%{tde_datadir}/apps/gvimagepart/gvimagepart.rc
%{tde_datadir}/apps/gvimagepart/gvimagepartpopup.rc
%{tde_datadir}/apps/tdeconf_update/gwenview_1.4_osdformat.sh
%{tde_datadir}/apps/tdeconf_update/gwenview_1.4_osdformat.upd
%{tde_datadir}/apps/tdeconf_update/gwenview_thumbnail_size.sh
%{tde_datadir}/apps/tdeconf_update/gwenview_thumbnail_size.upd
%{tde_datadir}/apps/konqueror/servicemenus/konqgwenview.desktop
%{tde_datadir}/config.kcfg/fileoperationconfig.kcfg
%{tde_datadir}/config.kcfg/fileviewconfig.kcfg
%{tde_datadir}/config.kcfg/fullscreenconfig.kcfg
%{tde_datadir}/config.kcfg/gvdirpartconfig.kcfg
%{tde_datadir}/config.kcfg/imageviewconfig.kcfg
%{tde_datadir}/config.kcfg/miscconfig.kcfg
%{tde_datadir}/config.kcfg/slideshowconfig.kcfg
%{tde_datadir}/icons/crystalsvg/*/apps/gvdirpart.png
%{tde_datadir}/icons/crystalsvg/scalable/apps/gvdirpart.svg
%{tde_datadir}/icons/hicolor/*/apps/gwenview.png
%{tde_datadir}/icons/hicolor/*/apps/gvdirpart.png
%{tde_datadir}/icons/hicolor/scalable/apps/gvdirpart.svg
%{tde_datadir}/icons/hicolor/scalable/apps/gwenview.svgz
%{tde_datadir}/man/man1/gwenview.1*
%{tde_datadir}/services/gvdirpart.desktop
%{tde_datadir}/services/gvimagepart.desktop
%lang(en) %{tde_tdedocdir}/HTML/en/gwenview/

