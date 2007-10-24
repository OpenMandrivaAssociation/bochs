#TODO: the latest dlxlinux release dates from 2001, drop it?

%define name	bochs
%define version	2.3.5
%define release %mkrel 1

Summary:	Bochs Project x86 PC Emulator
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Emulators
URL:		http://bochs.sourceforge.net/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/bochs/%{name}-%{version}.tar.gz
Source1:	dlxlinux4.tar.bz2
BuildRequires:	X11-devel 
BuildRequires:  readline-devel 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%package	dlxlinux
Summary: 	Small GNU/Linux distrib for Bochs project x86 PC emulator
Group:          Emulators
Requires:	%{name}

%description	dlxlinux
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%prep
%setup -q -a1 -n %{name}-%{version}
# remove any references to CVS repository
find . -type d -name CVS | xargs rm -rf
perl -pi -e "s#1\.1\.2#2\.0\.2#g" dlxlinux/bochsrc.txt
perl -pi -e "s#/usr/local/bochs/latest#%{_datadir}/bochs#g" dlxlinux/bochsrc.txt

%build

%configure \
	--enable-sb16=linux \
	--enable-ne2000 \
	--enable-cdrom \
	--enable-vbe \
	--enable-split-hd \
	--enable-x86-64 --enable-sse=2 \
	--enable-all-optimizations \
	--with-x11 \
	--with-nogui \
	--without-wx \
	--without-sdl \
	--enable-readline \
	--disable-docbook \
	--enable-disasm \
	--enable-smp \
	--enable-debugger \
	--enable-4meg-pages \
	--enable-global-pages \
	--enable-pae \
	--with-all-libs

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall install_dlx

# fix docs
install -m644 $RPM_BUILD_ROOT%{_datadir}/doc/bochs/bochsrc-sample.txt .
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

install -m644 gui/keymaps/convertmap.pl -D $RPM_BUILD_ROOT%{_datadir}/bochs/keymaps/convertmap.pl

%preun dlxlinux
# clean up the bochsout.txt that is always produced if you 
# run bochs-dlx.
rm -rf %{_datadir}/bochs/dlxlinux/bochsout.txt core

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%doc README CHANGES COPYING
%doc bochsrc-sample.txt
%doc docs-html
#
%{_bindir}/bochs
%{_bindir}/bximage
%{_bindir}/bxcommit
#
%dir %{_datadir}/bochs
%{_datadir}/bochs/BIOS-*
%{_datadir}/bochs/VGABIOS-*
%dir %{_datadir}/bochs/keymaps
%{_datadir}/bochs/keymaps/*.map
%{_datadir}/bochs/keymaps/convertmap.pl
#
%{_mandir}/man1/bochs.1*
%{_mandir}/man1/bximage.1*
%{_mandir}/man1/bxcommit.1*
%{_mandir}/man5/bochsrc.5*

%files dlxlinux
%defattr(-, root, root)

%dir %{_datadir}/bochs/dlxlinux
%{_datadir}/bochs/dlxlinux/readme.txt
%{_datadir}/bochs/dlxlinux/bochsrc.txt
%{_datadir}/bochs/dlxlinux/hd10meg.img.gz
%{_datadir}/bochs/dlxlinux/testform.txt
%{_mandir}/man1/bochs-dlx.1*
%{_bindir}/bochs-dlx
