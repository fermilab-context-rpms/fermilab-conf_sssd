_default:
	@echo "make"
sources:
	@echo "make sources"
	tar cvf -  sssd_conf.d | xz > fermilab-conf_sssd.tar.xz
srpm: sources
	rpmbuild -bs --define '_sourcedir .' --define '_srcrpmdir .' fermilab-conf_sssd.spec
