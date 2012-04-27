#
# TODO:
#	- some tests still fail on builders
#
# Conditional build:
%bcond_with	tests		# perform "make check"

Summary:	Event-based init daemon
Summary(hu.UTF-8):	Esemény-vezérelt init démon
Summary(pl.UTF-8):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	1.3
Release:	7
License:	GPL v2
Group:		Base
Source0:	http://launchpad.net/upstart/1.x/1.3/+download/%{name}-%{version}.tar.gz
# Source0-md5:	7820797b64878c27115fff6a7398a6a9
URL:		http://upstart.at/
Patch0:		pldize.patch
Patch1:		%{name}-tests.patch
Source1:	start-ttys.conf
Source2:	tty.conf
Source3:	%{name}.sysconfig
Source4:	sysvinit.logrotate
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.2.16-1
BuildRequires:	expat-devel
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gettext >= 0.14.5
BuildRequires:	glibc-headers >= 6:2.4.0
BuildRequires:	libnih-devel >= 1.0.3
BuildRequires:	libtool >= 2:1.5.22
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.615
BuildRequires:	udev-devel >= 146
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	SysVinit-tools
Requires:	dbus-libs >= 1.2.14-2
Requires:	filesystem >= 4.0
Suggests:	dbus
Suggests:	vim-syntax-upstart
Provides:	group(utmp)
Provides:	virtual(init-daemon)
Obsoletes:	virtual(init-daemon)
Conflicts:	dbus < 1.2.12-2
Conflicts:	upstart-SysVinit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
upstart is a replacement for the /sbin/init daemon which handles
starting of tasks and services during boot, stopping them during
shutdown and supervising them while the system is running.

%description  -l hu.UTF-8
upstart az /sbin/init helyére pályázik. Az upstart kezelni tudja
feladatok és szolgáltatások indítását boot-kor, leállítását a gép
leállításakor és menedzselni, amíg a rendszer fut.

%description -l pl.UTF-8
upstart jest zamiennikiem demona /sbin/init zajmującym się
uruchamianiem zadań i usług podczas startu systemu, ich zatrzymywaniem
podczas wyłączania systemu, a także nadzorowaniem ich pracy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
cp -p %{SOURCE1} conf
cp -p %{SOURCE2} conf

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%{?with_tests:TERM=linux %{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,sysconfig},/lib/init,/var/{run,log}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang upstart

cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT%{_sysconfdir}
cp -a %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit
> $RPM_BUILD_ROOT/var/run/initrunlvl
> $RPM_BUILD_ROOT%{_sysconfdir}/ioctl.save
> $RPM_BUILD_ROOT/var/log/faillog
> $RPM_BUILD_ROOT/var/log/lastlog
> $RPM_BUILD_ROOT/var/log/wtmpx
> $RPM_BUILD_ROOT/var/log/btmpx

# no -devel
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.{la,so}
rm -rf $RPM_BUILD_ROOT%{_aclocaldir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 22 utmp

%post
/sbin/ldconfig

touch %{_sysconfdir}/ioctl.save /var/log/{{fail,last}log,btmpx}
chmod 000 %{_sysconfdir}/ioctl.save /var/log/{fail,last}log
chown root:root %{_sysconfdir}/ioctl.save /var/log/faillog
chown root:utmp /var/log/lastlog
chmod 600 %{_sysconfdir}/ioctl.save
chmod 640 /var/log/faillog
chmod 660 /var/log/lastlog
chmod 640 /var/log/btmpx

/sbin/telinit u || :

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%groupremove utmp
fi

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/init/upstart-socket-bridge.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/init/upstart-udev-bridge.conf
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
%attr(755,root,root) %{_sbindir}/upstart-socket-bridge
%attr(755,root,root) %{_sbindir}/upstart-udev-bridge
%attr(755,root,root) %{_bindir}/init-checkconf
%attr(755,root,root) %{_bindir}/initctl2dot
%dir /lib/init
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*

%attr(640,root,root) /etc/logrotate.d/sysvinit
%ghost %{_sysconfdir}/initrunlvl
%ghost /var/run/initrunlvl
%attr(600,root,root) %ghost %{_sysconfdir}/ioctl.save
%attr(640,root,root) %ghost /var/log/faillog
%attr(660,root,utmp) %ghost /var/log/lastlog
%attr(664,root,utmp) %ghost /var/log/wtmpx
%attr(640,root,root) %ghost /var/log/btmpx
