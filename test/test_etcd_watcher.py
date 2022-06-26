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

from unittest import TestCase

import etcd3

import etcd_watcher


class TestCaseBase(TestCase):
    def get_watcher(self, endpoints, keyname):
        watcher = etcd_watcher.ETCDWatcher(endpoints=endpoints, running=True, callback=None, key_name=keyname)
        watcher.create_client()
        return watcher


class TestConfig(TestCaseBase):
    def test_etcd_watcher_init(self):
        watcher = self.get_watcher(endpoints=["localhost", 2379], keyname="test")
        assert isinstance(watcher.client, etcd3.Etcd3Client)

    def test_update_etcd_watcher(self):
        watcher = self.get_watcher(endpoints=["localhost", 2379], keyname="test")
        assert watcher.update() is False

    def test_update_callback(self):
        def _test_update_callback():
            pass

        watcher = self.get_watcher(endpoints=["localhost", 2379], keyname="test")

        watcher.set_update_callback(_test_update_callback)
        assert watcher.callback == _test_update_callback
