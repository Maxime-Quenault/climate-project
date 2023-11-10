const consumer = kafka.consumer({ groupId: 'mon-group' });

const consommerMessages = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'mon-topic', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log({
        partition,
        offset: message.offset,
        value: message.value.toString(),
      });
    },
  });
};

consommerMessages().catch(console.error);