from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# create a connection to the database
cnx = mysql.connector.connect(
  host="localhost",
  user="nvkhoan",
  password="asdf",
  database="testt"
)
cursor = cnx.cursor()
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
# define a route to handle GET requests to retrieve data
@app.route('/get-data', methods=['GET'])
def get_data():
    # get the studentID from the query parameters
    student_id = request.args.get('id')
    code=   request.args.get('group')
    groups = {
        "A00": ["math", "physics", "chemistry"],
        "A01": ["math", "physics", "english"],
        "D07": ["math", "chemistry", "english"],
        "C00": ["literature", "history", "geography"],
        "B00": ["math","biology", "chemistry"],
        "D01": ["math", "literature", "english"],
    }


    agrs = {
        "math": {"mean": 6.836442291524553, "std": 1.5354965095892972, "meannow": 6.636078660481128, "stdnow": 1.5671146978988335},
        "english": {"mean": 5.9092079364608905, "std": 2.206597448021071, "meannow": 5.152782928569674, "stdnow": 1.9449481793834826},
        "history": {"mean": 5.080244073978664, "std": 1.7465708926693815, "meannow": 6.455650267989012, "stdnow": 1.5577865101464672},
        "chemistry": {"mean":6.626887883072232, "std": 1.574503753310547, "meannow": 6.686574849486216, "stdnow": 1.588928435660692},
        "biology": {"mean":5.512567702665081, "std": 1.402295524426237, "meannow": 5.001529301777905, "stdnow": 1.4144475352591064},
        "physics": {"mean": 6.57996923135303, "std": 1.3691363438974284, "meannow": 6.729461973861576, "stdnow": 1.4288957061146286},
        "geography": {"mean": 7.0680099763985975, "std": 1.1147381370857605, "meannow": 6.765857567293365, "stdnow": 1.1735170775384047},
        "civil": {"mean": 8.394348466902459, "std": 1.145314959889694, "meannow": 8.033980967052898, "stdnow": 1.0644302754269304},
        "literature": {"mean": 6.612465517838241, "std": 1.259447225329555, "meannow": 6.654560386651909, "stdnow": 1.296653077856961}
    }

    # execute the SELECT query to retrieve data from the database
    query = """
        SELECT
            studentID,
            literature,
            math,
            english,
            physics,
            chemistry,
            biology,
            history,
            geography,
            civil,
            ProvinceCode,
            year
        FROM factscore
        WHERE studentID = %s and year=2022
    """
    cursor.execute(query, (student_id,))
    row = cursor.fetchone()


    if row:
        res={
            'studentID': row[0],
            'literature': row[1],
            'math': row[2],
            'english': row[3],
            'physics': row[4],
            'chemistry': row[5],
            'biology': row[6],
            'history': row[7],
            'geography': row[8],
            'year': row[11]
        }
        total=0
        equitot=0
        for subject in groups[code]:
            curent=float(res[subject])
            equi=(agrs[subject]["std"]/agrs[subject]["stdnow"])*(curent-agrs[subject]["meannow"])+agrs[subject]["mean"]
            total+=curent
            equitot+=equi
        # print(total)
        # print(equitot)
        res['total']=total
        res['equi']= f"{equitot:.2f}"
        query = "SELECT * FROM university WHERE Year = 2021 AND SubjectGroup = %s AND BenchMark < %s ORDER BY BenchMark DESC LIMIT 10;"
        cursor.execute(query, (code, equitot))
        rows = cursor.fetchall()
        res['rows']=rows
        return render_template('show.html', data=res)
        return res
    else:
        return 'Data not found'

# run the application
if __name__ == '__main__':
    app.run()
