Name:           rfpkg
Version:        1.27.4
Release:        3%{?dist}
Summary:        RPM Fusion utility for working with dist-git
License:        GPLv2+
Group:          Applications/System
URL:            https://github.com/rpmfusion-infra/rfpkg
Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  python-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpkg
BuildRequires:  python3-six
# We br these things for man page generation due to imports
BuildRequires:  python3-rpmfusion-cert
BuildRequires:  rfpkgdb-cli
# For testing
BuildRequires:  python3-pytest
BuildRequires:  python3-distro
#BuildRequires:  python3-bugzilla
BuildRequires:  python3-freezegun
#BuildRequires:  python3-bodhi-client

Requires:       python3-rpkg
Requires:       python3-pycurl
Requires:       python3-rpmfusion-cert
Requires:       rfpkgdb-cli

# python3-rpkg already requires
# mock
# redhat-rpm-config
# rpm-build
# rpmlint
Requires:       git-core
Requires:       koji
Recommends:     rpmdevtools
Recommends:     mock-rpmfusion-free
Recommends:     mock-rpmfusion-nonfree

%description
RPM Fusion utility for working with dist-git.

%prep
%autosetup -p1

%build
%py3_build
%{__python3} doc/rfpkg_man_page.py > rfpkg.1


%install
%py3_install
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 rfpkg.1 %{buildroot}%{_mandir}/man1


%check
%pytest


%files
%doc README
%license COPYING
%config(noreplace) %{_sysconfdir}/rpkg/rfpkg.conf
%{_bindir}/rfpkg
%{_mandir}/man1/rfpkg.1*
%{python3_sitelib}/rfpkg/
%{python3_sitelib}/rfpkg-%{version}-py%{python3_version}.egg-info/
%bash_completions_dir/rfpkg.bash
# zsh completion
%zsh_completions_dir/_%{name}


%changelog
* Fri Jan 31 2025 Sérgio Basto <sergio@serjux.com> - 1.27.4-3
- Use recommends instead suggests for mock-rpmfusion configurations and rpmdevtools
- Drop support to el7 and python2

* Thu Jun 13 2024 Leigh Scott <leigh123linux@gmail.com> - 1.27.4-2
- Rebuilt for Python 3.13

* Mon Apr 08 2024 Sérgio Basto <sergio@serjux.com> - 1.27.4-1
- Update rfpkg to 1.27.4

* Fri Feb 02 2024 Nicolas Chauvet <kwizart@gmail.com> - 1.27.3-1
- Update to 1.27.3

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 1.27.2-2
- Rebuilt for Python 3.12

* Mon Dec 19 2022 Sérgio Basto <sergio@serjux.com> - 1.27.2-1
- Update rfpkg to 1.27.2

* Sun Oct 02 2022 Sérgio Basto <sergio@serjux.com> - 1.27.1-2
- Use unittest.mock on Python 3 and remove python3-mock dependency, to allow
  build on el9

* Fri Sep 09 2022 Sérgio Basto <sergio@serjux.com> - 1.27.1-1
- Update rfpkg to 1.27.1
- tag has moved to a new commit

* Fri Sep 09 2022 Leigh Scott <leigh123linux@gmail.com> - 1.27.0-7
- Fix for rpkg-1.65 change

* Tue Sep 06 2022 Sérgio Basto <sergio@serjux.com> - 1.27.0-6
- Disable multilibs builds on el8, 9 and 9-next

* Sat Jun 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.27.0-5
- Rebuilt for Python 3.11

* Tue May 24 2022 Sérgio Basto <sergio@serjux.com> - 1.27.0-4
- now that is add the patch to fix to download of old sources with md5 hash

* Tue Feb 15 2022 Sérgio Basto <sergio@serjux.com> - 1.27.0-3
- add an fix to download of old sources with md5 hash

* Sat Feb 12 2022 Sérgio Basto <sergio@serjux.com> - 1.27.0-2
- update target of 2 packages

* Sat Oct 23 2021 Sérgio Basto <sergio@serjux.com> - 1.27.0-1
- Update to 1.27.0

* Tue Jun 15 2021 Leigh Scott <leigh123linux@gmail.com> - 1.26.3-6
- Rebuild for python-3.10

* Sun Nov 29 2020 Sérgio Basto <sergio@serjux.com> - 1.26.3-5
- Requires and BuildRequires review

* Wed Sep 16 2020 Sérgio Basto <sergio@serjux.com> - 1.26.3-4
- Fix (#5756) and python3 -m nose

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 1.26.3-3
- Rebuild for python-3.9

* Wed May 27 2020 Sérgio Basto <sergio@serjux.com> - 1.26.3-2
- Add zsnes, gens and dega-sdl to multilibs

* Sat Mar 14 2020 Sérgio Basto <sergio@serjux.com> - 1.26.3-1
- Update to 1.26.3

* Tue Nov 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.26.2-3
- Fix F32 issue

* Sat Oct 12 2019 Sérgio Basto <sergio@serjux.com> - 1.26.2-2
- Fixup buildrequires and use correct python macros

* Thu Sep 26 2019 Sérgio Basto <sergio@serjux.com> - 1.26.2-1
- New version with more fixes on multilib builds and python2

* Tue Sep 24 2019 Sérgio Basto <sergio@serjux.com> - 1.26.1-1
- Bug fix (rfpkg new-sources)

* Tue Sep 24 2019 Sérgio Basto <sergio@serjux.com> - 1.26.0-1
- Update to 1.26.0
- Sync with fedpkg 1.37

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

