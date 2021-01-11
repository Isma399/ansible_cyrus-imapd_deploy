#%PAM-1.0
auth	   sufficient	pam_cas.so -simap://imap.{{ mail_domain }} -f/etc/pam_cas.conf
auth	   sufficient	pam_ldap.so 
account	   sufficient	pam_ldap.so
auth       required     pam_nologin.so
auth       include      password-auth
account    include      password-auth
session    include      password-auth
