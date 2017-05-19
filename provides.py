# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class HBaseProvides(RelationBase):
    # Every unit connecting will get the same information
    scope = scopes.GLOBAL

    @hook('{provides:hbase}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.joined')

    @hook('{provides:hbase}-relation-changed')
    def changed(self):
        self.set_state('{relation_name}.ready')

    @hook('{provides:hbase}-relation-departed')
    def departed(self):
        conv = self.conversation()
        if len(conv.units) <= 1:  # last remaining unit departing
            conv.remove_state('{relation_name}.joined')
            conv.remove_state('{relation_name}.ready')

    def clear_hbase_started(self):
        self.set_remote('hbase_started', False)

    def send_connection(self, master_port, regionserver_port, thrift_port,
                        host=None, zk_connect=None):
        '''
        Send ready flag along with connection info. Some clients (e.g. Hive)
        need to know about the zookeeper ensemble that HBase is using, so send
        the zk connect string as well.
        '''
        conv = self.conversation()
        conv.set_remote(data={
            'hbase_started': True,
            'master_port': master_port,
            'regionserver_port': regionserver_port,
            'thrift_port': thrift_port,
            'host': host,
            'zk_connect': zk_connect,
        })

    # Synonym for send_connection (for now)
    send_port = send_connection
