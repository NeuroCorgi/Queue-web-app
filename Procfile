release: ./release.sh
web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 index:app