# NOTE: for newer versions (>=1) of libx86emu library see libx86emu.spec
#
# Conditional build:
%bcond_without	klibc	# use klibc for initrd/initramfs purposes
#
Summary:	Intel x86 CPU real mode emulator
Summary(pl.UTF-8):	Emulator trybu rzeczywistego procesorów Intel x86
Name:		x86emu
Version:	0.8
Release:	5
License:	MIT
Group:		Libraries
Source0:	http://www.scitechsoft.com/ftp/devel/obsolete/x86emu/%{name}-%{version}.tar.gz
# Source0-md5:	88c58c4687ef9c1aa082d8ea55ab956a
Patch0:		%{name}-build.patch
Patch1:		%{name}-update.patch
Patch2:		%{name}-update-v86d.patch
Patch3:		%{name}-klibc-makefile.patch
URL:		http://www.scitechsoft.com/products/dev/x86_emulator.html
%{?with_klibc:BuildRequires:	klibc-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with klibc}
%define		_klibdir	%{_prefix}/%{_lib}/klibc
%define		_kincludedir	%{_prefix}/include/klibc
%endif

%description
The SciTech x86emu is an emulator for executing Intel x86 real mode
code on any CPU platform, including the Intel x86 CPU family. The
emulator started out as the free equivalent to the Digital Equipment
x86 emulator used in the Linux MILO loader. The project was originally
started and developed by David Mosberger-Tang, and after David lost
interest in the project SciTech took over as the official maintainers.
Since then the emulator has been updated to include support for 32-bit
real mode instructions, optimised for better performance, and should
be able to completely replace the Digitial Equipment proprietary
emulator in MILO.

%description -l pl.UTF-8
SciTech x86emu to emulator do wykonywania kodu trybu rzeczywistego
procesorów Intel x86 na dowolnej architekturze procesora. Emulator
został zapoczątkowany jako wolnodostępny odpowiednik emulatora x86
firmy Digital Equipment używanego w bootloaderze Linuksa MILO. Projekt
początkowo tworzył David Mosberger-Tang, a po nim opieka została
przejęta przez SciTech. Od tamtego czasu emulator został uaktualniony
o obsługę 32-bitowych instrukcji trybu rzeczywistego, zoptymalizowany
pod kątem lepszej wydajności i powinien całkowicie zastąpić
własnościowy emulator Digital Equipment w MILO.

%package devel
Summary:	Header files and static x86emu library
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteka statyczna x86emu
Group:		Development/Libraries

%description devel
Header files and static x86emu library.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteka statyczna x86emu.

%package klibc-devel
Summary:	Header files and static x86emu library for klibc
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteka statyczna x86emu dla klibc
Group:		Development/Libraries

%description klibc-devel
Header files and static x86emu library for klibc.

%description klibc-devel -l pl.UTF-8
Pliki nagłówkowe i biblioteka statyczna x86emu dla klibc.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%if %{with klibc}
%{__make} -C scitech/src/x86emu -f makefile.klibc \
	OPT="%{rpmcflags} -Os"

mkdir -p klibc
cp scitech/src/x86emu/libx86emu*.a klibc/
%{__make} -C scitech/src/x86emu -f makefile.klibc clean
%endif

%{__make} -C scitech/src/x86emu -f makefile.linux \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

# only partially multi-arch, some pieces look like x86-only
%ifarch %{ix86} %{x8664}
# actually not packaged, but build to check if library is usable
%{__make} -C scitech/src/v86bios -f makefile.linux vbios.x86emu cbios.x86emu \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install scitech/src/x86emu/libx86emu*.a $RPM_BUILD_ROOT%{_libdir}
install scitech/include/x86emu.h $RPM_BUILD_ROOT%{_includedir}/x86emu.h
cp -a scitech/include/x86emu $RPM_BUILD_ROOT%{_includedir}/x86emu

%if %{with klibc}
install -d $RPM_BUILD_ROOT{%{_klibdir},%{_kincludedir}}
install klibc/libx86emu*.a $RPM_BUILD_ROOT%{_klibdir}
install scitech/include/x86emu.h $RPM_BUILD_ROOT%{_kincludedir}/x86emu.h
cp -a scitech/include/x86emu $RPM_BUILD_ROOT%{_kincludedir}/x86emu
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# *bios.x86emu not really useful - not packaging

%files devel
%defattr(644,root,root,755)
%doc scitech/src/x86emu/LICENSE
%{_libdir}/libx86emu.a
%{_libdir}/libx86emud.a
%{_includedir}/x86emu.h
%{_includedir}/x86emu

%if %{with klibc}
%files klibc-devel
%defattr(644,root,root,755)
%doc scitech/src/x86emu/LICENSE
%{_klibdir}/libx86emu.a
%{_kincludedir}/x86emu.h
%{_kincludedir}/x86emu
%endif
