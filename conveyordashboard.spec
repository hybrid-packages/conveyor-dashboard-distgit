%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name conveyor-dashboard
%global mod_name conveyordashboard

Name:           conveyor-ui
Version:        XXX
Release:        XXX
Summary:        The UI component for the OpenStack conveyor service
Group:          Applications/Communications
License:        ASL 2.0
URL:            https://github.com/Hybrid-Cloud/%{pypi_name}
Source0:		https://github.com/Hybrid-Cloud/%{name}/%{name}-%{upstream_version}.tar.gz

BuildRequires:  gettext
BuildRequires:  openstack-dashboard
BuildRequires:  python-devel
# BuildRequires:  python-django-formtools
# BuildRequires:  python-django-nose
BuildRequires:  python-mock
BuildRequires:  python-mox3
BuildRequires:  python-conveyorclient
# BuildRequires:  python-oslo-config >= 2:3.14.0
BuildRequires:  python-pbr >= 1.6
BuildRequires:  python-setuptools
BuildRequires:  python-testtools
# BuildRequires:  python-yaql >= 1.1.0

Requires:       openstack-dashboard
Requires:       PyYAML >= 3.10
Requires:       python-babel >= 2.3.4
Requires:       python-django >= 1.8
Requires:       python-iso8601 >= 0.1.11
Requires:       python-conveyorclient
Requires:       python-six >= 1.9.0
BuildArch:      noarch

%description
Conveyor Dashboard
Sytem package - conveyor-dashboard
Python package - conveyor-dashboard
Conveyor Dashboard is an extension for OpenStack Dashboard that provides a UI
for Conveyor.

%package doc
Summary:        Documentation for OpenStack conveyor dashboard
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-reno

%description doc
Conveyor Dashboard is an extension for OpenStack Dashboard that provides a UI
for Conveyor.
This package contains the documentation.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

# Generate i18n files
pushd build/lib/%{mod_name}
django-admin compilemessages
popd

# generate html docs
# %{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
# Enable Horizon plugin for conveyor-dashboard
cp %{_builddir}/%{pypi_name}-%{upstream_version}/conveyordashboard/local/_50_conveyor.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;
find %{buildroot} -name djangojs.po -exec rm '{}' \;

# Find language files
%find_lang django --all-name

#%check
#export PYTHONPATH="%{_datadir}/openstack-dashboard:%{python2_sitearch}:%{python2_sitelib}:%{buildroot}%{python2_sitelib}"
#%{__python2} manage.py test conveyordashboard --settings=conveyordashboard.tests.settings

%post
%systemd_postun_with_restart httpd.service

%postun
%systemd_postun_with_restart httpd.service

%files -f django.lang
%license LICENSE
%doc README.md
%{python2_sitelib}/conveyordashboard
%{python2_sitelib}/conveyor_dashboard*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/*

%files doc
%license LICENSE
# %doc doc/build/html

%changelog