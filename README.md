# Overview

This interface layer handles the communication between Apache HBase and its
clients. The provider of this interface provides HBase services.
The consumer requires the existence of a provider to function.


# Usage

## Provides

Charms providing the Apache HBase services *provide* this interface. This
interface layer will set the following states, as appropriate:

  * `{relation_name}.joined` The provider has been related to a client. At this
  point, the provider should broadcast availability details:

    * If HBase is running and HDFS/Zookeeper are available:
        * `send_connection(master_port, regionserver_port, thrift_port, hostname, zk_connect)`
    * If HBase is not running or HDFS/Zookeeper are not available:
        * `clear_hbase_started()`

  * `{relation_name}.ready`  HBase configuration details have been sent.
  The provider and client should now be able to communicate.

HBase provider example:

```python
@when('hbase.installed')
@when('hadoop.hdfs.ready', 'zookeeper.ready', 'client.joined')
def serve_client(hdfs, zk, client):
    client.send_connection(
        get_master_port(), get_region_port(), get_thrift_port(),
        get_fqdn(), get_zk_connect(zk))

@when('client.joined')
@when_not_all('hbase.installed', 'hadoop.hdfs.ready', 'zookeeper.ready')
def stop_serving_client(client):
    client.clear_hbase_started()
```


## Requires

Clients *require* this interface to connect to Apache HBase. This interface
layer will set the following states, as appropriate:

  * `{relation_name}.joined` The client charm has been related to a HBase
  provider. At this point, the charm waits for HBase configuration details.

  * `{relation_name}.ready`  HBase is now ready for clients. The client
  charm should get HBase configuration details using:
    * `hbase_servers()` returns a list of HBase unit dicts:
          {host: 'xyz',
           master_port: n,
           regionserver_port: m,
           thrift_port: o,
           zk_connect: 'zk1,zk2,zk3'
          }


HBase client example:

```python
@when('hbase.joined')
@when_not('hbase.ready')
def wait_for_hbase(hbase):
    hookenv.status_set('waiting', 'Waiting for HBase to become available')


@when('hbase.ready')
@when_not('myservice.configured')
def configure(hbase):
    for unit in hbase.hbase_servers():
        add_hbase(unit['host'], unit['master_port'], unit['regionserver_port'])
    set_state('myservice.configured')
```


# Contact Information

- <bigdata@lists.ubuntu.com>
