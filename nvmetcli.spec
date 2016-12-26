Summary:	Command line interface for the kernel NVMe nvmet
Summary(pl.UTF-8):	Interfejs linii poleceń do modułu jądra NVMe nvmet
Name:		nvmetcli
Version:	0.2
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	ftp://ftp.infradead.org/pub/nvmetcli/%{name}-%{version}.tar.gz
# Source0-md5:	f7e82fa86001d5caaafffb3eed2cf798
URL:		http://git.infradead.org/users/hch/nvmetcli.git
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpmbuild(macros) >= 1.704
BuildRequires:	systemd-units
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires:	python-configshell
Requires:	python-kmod
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the command line interface to the NVMe over
Fabrics nvmet in the Linux kernel. It allows configuring the nvmet
interactively as well as saving/restoring the configuration to/from a
JSON file.

%description -l pl.UTF-8
Ten pakiet zawiera interfejs linii poleceń do modułu jądra Linuksa
nvmet (NVMe over Fabrics). Pozwala na interaktywną konfigurację
nvmet oraz zapis/odczyt konfiguracji z/do pliku JSON.

%prep
%setup -q

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT

%py_install

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/nvmet,%{systemdunitdir}}
cp -p nvmetcli $RPM_BUILD_ROOT%{_sbindir}/nvmetcli
cp -p nvmet.service $RPM_BUILD_ROOT%{systemdunitdir}/nvmet.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post nvmet.service

%preun
%systemd_preun nvmet.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/nvmetcli
%{py_sitescriptdir}
%dir %{_sysconfdir}/nvmet
%{systemdunitdir}/nvmet.service
