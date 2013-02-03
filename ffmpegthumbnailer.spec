Summary:	Lightweight video thumbnailer
Summary(pl.UTF-8):	Lekki program do wykonywania miniaturek dla filmów
Name:		ffmpegthumbnailer
Version:	2.0.8
Release:	2
License:	GPL v2
Group:		Applications/Graphics
Source0:	http://ffmpegthumbnailer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	03e081f89778cd5e4fce30b29a4630e1
URL:		http://code.google.com/p/ffmpegthumbnailer/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
# libavcodec >= 52.26.0 libavformat libavutil libswscale
BuildRequires:	ffmpeg-devel >= 0.6
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
# dlopens libglib-2.0.so.0 libgobject-2.0.so.0 libgio-2.0.so.0
Requires:	glib2
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

# use runtime library paths for dlopen
%{__sed} -i -e '
	# glib2
	s,"libglib-2.0.so","libglib-2.0.so.0",
	s,"libgobject-2.0.so","libgobject-2.0.so.0",
	s,"libgio-2.0.so","libgio-2.0.so.0",
' main.cpp

%build
%configure \
	--enable-gio \
	--enable-thumbnailer

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
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
%{_libdir}/libffmpegthumbnailer.la
%{_includedir}/libffmpegthumbnailer
%{_pkgconfigdir}/libffmpegthumbnailer.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libffmpegthumbnailer.a
