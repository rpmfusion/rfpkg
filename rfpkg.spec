%define compdir %(pkg-config --variable=completionsdir bash-completion)
%if "%{compdir}" == ""
%define compdir "/etc/bash_completion.d"
%endif

Name:           rfpkg
Version:        1.25.6
Release:        5%{?dist}
Summary:        RPM Fusion utility for working with dist-git
License:        GPLv2+
Group:          Applications/System
URL:            https://github.com/rpmfusion-infra/rfpkg
Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         py3.patch
Patch1:         koji_destname.patch

BuildArch:      noarch

# fedpkg command switched to python3 on Fedora 30 and RHEL > 7:
%if 0%{?fedora} > 29 || 0%{?rhel} > 7
%bcond_with python2
%else
%bcond_without python2
%endif

BuildRequires:  bash-completion
BuildRequires:  git

Requires:       bodhi-client
Requires:       redhat-rpm-config
Requires:       koji

%if %{with python2}
# This package redefines __python and can use the python_ macros
%global __python %{__python2}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  pkgconfig
# We br these things for man page generation due to imports
BuildRequires:  rpmfusion-cert
BuildRequires:  packagedb-cli > 2.2
BuildRequires:  pyrpkg >= 1.44
# For testing
BuildRequires:  python-nose
BuildRequires:  python-mock

Requires:       pyrpkg >= 1.45
Requires:       python-pycurl
Requires:       python-fedora
Requires:       rpmfusion-cert
Requires:       rpmfusion-packager >= 0.6.1
Requires:       packagedb-cli > 2.2

%else  # python3
# This package redefines __python and can use the python_ macros
%global __python %{__python3}

BuildRequires:  python3-devel
BuildRequires:  python3-future
BuildRequires:  python3-setuptools
BuildRequires:  pkgconfig

# We br these things for man page generation due to imports
BuildRequires:  python3-rpmfusion-cert
BuildRequires:  rfpkgdb-cli
BuildRequires:  python3-rpkg

# For testing
BuildRequires:  python3-nose
BuildRequires:  python3-mock

Requires:       python3-rpkg
Requires:       redhat-rpm-config
Requires:       python3-pycurl
Requires:       python3-fedora
Requires:       python3-future
Requires:       python3-rpmfusion-cert
Requires:       rpmfusion-packager >= 0.6.3-2
Requires:       bodhi-client
Requires:       rfpkgdb-cli
%endif

%description
RPM Fusion utility for working with dist-git.

%prep
%setup -q
%if ! %{with python2}
%patch0 -p1
%endif
%patch1 -p1

%build
%if %{with python2}
%py2_build
%{__python2} src/rfpkg_man_page.py > rfpkg.1
%else
%py3_build
%{__python3} src/rfpkg_man_page.py > rfpkg.1
%endif

%install
%if %{with python2}
%py2_install

sed -e 's|^#!python|#!%{__python2}|g' -i $RPM_BUILD_ROOT%{_bindir}/rfpkg
chmod a+x $RPM_BUILD_ROOT%{python2_sitelib}/rfpkg/__main__.py

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 0644 rfpkg.1 $RPM_BUILD_ROOT%{_mandir}/man1
%if 0%{?rhel} && 0%{?rhel} == 7
# The completion file must be named similarly to the command.
mv $RPM_BUILD_ROOT%{compdir}/rfpkg.bash $RPM_BUILD_ROOT%{compdir}/rfpkg
%endif
%else
%py3_install

sed -e 's|^#!python|#!%{__python3}|g' -i $RPM_BUILD_ROOT%{_bindir}/rfpkg
sed -e 's|^#!/usr/bin/python2|#!%{__python3}|g' -i $RPM_BUILD_ROOT%{python3_sitelib}/rfpkg/__main__.py
chmod a+x $RPM_BUILD_ROOT%{python3_sitelib}/rfpkg/__main__.py

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 0644 rfpkg.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif


%files
%doc README
%license COPYING
%{_bindir}/rfpkg
%if %{with python2}
%{python2_sitelib}/rfpkg/
%{python2_sitelib}/rfpkg-%{version}-py%{python2_version}.egg-info/
%else
%{python3_sitelib}/rfpkg/
%{python3_sitelib}/rfpkg-%{version}-py%{python3_version}.egg-info/
%endif
%{_mandir}/man1/rfpkg.1*
%(dirname %{compdir})
%dir %{_sysconfdir}/rpkg
%config(noreplace) %{_sysconfdir}/rpkg/rfpkg.conf
# zsh completion
%{_datadir}/zsh/site-functions/_%{name}


%changelog
* Sat Aug 24 2019 Leigh Scott <leigh123linux@gmail.com> - 1.25.6-5
- Rebuild for python-3.8

* Fri Mar 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.25.6-4
- Fix --dist/--release option for 'master' %dist detection

* Tue Mar 26 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.25.6-3
- Fix python2 shebang in python3 build

* Tue Mar 26 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.25.6-2
- Switch to python3 for f30

* Mon Sep 03 2018 Sérgio Basto <sergio@serjux.com> - 1.25.6-1
- Update to 1.25.6 Fix new warnings of rpkg modules are deprecated

* Tue Jul 24 2018 Sérgio Basto <sergio@serjux.com> - 1.25.5-1
- Update to 1.25.5 fix kojiprofiles

* Mon Jul 23 2018 Sérgio Basto <sergio@serjux.com> - 1.25.4-1
- Update to 1.25.4 use kojiprofile and https for anongiturl

* Wed Feb 07 2018 Sérgio Basto <sergio@serjux.com> - 1.25.3-1
- Update to 1.25.3, need rpmfusion-packager 0.6.1
- Arrange some items
- Delete obsolete hack

* Thu Oct 12 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.25.2-1
- Update to 1.25.2

* Fri Aug 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.25.1-3
- Fix python-rpkg issue (rfbz #4638)

* Mon Dec 12 2016 leigh scott <leigh123linux@googlemail.com> - 1.25.1-2
- Fix realms error

* Wed Sep 14 2016 Sérgio Basto <sergio@serjux.com> - 1.25.1-1
- Update to 1.25.1, force use rpmfusion-packager >= 0.5.2
- Fix rfpkg srpm in git master.

* Fri Sep 09 2016 Miro Hrončok <mhroncok@redhat.com> - 1.25.0-1
- Update to 1.25.0

* Fri Aug 19 2016 Antonio Trande <sagitterATfedoraproject.org> 1.24.0-2
- Fix Python shebang

* Fri Aug 05 2016 Nicolas Chauvet <nicolas.chauvet@kwizart.fr> - 1.24.0-1
- Update to 1.24.0

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

