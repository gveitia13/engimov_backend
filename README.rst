Engimov Website-Like Application 🐳
====================================

Preparing stage
----------------
1. Install `docker <https://docs.docker.com/engine/install/>`_

Deployment with docker-compose
-------------------------------

.. code-block:: bash

    docker compose up -d

Deployment with stack (Swarm mode)
-----------------------------------

.. code-block:: bash

    HOSTNAME=$HOSTNAME docker stack deploy -c docker-compose.yml engimov

**NOTE:** If you don't want to run your project in just one node (DEFAULT) please go to the docker-compose.yml remove the constraint from the deploy increase your replicas and voila... Please beware of this project's
configuration file doesn't include any support for cluster-wide storage, you must configure your own underlying storage management cluster (for example glusterphs, ceph and tfprotocol which is coming soon).
Use docker swarm capabilities under your own responsibility. minor configurations are needed for this project to run as intended.

