Summary:	Lightweight video thumbnailer
Name:		ffmpegthumbnailer
Version:	1.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://ffmpegthumbnailer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	20c6b80dbbcf7a2f73d8879dc9c94c93
Patch0:		%{name}-link.patch
URL:		http://code.google.com/p/ffmpegthumbnailer/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel
BuildRequires:	libpng-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ffmpegthumbnailer can be used by file managers to create thumbnails
for your video files. It uses ffmpeg to decode frames from the video
files.

%prep
%setup -q
%patch0 -p1

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
