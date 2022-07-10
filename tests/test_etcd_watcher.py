# Copyright 2022 The casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from unittest import TestCase

import casbin
import etcd3

from etcd_watcher import new_watcher


def get_examples(path):
    examples_path = os.path.split(os.path.realpath(__file__))[0] + "/../examples/"
    return os.path.abspath(examples_path + path)


class TestConfig(TestCase):
    def test_etcd_watcher_init(self):
        watcher = new_watcher(endpoints=["localhost", 2379], keyname="test0")
        assert isinstance(watcher.client, etcd3.Etcd3Client)

    def test_update_etcd_watcher(self):
        watcher = new_watcher(endpoints=["localhost", 2379], keyname="tests")
        watcher.client.put("tests", "test_value")
        assert watcher.update() is True

    def test_with_enforcer(self):
        def _test_update_callback(event):
            print("update callback, event: {}".format(event))

        watcher = new_watcher(endpoints=["localhost", 2379], keyname="/casbin")
        watcher.set_update_callback(_test_update_callback)

        e = casbin.Enforcer(
            get_examples("rbac_model.conf"), get_examples("rbac_policy.csv")
        )
        e.set_watcher(watcher)
        e.save_policy()
        # related update function not be called in py-casbin yet
        e.add_policy("eve", "data3", "read")
        e.remove_policy("eve", "data3", "read")
        rules = [
            ["jack", "data4", "read"],
            ["katy", "data4", "write"],
            ["leyo", "data4", "read"],
            ["ham", "data4", "write"],
        ]
        e.add_policies(rules)
        e.remove_policies(rules)
