from flask import Flask, render_template,flash, request,jsonify
from  genodbase import GetFromCgamos
from threading import Thread
import settings

app=Flask(__name__)
app.config['SECRET_KEY']='djhfsuhdfdjhfsjkdghfbxcvnhb'
settings.init()

STATUS_WAIT='ожидание'

@app.route('/',methods=["POST","GET"])
def index():
    selected_arhiv="archive.admoblkaluga.ru"
    if request.method=='POST':
        print(request.form)
        #print ( request.files['file'].read())
        iod=request.form.get('iod')
        page_start=request.form.get('page_start','') if request.form.get('page_start','').isdigit() else ""
        page_stop=request.form.get('page_stop','') if request.form.get('page_stop','').isdigit() else ""
        selected_arhiv=request.form.get('arhiv','') 
        if request.form.get('AddOid') and len(iod)>0:
            append_rec={'iod':iod,'page_start':page_start,'page_stop':page_stop,'count_rec':"",'status':STATUS_WAIT}
            if append_rec not in settings.trs:
                settings.trs.append(append_rec)
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
                    append_rec={'iod':load_data_split[0],'page_start':load_data_split[1],'page_stop':load_data_split[2],'count_rec':"",'status':STATUS_WAIT}
                    if append_rec not in settings.trs:
                        settings.trs.append(append_rec)
                        file_info_append=True
                elif len(load_data_split)==1:

                    append_rec={'iod':load_data_split[0],'page_start':"",'page_stop':"",'count_rec':"",'status':STATUS_WAIT}
                    if append_rec not in settings.trs:
                        settings.trs.append(append_rec)
                        file_info_append=True
            if file_info_append:
                flash('Добавлена информация из файла',category='success')
            #else:
            #    flash('Ошибка добавления информации из файла',category='error') 
        else:
            if request.form.get('AddOid'):
                flash('Ошибка добавления',category='error')
        if request.form.get('start'):
            if request.form.get('start'):
                if request.form.get('arhiv')=='cgamos.ru':
                    for n,trs_rec in enumerate(settings.trs):
                        start_image=trs_rec['page_start']
                        stop_image=trs_rec['page_stop']
                        th = Thread(target=GetFromCgamos, args=(trs_rec['iod'],start_image,stop_image,n))
                        th.start()
                        #th.join()
                        #break

    return render_template('index.html',trs=settings.trs,selected_arhiv=selected_arhiv)

@app.route('/update_data')
def update_data():
    #print (trs)
    # Обновляем значение 
    return jsonify(settings.trs)
if __name__=='__main__':
    app.run(debug=True)