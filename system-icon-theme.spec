Summary: System icon theme
Name: system-icon-theme
Version: 6.0.0
Release: 2%{?dist}
BuildArch: noarch
License: GPLv2+
Group: User Interface/Desktops
# There is no upstream
Source0: %{name}-%{version}.tar.bz2
URL: http://www.redhat.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: perl(XML::Parser)
BuildRequires: intltool
Requires: gnome-themes

Obsoletes: fedora-icon-theme < %{version}

%description
This package contains the system icon theme.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# We provide the redhat files in pixmaps for backward compat,
# and so they're available for all themes.
# If we didn't care about backward compat, then hicolor would
# be better than pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
(cd $RPM_BUILD_ROOT%{_datadir}/pixmaps;
   for icon in ../icons/System/48x48/apps/{redhat-,temp-home}*.png; do
       ln -s $icon .
   done
)

# These are empty
rm -f ChangeLog NEWS README

# The upstream packages may gain po files at some point in the near future
%find_lang %{name} || touch %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/System
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache -f --quiet %{_datadir}/icons/System || :
fi

%postun
touch --no-create %{_datadir}/icons/System
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache -f --quiet %{_datadir}/icons/System || :
fi

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING
%{_datadir}/icons/System
%{_datadir}/pixmaps/*.png

%changelog
* Tue May 04 2010 Ray Strode <rstrode@redhat.com> 6.0.0-2
- Add Obsoletes for fedora-icon-theme to ease upgrade pain

* Tue May 04 2010 Ray Strode <rstrode@redhat.com> 6.0.0-1
- Add system icon theme package
