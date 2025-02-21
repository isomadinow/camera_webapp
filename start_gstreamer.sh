#!/bin/bash

start_stream() {
    local PORT=$1
    gst-launch-1.0 -v videotestsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! \
        rtph264pay config-interval=1 pt=96 ! udpsink host=172.20.76.82 port=$PORT &
}


for PORT in 2025 2026 2027 2028; do
    echo "Запускаем GStreamer на порту $PORT..."
    start_stream $PORT
done

echo "Все потоки запущены."
