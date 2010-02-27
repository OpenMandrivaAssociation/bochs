Summary:	Bochs Project x86 PC Emulator
Name:		bochs
Version:	2.4.2
Release:	%mkrel 1
License:	LGPLv2+
Group:		Emulators
URL:		http://bochs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         %{name}-nonet-build.patch
Patch1:         %{name}-config.patch
BuildRequires:	X11-devel gtk+2-devel
BuildRequires:  readline-devel 
BuildRequires:	byacc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%prep
%setup -q
%patch0 -p0 -z .nonet

# remove any references to CVS repository
find . -type d -name CVS | xargs rm -rf
perl -pi -e "s#1\.1\.2#2\.0\.2#g" dlxlinux/bochsrc.txt
perl -pi -e "s#/usr/local/bochs/latest#%{_datadir}/bochs#g" dlxlinux/bochsrc.txt

%build
%configure2_5x \
	--enable-sb16=linux \
	--enable-ne2000 \
	--enable-cdrom \
	--enable-vbe \
	--enable-split-hd \
	--enable-x86-64 --enable-sse=4 \
	--enable-sse-extension \
	--enable-misaligned-sse \
	--enable-mmx \
	--enable-3dnow \
	--enable-fpu \
	--enable-all-optimizations \
	--with-x11 \
	--with-nogui \
	--without-wx \
	--without-sdl \
	--enable-readline \
	--disable-docbook \
	--enable-disasm \
	--enable-smp \
	--enable-apic \
	--enable-debugger \
	--enable-xsave \
	--enable-aes \
	--enable-popcnt \
	--enable-usb \
	--enable-acpi \
	--enable-pci \
	--enable-pcidev \
	--enable-idle-hack \
	--enable-repeat-speedups \
	--enable-trace-cache \
	--enable-fast-function-calls \
	--enable-alignment-check \
	--enable-sep \
	--enable-cpu-level=6

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# fix docs
install -m644 $RPM_BUILD_ROOT%{_datadir}/doc/bochs/bochsrc-sample.txt .
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -f %{buildroot}%{_mandir}/man*/*dlx*

install -m644 gui/keymaps/convertmap.pl -D $RPM_BUILD_ROOT%{_datadir}/bochs/keymaps/convertmap.pl

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
