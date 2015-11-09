    - spout:
        name: kafka_user_location
        type: kafka
        options:
            #module: streaming_topology.user_behavior_spout
            # The Kafka topic to stream from.
            # Required.
            topic: location

            # ZooKeeper connection string. Comma-separated list of ZooKeeper
            # servers.
            # Required.
            zk_hosts: 119.254.111.40:2181/kafka/q-63lnrnga

            # Root path in ZooKeeper to store consumer offsets.
            # Defaults to: /pyleus-kafka-offsets/<topology name>
            zk_root: /pyleus-kafka-offsets/streaming_topology

            # Kafka consumer ID.
            # Defaults to: pyleus-<topology name>
            consumer_id: pyleus-Streaming_Topology

            # Whether the initial offset should be that specified by
            # start_offset_time (true) or the head of the stream (false).
            # Defaults to false.
            from_start: false

            # The offset time to start with if from_start is true.
            # Defaults to the earliest offset time in the stream.
            start_offset_time: 1398971060

            # support binary data like google protobuf
            binary_data: true

    - bolt:
        name: classfierByUid_bolt
        module: Streaming_Topology.classfierByUid_bolt
        groupings:
            - shuffle_grouping:
                component: kafka_user_location