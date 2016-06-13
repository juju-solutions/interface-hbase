# Overview

This interface layer handles the communication between Apache HBase and its
clients. The provider end of this interface provides the HBase services.
The consumer part requires the existence of a provider to function.


# Usage

## Provides

Charms providing the Apache HBase services *provide* this interface. This
interface layer will set the following states, as appropriate:

  * `{relation_name}.joined` The provider has been related to a client,
  though the client service may not be available yet. At this point,
  the provider should broadcast configuration details using:

    * `send_port(master_port, regionserver_port, thrift_port)`


  * `{relation_name}.ready`  HBase configuration details have been sent.
  The provider and client should now be able to communicate.


HBase provider example:

```python
@when('client.joined')
@when_not('client.ready')
def send_config(client):
    client.send_port(get_master_port(), get_region_port(), get_thrift_port())
```


## Requires

Clients *require* this interface to connect to Apache HBase. This interface
layer will set the following states, as appropriate:

  * `{relation_name}.joined` The client charm has been related to a HBase
  provider. At this point, the charm waits for HBase configuration details.

  * `{relation_name}.ready`  HBase is now ready for clients. The client
  charm should get Zookeeper configuration details using:

    * `servers()` returns a list of HBase units 
                     {host: xyz, master_port: n, regionserver_port: m, thrift_port: o} dicts


HBase client example:

```python
@when('hbase.joined')
@when_not('hbase.ready')
def wait_for_hbase(hbase):
    hookenv.status_set('waiting', 'Waiting for HBase to become available')


@when('hbaser.ready')
@when_not('myservice.configured')
def configure(hbase):
    for unit in hbase.servers():
        add_hbase_master(unit['host'], zk_unit['master_port'])
    set_state('myservice.configured')
```


# Contact Information

- <bigdata@lists.ubuntu.com>
