%define _topdir	 	/root/rpmbuild
%define name	        gt.m
%define version         6.2.002A
%define release		1
%define buildroot %{_topdir}/%{name}-%{version}-root
%define debug_package %{nil}

BuildRoot:	    %{buildroot}
Summary: 	    FIS GT.M
License: 	    GNU Affero GPL v3
Name: 		    %{name}
Version: 	    %{version}
Release: 	    %{release}
Source: 	    gtm_V62002A_linux_x8664_pro.tar.gz
Prefix: 	    /opt
Group: 		    Applications/Databases
Requires:           libicu >= 3.6
Requires(pre):      /usr/sbin/useradd, /usr/bin/getent
Requires(postun):   /usr/sbin/userdel
#AutoReqProv:        no


%description
GT.M[tm] is a vetted industrial strength, transaction processing application platform consisting of a key-value database engine optimized for extreme transaction processing throughput & business continuity.
Features
    Key-value database files into the TB range (unlimited aggregate database sizes)
    ACID (Atomic, Consistent, Isolated, Durable) transactions
    Large scale replication for business continuity
    Thousands of concurrent users at largest production sites
    Plug-in architecture for database encryption


%pre
echo "Create technical user sca:sca"
/usr/bin/getent group sca || /usr/sbin/groupadd -r sca
/usr/bin/getent passwd sca || /usr/sbin/useradd -g sca -r -M -s /sbin/nologin sca

%postun
/usr/sbin/userdel sca


%prep
%setup -q -c

