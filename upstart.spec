# TODO:
# - userland headers needs to be fixed - inotify.h is missing
# - it seems it requires some kernel-related definitions...
#
Summary:	Event-based init daemon
Summary(pl.UTF-8):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	0.3.9
Release:	0.1
License:	GPL v2
Group:		Base
Source0:	http://upstart.ubuntu.com/download/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	794208083d405ece123ad59a02f3e233
URL:		https://launchpad.net/upstart
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	libtool >= 2:1.5.22
BuildRequires:	gettext >= 0.14.5
BuildRequires:	gcc >= 5:4.0
BuildRequires:	glibc-headers >= 6:2.4.0
Provides:	initscripts
Obsoletes:	initscripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir			/%{_lib}/
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

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang upstart

%clean
rm -rf $RPM_BUILD_ROOT

%files -f upstart.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS TODO
%dir %{_sysconfdir}/upstart
%dir %{_sysconfdir}/upstart/event.d
%{_sysconfdir}/upstart/event.d/logd
%dir %{_libdir}/upstart
%attr(755,root,root) %{_libdir}/upstart/*.so
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
