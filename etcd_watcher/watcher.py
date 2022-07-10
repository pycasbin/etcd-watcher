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
import time

import casbin
import etcd3


class ETCDWatcher(object):
    def __init__(self, endpoints, running, callback, key_name):
        self.client = None
        self.endpoints = endpoints
        self.running = running
        self.callback = callback
        self.keyName = key_name
        self.mutex = threading.Lock()
        self.watch_thread = threading.Thread(target=self.start_watch, daemon=True)
        self.logger = logging.getLogger(__name__)

    def create_client(self):
        self.client = etcd3.Etcd3Client(host=self.endpoints[0], port=self.endpoints[1])

    def close(self):
        self.running = False
        self.logger.info("ETCD watcher closed")

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
        update the policy
        """
        self.client.put(self.keyName, str(time.time()))
        return True

    def update_for_add_policy(self, section, ptype, *params):
        """
        update for add policy
        :param section: section
        :param ptype:   policy type
        :param params:  other params
        :return:    True if updated
        """
        message = "Update for add policy: " + section + " " + ptype + " " + str(params)
        self.logger.info(message)
        return self.update()

    def update_for_remove_policy(self, section, ptype, *params):
        """
        update for remove policy
        :param section: section
        :param ptype:   policy type
        :param params:  other params
        :return:    True if updated
        """
        message = (
            "Update for remove policy: " + section + " " + ptype + " " + str(params)
        )
        self.logger.info(message)
        return self.update()

    def update_for_remove_filtered_policy(self, section, ptype, field_index, *params):
        """
        update for remove filtered policy
        :param section: section
        :param ptype:   policy type
        :param field_index: field index
        :param params: other params
        :return:
        """
        message = (
            "Update for remove filtered policy: "
            + section
            + " "
            + ptype
            + " "
            + str(field_index)
            + " "
            + str(params)
        )
        self.logger.info(message)
        return self.update()

    def update_for_save_policy(self, model: casbin.Model):
        """
        update for save policy
        :param model: casbin model
        :return:
        """
        message = "Update for save policy: " + model.to_text()
        self.logger.info(message)
        return self.update()

    def update_for_add_policies(self, section, ptype, *params):
        """
        update for add policies
        :param section: section
        :param ptype:   policy type
        :param params:  other params
        :return:
        """
        message = (
            "Update for add policies: " + section + " " + ptype + " " + str(params)
        )
        self.logger.info(message)
        return self.update()

    def update_for_remove_policies(self, section, ptype, *params):
        """
        update for remove policies
        :param section: section
        :param ptype:   policy type
        :param params:  other params
        :return:
        """
        message = (
            "Update for remove policies: " + section + " " + ptype + " " + str(params)
        )
        self.logger.info(message)
        return self.update()

    def start_watch(self):
        """
        starts the watch thread
        :return:
        """
        events_iterator, cancel = self.client.watch(self.keyName)
        for event in events_iterator:
            if isinstance(event, etcd3.events.PutEvent) or isinstance(
                event, etcd3.events.DeleteEvent
            ):
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
    etcd = ETCDWatcher(
        endpoints=endpoints, running=True, callback=None, key_name=keyname
    )
    etcd.create_client()
    etcd.watch_thread.start()
    etcd.logger.info("ETCD watcher started")
    return etcd
