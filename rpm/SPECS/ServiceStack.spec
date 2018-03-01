#sudo mozroots --import --machine --sync
#sudo certmgr -ssl -m https://go.microsoft.com
#sudo certmgr -ssl -m https://nugetgallery.blob.core.windows.net
#sudo certmgr -ssl -m https://nuget.org

%global debug_package %{nil}

%define libdir /lib

Name:           ServiceStack
Version:        5.0.2
Release:        1%{?dist}
Summary:        ServiceStack webservice framework: Faster, Cleaner, Modern WCF alternative.

Group:          Development/Languages
License:        Copyright 2017 ServiceStack
URL:            https://www.nuget.org/packages/ServiceStack
Prefix:		/usr

BuildArch:	noarch

BuildRequires:  mono-devel
BuildRequires:  nuget

Requires:	mono-core >= 4.0.0

%description
A simple and fast alternative to WCF, MVC and Web API in one cohesive framework 
for all your services and web apps that's intuitive and Easy to use!

%prep
%setup -c %{name}-%{version} -T
nuget install %{name} -Version %{version}

cat > ServiceStack.pc << \EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_prefix}%{libdir}/mono

Name: ServiceStack
Description: ServiceStack webservice framework: Faster, Cleaner, Modern WCF alternative.
Requires:
Version: %{version}
Libs: -r:${libdir}/ServiceStack/ServiceStack.dll -r:${libdir}/ServiceStack.Common/ServiceStack.Common.dll -r:${libdir}/ServiceStack.Client/ServiceStack.Client.dll -r:${libdir}/ServiceStack.Text/ServiceStack.Text.dll -r:${libdir}/ServiceStack.Interfaces/ServiceStack.Interfaces.dll
Cflags:
EOF

cat > ServiceStack.Interfaces.pc << \EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_prefix}%{libdir}/mono

Name: ServiceStack.Interfaces
Description: Lightweight and implementation-free interfaces for DTO's, providers and adapters.
Requires:
Version: %{version}
Libs: -r:${libdir}/ServiceStack.Interfaces/ServiceStack.Interfaces.dll
Cflags:
EOF


%build

%install
%{__rm} -rf %{buildroot}

install -d -m 755 $RPM_BUILD_ROOT%{_prefix}%{libdir}/mono/gac
gacutil -i ServiceStack.%{version}/lib/net45/ServiceStack.dll -package %{name} -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac
gacutil -i ServiceStack.Common.%{version}/lib/net45/ServiceStack.Common.dll -package %{name}.Common -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac
gacutil -i ServiceStack.Client.%{version}/lib/net45/ServiceStack.Client.dll -package %{name}.Client -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac
gacutil -i ServiceStack.Text.%{version}/lib/net45/ServiceStack.Text.dll -package %{name}.Text -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac
gacutil -i ServiceStack.Interfaces.%{version}/lib/net45/ServiceStack.Interfaces.dll -package %{name}.Interfaces -root $RPM_BUILD_ROOT%{_prefix}%{libdir} -gacdir mono/gac

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pkgconfig/
install -m 644 ServiceStack.pc $RPM_BUILD_ROOT%{_datadir}/pkgconfig/
install -m 644 ServiceStack.Interfaces.pc $RPM_BUILD_ROOT%{_datadir}/pkgconfig/

%clean
#%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}%{libdir}/mono/gac
%{_prefix}%{libdir}/mono/ServiceStack/ServiceStack.dll
%{_prefix}%{libdir}/mono/ServiceStack.Common/ServiceStack.Common.dll
%{_prefix}%{libdir}/mono/ServiceStack.Client/ServiceStack.Client.dll
%{_prefix}%{libdir}/mono/ServiceStack.Text/ServiceStack.Text.dll
%{_prefix}%{libdir}/mono/ServiceStack.Interfaces/ServiceStack.Interfaces.dll
%{_datadir}/pkgconfig/ServiceStack.pc
%{_datadir}/pkgconfig/ServiceStack.Interfaces.pc

%changelog
* Thu Nov 23 2017 Mikkel Kruse Johnsen <mikkel@xmedicus.com> - 4.5.14-1
- Initial version
