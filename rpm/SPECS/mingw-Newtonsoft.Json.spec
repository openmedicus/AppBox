%?mingw_package_header

%global __strip /bin/true

%global mingw_pkg_name Newtonsoft.Json
%global mingw_build_win32 1
%global mingw_build_win64 1

%define debug_package %{nil}

%define libdir /lib
%define apiversion 10.0.0.0

Name:           mingw-Newtonsoft.Json
Version:        10.0.3
Release:        2%{?dist}
Summary:        Json.NET is a popular high-performance JSON framework for .NET

Group:          Development/Languages
License:        MIT
URL:            http://json.codeplex.com/

Prefix:		/usr
BuildArch:	noarch

BuildRequires:  mono-devel
BuildRequires:  nuget

%description
Json.NET is a popular high-performance JSON framework for .NET

# Mingw32
%package -n mingw32-%{mingw_pkg_name}
Summary:       %{summary}
Requires:       mingw32-mono

Obsoletes:      mingw32-newtonsoft-json
Provides:       mingw32-newtonsoft-json

%description -n mingw32-%{mingw_pkg_name}
Json.NET is a popular high-performance JSON framework for .NET

# Mingw64
%package -n mingw64-%{mingw_pkg_name}
Summary:       %{summary}
Requires:       mingw64-mono

Obsoletes:      mingw64-newtonsoft-json
Provides:       mingw64-newtonsoft-json

%description -n mingw64-%{mingw_pkg_name}
Json.NET is a popular high-performance JSON framework for .NET

%prep
%setup -c %{name}-%{version} -T
nuget install %{mingw_pkg_name} -Version %{version}

cat > Newtonsoft.Json32.pc << \EOF
prefix=%{mingw32_prefix}
exec_prefix=${prefix}
libdir=%{mingw32_prefix}%{libdir}/mono

Name: Newtonsoft.Json
Description: %{name} - %{summary}
Requires:
Version: %{version}
Libs: -r:${libdir}/Newtonsoft.Json/Newtonsoft.Json.dll
Cflags:
EOF

cat > Newtonsoft.Json64.pc << \EOF
prefix=%{mingw64_prefix}
exec_prefix=${prefix}
libdir=%{mingw64_prefix}%{libdir}/mono

Name: Newtonsoft.Json
Description: %{name} - %{summary}
Requires:
Version: %{version}
Libs: -r:${libdir}/Newtonsoft.Json/Newtonsoft.Json.dll
Cflags:
EOF


%build

%install
%{__rm} -rf %{buildroot}

# Mingw32
install -d -m 755 $RPM_BUILD_ROOT%{mingw32_prefix}%{libdir}/mono/gac
gacutil -i Newtonsoft.Json.%{version}/lib/net45/Newtonsoft.Json.dll -package %{mingw_pkg_name} -root $RPM_BUILD_ROOT%{mingw32_prefix}%{libdir} -gacdir mono/gac

install -d -m 755 $RPM_BUILD_ROOT%{mingw32_datadir}/pkgconfig/
install -m 644 Newtonsoft.Json32.pc $RPM_BUILD_ROOT%{mingw32_datadir}/pkgconfig/Newtonsoft.Json.pc

# Mingw64
install -d -m 755 $RPM_BUILD_ROOT%{mingw64_prefix}%{libdir}/mono/gac
gacutil -i Newtonsoft.Json.%{version}/lib/net45/Newtonsoft.Json.dll -package %{mingw_pkg_name} -root $RPM_BUILD_ROOT%{mingw64_prefix}%{libdir} -gacdir mono/gac

install -d -m 755 $RPM_BUILD_ROOT%{mingw64_datadir}/pkgconfig/
install -m 644 Newtonsoft.Json64.pc $RPM_BUILD_ROOT%{mingw64_datadir}/pkgconfig/Newtonsoft.Json.pc


%clean
#%{__rm} -rf %{buildroot}

%files -n mingw32-%{mingw_pkg_name}
%defattr(-,root,root,-)
%{mingw32_prefix}%{libdir}/mono/gac
%{mingw32_prefix}%{libdir}/mono/Newtonsoft.Json/Newtonsoft.Json.dll
%{mingw32_datadir}/pkgconfig/Newtonsoft.Json.pc

%files -n mingw64-%{mingw_pkg_name}
%defattr(-,root,root,-)
%{mingw64_prefix}%{libdir}/mono/gac
%{mingw64_prefix}%{libdir}/mono/Newtonsoft.Json/Newtonsoft.Json.dll
%{mingw64_datadir}/pkgconfig/Newtonsoft.Json.pc


%changelog
* Thu Sep 7 2017 Mikkel Kruse Johnsen <mikkel@xmedicus.com> - 10.0.3-1
- Initial version
