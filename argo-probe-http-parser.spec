%define underscore() %(echo %1 | sed 's/-/_/g')

Summary:       ARGO probe that parses http response.
Name:          argo-probe-http-parser
Version:       0.3.2
Release:       1%{?dist}
Source0:       %{name}-%{version}.tar.gz
License:       ASL 2.0
Group:         Development/System
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix:        %{_prefix}
BuildArch:     noarch

BuildRequires: python3-devel

%if 0%{?el7}
Requires: python36-requests

%else
Requires:      python3-requests

%endif


%description
ARGO probe that parses http response.


%prep
%setup -q


%build
%{py3_build}


%install
%{py3_install "--record=INSTALLED_FILES" }


%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root)
%dir %{python3_sitelib}/%{underscore %{name}}/
%{python3_sitelib}/%{underscore %{name}}/*.py


%changelog
* Wed May 22 2024 Katarina Zailac <kzailac@srce.hr> - 0.3.2-1
- ARGO-4546 Prepare el9 build for argo-probe-http-parser probe
* Thu Mar 23 2023 Katarina Zailac <kzailac@srce.hr> - 0.3.1-1
- ARGO-4252 Fix formatting of check_http_parser probe
* Thu Sep 1 2022 Katarina Zailac <kzailac@srce.hr> - 0.3.0-1
- AO-651 Harmonize EGI probes
* Mon Jul 12 2021 Emir Imamagic <eimamagi@srce.hr> - 0.2.0-1
- ARGO-3216 Add parameter --case-sensitive
* Mon Jun 28 2021 Katarina Zailac <kzailac@srce.hr> - 0.1.0-1%{?dist}
- ARGO-3175 Change default returned messages for nagios-plugins-http-parser
- ARGO-3173 Add custom message for unknown status for nagios-plugins-http-parser probe
- ARGO-3149 Create probe that parses http response
