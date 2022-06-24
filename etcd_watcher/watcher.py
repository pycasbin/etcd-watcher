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

import logging
import threading

import etcd3


class ETCDWatcher(object):
    def __init__(self, endpoints, running, callback, key_name):
        self.client = None
        self.endpoints = endpoints
        self.running = running
        self.callback = callback
        self.keyName = key_name
        self.mutex = threading.Lock()

    def create_client(self):
        self.client = etcd3.Etcd3Client(host=self.endpoints[0], port=self.endpoints[1])

    def close(self):
        self.client.close()

    def set_update_callback(self, callback):
        """
        sets the callback function to be called when the policy is updated
        :param callback:
        :return:
        """
        self.mutex.acquire()
        self.callback = callback
        self.mutex.release()

    def update(self):
        """
        calls the update callback of other instances to synchronize their policy
        """
        rev = 0
        kv_metadata = self.client.get(self.keyName)
        if kv_metadata[1] is None:
            return False
        else:
            resp = kv_metadata[1].response_header
            if resp is not None:
                rev = int(resp.revision)
                logging.info("Get revision: %d", rev)
                rev = rev + 1

        new_rev = str(rev)
        logging.info("Set revision: %s", new_rev)
        self.client.put(self.keyName, new_rev)
        return True

    def start_watch(self):
        """
        starts the watch thread
        :return:
        """
        events_iterator, cancel = self.client.watch(self.keyName)
        for event in events_iterator:
            print("Event: %s", event)
            if isinstance(event, etcd3.events.PutEvent) or isinstance(event, etcd3.events.DeleteEvent):
                self.mutex.acquire()
                if self.callback is not None:
                    self.callback(event)
                self.mutex.release()


def new_watcher(endpoints, keyname):
    """
    creates a new watcher
    :param endpoints:
    :param keyname:
    :return: a new watcher
    """
    return ETCDWatcher(endpoints=endpoints, running=True, callback=None, key_name=keyname)
