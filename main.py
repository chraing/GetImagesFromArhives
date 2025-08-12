from flask import Flask, render_template,flash, request

app=Flask(__name__)
app.config['SECRET_KEY']='djhfsuhdfdjhfsjkdghfbxcvnhb'
trs=[]

@app.route('/',methods=["POST","GET"])
def index():
    #trs=[[1,2,3,4,5],['1q','2q','3q','4q','5q']]
    selected_arhiv="archive.admoblkaluga.ru"
    if request.method=='POST':
        print(request.form)
        iod=request.form.get('iod')
        page_start=request.form.get('page_start','') if request.form.get('page_start','').isdigit() else ""
        page_stop=request.form.get('page_stop','') if request.form.get('page_stop','').isdigit() else ""
        selected_arhiv=request.form.get('arhiv','') 
        if request.form.get('AddOid') and len(iod)>0:
            flash('Документ добавлен',category='success')
            trs.append([iod,page_start,page_stop,"","ожидание",])
        else:
            if request.form.get('AddOid'):
                flash('Ошибка добавления',category='error')
    return render_template('index.html',trs=trs,selected_arhiv=selected_arhiv)

if __name__=='__main__':
    app.run(debug=True)