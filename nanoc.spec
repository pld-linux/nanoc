Summary:	Static site compiler framework
Name:		nanoc
Version:	2.2.2
Release:	1
License:	Ruby's
Group:		Development/Languages
Source0:	http://gems.rubyforge.org/gems/%{name}-%{version}.gem
# Source0-md5:	42fdae4c3ad07727513937ffd3a86bad
URL:		http://nanoc.rubyforge.org
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	setup.rb = 3.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nanoc is a site compiler written in Ruby for building awesome web
sites.

%prep
%setup -q -c
tar xzf data.tar.gz
cp %{_datadir}/setup.rb .
cp %{_datadir}/setup.rb vendor/cri

%build
ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

rdoc --op rdoc lib
rdoc --ri --op ri lib

cd vendor/cri

ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

rdoc --op rdoc lib
rdoc --ri --op ri lib

cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_ridir}}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cd vendor/cri

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cd ../..

rm ri/created.rid
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc rdoc
%attr(755,root,root) %{_bindir}/nanoc
%{ruby_rubylibdir}/nanoc*
%{ruby_rubylibdir}/cri*
%{ruby_ridir}/*
