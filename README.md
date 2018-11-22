# Tool for Redis Cluster administration.
## Description
This tool is a Python CLI built on the top of [redis-cli](https://redis.io/topics/rediscli).
The reason this tool was made is that some automation features are missing in redis-cli. 
For example, to reshard a Redis cluster, a user has to manually move slots from one node to another.
Moreover, it is not possible to add more than one node to a Redis cluster once in a time.

Possibly those features will be added natively to redis-cli in [a near future](https://github.com/antirez/redis/issues/4052).
### Data sharding

Generally, there are 16383 [hash slots](https://stackoverflow.com/questions/48314328/what-do-we-mean-by-hash-slot-in-redis-cluster) in one Redis cluster instance.
Therefore, upon starting a Redis cluster with 3 masters and 3 slaves you will have:
- Master 1 contains hash slots from 0 to 5500. Slave 1 replicates Master 1
- Master 2 contains hash slots from 5501 to 11000. Slave 2 replicates Master 2
- Master 2 contains hash slots from 11001 to 16383. Slave 3 replicates Master 3

As you can see, Redis Cluster strives to keep an equal amount of hash slots on each master.
The concept of hash slots, allows easily add and remove master nodes.
The only catch here, you have to do resharding of your cluster each time amount of masters changes.
One option to do it [manually](https://redis.io/topics/cluster-tutorial).
Another one is to use my python CLI.

It works as following:
 - Define master nodes that contain has slots
 - Define "empty" master nodes - ones that contain no hash slots
 - Calculate how many slots can be moved from each master with slots
 - Perform `redis-cli --cluster reshard ` for each master with slots. This command will transfer slots to an "empty" master.
 - Check if all hash slots have been covered
 
 
In this image you can see the way hash slots will be distributed:

![Hash slots distribution](https://github.com/AntonAleksandrov13/python-redis-tool/blob/master/docs/sharding.png)

#### Pros/cons
Pros
- Executed in a single command.
- Done via redis-cli.
- Zero downtime. A client is still able to wrote to a Redis cluster while resharding is done.

Cons
- Processing time grows linearly depending on amount of master nodes.


### Adding multiple nodes 
In my opinion, scaling up is never done by adding one master of one slave node to a Redis Cluster.
Therefore, another feature in my CLI is to add multiple nodes with a certain role at once.

A user can define in which mode certain nodes will be launched using `--role` argument with `add_node`.
You don`t have to worry to which master a slave will be assigned. redis-cli finds master with the least amount slaves itself.

## tl;dr
This CLI is just a wrapper for redis-cli with two key features: adding nodes and resharding a Redis cluster.

### Resharding 
Resharding is done by `python redis-tool.py -s SOURCE_NODE_ADDRESS reshard`.
`SOURCE_NODE_ADDRESS` - One of the nodes from the Redis cluster. It will be used as an entrypoint to all cluster operations.
`reshard` command requires at least one "empty" master. Otherwise, it will not work.

### Adding multiple nodes
Adding multiple node is done by `python redis-tool.py -s SOURCE_NODE_ADDRESS add_node --role{master,slave} --target<TARGET_NODE_ADDRESS...>`.
`SOURCE_NODE_ADDRESS` - One of the nodes from the Redis cluster. `TARGET_NODE_ADDRESS` - Address of the node you would like to add to the cluster.
You can provide more than one `TARGET_NODE_ADDRESS`.

# Sum up
This tool does not aims to replace redis-cli. It only tries to supplement redis-cli functionality.

In order to get more information about how to use this tool, please use `python redis-tool.py -h`.
If you want to have more information about a specific command run `python redis-tool.py add_node|reshard -h`.