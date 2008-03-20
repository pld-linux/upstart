Summary:	Event-based init daemon
Summary(pl.UTF-8):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	0.3.9
Release:	2
License:	GPL v2
Group:		Base
Source0:	http://upstart.ubuntu.com/download/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	794208083d405ece123ad59a02f3e233
URL:		https://launchpad.net/upstart
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gettext >= 0.14.5
BuildRequires:	glibc-headers >= 6:2.4.0
BuildRequires:	libtool >= 2:1.5.22
Provides:	virtual(init-daemon)
Obsoletes:	virtual(init-daemon)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir			/%{_lib}
%define		_sbindir		/sbin
%define		_sysconfdir		/etc/%{name}

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
%dir %{_sysconfdir}
%dir %{_sysconfdir}/event.d
%{_sysconfdir}/event.d/logd
%attr(755,root,root) %{_sbindir}/halt
%attr(755,root,root) %{_sbindir}/init
%attr(755,root,root) %{_sbindir}/initctl
%attr(755,root,root) %{_sbindir}/logd
%attr(755,root,root) %{_sbindir}/poweroff
%attr(755,root,root) %{_sbindir}/reboot
%attr(755,root,root) %{_sbindir}/runlevel
%attr(755,root,root) %{_sbindir}/shutdown
%attr(755,root,root) %{_sbindir}/start
%attr(755,root,root) %{_sbindir}/status
%attr(755,root,root) %{_sbindir}/stop
%attr(755,root,root) %{_sbindir}/telinit
%attr(755,root,root) %{_libdir}/libnih.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnih.so.0
%attr(755,root,root) %{_libdir}/libupstart.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libupstart.so.0
%{_mandir}/man8/*.8*
