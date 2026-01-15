Name:           xdg-desktop-portal-luminous
Version:        0.1.13
Release:        1%{?dist}
Summary:        A wlroots-based xdg-desktop-portal implementation

License:        GPL-3.0-only
URL:            https://github.com/waycrate/xdg-desktop-portal-luminous
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  rust-packaging
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  systemd-rpm-macros

Requires:       xdg-desktop-portal
Requires:       pipewire

%description
Luminous is a portal frontend for wlroots compositors. It implements 
ScreenCast, ScreenShot, and RemoteDesktop portals using modern Wayland 
protocols.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

# --- FIX 1: Cleanup Meson's Misplaced Files ---
# Meson incorrectly installed the service to /usr/lib64/systemd/user.
# We delete it so it doesn't trigger "Installed (but unpackaged)" errors.
rm -rf %{buildroot}/usr/lib64/systemd

# --- FIX 2: Create Correct Service File Manually ---
# We write the service file to the correct standard location (/usr/lib/systemd/user).
install -d -m 0755 %{buildroot}%{_userunitdir}
cat <<EOF > %{buildroot}%{_userunitdir}/%{name}.service
[Unit]
Description=Portal service (Luminous implementation)
PartOf=graphical-session.target
After=graphical-session.target

[Service]
Type=dbus
BusName=org.freedesktop.impl.portal.desktop.luminous
ExecStart=%{_libexecdir}/%{name}
EOF

# Find and install the portal config file
install -d -m 0755 %{buildroot}%{_datadir}/xdg-desktop-portal/portals
find . -name "luminous.portal" -exec install -p -m 0644 {} %{buildroot}%{_datadir}/xdg-desktop-portal/portals/luminous.portal \;

%files
%license LICENSE
%doc README.md
%{_libexecdir}/%{name}
%{_datadir}/xdg-desktop-portal/portals/luminous.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.luminous.service
%{_userunitdir}/%{name}.service

%changelog
* Wed Jan 14 2026 Fedora Packager <packager@fedoraproject.org> - 0.1.11-1
- Initial release of 0.1.11
- Fixed systemd service installation paths
