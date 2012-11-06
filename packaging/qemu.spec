#
# spec file for package qemu
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           qemu
Version:        1.2.0
Release:        0
License:        BSD-3-Clause ; GPL-2.0+ ; LGPL-2.1+ ; MIT
Summary:        Universal CPU emulator
Url:            http://www.qemu.org/
Group:          System/Emulators/PC
Source:         %{name}-%{version}.tar.bz2
Patch0001:      0001-Handle-CPU-interrupts-by-inline-che.patch
Patch0002:      0002-XXX-dont-dump-core-on-sigabort.patc.patch
Patch0003:      0003-XXX-work-around-SA_RESTART-race-wit.patch
Patch0004:      0004-qemu-0.9.0.cvs-binfmt.patch.patch
Patch0005:      0005-qemu-cvs-alsa_bitfield.patch.patch
Patch0006:      0006-qemu-cvs-alsa_ioctl.patch.patch
Patch0007:      0007-qemu-cvs-alsa_mmap.patch.patch
Patch0008:      0008-qemu-cvs-gettimeofday.patch.patch
Patch0009:      0009-qemu-cvs-ioctl_debug.patch.patch
Patch0010:      0010-qemu-cvs-ioctl_nodirection.patch.patch
Patch0011:      0011-block-vmdk-Support-creation-of-SCSI.patch
Patch0012:      0012-configure-Enable-mipsn32-linux-user.patch
Patch0013:      0013-linux-user-add-binfmt-wrapper-for-a.patch
Patch0014:      0014-linux-user-Ignore-timer_create-sysc.patch
Patch0015:      0015-linux-user-be-silent-about-capget-f.patch
Patch0016:      0016-PPC-KVM-Disable-mmu-notifier-check..patch
Patch0017:      0017-linux-user-fix-segfault-deadlock.pa.patch
Patch0018:      0018-linux-user-binfmt-support-host-bina.patch
Patch0019:      0019-linux-user-arm-no-tb_flush-on-reset.patch
Patch0020:      0020-linux-user-fix-multi-threaded-proc-.patch
Patch0021:      0021-use-libexecdir-instead-of-ignoring-.patch
Patch0022:      0022-linux-user-Ignore-broken-loop-ioctl.patch
Patch0023:      0023-linux-user-fix-segmentation-fault-p.patch
Patch0024:      0024-linux-user-lock-tcg.patch.patch
Patch0025:      0025-linux-user-Run-multi-threaded-code-.patch
Patch0026:      0026-linux-user-lock-tb-flushing-too.pat.patch
Patch0027:      0027-linux-user-Fake-proc-cpuinfo.patch.patch
Patch0028:      0028-linux-user-implement-FS_IOC_GETFLAG.patch
Patch0029:      0029-linux-user-implement-FS_IOC_SETFLAG.patch
Patch0030:      0030-linux-user-fix-statfs.patch.patch
Patch0031:      0031-linux-user-XXX-disable-fiemap.patch.patch
Patch0032:      0032-slirp-nooutgoing.patch.patch
Patch0033:      0033-vnc-password-file-and-incoming-conn.patch
# this is to make lint happy
Source300:      rpmlintrc
Source302:      bridge.conf
Source400:      update_git.sh
#BuildRequires:  SDL-devel
BuildRequires:  bison
#BuildRequires:  bluez-devel
BuildRequires:  curl-devel
#BuildRequires:  cyrus-sasl-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gnutls-devel
#BuildRequires:  libaio
#BuildRequires:  libaio-devel
BuildRequires:  libattr-devel
BuildRequires:  libcap-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libjpeg8-devel
#BuildRequires:  libpcap-devel
BuildRequires:  libpng-devel
BuildRequires:  ncurses-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# we must not install the qemu package when under qemu build
%if 0%{?qemu_user_space_build:1}
BuildRequires:  -post-build-checks
%endif
BuildRequires:  fdupes
BuildRequires:  glibc-devel-static
BuildRequires:  libattr-devel-static
BuildRequires:  pcre-devel-static
#BuildRequires:  libvdeplug3-devel
BuildRequires:  pwdutils
BuildRequires:  python-base
BuildRequires:  zlib-devel-static
BuildRequires:  pkgconfig(glib-2.0)
#BuildRequires:  libfdt1-devel
BuildRequires:  pkgconfig(glib-2.0)-static
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
Group:          System/Emulators/PC
Provides:       qemu:%{_libexecdir}/qemu-bridge-helper

