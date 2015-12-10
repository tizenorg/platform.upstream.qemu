Name:           qemu
Url:            http://www.qemu.org/
Summary:        Universal CPU emulator
License:        BSD-3-Clause and GPL-2.0 and GPL-2.0+ and LGPL-2.1+ and MIT
Group:          System/Utilities
Version:        2.2.0
Release:        0
Source:         %name-%version.tar.bz2
# this is to make lint happy
Source300:      rpmlintrc
Source302:      bridge.conf
Source303:      baselibs.conf
Source400:      update_git.sh
BuildRequires:  bison
#BuildRequires:  curl-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libattr-devel
#BuildRequires:  libcap-devel
#BuildRequires:  libcap-ng-devel
#BuildRequires:  libgnutls-devel
#BuildRequires:  libjpeg8-devel
#BuildRequires:  libpng-devel
#BuildRequires:  ncurses-devel
# we must not install the qemu package when under qemu build
%if 0%{?qemu_user_space_build:1}
BuildRequires:  -post-build-checks
%endif
BuildRequires:  zlib-devel-static
BuildRequires:  glibc-devel-static
BuildRequires:  libattr-devel-static
BuildRequires:  glib2-devel-static
BuildRequires:  pcre-devel-static
BuildRequires:  fdupes
BuildRequires:  glib2-devel
#BuildRequires:  pwdutils
BuildRequires:  python
#BuildRequires:  pkgconfig(sdl)
Requires:       /usr/sbin/groupadd
Requires:       pwdutils
Requires:       timezone

%description
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

%package tools
Summary:        Universal CPU emulator -- Tools
Provides:       qemu:%_libexecdir/qemu-bridge-helper

%description tools
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains various tools, including a bridge helper.

%package guest-agent
Summary:        Universal CPU emulator -- Guest agent
Provides:       qemu:%_bindir/qemu-ga

%description guest-agent
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains the guest agent.

%package linux-user
Summary:        Universal CPU emulator -- Linux User binaries
Provides:       qemu:%_bindir/qemu-arm

%description linux-user
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains statically linked binaries for running linux-user
emulations. This can be used together with the OBS build script to
run cross-architecture builds.

%prep
%setup -q -n %name-%version

%build
export QEMU_OPT_FLAGS="$QEMU_OPT_FLAGS -Wno-error=type-limits"
# build QEMU
mkdir -p dynamic
# build qemu-system
./configure --prefix=%_prefix \
	--sysconfdir=%_sysconfdir \
	--libexecdir=%_libexecdir \
	--enable-attr \
	--disable-linux-aio \
	--extra-cflags="$QEMU_OPT_FLAGS" \
	--enable-system \
	--disable-linux-user 

make %{?jobs:-j%jobs} V=1
mv *-softmmu/qemu-system-* dynamic
mv qemu-io qemu-img qemu-nbd qemu-bridge-helper dynamic
#mv qemu-img.1 qemu-nbd.8 dynamic
mv qemu-ga dynamic
make clean
# build userland emus
./configure --prefix=%_prefix --sysconfdir=%_sysconfdir \
	--libexecdir=%_libexecdir \
	--enable-linux-user \
	--disable-system \
	--enable-attr \
	--static --disable-linux-aio \
	--extra-cflags="$QEMU_OPT_FLAGS"
make %{?jobs:-j%jobs} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -fr $RPM_BUILD_ROOT/%_datadir/doc
install -m 755 dynamic/qemu-system-* $RPM_BUILD_ROOT/%_bindir
install -m 755 dynamic/qemu-io $RPM_BUILD_ROOT/%_bindir
install -m 755 dynamic/qemu-img $RPM_BUILD_ROOT/%_bindir
install -m 755 dynamic/qemu-nbd $RPM_BUILD_ROOT/%_bindir
install -m 755 dynamic/qemu-ga $RPM_BUILD_ROOT/%_bindir
install -d -m 755 $RPM_BUILD_ROOT/%_sbindir
install -m 755 scripts/qemu-binfmt-conf.sh $RPM_BUILD_ROOT/%_sbindir
install -d -m 755 $RPM_BUILD_ROOT/%_libexecdir
install -m 755 dynamic/qemu-bridge-helper $RPM_BUILD_ROOT/%_libexecdir
install -d -m 755 $RPM_BUILD_ROOT/%_mandir/man1
install -D -m 644 %{SOURCE302} $RPM_BUILD_ROOT/%{_sysconfdir}/qemu/bridge.conf
%ifnarch %ix86 x86_64
ln -sf ../../../emul/ia32-linux $RPM_BUILD_ROOT/usr/share/qemu/qemu-i386
%endif
%ifnarch ia64
mkdir -p $RPM_BUILD_ROOT/emul/ia32-linux
%endif
ln -sf /%_bindir/qemu-aarch64 $RPM_BUILD_ROOT/%_bindir/qemu-arm64
ln -sf /%_bindir/qemu-aarch64-binfmt $RPM_BUILD_ROOT/%_bindir/qemu-arm64-binfmt
%fdupes -s $RPM_BUILD_ROOT

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre
%{_bindir}/getent group kvm >/dev/null || %{_sbindir}/groupadd -r kvm 2>/dev/null
%{_bindir}/getent group qemu >/dev/null || %{_sbindir}/groupadd -r qemu 2>/dev/null
%{_bindir}/getent passwd qemu >/dev/null || \
  %{_sbindir}/useradd -r -g qemu -G kvm -d / -s /sbin/nologin \
  -c "qemu user" qemu

%files
%license COPYING
%defattr(-, root, root)
%doc COPYING COPYING.LIB Changelog README VERSION
%_bindir/qemu-system-*
%_datadir/%name
%ifnarch %ix86 x86_64 ia64
%dir /emul/ia32-linux
%endif
%dir %_sysconfdir/%name
%config %_sysconfdir/%name/target-x86_64.conf

%files tools
%defattr(-, root, root)
%_bindir/qemu-io
%_bindir/qemu-img
%_bindir/qemu-nbd
%verify(not mode) %_libexecdir/qemu-bridge-helper
%dir %_sysconfdir/%name
%config %_sysconfdir/%name/bridge.conf

%files guest-agent
%defattr(-, root, root)
%attr(755,root,kvm) %_bindir/qemu-ga

%files linux-user
%defattr(-, root, root)
%_bindir/qemu-alpha
%_bindir/qemu-aarch64
%_bindir/qemu-arm64
%_bindir/qemu-arm
%_bindir/qemu-armeb
%_bindir/qemu-cris
%_bindir/qemu-i386
%_bindir/qemu-m68k
%_bindir/qemu-microblaze
%_bindir/qemu-microblazeel
%_bindir/qemu-mips
%_bindir/qemu-mips64
%_bindir/qemu-mips64el
%_bindir/qemu-mipsel
%_bindir/qemu-mipsn32
%_bindir/qemu-mipsn32el
%_bindir/qemu-or32
%_bindir/qemu-ppc64abi32
%_bindir/qemu-ppc64
%_bindir/qemu-ppc64le
%_bindir/qemu-ppc
%_bindir/qemu-s390x
%_bindir/qemu-sh4
%_bindir/qemu-sh4eb
%_bindir/qemu-sparc32plus
%_bindir/qemu-sparc64
%_bindir/qemu-sparc
%_bindir/qemu-unicore32
%_bindir/qemu-x86_64
%_bindir/qemu-*-binfmt
%_sbindir/qemu-binfmt-conf.sh

%changelog
