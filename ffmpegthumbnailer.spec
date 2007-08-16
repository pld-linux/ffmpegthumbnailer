Summary:	Lightweight video thumbnailer
Summary(pl.UTF-8):	Lekki program do wykonywania miniaturek dla filmów
Name:		ffmpegthumbnailer
Version:	1.1.3
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://ffmpegthumbnailer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	8abed939bdbd7261cb22f6383b761e43
URL:		http://code.google.com/p/ffmpegthumbnailer/
BuildRequires:	a52dec-libs-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel
BuildRequires:	libpng-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ffmpegthumbnailer can be used by file managers to create thumbnails
for your video files. It uses ffmpeg to decode frames from the video
files.

%description -l pl.UTF-8
ffmpegthumbnailer może być używany przez zarządców plików do tworzenia
miniaturek dla plików filmów. Wykorzystuje ffmpeg do dekodowania
klatek.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/ffmpegthumbnailer
