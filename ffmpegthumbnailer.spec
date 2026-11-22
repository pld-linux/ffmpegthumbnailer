#
# Conditional build:
%bcond_without	static_libs	# static library
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

%prep
%setup -q

%build
mkdir build
cd build
%cmake .. \
	-DENABLE_GIO=ON \
	-DENABLE_TESTS=ON \
	%{?with_static_libs:-DENABLE_STATIC=ON} \
	-DENABLE_THUMBNAILER=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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
