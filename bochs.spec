%define _hardened_build 1
Name:		bochs
Version:	2.6
Release:	2
Summary:	Portable x86 PC emulator
Group:		Emulators
License:	LGPLv2+
URL:		http://bochs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source100:  bochs.rpmlintrc

Patch0:		%{name}-0001_bx-qemu.patch
Patch1:		%{name}-0006_qemu-bios-use-preprocessor-for-pci-link-routing.patch
Patch2:		%{name}-0007_bios-add-26-pci-slots,-bringing-the-total-to-32.patch
Patch3:		%{name}-0008_qemu-bios-provide-gpe-_l0x-methods.patch
Patch4:		%{name}-0009_qemu-bios-pci-hotplug-support.patch
Patch7:		%{name}-nonet-build.patch

BuildRequires:	pkgconfig(xt) 
BuildRequires:	libxpm-devel 
BuildRequires:	pkgconfig(sdl) 
BuildRequires:	readline-devel 
BuildRequires:	byacc
BuildRequires:	docbook-utils
BuildRequires:	docbook-style-xsl
BuildRequires:	sgml-common
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	pkgconfig(gtk+-2.0)
%ifarch %{ix86}	x86_64
BuildRequires:	svgalib-devel
BuildRequires:	dev86 
BuildRequires:	iasl
%endif
Requires:	%{name}-bios = %{version}-%{release}
Requires:	vgabios

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%files
%doc _installed-docs/* README-*
%{_bindir}/bochs
%{_bindir}/bxcommit
%{_bindir}/bximage
%{_libdir}/bochs/
%{_mandir}/man1/bochs.1*
%{_mandir}/man1/bxcommit.1*
%{_mandir}/man1/bximage.1*
%{_mandir}/man5/bochsrc.5*
%dir %{_datadir}/bochs/
%{_datadir}/bochs/keymaps/

#------------------------------------------------
%package	debugger
Summary:	Bochs with builtin debugger
Group:		Emulators
Requires	:%{name} = %{version}-%{release}

%description	debugger
Special version of bochs compiled with the builtin debugger.

%files debugger
%{_bindir}/bochs-debugger

#------------------------------------------------

%package	gdb
Summary:	Bochs with support for debugging with gdb
Group:		Emulators
Requires:	%{name} = %{version}-%{release}

%description	gdb
Special version of bochs compiled with a gdb stub so that the software running
inside the emulator can be debugged with gdb.

%files gdb
%{_bindir}/bochs-gdb

#------------------------------------------------
%ifarch %{ix86} x86_64
# building firmwares are quite tricky, because they often have to be built on
# their native architecture (or in a cross-capable compiler, that we lack in
# koji), and deployed everywhere. Recent koji builders support a feature
# that allow us to build packages in a single architecture, and create noarch
# subpackages that will be deployed everywhere. Because the package can only
# be built in certain architectures, the main package has to use
# BuildArch: <nativearch>, or something like that.
# Note that using ExclusiveArch is _wrong_, because it will prevent the noarch
# packages from getting into the excluded repositories.
%package	bios
Summary:	Bochs bios
Group:		Emulators
BuildArch:	noarch
Provides:	bochs-bios-data = 2.3.8.1
Obsoletes:	bochs-bios-data < 2.3.8.1


%description	bios
Bochs BIOS is a free implementation of a x86 BIOS
provided by the Bochs project.
It can also be used in other emulators, such as QEMU
%endif


%ifarch %{ix86} x86_64
%files bios
%{_datadir}/bochs/BIOS*
%{_datadir}/bochs/VGABIOS*
%endif
#------------------------------------------------

%package	devel
Summary:	Bochs header and source files
Group:		Emulators
Requires:	%{name} = %{version}-%{release}

%description	devel
Header and source files from bochs source.



%files devel
%{_prefix}/include/bochs/

#------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch7 -p0 -z .nonet

# Fix up some man page paths.
sed -i \
  -e 's|/usr/local/share/doc/bochs/|%{_docdir}/%{name}-%{version}/|' \
  -e 's|/usr/local/share/|%{_datadir}/|' \
  doc/man/*.*
# remove executable bits from sources to make rpmlint happy with the debuginfo
chmod -x `find -name '*.cc' -o -name '*.h' -o -name '*.inc'`
# Fix CHANGES encoding
iconv -f ISO_8859-2 -t UTF8 CHANGES > CHANGES.tmp
mv CHANGES.tmp CHANGES


%build
%ifarch %{ix86} x86_64
ARCH_CONFIGURE_FLAGS=--with-svga
%endif
# Note: the CPU level, MMX et al affect what the emulator will emulate, they
# are not properties of the build target architecture.
# Note2: passing --enable-pcidev will change bochs license from LGPLv2+ to
# LGPLv2 (and requires a kernel driver to be usefull)
CONFIGURE_FLAGS=" \
  --enable-plugins \
  --enable-ne2000 \
  --enable-pci \
  --enable-all-optimizations \
  --enable-clgd54xx \
  --enable-sb16=linux \
  --enable-3dnow
  --with-x11 \
  --with-nogui \
  --with-term \
  --with-rfb \
  --with-sdl \
  --without-wx \
  --enable-cpu-level=6 \
  --enable-disasm \
  --enable-usb \
  --enable-usb-ohci \
  $ARCH_CONFIGURE_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS -DPARANOID"

%configure2_5x $CONFIGURE_FLAGS --enable-x86-debugger --enable-debugger
%make
mv bochs bochs-debugger
make dist-clean

%configure2_5x $CONFIGURE_FLAGS --enable-x86-debugger --enable-gdb-stub
%make
mv bochs bochs-gdb
make dist-clean

%configure2_5x $CONFIGURE_FLAGS
%make

%ifarch %{ix86} x86_64
cd bios
make bios
cp BIOS-bochs-latest BIOS-bochs-kvm
%endif

%install
rm -rf %{buildroot} _installed-docs
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_prefix}/share/bochs/VGABIOS*
ln -s %{_prefix}/share/vgabios/VGABIOS-lgpl-latest.bin %{buildroot}%{_prefix}/share/bochs/VGABIOS-lgpl-latest
ln -s %{_prefix}/share/vgabios/VGABIOS-lgpl-latest.cirrus.bin %{buildroot}%{_prefix}/share/bochs/VGABIOS-lgpl-latest.cirrus
ln -s %{_prefix}/share/vgabios/VGABIOS-lgpl-latest.cirrus.debug.bin %{buildroot}%{_prefix}/share/bochs/VGABIOS-lgpl-latest.cirrus.debug
ln -s %{_prefix}/share/vgabios/VGABIOS-lgpl-latest.debug.bin %{buildroot}%{_prefix}/share/bochs/VGABIOS-lgpl-latest.debug
%ifnarch %{ix86} x86_64
rm -rf %{buildroot}%{_prefix}/share/bochs/*BIOS*
%endif
install -m 755 bochs-debugger bochs-gdb %{buildroot}%{_bindir}
mv %{buildroot}%{_docdir}/bochs _installed-docs
rm %{buildroot}%{_mandir}/man1/bochs-dlx.1*

mkdir -p %{buildroot}%{_prefix}/include/bochs/disasm
cp -pr disasm/*.h %{buildroot}%{_prefix}/include/bochs/disasm/
cp -pr disasm/*.cc %{buildroot}%{_prefix}/include/bochs/disasm/
cp -pr disasm/*.inc %{buildroot}%{_prefix}/include/bochs/disasm/
cp -pr config.h %{buildroot}%{_prefix}/include/bochs/







