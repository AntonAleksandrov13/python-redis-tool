# Tool for Redis Cluster administration.
## Description
This tool is a Python CLI built on the top of [redis-cli](https://redis.io/topics/rediscli).
The reason this tool was made is that some automation features is missing in redis-cli. 
For example, to reshard a Redis cluster, a user has to manually move slots from one node to another.
Moreover, it is not possible to add more than one node to a Redis cluster once in a time.

Possible those features will be added natively to redis-cli in [a near future](https://github.com/antirez/redis/issues/4052).
### Data sharding

Generally, there are 16383 [hash slots](https://stackoverflow.com/questions/48314328/what-do-we-mean-by-hash-slot-in-redis-cluster) in one Redis cluster instance.
Therefore, upon starting a Redis cluster with 3 masters and 3 slaves you will have:
- Master 1 contains hash slots from 0 to 5500. Slave 1 replicates Master 1
- Master 2 contains hash slots from 5501 to 11000. Slave 2 replicates Master 2
- Master 2 contains hash slots from 11001 to 16383. Slave 3 replicates Master 3

As you can see, Redis Cluster strives to keep equal amount of hash slots on each master.
Concept of hash slots, allows easily add and remove master nodes.
The only catch here, you have to do resharding of your cluster each time amount of masters changes.
One option to do it [manually](https://redis.io/topics/cluster-tutorial).
Another one is to use my python CLI.

It works as following:
 - Define master nodes that contain has slots
 - Define "empty" masters - ones that contain no hash slots
 - Calculate how many slots can be moved from each master with slots
 - Perform `redis-cli --cluster reshard ` for each master with slots.
 - Check if all hash slots have been covered
 
 
In this image you can see the way hash slots will be distributed
[](./docs/sharding.png)

