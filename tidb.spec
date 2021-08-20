Name:           tidb
Version:        4.0.14
Release:        1
Summary:        TiDB is a distributed NewSQL database compatible with MySQL protocol

License:        QL and STRUTIL
URL:            https://github.com/pingcap/tidb
Source0:        https://github.com/pingcap/tidb/archive/refs/tags/v4.0.14.tar.gz
Source1:        tidb-server.service
Source2:        tidb-server.toml
#Go mod for non-extranet environments
Source3:        vendor.tar.gz
Patch0:         Set-GOFLAG-to-go-mod-vendor.patch
BuildRequires:  golang >= 1.10.0
Requires(pre):  shadow-utils
Requires(post): systemd

%description
TiDB is a distributed NewSQL database compatible with MySQL protocol

%prep
%autosetup -p1
tar xvf %{SOURCE3} -C .

%build
%make_build

%install
mkdir -p %{buildroot}/var/log/tidb

install -D -p -m 755 bin/tidb-server  %{buildroot}%{_bindir}/tidb-server

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/tidb-server <<EOF
OPTIONS="-config /etc/tidb/tidb-server.toml"
EOF
mkdir -p %{buildroot}%{_sysconfdir}/tidb
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/tidb

mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE1} %{buildroot}%{_unitdir}

%files
%{_bindir}/tidb-server
%{_unitdir}/tidb-server.service
%config(noreplace) %{_sysconfdir}/tidb/tidb-server.toml
%config(noreplace) %{_sysconfdir}/sysconfig/tidb-server
%dir %{_sysconfdir}/tidb
%dir %attr(0755, mysql, mysql) %{_localstatedir}/log/tidb
%doc README.md
%license LICENSE

%changelog
* Fri Aug 20 2021 huanghaitao <huanghaitao8@huawei.com>
- Package init