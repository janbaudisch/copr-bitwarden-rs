Name: bitwarden-rs-web-bin
Version: 2.13.2b
Release: 1%{?dist}
Summary: Bitwarden web vault with patches for bitwarden-rs (upstream build)
License: GPL-3.0-only
URL: https://github.com/dani-garcia/bw_web_builds
Provides: bitwarden-rs-web = %{version}
Conflicts: bitwarden-rs-web
Source0: https://github.com/dani-garcia/bw_web_builds/releases/download/v%{version}/bw_web_v%{version}.tar.gz

%description
This is the Bitwarden web vault with patches applied to make it work with bitwarden-rs.
Upstream built, just packaged.

%prep

%install
tar xf %{SOURCE0}
install -d %{buildroot}/usr/libexec/bitwarden-rs
mv web-vault %{buildroot}/usr/libexec/bitwarden-rs/web-vault

%files
/usr/libexec/bitwarden-rs/web-vault
