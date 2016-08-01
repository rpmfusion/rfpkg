%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global python2_version 2.6
%endif

%global   checkout f5465b851ad4a10fe4504a6f499409dd54b93c04

Name:           rfpkg
Summary:        RPM Fusion utility for working with dist-git
Version:        1.23.4
Release:        3%{?dist}
License:        GPLv2+
Group:          Applications/System
URL:            https://github.com/rpmfusion-infra/rfpkg
Source0:        https://github.com/rpmfusion-infra/rfpkg/archive/v%{version}.zip#/%{name}-%{version}.tar.gz

%{?python_provide:%python_provide python2-%{name}}
BuildArch:      noarch

BuildRequires:  python2-devel, python-setuptools, bash-completion

BuildRequires:  pyrpkg, fedora-cert
BuildRequires:  python-fedora, packagedb-cli > 2.2

Requires: bodhi-client
#We need rpmfusion-packager instead - but don't do circle dependency
#Requires: fedora-cert
Requires: koji
Requires: packagedb-cli > 2.2
Requires: pyrpkg >= 1.33
Requires: python-pycurl
Requires: redhat-rpm-config


%description
RPM Fusion utility for working with dist-git.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python2} setup.py build
%{__python2} src/rfpkg_man_page.py > rfpkg.1

%install
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

sed -e 's|^#!python|#!%{__python2}|g' -i $RPM_BUILD_ROOT%{_bindir}/rfpkg

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 0644 rfpkg.1 $RPM_BUILD_ROOT%{_mandir}/man1


%files
%{!?_licensedir:%global license %doc}
%doc README
%license COPYING
%{_bindir}/rfpkg
%{python2_sitelib}/rfpkg/
%{python2_sitelib}/rfpkg-%{version}-py%{python2_version}.egg-info/
%{_mandir}/man1/rfpkg.1*
%if 0%{?fedora}
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/rfpkg
%else
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/rfpkg
%endif
%dir %{_sysconfdir}/rpkg
%config(noreplace) %{_sysconfdir}/rpkg/rfpkg.conf


%changelog
* Mon Aug 01 2016 Sérgio Basto <sergio@serjux.com> - 1.23.4-3
-
  https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 04 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.23.4-2
- rebuilt

* Mon Jul 04 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.23.4-1
- Update to 1.23.4

* Fri Jul 01 2016 Nicolas Chauvet <nicolas.chauvet@kwizart.fr> - 1.23.3-1
- Update to 1.23.3
- Remove broken rfpkg-free and rfpkg-nonfree

* Sun Jun 19 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.23.2-1
- Update to 1.23.2

* Sat Jun 18 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.23.1-1
- Update to 1.23.1

* Fri Jun 17 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.23-1
- Rebase on top of fedpkg 1.23

* Fri Jun 17 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.21-1
- Update to 1.21

* Mon Nov 16 2015 Antonio Trande <sagitterATfedoraproject.org> 1.20-5.20151027git62a8b0
- Made 'rfpkg' free/nonfree scripts

* Mon Nov 09 2015 Antonio Trande <sagitterATfedoraproject.org> 1.20-4.20151027git62a8b0
- Added bash-completion as BR package

* Sun Nov 08 2015 Antonio Trande <sagitterATfedoraproject.org> 1.20-3.20151027git62a8b0
- All configuration files pushed in main package

* Fri Nov 06 2015 Antonio Trande <sagitterATfedoraproject.org> 1.20-2.20151027git62a8b0
- Cleanup of the EPEL5 tasks
- Fixed the installation of the script file for Bash

* Thu Nov 05 2015 Antonio Trande <sagitterATfedoraproject.org> 1.20-1.20151027git62a8b0
- Initial build