%description tools
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains various tools, including a bridge helper.

%package guest-agent
Summary:        Universal CPU emulator -- Guest agent
Group:          System/Emulators/PC
Provides:       qemu:%{_bindir}/qemu-ga

%description guest-agent
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

This sub-package contains the guest agent.

%package linux-user
Summary:        Universal CPU emulator -- Linux User binaries
Group:          System/Emulators/PC
Provides:       qemu:%{_bindir}/qemu-arm

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
%setup -q -n %{name}-%{version}
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1

%build
# build QEMU
mkdir -p dynamic
# build qemu-system
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} \
	--libexecdir=%{_libexecdir} \
	--enable-curl \
	--enable-virtfs --disable-linux-aio \
	--extra-cflags="$QEMU_OPT_FLAGS" --enable-system --disable-linux-user
make %{?_smp_mflags} V=1
mv *-softmmu/qemu-system-* dynamic
mv qemu-io qemu-img qemu-nbd qemu-bridge-helper dynamic
#mv qemu-img.1 qemu-nbd.8 dynamic
mv qemu-ga dynamic
mv fsdev/virtfs-proxy-helper dynamic
make clean
# build userland emus
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} \
	--libexecdir=%{_libexecdir} \
	--enable-linux-user \
	--disable-system \
	--static --disable-linux-aio \
	--extra-cflags="$QEMU_OPT_FLAGS"
make %{?_smp_mflags} V=1

%install
%make_install
rm -fr %{buildroot}/%{_datadir}/doc
install -m 755 dynamic/qemu-system-* %{buildroot}/%{_bindir}
install -m 755 dynamic/qemu-io %{buildroot}/%{_bindir}
install -m 755 dynamic/qemu-img %{buildroot}/%{_bindir}
install -m 755 dynamic/qemu-nbd %{buildroot}/%{_bindir}
install -m 755 dynamic/qemu-ga %{buildroot}/%{_bindir}
install -m 755 dynamic/virtfs-proxy-helper %{buildroot}/%{_bindir}
install -d -m 755 %{buildroot}/%{_sbindir}
install -m 755 scripts/qemu-binfmt-conf.sh %{buildroot}/%{_sbindir}
install -d -m 755 %{buildroot}/%{_libexecdir}
install -m 755 dynamic/qemu-bridge-helper %{buildroot}/%{_libexecdir}
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -D -m 644 %{SOURCE302} %{buildroot}/%{_sysconfdir}/qemu/bridge.conf
%ifnarch %ix86 x86_64
ln -sf ../../../emul/ia32-linux %{buildroot}/usr/share/qemu/qemu-i386
%endif
%ifnarch ia64
mkdir -p %{buildroot}/emul/ia32-linux
%endif
%fdupes -s %{buildroot}

%pre
%{_bindir}/getent group kvm >/dev/null || %{_sbindir}/groupadd -r kvm 2>/dev/null
%{_bindir}/getent group qemu >/dev/null || %{_sbindir}/groupadd -r qemu 2>/dev/null
%{_bindir}/getent passwd qemu >/dev/null || \
  %{_sbindir}/useradd -r -g qemu -G kvm -d / -s /sbin/nologin \
  -c "qemu user" qemu

%files
%defattr(-, root, root)
%doc COPYING COPYING.LIB Changelog README TODO VERSION
%{_bindir}/qemu-system-*
%{_datadir}/%{name}
%ifnarch %ix86 x86_64 ia64
%dir /emul/ia32-linux
%endif
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/target-x86_64.conf

%files tools
%defattr(-, root, root)
%{_bindir}/qemu-io
%{_bindir}/qemu-img
%{_bindir}/qemu-nbd
%{_bindir}/virtfs-proxy-helper
%verify(not mode) %{_libexecdir}/qemu-bridge-helper
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/bridge.conf

%files guest-agent
%defattr(-, root, root)
%attr(755,root,kvm) %{_bindir}/qemu-ga

%files linux-user
%defattr(-, root, root)
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-i386
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-sparc
%{_bindir}/qemu-unicore32
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-*-binfmt
%{_sbindir}/qemu-binfmt-conf.sh

%changelog
