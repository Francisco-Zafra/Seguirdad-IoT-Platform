from flask import Flask, render_template,request, redirect
import IoT_platform
import threading
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    
    #sensor_topics = [['/Device/Temperatura-1', 'Temperatura-1', [[19, '15-03-2023 23:59:55'],[20, '15-03-2023 23:59:55']], 3], ['/Device/Temperatura-2', 'Temperatura-2', [120, '15-03-2023 23:59:55'], 3],
    #               ['/Device/Humedad-1', 'Humedad-1', [25, '15-03-2023 23:59:55'], 3], ['/Device/Intensidad_Luminosa-1', 'Intensidad_Luminosa-1' , [19, '15-03-2023 23:59:55'], 3]]
    
    # sensor_topics = {
    #     "Nombre_del_dispositivo":{    
    #                     "topic": "topic_name",
    #                     "data": [
    #                         {
    #                             "value": 8,
    #                             "date": '15-03-2023 23:59:55'
    #                         }],
    #                     "intervalo": 4
    #                     },
    #     "Nombre_del_dispositivo2":{    
    #             "topic": "topic_name",
    #             "data": [
    #                 {
    #                     "value": 8,
    #                     "date": '15-03-2023 23:59:55'
    #                 }],
    #             "intervalo": 4
    #             },
    #     }
    # sensor_topics["Nombre_del_dispositivo2"]["topic"]
    # sensor_topics["Nombre_del_dispositivo2"]["data"]
    # sensor_topics["Nombre_del_dispositivo2"]["intervalo"]

    #output_topics = [['/Device/outputDevice-1', 2], ['/Device/outputDevice-1', 2]]
    if request.method == 'GET':
        print(input_topics)
        return render_template('index.html', sensor_topics=sensor_topics, input_topics = input_topics)
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
        print('-----------------------------------')
        print('Unsubscribe: ', topic)
        client.unsubscribe(topic=topic)

        return redirect('/')
    else:
        pass



if __name__ == "__main__":
    global client, sensor_topics, input_topics
    sensor_topics = []
    input_topics = []

    client = mqtt.Client()
    x = threading.Thread(target=IoT_platform.platform, args=(client,sensor_topics, input_topics,), daemon=True)
    x.start()

    app.run(debug=False)