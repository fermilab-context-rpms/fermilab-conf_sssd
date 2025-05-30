Name:		fermilab-conf_sssd
Version:	1.1
Release:	2%{?dist}
Summary:	Configure SSSD to permit FNAL Kerberos authentication

Group:		Fermilab
License:	GPL
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_sssd

Source0:	%{name}.tar.xz

BuildArch:	noarch
Requires:	sssd sssd-krb5
Requires(post):	authselect coreutils util-linux-core

%if 0%{?rhel} < 10
Obsoletes:	fermilab-conf_kerberos-local-passwords
%endif

%description
The default configuration of Enterprise Linux is to require local passwords,
which may not be suitable for all situations.

This RPM will update the SSSD configuration to permit FNAL Kerberos
passwords to be used in addition to any local passwords.


%prep
%setup -q -n sssd_conf.d

%build


%install
%{__install} -D 20-service-settings.conf %{buildroot}/%{_sysconfdir}/sssd/conf.d/20-service-settings.conf
%{__install} -D 24-FNAL-domain-enable.conf %{buildroot}/%{_sysconfdir}/sssd/conf.d/24-FNAL-domain-enable.conf
%{__install} -D 25-FNAL-domain.conf %{buildroot}/%{_sysconfdir}/sssd/conf.d/25-FNAL-domain.conf

%post -p /bin/bash

%if 0%{?rhel} < 9 && 0%{?fedora} < 31
if [[ ! -e /%{_sysconfdir}/sssd/sssd.conf ]]; then
    touch /%{_sysconfdir}/sssd/sssd.conf
fi
if [[ -f /%{_sysconfdir}/sssd/sssd.conf ]]; then
    chown root:root /%{_sysconfdir}/sssd/sssd.conf
    chmod 600 /%{_sysconfdir}/sssd/sssd.conf
    if [[ ! -s /%{_sysconfdir}/sssd/sssd.conf ]]; then
        echo "[sssd]" > /%{_sysconfdir}/sssd/sssd.conf
    fi
fi
%endif

systemctl enable sssd.service
systemctl condrestart sssd.service

authselect current | grep -q sssd
if [[ $? -ne 0 ]]; then
  authselect select sssd
  if [[ $? -ne 0 ]]; then
      echo "" >&2
      echo "authselect select sssd : failed" >&2
      echo "" >&2
      echo "Please run manually" >&2
      echo "" >&2
      echo "authselect select sssd : failed" | logger -p auth.err
  else
      echo "authselect select sssd : complete" | logger -p auth.notice
  fi
fi

systemctl is-active sssd.service >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "" >&2
    echo "SSSD not running, you may need to run" >&2
    echo "systemctl start sssd.service" >&2
    echo "" >&2
    echo "sssd failed to start" | logger -p auth.err
fi


%files
%defattr(0644,root,root,0755)
%if 0%{?rhel} < 10
%config %attr(0600,root,root) %{_sysconfdir}/sssd/conf.d/*.conf
%else
%config %attr(0640,root,sssd) %{_sysconfdir}/sssd/conf.d/*.conf
%endif

%changelog
* Fri Apr 22 2022 Pat Riehecky <riehecky@fnal.gov> 1.1-2
- Per admin request, don't make the stub files, leave a note about how

* Wed Apr 13 2022 Pat Riehecky <riehecky@fnal.gov> 1.1-1.1
- Add more logging about state

* Wed Mar 16 2022 Pat Riehecky <riehecky@fnal.gov> 1.1-1
- Drop EL7 support

* Tue Dec 07 2021 Pat Riehecky <riehecky@fnal.gov> 1.0-9
- Prep for EL9

* Tue May 04 2021 Pat Riehecky <riehecky@fnal.gov> 1.0-8
- More clarity in augeas matches

* Tue Feb 16 2021 Pat Riehecky <riehecky@fnal.gov> 1.0-7
- SSSD seems to be more strict about where pwfield lives

* Wed Apr 22 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-6.1
- quietly Fix BZ1636002

* Tue Apr 21 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-6
- Primary servers are DNS SRV, fall back to hard coded

* Tue Apr 21 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-5.2
- Just let the krb_ccache fall through

* Mon Apr 20 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-5.1
- Fix dir typo

* Fri Apr 17 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-5
- Force authselect config on EL8+ when config status is messed up
- Better use of socket actived sssd settings

* Fri Mar 13 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-4
- Newest SSSD is more strict on config file syntax

* Mon Dec 16 2019 Pat Riehecky <riehecky@fnal.gov> 1.0-3.1
- Also provide fermilab-conf_kerberos-local-passwords

* Mon Dec 16 2019 Pat Riehecky <riehecky@fnal.gov> 1.0-3
- Better fall back behavior for EL7

* Thu Sep 19 2019 Pat Riehecky <riehecky@fnal.gov> 1.0-2
- Use socket services rather than explicit config

* Fri Jul 19 2019 Pat Riehecky <riehecky@fnal.gov> 1.0-1
- Initial build for EL7
