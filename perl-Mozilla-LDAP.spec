%include	/usr/lib/rpm/macros.perl
Summary:	PerLDAP - Mozilla::LDAP perl modules
Summary(pl):	PerLDAP - modu³y perla Mozilla::LDAP
Name:		perl-Mozilla-LDAP
Version:	1.4.1
Release:	1
License:	MPL
Group:		Development/Languages/Perl
Group(de):	Entwicklung/Sprachen/Perl
Group(pl):	Programowanie/Jêzyki/Perl
Source0:	ftp://ftp.mozilla.org/pub/directory/perldap/perldap-%{version}.tar.gz
BuildRequires:	rpm-perlprov >= 3.0.3-16
BuildRequires:	mozilla-embedded-devel
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

%build
perl Makefile.PL <<EOF
/usr/X11R6
yes
no
-L/usr/X11R6/lib -lldap40 -llber40
EOF

%{__make} OPTIMIZE="%{rpmcflags} -I/usr/X11R6/include/mozilla/ldap"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

(cd examples
for f in *.pl ; do
	sed -e 's@/usr/bin/perl5@/usr/bin/perl@' $f \
		> $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/$f
done
)

gzip -9nf ChangeLog CREDITS MPL-1.1.txt README RELEASE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%{perl_sitearch}/Mozilla
%dir %{perl_sitearch}/auto/Mozilla
%dir %{perl_sitearch}/auto/Mozilla/LDAP
%dir %{perl_sitearch}/auto/Mozilla/LDAP/API
%{perl_sitearch}/auto/Mozilla/LDAP/API/autosplit.ix
%{perl_sitearch}/auto/Mozilla/LDAP/API/API.bs
%attr(755,root,root) %{perl_sitearch}/auto/Mozilla/LDAP/API/API.so
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
