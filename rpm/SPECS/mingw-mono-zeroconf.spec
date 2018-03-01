%{?mingw_package_header}

%global mingw_pkg_name mono-zeroconf
%global mingw_build_win32 1
%global mingw_build_win64 1

%define debug_package %{nil}

Name:           mingw-mono-zeroconf
Version:        0.9.0
Release:        2%{?dist}
Summary:        Mono.Zeroconf networking library
Group:          Development/Languages
License:        MIT
URL:            http://banshee-project.org/files/mono-zeroconf
Source0:        mono-zeroconf-%{version}.tar.bz2
Patch0:         mono-zeroconf-0.9.0-profile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	mingw32-filesystem
BuildRequires:  mono-devel >= 2.11 monodoc-devel

%description
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET.

# Mingw32
%package -n mingw32-%{mingw_pkg_name}
Summary:        %{summary}
Requires:       mingw32-glib2
Requires:       mingw32-mono >= 2.11

%description -n mingw32-%{mingw_pkg_name}
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET.

# Mingw64
%package -n mingw64-%{mingw_pkg_name}
Summary:        %{summary}
Requires:       mingw64-glib2
Requires:       mingw64-mono >= 3.8

%description -n mingw64-%{mingw_pkg_name}
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET.


%prep
%setup -q -n mono-zeroconf-%{version}
%patch0 -p1

%build
%mingw_configure "--disable-mdnsresponder" "--disable-docs"

find . -name Makefile | while read f ;
         do
           sed -i -e 's!MCS = /usr/i686-w64-mingw32/sys-root/mingw/bin/gmcs!MCS = /usr/bin/mcs!' "$f"
           sed -i -e 's!MCS = /usr/x86_64-w64-mingw32/sys-root/mingw/bin/gmcs!MCS = /usr/bin/mcs!' "$f"
         done

#parallel build doesn't work
%mingw_make

%install
%{__rm} -rf %{buildroot}
%mingw_make_install program_transform_name="" DESTDIR=$RPM_BUILD_ROOT GACDESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/mzclient
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/mzclient

%clean
%{__rm} -rf %{buildroot}

%files -n mingw32-%{mingw_pkg_name} 
%defattr(-,root,root,-)
%{mingw32_libdir}/mono-zeroconf/*
%{mingw32_libdir}/mono/gac/Mono.Zeroconf
%{mingw32_libdir}/mono/mono-zeroconf
%{mingw32_libdir}/mono/gac/policy.*
%{mingw32_libdir}/pkgconfig/*

%files -n mingw64-%{mingw_pkg_name}
%defattr(-,root,root,-)
%{mingw64_libdir}/mono-zeroconf/*
%{mingw64_libdir}/mono/gac/Mono.Zeroconf
%{mingw64_libdir}/mono/mono-zeroconf
%{mingw64_libdir}/mono/gac/policy.*
%{mingw64_libdir}/pkgconfig/*


%changelog
* Thu Oct 29 2009 Dennis Gilmore <dennis@ausil.us> - 0.9.0-3
- ExcludeArch sparc64

* Thu Oct 22 2009 Michel Salim <salimma@fedoraproject.org> - 0.9.0-2
- Make AvahiDbus the only provider for now

* Thu Oct 22 2009 Paul Lange <palango@gmx.de> - 0.9-1
- update to version 0.9
- move docs into devel package

* Thu Aug 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.6-10
- Rebuild for ppc64 packages due to obsolete of packageset last time.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.7.6-9
- Build arch ppc64.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.7.6-7
- add ppc

* Thu Dec 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-6
- Another fix for x86_64

* Thu Dec 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-5
- Remove patch file (use sed)
- Additional BRs and Rs

* Thu Dec 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-4
- remove ppc build for now

* Thu Dec 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-3
- rebuild (0.8.0 is buggy)

* Thu Aug 14 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-2
- bump to new version
- libdir clean now

* Tue Apr 07 2008 David Nielsen <gnomeuser@gmail.com> - 0.7.5-4
- Our CVS has odd bugs - pointless bump to make upgrade path work

* Mon Mar 31 2008 David Nielsen <gnomeuser@gmail.com> - 0.7.5-3
- Remove debuginfo

* Fri Feb 01 2008 David Nielsen <david@lovesunix.net> - 0.7.5-2
- Exclude ppc64
- Spec fixes

* Fri Feb 01 2008 David Nielsen <david@lovesunix.net> - 0.7.5-1
- bump to 0.7.5
- patch for libdir madness

* Fri Jan 04 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.3-2
- spec fixes

* Thu Dec 29 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.3-1
- Initial import for FE