%build
tmp_icu=$(/bin/icu-config-64 --version | cut -d"." -f 1)
if [[ $tmp_icu > 4 ]]
then
    icu_ver=${tmp_icu:0:1}.${tmp_icu:1:${#tmp_icu}}
else
    icu_ver=$(/bin/icu-config-64 --version | sed -r 's/(^[0-9]+\.[0-9]+)\..*$/\1/')
fi
echo $icu_ver
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
./configure <<PARAMS 
sca
sca
n
$RPM_BUILD_ROOT/opt/fis-gtm/%{version}
y
y
y
${icu_ver}
n
n
n
PARAMS
ktmp=$(uuidgen -r)
mkdir /tmp/$ktmp
cd /tmp/$ktmp
cp $RPM_BUILD_ROOT/opt/fis-gtm/%{version}/plugin/gtmcrypt/source.tar .
tar -xvf source.tar
export gtm_dist="$RPM_BUILD_ROOT/opt/fis-gtm/%{version}"
make uninstall
make
make install
[ -d /tmp/$ktmp ] && rm -fr /tmp/$ktmp
cd $gtm_dist
sed -i 's/\/root\/rpmbuild\/BUILDROOT\/gt.m-%{version}-%{release}.x86_64//g' gtm gtmbase gtmcshrc gtmprofile gtmprofile_preV54000



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(0444,sca,sca,0555)
%doc %attr(0444,root,root) COPYING
%doc %attr(0444,root,root) README.txt
%attr(0500,root,root) /opt/fis-gtm/%{version}/gtmsecshrdir
%attr(4555,root,root) /opt/fis-gtm/%{version}/gtmsecshr
%attr(0500,root,root) /opt/fis-gtm/%{version}/gtmstart
%attr(0500,root,root) /opt/fis-gtm/%{version}/gtmstop
%attr(0500,root,root) /opt/fis-gtm/%{version}/gtcm_run
%attr(0500,root,root) /opt/fis-gtm/%{version}/gtcm_slist
%attr(0500,root,root) /opt/fis-gtm/%{version}/utf8/gtmsecshrdir
%attr(4555,root,root) /opt/fis-gtm/%{version}/utf8/gtmsecshr
%attr(0555,-,-) /opt/fis-gtm/%{version}/dse
%attr(0555,-,-) /opt/fis-gtm/%{version}/ftok
%attr(0555,-,-) /opt/fis-gtm/%{version}/geteuid
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtcm_gnp_server
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtcm_pkdisp
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtcm_play
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtcm_server
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtcm_shmclean
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtm
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtmbase
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtmcshrc
%attr(0555,-,-) /opt/fis-gtm/%{version}/gtmprofile
%attr(0555,-,-) /opt/fis-gtm/%{version}/libgtmshr.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/libgtmutil.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/lke
%attr(0555,-,-) /opt/fis-gtm/%{version}/mumps
%attr(0555,-,-) /opt/fis-gtm/%{version}/mupip
%attr(0555,-,-) /opt/fis-gtm/%{version}/semstat2
%attr(0555,-,-) /opt/fis-gtm/%{version}/utf8/libgtmutil.so
/opt/fis-gtm/%{version}/*.m
/opt/fis-gtm/%{version}/*.h
/opt/fis-gtm/%{version}/utf8/*.m
/opt/fis-gtm/%{version}/utf8/*.h
/opt/fis-gtm/%{version}/COPYING
/opt/fis-gtm/%{version}/README.txt
/opt/fis-gtm/%{version}/custom_errors_sample.txt
/opt/fis-gtm/%{version}/dsehelp.dat
/opt/fis-gtm/%{version}/dsehelp.gld
/opt/fis-gtm/%{version}/gdedefaults
/opt/fis-gtm/%{version}/gdehelp.dat
/opt/fis-gtm/%{version}/gdehelp.gld
/opt/fis-gtm/%{version}/gtmhelp.dat
/opt/fis-gtm/%{version}/gtmhelp.gld
/opt/fis-gtm/%{version}/gtmprofile_preV54000
/opt/fis-gtm/%{version}/lkehelp.dat
/opt/fis-gtm/%{version}/lkehelp.gld
/opt/fis-gtm/%{version}/mupiphelp.dat
/opt/fis-gtm/%{version}/mupiphelp.gld
/opt/fis-gtm/%{version}/utf8/COPYING
/opt/fis-gtm/%{version}/utf8/README.txt
/opt/fis-gtm/%{version}/utf8/custom_errors_sample.txt
/opt/fis-gtm/%{version}/utf8/dse
/opt/fis-gtm/%{version}/utf8/dsehelp.dat
/opt/fis-gtm/%{version}/utf8/dsehelp.gld
/opt/fis-gtm/%{version}/utf8/ftok
/opt/fis-gtm/%{version}/utf8/gdedefaults
/opt/fis-gtm/%{version}/utf8/gdehelp.dat
/opt/fis-gtm/%{version}/utf8/gdehelp.gld
/opt/fis-gtm/%{version}/utf8/geteuid
/opt/fis-gtm/%{version}/utf8/gtcm_gnp_server
/opt/fis-gtm/%{version}/utf8/gtcm_pkdisp
/opt/fis-gtm/%{version}/utf8/gtcm_play
/opt/fis-gtm/%{version}/utf8/gtcm_run
/opt/fis-gtm/%{version}/utf8/gtcm_server
/opt/fis-gtm/%{version}/utf8/gtcm_shmclean
/opt/fis-gtm/%{version}/utf8/gtcm_slist
/opt/fis-gtm/%{version}/utf8/gtm
/opt/fis-gtm/%{version}/utf8/gtmbase
/opt/fis-gtm/%{version}/utf8/gtmcshrc
/opt/fis-gtm/%{version}/utf8/gtmhelp.dat
/opt/fis-gtm/%{version}/utf8/gtmhelp.gld
/opt/fis-gtm/%{version}/utf8/gtmprofile
/opt/fis-gtm/%{version}/utf8/gtmprofile_preV54000
/opt/fis-gtm/%{version}/utf8/gtmstart
/opt/fis-gtm/%{version}/utf8/gtmstop
/opt/fis-gtm/%{version}/utf8/libgtmshr.so
/opt/fis-gtm/%{version}/utf8/lke
/opt/fis-gtm/%{version}/utf8/lkehelp.dat
/opt/fis-gtm/%{version}/utf8/lkehelp.gld
/opt/fis-gtm/%{version}/utf8/mumps
/opt/fis-gtm/%{version}/utf8/mupip
/opt/fis-gtm/%{version}/utf8/mupiphelp.dat
/opt/fis-gtm/%{version}/utf8/mupiphelp.gld
/opt/fis-gtm/%{version}/utf8/semstat2
# crypt plugin
%attr(0444,root,root) /opt/fis-gtm/%{version}/plugin/gpgagent.tab
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/encrypt_sign_db_key.sh
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/gen_keypair.sh
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/gen_sym_hash.sh
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/gen_sym_key.sh
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/import_and_sign_key.sh
/opt/fis-gtm/%{version}/plugin/gtmcrypt/maskpass
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/pinentry-gtm.sh
/opt/fis-gtm/%{version}/plugin/gtmcrypt/pinentry.m
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/gtmcrypt/show_install_config.sh
/opt/fis-gtm/%{version}/plugin/gtmcrypt/source.tar
/opt/fis-gtm/%{version}/plugin/libgtmcrypt.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/libgtmcrypt_gcrypt_AES256CFB.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/libgtmcrypt_openssl_AES256CFB.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/libgtmcrypt_openssl_BLOWFISHCFB.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/libgtmcryptutil.so
%attr(0555,-,-) /opt/fis-gtm/%{version}/plugin/libgtmtls.so
/opt/fis-gtm/%{version}/utf8/plugin

