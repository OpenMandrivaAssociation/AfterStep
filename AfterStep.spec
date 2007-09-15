%define	name	AfterStep
%define	version	2.2.4
%define	release	%mkrel 1
%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} %{major} -d
%define	ltitle	AfterStep Window Manager

Summary:	%{ltitle}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:          4
License:	GPL
Group:		Graphical desktop/Other
URL:		http://www.afterstep.org/

Source:		ftp://ftp.afterstep.org/stable/AfterStep-%version.tar.bz2
Source1:	%{name}-mdkconf.tar.bz2
Source3:	%{name}.png.bz2
Source4:	%{name}32.png.bz2
Source5:	%{name}48.png.bz2
Patch2:		%{name}-1.8.9-menuname.patch
Patch3:         %{name}.MenuKey.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires:	Mandriva_desk >= 7.2-1mdk xli 
# Requires: 	%libname = %{epoch}:%{version}-%{release}
BuildRequires:	XFree86-devel
BuildRequires:  libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:   gtk2-devel

%description
AfterStep is a Window Manager for X which started by emulating the NEXTSTEP
look and feel, but which has been significantly altered according to the
requests of various users. Many adepts will tell you that NEXTSTEP is not
only the most visually pleasant interface, but also one of the most functional
and intuitive out there. AfterStep aims to incorporate the advantages of the
NEXTSTEP interface, and add additional useful features.

The developers of AfterStep have also worked very hard to ensure stability and
a small program footprint. Without giving up too many features, AfterStep still
works nicely in environments where memory is at a premium.

%package -n %libname
Summary:	Libraries needed by AfterStep
Group:		Graphical desktop/Other
Provides:	lib%name = %version-%release
 
%description -n %libname
AfterStep is a Window Manager for X which started by emulating the NEXTSTEP
look and feel, but which has been significantly altered according to the
requests of various users. Many adepts will tell you that NEXTSTEP is not
only the most visually pleasant interface, but also one of the most functional
and intuitive out there. AfterStep aims to incorporate the advantages of the
NEXTSTEP interface, and add additional useful features.

The developers of AfterStep have also worked very hard to ensure stability and
a small program footprint. Without giving up too many features, AfterStep still
works nicely in environments where memory is at a premium.

This package contains libraries needed by AfterStep package.

%package -n %libname_devel
Summary:	Devel files needed to build applications based on AfterStep
Group:		Development/C
Provides:	%name-devel lib%name-devel
Requires:	%libname = %{epoch}:%version-%release

%description -n %libname_devel
AfterStep is a Window Manager for X which started by emulating the NEXTSTEP
look and feel, but which has been significantly altered according to the
requests of various users. Many adepts will tell you that NEXTSTEP is not
only the most visually pleasant interface, but also one of the most functional
and intuitive out there. AfterStep aims to incorporate the advantages of the
NEXTSTEP interface, and add additional useful features.

The developers of AfterStep have also worked very hard to ensure stability and
a small program footprint. Without giving up too many features, AfterStep still
works nicely in environments where memory is at a premium.

This package contains devel files needed to build applications based on
AfterStep.

%prep
%setup -q

# LMDK patches
%patch2 -p1
%patch3 -p1
#%patch4 -p0 -b .configshared

%build
rm -f config.status
export CFLAGS="%optflags"
export CCFLAGS="%optflags"

%configure	\
                --enable-sharedlibs \
		--with-imageloader="xsetbg" \
		--with-helpcommand="xterm -fn 9x15 -e man" \
		--with-desktops=1 \
		--with-deskgeometry=1x1 \
		--enable-different-looknfeels \
		--enable-i18n \
		--enable-savewindows \
		--enable-texture \
		--enable-shade \
		--enable-virtual \
		--enable-saveunders \
		--enable-windowlist \
		--enable-availability \
		--enable-shaping \
		--enable-xinerama \
		--enable-script \
		--with-xpm \
		--with-jpeg \
		--with-png \
                --with-ttf \
                --with-tiff

%make

if [ -x /usr/bin/sgml2html ]; then sgml2html doc/afterstep.sgml; fi


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF >$RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):needs=wm \
	section="Session/Windowmanagers" \
	icon="%{name}.png" \
	title="%{name}" \
	longtitle="%{ltitle}" \
	command="afterstep" \
        xdg="true"
EOF

# LMDK icons
install -m644 %SOURCE4 -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %SOURCE3 -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %SOURCE5 -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# Not needed with Linux-Mandriva menu
rm -fr $RPM_BUILD_ROOT/%{__datadir}/afterstep/start/Applications/

install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d/15%{name} << EOF
NAME=%{name}
ICON=%{name}.png
EXEC=%{_bindir}/afterstep
DESC=A NeXt like Window-Manager
SCRIPT:
exec %{_bindir}/afterstep
EOF

%if 0
%multiarch_binaries %buildroot%_bindir/afterimage-config
%multiarch_binaries %buildroot%_bindir/afterstep-config
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%make_session

%post -n %libname -p /sbin/ldconfig

%postun
%clean_menus
%make_session

%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/15%{name}
%doc COPYRIGHT ChangeLog NEW README TEAM UPGRADE doc/languages doc/licences
%{_menudir}/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%dir %{_datadir}/afterstep
%{_datadir}/afterstep/*
%_datadir/xsessions/AfterStep.desktop

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/*.so.%major
%{_libdir}/*.so.%major.*

%files -n %libname_devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.a
%dir %_includedir/libAfterConf
%_includedir/libAfterConf/*.h
%dir %_includedir/libAfterStep
%_includedir/libAfterStep/*.h
%_includedir/libASGTK


