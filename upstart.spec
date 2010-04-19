#
# Conditional build:
%bcond_without	tests	# don't perform "make check"

Summary:	Event-based init daemon
Summary(pl.UTF-8):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	0.6.5
Release:	1
License:	GPL v2
Group:		Base
Source0:        http://upstart.ubuntu.com/download/0.6/upstart-%{version}.tar.gz
# Source0-md5:	f9466bba72b655c2408353b64105853f
URL:            http://upstart.ubuntu.com/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.2.16-1
BuildRequires:	libnih-devel >= 1.0.1
BuildRequires:	expat-devel
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gettext >= 0.14.5
BuildRequires:	glibc-headers >= 6:2.4.0
BuildRequires:	libtool >= 2:1.5.22
BuildRequires:	pkgconfig
Requires:	dbus-libs >= 1.2.14-2
Suggests:	dbus
Conflicts:	dbus < 1.2.12-2
Provides:	virtual(init-daemon)
Obsoletes:	virtual(init-daemon)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
upstart is a replacement for the /sbin/init daemon which handles
starting of tasks and services during boot, stopping them during
shutdown and supervising them while the system is running.

%description -l pl.UTF-8
upstart jest zamiennikiem demona /sbin/init zajmującym się
uruchamianiem zadań i usług podczas startu systemu, ich zatrzymywaniem
podczas wyłączania systemu, a także nadzorowaniem ich pracy.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang upstart

# no -devel
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.{la,so}
rm -rf $RPM_BUILD_ROOT%{_aclocaldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/telinit u || :

%postun	-p /sbin/ldconfig

%triggerpostun -- glibc
/sbin/telinit u || :

%files -f upstart.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS TODO
%{_sysconfdir}/dbus-1/system.d/Upstart.conf
%dir %{_sysconfdir}/init
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/init/*.conf
%attr(755,root,root) %{_sbindir}/halt
%attr(755,root,root) %{_sbindir}/init
%attr(755,root,root) %{_sbindir}/initctl
%attr(755,root,root) %{_sbindir}/poweroff
%attr(755,root,root) %{_sbindir}/reboot
%attr(755,root,root) %{_sbindir}/reload
%attr(755,root,root) %{_sbindir}/restart
%attr(755,root,root) %{_sbindir}/runlevel
%attr(755,root,root) %{_sbindir}/shutdown
%attr(755,root,root) %{_sbindir}/start
%attr(755,root,root) %{_sbindir}/status
%attr(755,root,root) %{_sbindir}/stop
%attr(755,root,root) %{_sbindir}/telinit
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
