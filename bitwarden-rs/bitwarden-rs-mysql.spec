%define debug_package %{nil}

Name: bitwarden-rs-mysql
Version: 1.19.0
Release: 1%{?dist}
Summary: Unofficial Bitwarden compatible server written in Rust (MySQL backend)
License: GPL-3.0-only
URL: https://github.com/dani-garcia/bitwarden_rs
Provides: bitwarden-rs = %{version}
Conflicts: bitwarden-rs-postgresql
Conflicts: bitwarden-rs-sqlite
Source0: https://github.com/dani-garcia/bitwarden_rs/archive/%{version}.tar.gz
Source1: bitwarden-rs.service
Patch0: config.patch
BuildRequires: pkgconfig(libmariadb)
BuildRequires: pkgconfig(openssl)
BuildRequires: systemd
BuildRequires: /usr/bin/cc
Requires: bitwarden-rs-web

%description
A Bitwarden server API implementation written in Rust compatible with upstream Bitwarden clients.
This version uses MySQL as its backend.

%prep
%setup -qn bitwarden_rs-%{version}
%patch0 -p1
curl -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain $(cat rust-toolchain)

%build
source $HOME/.cargo/env
cargo build --features mysql --release

%install
install -Dpm 755 target/release/bitwarden_rs %{buildroot}%{_bindir}/bitwarden-rs
install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/bitwarden-rs.service
cp %{buildroot}%{_unitdir}/bitwarden-rs.service %{buildroot}%{_unitdir}/bitwarden-rs-waitformariadb.service
cp %{buildroot}%{_unitdir}/bitwarden-rs.service %{buildroot}%{_unitdir}/bitwarden-rs-waitformysqld.service
sed -i "s/After=network.target/After=network.target mariadb.service/" %{buildroot}%{_unitdir}/bitwarden-rs-waitformariadb.service
sed -i "s/After=network.target/After=network.target mysqld.service/" %{buildroot}%{_unitdir}/bitwarden-rs-waitformysqld.service
install -Dpm 644 .env.template %{buildroot}%{_sysconfdir}/bitwarden-rs/bitwarden-rs.env

%files
%license LICENSE.txt
%{_bindir}/bitwarden-rs
%{_unitdir}/bitwarden-rs.service
%{_unitdir}/bitwarden-rs-waitformariadb.service
%{_unitdir}/bitwarden-rs-waitformysqld.service
%config(noreplace) %{_sysconfdir}/bitwarden-rs/bitwarden-rs.env

%pre
getent group bitwarden-rs > /dev/null || groupadd --system bitwarden-rs
getent passwd bitwarden-rs > /dev/null || useradd -Mrg bitwarden-rs -d /usr/share/bitwarden-rs bitwarden-rs

%post
mkdir -p /usr/share/bitwarden-rs/data
chown -R bitwarden-rs /usr/share/bitwarden-rs/data
