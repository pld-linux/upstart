# TODO:
# - userland headers needs to be fixed - inotify.h is missing
# - does it require gcc4?? __builtin_offsetof definition added for gcc3.3
# - it seems it requires some kernel-related definitions...
#
Summary:	Event-based init daemon
Summary(pl):	Oparty na zdarzeniach demon init
Name:		upstart
Version:	0.2.1
Release:	0.2
License:	GPL v2
Group:		Base
# Isn't there better download URL???
Source0:	http://people.ubuntu.com/~scott/software/upstart/%{name}-%{version}.tar.bz2
# Source0-md5:	67be7df5ed181713d638d18269d86e8f
Patch0:		%{name}-builtin_offsetof.patch
URL:		https://launchpad.net/products/upstart
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
# Really needed?
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gettext
BuildRequires:	glibc-headers >= 6:2.4.0
#Requires(post):	/sbin/ldconfig
#Requires(post):	/sbin/telinit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_sysconfdir		/etc/%{name}
%define		_libdir			/%{_lib}/%{name}
%define		_bindir			%{_prefix}/sbin
# this is to avoid ugly //sbin
%define		_sbindir		/sbin

%description
upstart is a replacement for the /sbin/init daemon which handles
starting of tasks and services during boot, stopping them during
shutdown and supervising them while the system is running.

%description -l pl
upstart jest zamiennikiem demona /sbin/init zajmuj�cym si�
uruchamianiem zada� i serwis�w podczas startu systemu, ich
zatrzymywaniem podczas wy��czania systemu, a tak�e nadzorowaniem ich
pracy.

%prep
%setup -q
# for gcc3.3 only:
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_sysconfdir}

#%{__make} install \
#	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
#if [ "$1" = 1 ]; then
#	%banner -e %{name} <<-EOF
#Remember to add init=%{_sbindir}/initng in your grub or lilo config to use initng.
#
#You should install 'initng-pld' for PLD Linux rc-scripts based scripts,
#or 'initng-initscripts' for the original distributed scripts.
#
#Happy testing.
#EOF
#fi
#
#/sbin/telinit u || :

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS TODO
#%dir %{_sysconfdir}
#%dir %{_libdir}
#%attr(755,root,root) /%{_lib}/libinitng.so.*.*.*
#%attr(755,root,root) %{_sbindir}/initng
#%{_mandir}/man8/initng.8*
