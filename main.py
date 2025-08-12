from flask import Flask, render_template,flash, request

app=Flask(__name__)
app.config['SECRET_KEY']='djhfsuhdfdjhfsjkdghfbxcvnhb'
trs=[]

STATUS_WAIT='ожидание'

@app.route('/',methods=["POST","GET"])
def index():
    #trs=[[1,2,3,4,5],['1q','2q','3q','4q','5q']]
    selected_arhiv="archive.admoblkaluga.ru"
    if request.method=='POST':
        print(request.form)
        #print ( request.files['file'].read())
        iod=request.form.get('iod')
        page_start=request.form.get('page_start','') if request.form.get('page_start','').isdigit() else ""
        page_stop=request.form.get('page_stop','') if request.form.get('page_stop','').isdigit() else ""
        selected_arhiv=request.form.get('arhiv','') 
        if request.form.get('AddOid') and len(iod)>0:
            append_rec=[iod,page_start,page_stop,"",STATUS_WAIT,]
            if append_rec not in trs:
                trs.append(append_rec)
                flash('Документ добавлен',category='success')
            else:
                flash('Такой документ уже есть',category='error')     
        elif request.form.get('AddOid') and request.files['file']:
            file_data=request.files['file'].read().split()
            #print (file_data)
            file_info_append=False
            for load_data in file_data:
                try:
                    load_data=load_data.decode()
                except:
                    break
                load_data_split=load_data.split(';')
                if len(load_data_split)==3:
                    append_rec=[load_data_split[0],load_data_split[1],load_data_split[2],"",STATUS_WAIT]
                    if append_rec not in trs:
                        trs.append(append_rec)
                        file_info_append=True
                elif len(load_data_split)==1:
                    append_rec=[load_data_split,"","","",STATUS_WAIT]
                    if append_rec not in trs:
                        trs.append(append_rec)
                        file_info_append=True
            if file_info_append:
                flash('Добавлена информация из файла',category='success')
            else:
                flash('Ошибка добавления информации из файла',category='error') 
        else:
            if request.form.get('AddOid'):
                flash('Ошибка добавления',category='error')
    return render_template('index.html',trs=trs,selected_arhiv=selected_arhiv)

if __name__=='__main__':
    app.run(debug=True)