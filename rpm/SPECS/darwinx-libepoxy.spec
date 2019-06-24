Name:           darwinx-libepoxy
Version:        1.5.3
Release:        1%{?dist}
Summary:        Epoxy is a library for handling OpenGL function pointer management for you.

License:        LGPLv2+
Group:          Development/Libraries
URL:		https://github.com/anholt/libepoxy/releases
Source0:        https://github.com/anholt/libepoxy/releases/libepoxy-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  darwinx-filesystem-base >= 18
BuildRequires:  darwinx-gcc
BuildRequires:  darwinx-gettext

Requires:  	darwinx-filesystem >= 18

%description
Epoxy is a library for handling OpenGL function pointer management for you.

It hides the complexity of dlopen(), dlsym(), glXGetProcAddress(), 
eglGetProcAddress(), etc. from the app developer, with very little knowledge 
needed on their part. They get to read GL specs and write code using 
undecorated function names like glCompileShader().

Don't forget to check for your extensions or versions being present before 
you use them, just like before! We'll tell you what you forgot to check for 
instead of just segfaulting, though.

%package static
Summary:        A portable foreign function interface library
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description static
Static version of the libepoxy library.

%prep
%setup -q -n libepoxy-%{version}

%build
#NOCONFIGURE=1 sh autogen.sh
%{_darwinx_configure} --enable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT%{_darwinx_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_darwinx_libdir}/libepoxy.dylib
%{_darwinx_libdir}/libepoxy.*.dylib
%{_darwinx_libdir}/libepoxy.la
%{_darwinx_libdir}/pkgconfig/epoxy.pc
%{_darwinx_includedir}/epoxy/common.h
%{_darwinx_includedir}/epoxy/gl.h
%{_darwinx_includedir}/epoxy/gl_generated.h


%files static
%defattr(-,root,root)
%{_darwinx_libdir}/libepoxy.a

%changelog
* Thu Jun 9 2015 Mikkel Kruse Johnsen <mikkel@xmedicus.com> - 1.2-1
- Initial RPM release
