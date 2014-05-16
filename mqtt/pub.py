import mosquitto
import time

def on_connect(mqttc, obj, rc):
    mqttc.subscribe("$SYS/#", 0)
    print("rc :" + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_log(mqttc, obj, level, string):
    print(string)

if __name__ == "__main__":
    cli = mosquitto.Mosquitto()
    cli.on_connect = on_connect
    cli.on_publish = on_publish
    cli.on_message = on_message

    cli.connect("127.0.0.1")
    for i in range(1, 100):
        cli.publish("my/topic/string", str(i), 1) #qos?
        time.sleep(1)

