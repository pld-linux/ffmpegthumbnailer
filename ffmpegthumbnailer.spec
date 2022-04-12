#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Lightweight video thumbnailer
Summary(pl.UTF-8):	Lekki program do wykonywania miniaturek dla filmów
Name:		ffmpegthumbnailer
Version:	2.2.2
Release:	1
License:	GPL v2
Group:		Applications/Graphics
#Source0Download: https://github.com/dirkvdb/ffmpegthumbnailer/releases
Source0:	https://github.com/dirkvdb/ffmpegthumbnailer/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	ef466e64df666ba006c0b071eb48018e
Patch0:		%{name}-pc.patch
URL:		https://github.com/dirkvdb/ffmpegthumbnailer
BuildRequires:	cmake >= 3.5
# libavcodec >= 52.26.0 libavformat libavutil libswscale
BuildRequires:	ffmpeg-devel >= 0.6
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
# dlopens libglib-2.0.so.0 libgobject-2.0.so.0 libgio-2.0.so.0
Requires:	glib2 >= 2.0
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
Requires:	%{name} = %{version}-%{release}
Requires:	ffmpeg-devel
Requires:	libjpeg-devel
Requires:	libpng-devel

%description devel
Header files for libffmpegthumbnailer library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libffmpegthumbnailer.

%package static
Summary:	Static libffmpegthumbnailer library
Summary(pl.UTF-8):	Statyczna biblioteka libffmpegthumbnailer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libffmpegthumbnailer library.

%description static -l pl.UTF-8
Statyczna biblioteka libffmpegthumbnailer.

%prep
%setup -q
%patch0 -p1

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
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/ffmpegthumbnailer
%attr(755,root,root) %{_libdir}/libffmpegthumbnailer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libffmpegthumbnailer.so.4
%{_datadir}/thumbnailers/ffmpegthumbnailer.thumbnailer
%{_mandir}/man1/ffmpegthumbnailer.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffmpegthumbnailer.so
%{_includedir}/libffmpegthumbnailer
%{_pkgconfigdir}/libffmpegthumbnailer.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libffmpegthumbnailer.a
%endif
