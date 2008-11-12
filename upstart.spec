Summary:	Event-based init daemon
Summary(pl.UTF-8):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	0.5.0
Release:	3
License:	GPL v2
Group:		Base
Source0:	http://edge.launchpad.net/upstart/0.5/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	df5e2db549b6ebf406d48419831a66b8
Patch0:		%{name}-oomfail.patch
URL:		https://launchpad.net/upstart
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gettext >= 0.14.5
BuildRequires:	glibc-headers >= 6:2.4.0
BuildRequires:	libtool >= 2:1.5.22
Provides:	virtual(init-daemon)
Obsoletes:	virtual(init-daemon)
Suggests:	dbus
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
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-compat
%{__make}

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f upstart.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS TODO
%{_sysconfdir}/dbus-1/system.d/Upstart.conf
%dir %{_sysconfdir}/init
%dir %{_sysconfdir}/init/conf.d
%dir %{_sysconfdir}/init/jobs.d
%attr(755,root,root) %{_sbindir}/halt
%attr(755,root,root) %{_sbindir}/init
%attr(755,root,root) %{_sbindir}/initctl
%attr(755,root,root) %{_sbindir}/poweroff
%attr(755,root,root) %{_sbindir}/reboot
%attr(755,root,root) %{_sbindir}/runlevel
%attr(755,root,root) %{_sbindir}/shutdown
%attr(755,root,root) %{_sbindir}/start
%attr(755,root,root) %{_sbindir}/status
%attr(755,root,root) %{_sbindir}/stop
%attr(755,root,root) %{_sbindir}/telinit
%{_mandir}/man8/*.8*
