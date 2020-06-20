import time
import mqttclient as mq

# Subscribeしたメッセージのハンドラ
# 第一引数にtopic名、第二引数にメッセージの中身が渡される。
def handler(topic, payload):
    print("handler-recv : {}, {}".format(topic, payload.decode("utf-8", "ignore")))

# Subscribe
def subscribe_start(broker_host_name, topic):
    # クライアント作成、トピック設定
    client = mq.MqttClient(broker_host_name)
    recv_topic = [(topic, 1)]
    # Subscribeしたメッセージを処理するハンドラの登録
    client.set_recv_handler(handler)
    # 接続とsubscribe開始
    client.connect(logprint=True)
    client.subscribe_to(recv_topic)

# Publush
def publish_start(broker_host_name, topic):
    # クライアント作成、トピック設定
    client = mq.MqttClient(broker_host_name)
    send_topic = [(topic, 1)]
    # 接続とメッセージを10個Publish
    client.connect(logprint=True)
    for i in range(10):
        client.publish_to(send_topic, str(i))


if __name__ == '__main__':
    broker_host_name = "aaa.example.com"
    topic = "sample"
    publish_start(broker_host_name, topic)
    subscribe_start(broker_host_name)
    time.sleep(10)