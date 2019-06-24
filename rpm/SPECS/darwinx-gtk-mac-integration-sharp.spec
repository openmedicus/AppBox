Name:		darwinx-gtk-mac-integration-sharp
Version:	2.0.7
Release:	4%{?dist}
Summary:	.NET bindings for GtkOSXApplication
Group:		Development/Languages
License:	MIT
Source0:	gtk-mac-integration-sharp-%{version}.tar.xz
Source1:	xcare.pub
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	darwinx-gtk-mac-integration
BuildRequires:	darwinx-mono-core
BuildRequires:	darwinx-GtkSharp

Requires:  	darwinx-GtkSharp

Obsoletes:	darwinx-gtkosxapplication-sharp

%description
GtkOSXApplication-sharp

%prep
%setup -q -n gtk-mac-integration-sharp-%{version}

sed -i -e 's!/usr/darwinx/include!/usr/darwinx/usr/include!' sources/gtkosxapplication-sharp-sources.xml 

%build
sh autogen.sh
%{_darwinx_configure}

cp %{SOURCE1} sources/

sed -i '' "s!CSC = /usr/darwinx/usr/bin/mcs!CSC=/usr/darwinx/usr/bin/mcs -keyfile:xcare.pub!" sources/Makefile

cd sources
make api
%{_darwinx_make}

%install
%{__rm} -rf %{buildroot}

#{_darwinx_makeinstall}

mkdir -p $RPM_BUILD_ROOT%{_darwinx_libdir}
cp sources/gtkosxapplication-sharp.dll $RPM_BUILD_ROOT%{_darwinx_libdir}/

mkdir -p $RPM_BUILD_ROOT%{_darwinx_datadir}/pkgconfig/
cp sources/gtkosxapplication-sharp-2.0.pc $RPM_BUILD_ROOT%{_darwinx_datadir}/pkgconfig/
sed -i '' 's!mono/gtkosxapplication-sharp-2.0/!!g' $RPM_BUILD_ROOT%{_darwinx_datadir}/pkgconfig/gtkosxapplication-sharp-2.0.pc

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_darwinx_libdir}/gtkosxapplication-sharp.dll
%{_darwinx_datadir}/pkgconfig/gtkosxapplication-sharp-2.0.pc

%changelog
* Sat Apr 09 2011 Mikkel Kruse Johnsen <mikkel@linet.dk> - 0.9.7-1
- Initial package
