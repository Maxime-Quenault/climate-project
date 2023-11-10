const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'mon-app',
  brokers: ['kafka-broker:9092']
});

const producer = kafka.producer();

const produireMessage = async () => {
  await producer.connect();
  await producer.send({
    topic: 'mon-topic',
    messages: [
      { value: 'Bonjour Kafka' },
    ],
  });

  await producer.disconnect();
};

produireMessage().catch(console.error);