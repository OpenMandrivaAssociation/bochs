Summary:	Bochs Project x86 PC Emulator
Name:		bochs
Version:	2.4.5
Release:	%mkrel 2
License:	LGPLv2+
Group:		Emulators
URL:		http://bochs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		bochs-2.4.5-3dnow-compile-fix.patch
Buildrequires:	libx11-devel
Buildrequires:	libxpm-devel
BuildRequires:	libalsa-devel
BuildRequires:	zlib-devel
BuildRequires:  readline-devel 
BuildRequires:	byacc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%prep
%setup -q
%patch0 -p1 -b .compile~

%build
%configure2_5x \
	--enable-x2apic \
	--enable-compressed-hd \
	--enable-sb16=linux \
	--enable-gameport \
	--enable-ne2000 \
	--enable-pnic \
	--enable-cdrom \
	--enable-vbe \
	--enable-split-hd \
	--enable-x86-64 \
	--enable-misaligned-sse \
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
	--enable-debugger \
	--enable-usb \
	--enable-usb-ohci \
	--enable-acpi \
	--enable-pci \
	--enable-pcidev \
	--enable-idle-hack \
	--enable-repeat-speedups \
	--enable-trace-cache \
	--enable-fast-function-calls \
	--enable-alignment-check \
	--enable-cpu-level=6 \
	--enable-monitor-mwait \
	--enable-long-phy-address \
	--enable-a20-pin \
	--enable-configurable-msrs \
	--enable-host-specific-asms \
	--enable-configurable-msrs \
	--enable-clgd54xx \
%ifarch x86_64
	--enable-vmx=2 \
%else
	--enable-vmx=1 \
%endif
	--enable-raw-serial

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
%doc README CHANGES
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
