%define api_version 1.11.1
%define api_major_version 1.11

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake
Version:    %{api_version}
Release:    3
License:    GPLv2+ and GFDL and MIT 
Group:      Development/Tools
Source:     http://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Source1:    filter-provides-automake.sh
Source2:    filter-requires-automake.sh
Source3:    automake.man
Source4:    aclocal.man
Source5:    automake-rpmlintrc
URL:        http://sources.redhat.com/automake
Requires:   autoconf >= 2.62
Buildrequires:  autoconf >= 2.62
BuildArch:  noarch

%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles. If you install Automake, you will also need to install
GNU's Autoconf package.

%prep
%setup -q -n automake-%{version}

chmod +x %{SOURCE1}
chmod +x %{SOURCE2}

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
   --bindir=%{_bindir} --datadir=%{_datadir} --libdir=%{_libdir} \
   --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags}
mv -f NEWS NEWS_
iconv -f ISO_8859-15 -t UTF-8 NEWS_ -o NEWS

%install
rm -rf ${RPM_BUILD_ROOT}

%make_install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_mandir}/man1/automake.1
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_mandir}/man1/aclocal.1

# create this dir empty so we can own it
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/aclocal
rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}
%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS NEWS
%{_bindir}/*
%{_datadir}/automake-%{api_major_version}
%{_datadir}/aclocal-%{api_major_version}
%doc %{_mandir}/man1/*
%dir %{_datadir}/aclocal

