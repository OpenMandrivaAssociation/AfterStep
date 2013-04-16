#define debug_package %{nil}
%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} -d
%define	ltitle	AfterStep Window Manager

Summary:	%{ltitle}
Name:		AfterStep
Version:	2.2.11
Release:	3
Epoch:          4
License:	GPLv2+
Group:		Graphical desktop/Other
URL:		http://www.afterstep.org/

Source:		ftp://ftp.afterstep.org/stable/AfterStep-%version.tar.bz2
Source1:	%{name}-mdkconf.tar.bz2
Source3:	%{name}.png
Source4:	%{name}32.png
Source5:	%{name}48.png
Patch2:		%{name}-1.8.9-menuname.patch
Patch3:         %{name}.MenuKey.patch
Patch4:		afterstep-2.2.9-ldflags.patch
Patch5:		afterstep-2.2.9-libpng15.patch

Requires:	desktop-common-data xli 
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(gdk-2.0)

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
Obsoletes:	%mklibname -d %name 0

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
%patch4 -p0 -b .link
%patch5 -p1 

%build
rm -f config.status
export CFLAGS="%optflags"
export CCFLAGS="%optflags"

%configure2_5x	\
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
%makeinstall_std LDCONFIG=/bin/true

# LMDK icons
install -m644 %SOURCE4 -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %SOURCE3 -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %SOURCE5 -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# Not needed with Mandriva menu
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



%post
%make_session

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%postun
%make_session

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/15%{name}
%doc COPYRIGHT ChangeLog NEW README TEAM UPGRADE doc/languages doc/licences
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
%{_libdir}/*.so.%major
%{_libdir}/*.so.%major.*

%files -n %libname_devel
%{_libdir}/*.so
%{_libdir}/*.a
%_includedir/*


%changelog
* Wed Jan 19 2011 Funda Wang <fwang@mandriva.org> 4:2.2.11-1mdv2011.0
+ Revision: 631658
- New version 2.2.11

* Mon Jan 03 2011 Funda Wang <fwang@mandriva.org> 4:2.2.9-4mdv2011.0
+ Revision: 627679
- fix linkage

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 4:2.2.9-3mdv2011.0
+ Revision: 609926
- rebuild

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 4:2.2.9-2mdv2010.0
+ Revision: 419754
- rebuild for new libjpeg v7

  + Frederik Himpe <fhimpe@mandriva.org>
    - Update to new version 2.2.9
    - Use %%configure2_5x macro instead of %%configure to fix build

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 4:2.2.4-2mdv2009.0
+ Revision: 218439
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

* Mon Jan 07 2008 Funda Wang <fwang@mandriva.org> 4:2.2.4-2mdv2008.1
+ Revision: 146266
- New devel package policy
- fix requires on Mandriva_desk

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 4:2.2.4-1mdv2008.1
+ Revision: 135819
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel
    - s/Mandrake/Mandriva/


* Fri Dec 01 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 2.2.4-1mdv2007.0
+ Revision: 89500
- New version 2.2.4

* Thu Aug 03 2006 Olivier Thauvin <nanardon@mandriva.org> 4:2.2.2-1mdv2007.0
+ Revision: 43064
- remove menu (no longer supported, just hopping xdg menu are supported, else no menu)
- 2.2.2
- Import AfterStep

* Fri Jun 16 2006 Lenny Cartier <lenny@mandriva.com> 4:2.2.1-2mdv2007.0
- rebuild

* Tue Mar 07 2006 Olivier Thauvin <nanardon@mandriva.org> 2.2.1-1mdk
- 2.2.1

* Fri Oct 07 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1.0-2mdk
- Fix BuildRequires
- Remove redundant buildrequire

* Fri May 27 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1.0-1mdk
- 2.1.0

* Mon May 09 2005 Olivier Thauvin <nanardon@mandriva.org> 2.00.05-1mdk
- 2.00.05
- remove patch4, merge upstream

* Thu Jan 13 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.00.01-2mdk
- Fix lib installation

* Wed Jan 12 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.00.01-1mdk
- 2.00.01
- rediff patch3

* Sat Feb 28 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.8.11-5mdk
- Fix Dep (epoch)

