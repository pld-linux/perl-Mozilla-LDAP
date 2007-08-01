#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
Summary:	PerLDAP - Mozilla::LDAP perl modules
Summary(pl.UTF-8):	PerLDAP - moduły perla Mozilla::LDAP
Name:		perl-Mozilla-LDAP
Version:	1.5.2
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Development/Languages/Perl
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/directory/perldap/releases/%{version}/src/perl-mozldap-%{version}.tar.gz
# Source0-md5:	1f7af40a8ca42f4a8b805942129915e0
URL:		http://www.mozilla.org/directory/perldap.html
BuildRequires:	mozldap-devel >= 6.0
BuildRequires:	nspr-devel >= 4.0
BuildRequires:	nss-devel >= 3.0
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
Requires:	mozldap >= 6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libldap60.so libprldap60.so libssldap60.so

%description
PerLDAP is a set of modules written in Perl and C that allow
developers to leverage their existing Perl knowledge to easily access
and manage LDAP-enabled directories. PerLDAP makes it very easy to
search, add, delete, and modify directory entries. For example, Perl
developers can easily build web applications to access information
stored in a directory or create directory sync tools between
directories and other services.

%description -l pl.UTF-8
PerLDAP to zestaw modułów napisanych w Perlu i C, pozwalających na
dostęp do katalogów LDAP i zarządzanie nimi z poziomu Perla. PerLDAP
ułatwia przeszukiwanie, usuwanie i modyfikowanie pozycji.

%prep
%setup -q -n perl-mozldap-%{version}

%{__sed} -i -e 's|/usr/bin/perl5|%{__perl}|' examples/*.pl

%build
export LDAPSDKDIR=/usr
export LDAPSDKINCDIR=/usr/include/mozldap
export LDAPSDKLIBDIR=%{_libdir}
export LDAPSDKSSL=Y
export LDAPPR=Y
export NSPRDIR=/usr
export NSPRINCDIR=/usr/include/nspr
export NSPRLIBDIR=%{_libdir}
export NSSDIR=/usr
export NSSLIBDIR=%{_libdir}
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \

# no option to pass libs to Makefile.PL, use LDLOADLIBS here
%{__make} \
	LDLOADLIBS="-lssldap60 -lprldap60 -lldap60 -lssl3 -lnss3 -lplc4 -lplds4 -lnspr4"
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -r examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Mozilla/LDAP/API/.packlist

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog CREDITS MPL-1.1.txt README RELEASE
%{perl_vendorarch}/Mozilla
%dir %{perl_vendorarch}/auto/Mozilla
%dir %{perl_vendorarch}/auto/Mozilla/LDAP
%dir %{perl_vendorarch}/auto/Mozilla/LDAP/API
%{perl_vendorarch}/auto/Mozilla/LDAP/API/autosplit.ix
%{perl_vendorarch}/auto/Mozilla/LDAP/API/API.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Mozilla/LDAP/API/API.so
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
