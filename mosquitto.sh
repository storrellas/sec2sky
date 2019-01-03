# Publish message
mosquitto_pub -m "test" -t "sensor"

# Subscribe message
mosquitto_sub -v -t '#' -d
