import mosquitto

def on_connect(mqttc, obj, rc):
    mqttc.subscribe("$SYS/#", 0)
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

if __name__ == "__main__":
    cli = mosquitto.Mosquitto()
    cli.on_message = on_message
    cli.on_connect = on_connect
    cli.on_subscribe = on_subscribe

    cli.connect("127.0.0.1")
    cli.subscribe("my/topic/string", 0)
    
    cli.loop_forever()
