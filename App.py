from flask import Flask, render_template,request, redirect

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    sensor_topics = [['/Device/Temperatura-1', 'Temperatura-1', [[19, '15-03-2023 23:59:55'],[20, '15-03-2023 23:59:55']], 3], ['/Device/Temperatura-2', 'Temperatura-2', [120, '15-03-2023 23:59:55'], 3],
                      ['/Device/Humedad-1', 'Humedad-1', [25, '15-03-2023 23:59:55'], 3], ['/Device/Intensidad_Luminosa-1', 'Intensidad_Luminosa-1' , [19, '15-03-2023 23:59:55'], 3]]
    
    output_topics = [['/Device/outputDevice-1', 2], ['/Device/outputDevice-1', 2]]
    if request.method == 'GET':
        return render_template('index.html', sensor_topics=sensor_topics, output_topics = output_topics)
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

        return redirect('/')
    else:
        pass



if __name__ == "__main__":
    app.run(debug=True)