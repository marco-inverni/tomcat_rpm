# Apache Tomcat shared-software RPM for Oracle Linux 10.x.
# Tomcat version comes ONLY from the approved release manifest at build time.
# Override on rpmbuild CLI: --define 'tomcat_version 9.0.123'
%{!?tomcat_version:%{error:Pass --define 'tomcat_version X.Y.Z' from the approved release manifest}}

Name:           apache-tomcat9-custom
Version:        %{tomcat_version}
Release:        1%{?dist}
Summary:        Shared Apache Tomcat 9 foundation (independent CATALINA_BASE instances)
License:        Apache-2.0
URL:            https://tomcat.apache.org/
Source0:        apache-tomcat-%{version}.tar.gz
BuildArch:      noarch
# Do not autodetect Java requirements or install a JVM through DNF.
AutoReqProv:    no
Requires:       /bin/sh

%description
Shared read-only Apache Tomcat 9 binary distribution for Oracle Linux 10.
Runtime configuration, deployed applications and writable state must live in
independent CATALINA_BASE trees managed outside this RPM. Java is not included
and is intentionally NOT an RPM dependency; runtime administrators must provide
compatible Java separately. SELinux policies, systemd units, and instance
creation are delivered in Macro Task 5, not this foundational package.

%prep
%setup -q -n apache-tomcat-%{version}

%build
# Upstream's official precompiled binary distribution: no Java build.

%install
set -eu
home="%{buildroot}%{_datadir}/apache-tomcat9-custom"
install -d -m 0755 "$home/bin" "$home/lib" "$home/conf"

# Unix launch scripts and compiled Java libraries, no Windows native binaries,
# no sample applications and no optional Tomcat Native source distribution.
for f in bin/*.sh; do
  [ -f "$f" ] || continue
  install -m 0755 "$f" "$home/bin/"
done
for f in bin/*.jar lib/*.jar; do
  [ -f "$f" ] || continue
  case "$f" in
    bin/*) install -m 0644 "$f" "$home/bin/" ;;
    lib/*) install -m 0644 "$f" "$home/lib/" ;;
  esac
done
# This is a root-owned *template*, NOT live application configuration.
cp -a conf/. "$home/conf/"
find "$home/conf" -type d -exec chmod 0755 '{}' +
find "$home/conf" -type f -exec chmod 0644 '{}' +

# Sanity-check minimum files required by a future CATALINA_BASE initializer.
test -s "$home/bin/catalina.sh"
test -s "$home/bin/bootstrap.jar"
test -s "$home/bin/tomcat-juli.jar"
test -s "$home/lib/catalina.jar"
test -s "$home/conf/server.xml"
test -s "$home/conf/web.xml"

%files
%license LICENSE NOTICE
%doc RUNNING.txt RELEASE-NOTES
%{_datadir}/apache-tomcat9-custom
