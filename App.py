from flask import Flask, render_template,request, redirect
import IoT_platform
import random
import threading
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', sensor_topics=sensor_topics, input_topics = input_topics, password=password)
    else:
        pass

@app.route('/view_data/<name_d>', methods=['POST','GET'])
def view_data(name_d):
    if request.method == 'POST':
        topic = request.form['topic']
        data_device = eval(request.form['data_device'])
        return render_template('view_data.html', topic=topic, name_d=name_d, data_device=data_device)
    else:
        pass

@app.route('/unsubscribe', methods=['POST','GET'])
def unsubscribe():
    if request.method == 'POST':
        topic = request.form['device_topic']
        print('Unsubscribe: ', topic)
        client.unsubscribe(topic=topic)

        return redirect('/')
    else:
        pass



if __name__ == "__main__":
    global client, sensor_topics, input_topics, password
    sensor_topics = []
    input_topics = []
    password = random.randint(10000, 99999)

    client = mqtt.Client()
    x = threading.Thread(target=IoT_platform.platform, args=(client,sensor_topics, input_topics, password), daemon=True)
    x.start()

    app.run(debug=False)