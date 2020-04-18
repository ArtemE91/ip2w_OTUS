License:        BSD
Vendor:         Otus
Group:          PD01
URL:            http://otus.ru/lessons/3/
Source0:        otus-%{current_datetime}.tar.gz
BuildRoot:      %{_tmppath}/otus-%{current_datetime}
Name:           ip2w
Version:        0.0.1
Release:        1
BuildArch:      noarch
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires:	systemd, nginx, uwsgi, python3
Summary:  rpm package to serve ip to weather.


%description
Traing uwsgi daemon project. Upon request, IPv4 returns the current weather in the city to which ip belongs.
Git version: %{git_version} (branch: %{git_branch})

%define __etcdir    /usr/local/etc
%define __logdir    /val/log/ip2w
%define __bindir    /usr/local/ip2w
%define __systemddir	/usr/lib/systemd/system
%define __nginxconf /etc/nginx/conf.d

%prep
%setup -q -n otus-%{current_datetime}
%install
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}

%{__mkdir} -p %{buildroot}/%{__systemddir}
%{__install} -pD -m 644  %{name}.service %{buildroot}/%{__systemddir}/%{name}.service

%{__mkdir} -p %{buildroot}/%{__etcdir}
%{__install} -pD -m 644  %{name}.yml %{buildroot}/%{__etcdir}/%{name}.yml

%{__mkdir} -p %{buildroot}/%{__logdir}
%{__install} -pD -m 644  %{name}.log %{buildroot}/%{__logdir}/%{name}.log

%{__mkdir} -p %{buildroot}/%{__bindir}
%{__install} -pD -m 644  %{name}.py %{buildroot}/%{__bindir}/%{name}.py
%{__install} -pD -m 644  %{name}.uwsgi.ini %{buildroot}/%{__bindir}/%{name}.uwsgi.ini

%{__mkdir} -p %{buildroot}/%{__nginxconf}
%{__install} -pD -m 644  %{name}.nginx.conf %{buildroot}/%{__nginxconf}/%{name}.nginx.conf


%post
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%clean
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}


%files
%{__systemddir}/%{name}.service
%{__etcdir}/%{name}.yml
%{__logdir}/%{name}.log
%{__bindir}/%{name}.py
%{__bindir}/%{name}.uwsgi.ini
%{__nginxconf}/%{name}.nginx.conf

