import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_tomcat_systemd_file(host):
    f = host.file('/etc/systemd/system/tomcat.service')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('JAVA_HOME')


def test_opt_tomcat(host):
    f = host.file('/opt/tomcat')
    assert f.is_symlink
    assert f.exists


def test_tomcat_service(host):
    s = host.service('tomcat')
    assert s.is_running
    assert s.is_enabled


def test_tomcat_listen_address(host):
    # install iproute to use the socket test
    host.ansible("command", "yum -y install iproute", become=True, check=False)
    s = host.socket('tcp://0.0.0.0:8080')
    assert s.is_listening
