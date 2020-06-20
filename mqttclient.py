import paho.mqtt.client as mqtt
import sys


class MqttClient:
    port = 1883

    def __init__(self, broker_host_name):
        self.recv_handler = None
        self.hostname = broker_host_name
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)

    def set_recv_handler(self, recv_handler):
        self.recv_handler = recv_handler

    def on_connect(self, client, userdata, flags, res_code):
        print("connectted!! result code : {}".format(res_code), file=sys.stderr)

    def on_message(self, client, userdata, msg):
        print("recv : {}, {}".format(msg.topic, msg.payload), file=sys.stderr)
        if self.recv_handler is not None:
            self.recv_handler(msg.topic, msg.payload)

    def on_log(self, client, userdata, level, buf):
        print("[log] : {}".format(buf), file=sys.stderr)

    def publish_to_broker(self, topic, sendmsg):
        self.client.publish(topic, sendmsg)
        print("send message >n{}".format(sendmsg), file=sys.stderr)

    def subscribe_from_broker(self, topic):
        self.client.subscribe(topic)
        self.client.loop_start()

    def suspend_subscribe(self):
        self.client.loop_stop()

    def connect(self, logprint=False):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        if logprint:
            self.client.on_log = self.on_log
        self.client.connect(self.hostname, port=MqttClient.port, keepalive=30)

    def disconnect(self):
        self.client.disconnect()
