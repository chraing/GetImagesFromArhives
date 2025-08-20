from flask import Flask, render_template,flash, request,jsonify,redirect,url_for
from  genodbase import GetFromCgamos,GetFromYandexArhive
#from threading import Thread
import concurrent.futures as pool
import settings

app=Flask(__name__)
app.config['SECRET_KEY']='djhfsuhdfdjhfsjkdghfbxcvnhb'
settings.init()

STATUS_WAIT='ожидание'
selected_arhiv="archive.admoblkaluga.ru"

@app.route('/')
def index():
    return render_template('index.html',trs=settings.trs,selected_arhiv=selected_arhiv)

@app.route('/update_date',methods=["POST","GET"])
def update_date():
    if request.method=='POST':
        print("POST-/update_date",request.form)
        print("file->",request.files['file'])
        #print ( request.files['file'].read())
        iod=request.form.get('iod')
        page_start=request.form.get('page_start','') if request.form.get('page_start','').isdigit() else ""
        page_stop=request.form.get('page_stop','') if request.form.get('page_stop','').isdigit() else ""
        global selected_arhiv
        selected_arhiv=request.form.get('arhiv','') 
        if request.form.get('AddOid') and len(iod)>0:
            append_rec={'iod':iod,'page_start':page_start,'page_stop':page_stop,'count_rec':"",'status':STATUS_WAIT,'complete':False}
            if append_rec not in settings.trs:
                settings.trs.append(append_rec)
                flash('Документ добавлен',category='success')
            else:
                flash('Такой документ уже есть',category='error')     
        elif  request.files['file']:
            file_data=request.files['file'].read().split()
            print (file_data)
            file_info_append=False
            for load_data in file_data:
                try:
                    load_data=load_data.decode()
                except:
                    break
                load_data_split=load_data.split(';')
                if len(load_data_split)==3:
                    append_rec={'iod':load_data_split[0],'page_start':load_data_split[1],'page_stop':load_data_split[2],'count_rec':"",'status':STATUS_WAIT,'complete':False}
                    if append_rec not in settings.trs:
                        settings.trs.append(append_rec)
                        file_info_append=True
                elif len(load_data_split)==1:
                    append_rec={'iod':load_data_split[0],'page_start':"",'page_stop':"",'count_rec':"",'status':STATUS_WAIT,'complete':False}
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
                with pool.ThreadPoolExecutor() as executor:
                    # Запуск задачи асинхронно
                    futures=[]
                    for n,trs_rec in enumerate(settings.trs):
                        start_image=trs_rec['page_start']
                        stop_image=trs_rec['page_stop']
                        complete=trs_rec['complete']
                        if complete==False:
                            if request.form.get('arhiv')=='cgamos.ru':
                                f=GetFromCgamos
                            elif request.form.get('arhiv')=='yandex.ru':
                                f=GetFromYandexArhive
                            future=executor.submit(f, trs_rec['iod'],start_image,stop_image,n)
                            futures.append(future)
                        # Ожидание результата и получение его
                    for future in pool.as_completed(futures):
                        rez= future.result()
                        settings.trs[rez]['complete']=True

    return redirect(url_for('index'))

@app.route('/update_data_table')
def update_data(): 
    return jsonify(settings.trs)

if __name__=='__main__':
    app.run(debug=True)