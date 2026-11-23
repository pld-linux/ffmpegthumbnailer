#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	kde5		# KDE 5 service (predecesor of ka[56]-ffmpegthumbs)
#
Summary:	Lightweight video thumbnailer
Summary(pl.UTF-8):	Lekki program do wykonywania miniaturek dla filmów
Name:		ffmpegthumbnailer
Version:	2.4.2
Release:	1
License:	GPL v2
Group:		Applications/Graphics
#Source0Download: https://github.com/dirkvdb/ffmpegthumbnailer/releases
Source0:	https://github.com/dirkvdb/ffmpegthumbnailer/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	726375b0f72219e3c05dc10d3a6c548a
URL:		https://github.com/dirkvdb/ffmpegthumbnailer
BuildRequires:	cmake >= 3.12
# libavcodec >= 52.26.0 libavformat libavutil libswscale
BuildRequires:	ffmpeg-devel >= 0.6
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with kde5}
BuildRequires:	Qt5Core-devel >= 5.2.0
BuildRequires:	Qt5Gui-devel >= 5.2.0
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	kf5-kconfig-devel >= 5
BuildRequires:	kf5-ki18n-devel >= 5
BuildRequires:	kf5-kio-devel >= 5
BuildRequires:	qt5-build >= 5.2.0
%endif
# dlopens libglib-2.0.so.0 libgobject-2.0.so.0 libgio-2.0.so.0
Requires:	glib2%{?_isa} >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ffmpegthumbnailer can be used by file managers to create thumbnails
for your video files. It uses ffmpeg to decode frames from the video
files.

%description -l pl.UTF-8
ffmpegthumbnailer może być używany przez zarządców plików do tworzenia
miniaturek dla plików filmów. Wykorzystuje ffmpeg do dekodowania
klatek.

%package devel
Summary:	Header files for libffmpegthumbnailer library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libffmpegthumbnailer
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	ffmpeg-devel%{?_isa}
Requires:	libjpeg-devel%{?_isa}
Requires:	libpng-devel%{?_isa}
Requires:	libstdc++-devel%{?_isa} >= 6:7

%description devel
Header files for libffmpegthumbnailer library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libffmpegthumbnailer.

%package static
Summary:	Static libffmpegthumbnailer library
Summary(pl.UTF-8):	Statyczna biblioteka libffmpegthumbnailer
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libffmpegthumbnailer library.

%description static -l pl.UTF-8
Statyczna biblioteka libffmpegthumbnailer.

%package -n kffmpegthumbnailer
Summary:	FFmpeg based video thumbnail generator for KDE
Summary(pl.UTF-8):	Oparty na FFmpeg generator miniaturek filmów dla KDE
Group:		X11/Applications
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n kffmpegthumbnailer
FFmpeg based video thumbnail generator for KDE.

%description -n kffmpegthumbnailer -l pl.UTF-8
Oparty na FFmpeg generator miniaturek filmów dla KDE.

%prep
%setup -q

%build
topdir=$(pwd)
install -d build
cd build
%cmake .. \
	-DENABLE_GIO=ON \
	-DENABLE_TESTS=ON \
	%{?with_static_libs:-DENABLE_STATIC=ON} \
	-DENABLE_THUMBNAILER=ON

%{__make}

%if %{with kde5}
cd ../kffmpegthumbnailer
install -d build
cd build
%cmake .. \
	-DCMAKE_CXX_STANDARD=17 \
	-DFFMPEG_THUMBNAILER_INCLUDES=${topdir} \
	-DFFMPEG_THUMBNAILER_LIBRARIES=${topdir}/build/libffmpegthumbnailer.so \
	-DPLUGIN_INSTALL_DIR=%{_libdir}/qt5/plugins/kf5

%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with kde5}
%{__make} -C kffmpegthumbnailer/build install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md TODO
%attr(755,root,root) %{_bindir}/ffmpegthumbnailer
%{_libdir}/libffmpegthumbnailer.so.*.*.*
%ghost %{_libdir}/libffmpegthumbnailer.so.5
%{_datadir}/thumbnailers/ffmpegthumbnailer.thumbnailer
%{_mandir}/man1/ffmpegthumbnailer.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libffmpegthumbnailer.so
%{_includedir}/libffmpegthumbnailer
%{_pkgconfigdir}/libffmpegthumbnailer.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libffmpegthumbnailer.a
%endif

%if %{with kde5}
%files -n kffmpegthumbnailer
%defattr(644,root,root,755)
%{_libdir}/qt5/plugins/kf5/kffmpegthumbnailer.so
%{_datadir}/config.kcfg/kffmpegthumbnailersettings5.kcfg
%{_datadir}/kservices5/kffmpegthumbnailer.desktop
%endif
