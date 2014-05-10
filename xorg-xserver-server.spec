%define         gitver	%{nil}

Summary:	X.org server
Name:		xorg-xserver-server
Version:	1.15.1
%if "%{gitver}" != "%{nil}"
Release:	0.%{gitver}.1
Source0:	http://cgit.freedesktop.org/xorg/xserver/snapshot/xserver-%{gitver}.tar.bz2
# Source0-md5:	e4c70262ed89764be8f8f5d699ed9227
%else
Release:	2
Source0:	http://xorg.freedesktop.org/releases/individual/xserver/xorg-server-%{version}.tar.bz2
# Source0-md5:	e4c70262ed89764be8f8f5d699ed9227
%endif
License:	MIT
Group:		X11/Servers
# http://lists.x.org/archives/xorg-devel/2011-January/018623.html
Patch0:		%{name}-cache-indirect-opcode.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	dbus-devel
BuildRequires:	libdrm-devel
BuildRequires:	libpciaccess-devel >= 0.13
BuildRequires:	libtool
BuildRequires:	libunwind-devel
BuildRequires:	mtdev-devel
BuildRequires:	ncurses-devel
BuildRequires:	nettle-devel
BuildRequires:	perl-base
BuildRequires:	pixman-devel
BuildRequires:	pkg-config
BuildRequires:	pkgconfig(dri3proto)
BuildRequires:	pkgconfig(presentproto)
BuildRequires:	pkgconfig(xextproto) >= 7.3.0
BuildRequires:	pkgconfig(xproto) >= 7.0.25
BuildRequires:	xcb-util-image-devel
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xcb-util-wm-devel
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXau-devel
BuildRequires:	xorg-libXaw-devel
BuildRequires:	xorg-libXdamage-devel
BuildRequires:	xorg-libXdmcp-devel
BuildRequires:	xorg-libXevie-devel
BuildRequires:	xorg-libXext-devel
BuildRequires:	xorg-libXfont-devel
BuildRequires:	xorg-libXi-devel >= 1.7
BuildRequires:	xorg-libXrender-devel
BuildRequires:	xorg-libXres-devel
BuildRequires:	xorg-libXt-devel
BuildRequires:	xorg-libXtst-devel
BuildRequires:	xorg-libXv-devel
BuildRequires:	xorg-libXxf86dga-devel
BuildRequires:	xorg-libXxf86misc-devel
BuildRequires:	xorg-libXxf86vm-devel
BuildRequires:	xorg-libfontenc-devel
BuildRequires:	xorg-libxkbfile-devel
BuildRequires:	xorg-libxshmfence-devel
BuildRequires:	xorg-util-macros
BuildRequires:	xorg-xtrans-devel
# pixman-1 >= 0.21.8 xkbfile  xfont xau xdmcp
Requires:	xorg-xserver-common = %{version}-%{release}
Requires:	Mesa-dri-driver-swrast
Requires:	xkeyboard-config
Requires:	xorg-app-rgb
Requires:	xorg-app-xkbcomp
Requires:	xorg-driver-input-evdev
Requires:	xorg-font-alias
Requires:	xorg-font-cursor-misc
Requires:	xorg-font-misc-base
Requires:	xorg-libXt
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	libscanpci.so libxf1bpp.so

%description
Xorg server is a generally used X server which uses display hardware.
It requires proper driver for your display hardware.

%package -n xorg-xserver-common
Summary:	Common directories and files
Group:		X11Libraries

%description -n xorg-xserver-common
Common directories and files.

%package devel
Summary:	Header files for X.org server
Group:		X11/Development/Libraries
Requires:	libdrm-devel
Requires:	xorg-proto

%description devel
Header files for X.org server.

%package -n xorg-xserver-Xnest
Summary:	Nested X server
Group:		X11/Servers

%description -n xorg-xserver-Xnest
Xnest X server.

%package -n xorg-xserver-Xephyr
Summary:	Xephyr X server
Group:		X11/Servers

%description -n xorg-xserver-Xephyr
Xephyr X server.

%package -n xorg-xserver-Xvfb
Summary:	Xvfb X server
Group:		X11/Servers

%description -n xorg-xserver-Xvfb
Xvfb X server.

%prep
%if "%{gitver}" != "%{nil}"
%setup -qn xserver-%{gitver}
%else
%setup -qn xorg-server-%{version}
%endif

%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-config-dbus			\
	--disable-config-hal			\
	--disable-dmx				\
	--disable-linux-acpi			\
	--disable-linux-apm			\
	--disable-silent-rules			\
	--disable-xfake				\
	--disable-xfbdev			\
	--enable-config-udev			\
	--enable-glx-tls			\
	--enable-kdrive				\
	--enable-xephyr				\
	--enable-xnest				\
	--enable-xvfb				\
	--enable-xvmc				\
	--with-dri-driver-path=%{_libdir}/xorg/modules/dri	\
	--with-fontrootdir="%{_fontsdir}"	\
	--with-os-name="Freddix"		\
	--with-xkb-output=/var/lib/xkb		\
	--with-xkb-path=/usr/share/X11/xkb	\
	--without-dtrace
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{*,*/*}.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%if "%{gitver}" != "%{nil}"
%doc COPYING
%else
%doc COPYING ChangeLog
%endif
%attr(755,root,root) %{_bindir}/X
%attr(755,root,root) %{_bindir}/Xorg
%attr(755,root,root) %{_bindir}/cvt
%attr(755,root,root) %{_bindir}/gtf
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libglx.so
%attr(755,root,root) %{_libdir}/xorg/modules/lib*.so
%attr(755,root,root) %{_libdir}/xorg/modules/multimedia/*.so
%{_datadir}/X11/xorg.conf.d/*.conf

%dir /var/lib/xkb
/var/lib/xkb/README.compiled

%{_mandir}/man1/Xorg.1x*
%{_mandir}/man1/Xserver.1x*
%{_mandir}/man1/cvt.1*
%{_mandir}/man1/gtf.1x*
%{_mandir}/man4/exa.4*
%{_mandir}/man4/fbdevhw.4*
%{_mandir}/man5/xorg.conf.5x*
%{_mandir}/man5/xorg.conf.d.5x*

%files -n xorg-xserver-common
%defattr(644,root,root,755)
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/extensions
%dir %{_libdir}/xorg/modules/input
%dir %{_libdir}/xorg/modules/multimedia
%dir %{_datadir}/X11/xorg.conf.d
%dir /etc/X11/xorg.conf.d
%{_libdir}/xorg/protocol.txt

%files devel
%defattr(644,root,root,755)
%{_includedir}/xorg
%{_aclocaldir}/xorg-server.m4
%{_pkgconfigdir}/xorg-server.pc

%files -n xorg-xserver-Xnest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xnest
%{_mandir}/man1/Xnest.1x*

%files -n xorg-xserver-Xephyr
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1x*

%files -n xorg-xserver-Xvfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xvfb
%{_mandir}/man1/Xvfb.1x*

