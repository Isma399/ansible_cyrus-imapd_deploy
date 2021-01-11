#%PAM-1.0
auth       sufficient   /usr/lib64/security/pam_cas.so -ssmtp://{{ mail_domain }} -f/etc/pam_cas.conf
auth       include      password-auth
account    include      password-auth
