# TODO
# - 4 of 13 tests failed (3 with 'permission denied')
#
# Conditional build:
%bcond_with	statesave	# state-save experimental patch
%bcond_with	tests		# don't perform "make check"

Summary:	Event-based init daemon
Summary(pl.UTF-8):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	0.6.6
Release:	3
License:	GPL v2
Group:		Base
Source0:	http://upstart.ubuntu.com/download/0.6/%{name}-%{version}.tar.gz
# Source0-md5:	5a2e9962a4cea719fbe07c33e2591b06
URL:		http://upstart.ubuntu.com/
Patch0:		pldize.patch
# https://code.launchpad.net/~jajcus-jajcus/upstart/state-save-stable/+merge/27053/+preview-diff/+files/preview.diff
Patch1:		%{name}-state_save.patch
Source1:	start-ttys.conf
Source2:	tty.conf
Source3:	%{name}.sysconfig
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.2.16-1
BuildRequires:	expat-devel
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gettext >= 0.14.5
BuildRequires:	glibc-headers >= 6:2.4.0
BuildRequires:	libnih-devel >= 1.0.2
BuildRequires:	libtool >= 2:1.5.22
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.402
Requires:	dbus-libs >= 1.2.14-2
Requires:	filesystem >= 3.0-35
Suggests:	dbus
Suggests:	vim-syntax-upstart
Provides:	virtual(init-daemon)
Obsoletes:	virtual(init-daemon)
Conflicts:	dbus < 1.2.12-2
Conflicts:	upstart-SysVinit < 2.86-23.2
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
%{?with_statesave:%patch1 -p0}
cp -a %{SOURCE1} conf
cp -a %{SOURCE2} conf

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,/lib/init}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang upstart

cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

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

%triggerpostun -- upstart < 0.6.0
[ -f /proc/1/exe -a -d /proc/1/root ] && kill -TERM 1

%files -f upstart.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS TODO
/etc/dbus-1/system.d/Upstart.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/init/control-alt-delete.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/init/start-ttys.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/init/tty.conf
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
%dir /lib/init
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
