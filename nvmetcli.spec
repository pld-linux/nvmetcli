Summary:	Command line interface for the kernel NVMe nvmet
Summary(pl.UTF-8):	Interfejs linii poleceń do modułu jądra NVMe nvmet
Name:		nvmetcli
Version:	0.8
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	ftp://ftp.infradead.org/pub/nvmetcli/%{name}-%{version}.tar.gz
# Source0-md5:	52139449e3cbaa8b722333383d4b132e
URL:		http://git.infradead.org/users/hch/nvmetcli.git
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-units
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires:	python3-configshell-fb
Requires:	python3-kmod
Requires:	python3-six
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

%{__sed} -i -e '1s,/usr/bin/python,%{__python3},' nvmetcli

%build
%py3_build

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

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
%{py3_sitescriptdir}/nvmet
%{py3_sitescriptdir}/nvmetcli-%{version}-py*.egg-info
%dir %{_sysconfdir}/nvmet
%{systemdunitdir}/nvmet.service
