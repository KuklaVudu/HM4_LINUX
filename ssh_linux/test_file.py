import pytest
import yaml
from checkers import getout
from sshcheckers import ssh_checkout, upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def save_log(starttime, name):
    with open(name, 'w') as f:
        f.write(getout("journalctl --since '{}'".format(starttime)))


class TestPositive:

    def test_step1(self, start_time):
        res = []
        upload_files(data["ip"], data["user"], data["passwd"], data["pkg-name"] + ".deb",
                     "/home/{}/{}.deb".format(data["user"], data["pkg-name"]))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -i"
                                                                          " /home/{}/{}.deb".format(data["passwd"],
                                                                                                    data["user"],
                                                                                                    data["pkg-name"]),
                                "Настраивается пакет"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "echo '{}' | "
                                                                          "sudo -S dpkg -s {}".format(data["passwd"],
                                                                                                      data["pkg-name"]),
                                "Status: install ok installed"))
        save_log(start_time, "log1.txt")
        assert all(res), "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, start_time):
        res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {};"
                                                                      " 7z a {}/arx2".format(data["folder_in"],
                                                                                             data["folder_out"]),
                            "Everything is Ok")
        res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_out"]), "arx2.7z")
        save_log(start_time, "log2.txt")
        assert res1 and res2, "test2 FAIL"


if __name__ == '__main__':
    pytest.main()