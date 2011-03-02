#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Programs to generate and render cosmic recursive fractal flames
Name:		flam3
Version:	3.0.1
Release:	1
License:	GPL v3+
Group:		Applications/Multimedia
Source0:	http://flam3.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	916e1cda65b4ce2c84b3b4edc7d9605a
URL:		http://www.flam3.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flam3, or Fractal Flames, are algorithmically generated images and
animations. This is free software to render fractal flames as
described on http://flam3.com. Flam3-animate makes animations, and
flam3-render makes still images. Flam3-genome creates and manipulates
genomes (parameter sets).

%package devel
Summary:	C headers to generate and render cosmic recursive fractal flames
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Flam3, or Fractal Flames, are algorithmically generated images and
animations. This is free software to render fractal flames as
described on http://flam3.com. Flam3-animate makes animations, and
flam3-render makes still images. Flam3-genome creates and manipulates
genomes (parameter sets). This package contains a header file for C, a
library, and a pkgconfig file.

%package static
Summary:	Static flam3 library
Summary(pl.UTF-8):	Statyczna biblioteka flam3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of flam3.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną wersję biblioteki flam3.

%prep
%setup -q -n %{name}-%{version}/src

# drop redundant -O3 flag
%{__sed} -i 's,-O3,,' Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/flam3-animate
%attr(755,root,root) %{_bindir}/flam3-convert
%attr(755,root,root) %{_bindir}/flam3-genome
%attr(755,root,root) %{_bindir}/flam3-render
%attr(755,root,root) %{_libdir}/libflam3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libflam3.so.0
%{_datadir}/flam3
%{_mandir}/man1/flam3*.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/libflam3.so
%{_pkgconfigdir}/flam3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libflam3.a
%endif
