%global debug_package %{nil}

%define libdir /lib
%define apiversion 4.1.0.0

Name:           Seal.net
Version:        4.1.0
Release:        1%{?dist}
Summary:        Seal.NET er et API som har til formål at lette udviklingen af software som overholder DGWS.

Group:          Development/Languages
License:        MIT
URL:            https://www.nuget.org/packages/Seal.net/
Prefix:		/usr

BuildArch:	noarch

BuildRequires:  mono-devel
BuildRequires:  nuget

Obsoletes:	SealApi
Provides:	SealApi

%description
Seal.NET er et API som har til formål at lette udviklingen af software som overholder DGWS.
Seal.NET indpakker detaljerne vedrørende DGWS, og hjælper med at bygge, signere og serialisere id-kort

%prep
%setup -c %{name}-%{version} -T
nuget install %{name} -Version %{version}

cat > %{name}.pc << \EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_prefix}%{libdir}/mono

Name: %{name}
Description: %{name} - %{summary}
Requires:
Version: %{version}
Libs: -r:${libdir}/%{name}/Seal.dll -r:${libdir}/%{name}/DgwsTypes.dll
Cflags:
EOF

%build

%install
%{__rm} -rf %{buildroot}

gacutil -i %{name}.%{version}/lib/net462/DgwsTypes.dll -package %{name} -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac
gacutil -i %{name}.%{version}/lib/net462/Seal.dll -package %{name} -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pkgconfig/
install -m 644 %{name}.pc $RPM_BUILD_ROOT%{_datadir}/pkgconfig/

%clean
#%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}%{libdir}/mono/gac
%{_prefix}%{libdir}/mono/%{name}/Seal.dll
%{_prefix}%{libdir}/mono/%{name}/DgwsTypes.dll
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Mon Dec 04 2017 Mikkel Kruse Johnsen <mikkel@xmedicus.com> - 4.0.5-1
- Initial version
