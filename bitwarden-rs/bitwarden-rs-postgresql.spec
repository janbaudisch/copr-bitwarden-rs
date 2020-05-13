%define debug_package %{nil}

Name: bitwarden-rs-postgresql
Version: 1.14.2
Release: 3%{?dist}
Summary: Unofficial Bitwarden compatible server written in Rust (PostgreSQL backend)
License: GPL-3.0-only
URL: https://github.com/dani-garcia/bitwarden_rs
Provides: bitwarden-rs = %{version}
Conflicts: bitwarden-rs-mysql
Conflicts: bitwarden-rs-sqlite
Source0: https://github.com/dani-garcia/bitwarden_rs/archive/%{version}.tar.gz
Source1: bitwarden-rs.service
BuildRequires: pkgconfig(libpq)
BuildRequires: pkgconfig(openssl)
BuildRequires: systemd
BuildRequires: /usr/bin/cc
Requires: bitwarden-rs-web

%description
A Bitwarden server API implementation written in Rust compatible with upstream Bitwarden clients.
This version uses PostgreSQL as its backend.

%prep
%setup -qn bitwarden_rs-%{version}
curl -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly

%build
source $HOME/.cargo/env
cargo build --features postgresql --release

%install
install -Dpm 755 target/release/bitwarden_rs %{buildroot}/usr/libexec/bitwarden-rs/bitwarden-rs
install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/bitwarden-rs.service
install -Dpm 644 .env.template %{buildroot}/etc/bitwarden-rs.env
install -d %{buildroot}/usr/libexec/bitwarden-rs/data

%files
%license LICENSE.txt
/usr/libexec/bitwarden-rs/bitwarden-rs
%{_unitdir}/bitwarden-rs.service
/etc/bitwarden-rs.env

%pre
groupadd --system bitwarden-rs || true
useradd -Mrg bitwarden-rs -d /usr/libexec/bitwarden-rs bitwarden-rs || true

%post
chown -R bitwarden-rs /usr/libexec/bitwarden-rs/data
