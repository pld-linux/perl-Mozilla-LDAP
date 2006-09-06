#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
Summary:	PerLDAP - Mozilla::LDAP perl modules
Summary(pl):	PerLDAP - modu³y perla Mozilla::LDAP
Name:		perl-Mozilla-LDAP
Version:	1.4.1
Release:	13
License:	MPL 1.1
Group:		Development/Languages/Perl
Source0:	http://ftp.mozilla.org/pub/mozilla.org/directory/perldap/perldap-%{version}.tar.gz
# Source0-md5:	39a784c94f6fbed4682f681cd2f183fa
URL:		http://www.mozilla.org/directory/perldap.html
BuildRequires:	mozldap-devel >= 5.17
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
Requires:	mozldap >= 5.17
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PerLDAP is a set of modules written in Perl and C that allow
developers to leverage their existing Perl knowledge to easily access
and manage LDAP-enabled directories. PerLDAP makes it very easy to
search, add, delete, and modify directory entries. For example, Perl
developers can easily build web applications to access information
stored in a directory or create directory sync tools between
directories and other services.

%description -l pl
PerLDAP to zestaw modu³ów napisanych w Perlu i C, pozwalaj±cych na
dostêp do katalogów LDAP i zarz±dzanie nimi z poziomu Perla. PerLDAP
u³atwia przeszukiwanie, usuwanie i modyfikowanie pozycji.

%prep
%setup -q -n perldap-%{version}

%{__sed} -i -e 's@"lib"@"%{_lib}"@' Makefile.PL
%{__sed} -i -e 's|/usr/bin/perl5|%{__perl}|' examples/*.pl
rm -rf examples/CVS

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	<<EOF
%{_prefix}
yes
yes
-lldap50 -lssldap50 -lprldap50 -lssl3 -lpthread
EOF

%{__make} \
	OPTIMIZE="%{rpmcflags} -I/usr/include/mozldap"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -r examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
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
