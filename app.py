from flask import Flask, request,render_template
import joblib

app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template('index.html')

def bucket_cgpa(cgpa):
    if cgpa < 6:
        return 1
    elif cgpa < 8:
        return 2
    else:
        return 3


@app.route('/predict', methods=['POST',"GET"])
def predict():
    if request.method == 'POST':

        degree= int(request.form.get('degree'))
        technical_skills = int(request.form.get('technical_skills'))
        soft_skills = int(request.form.get('soft_skills'))
        cgpa = float(request.form.get('CGPA'))
        cgpa = bucket_cgpa(cgpa)
        projects = int(request.form.get('projects'))
        internships = int(request.form.get('internships'))
        csl= int(request.form.get('csl'))
        tsl= int(request.form.get('tsl'))
        years= int(request.form.get('years'))
        specialization = int(request.form.get('specialization'))

        project_exp=years*projects

        data= [[degree, technical_skills, soft_skills, cgpa, projects, internships, csl, tsl, years, specialization,project_exp]]
        model = joblib.load('salary_model.pkl')
        prediction = model.predict(data)

        degree_map = {
    1: "B.Sc",
    2: "B.Tech",
    3: "BCA",
    4: "M.Sc",
    5: "M.Tech",
    6: "MCA",
    7: "PhD"
}

        specialization_map = {
    1: "App Development",
    2: "Cybersecurity",
    3: "Data Science",
    4: "Cloud Computing",
    5: "AI/ML",
    6: "Web Development"
}


        return render_template('prediction.html',prediction=round(prediction[0],2),
            inputs={
                    'degree': degree_map.get(degree, "Unknown"),
                    'technical_skills': technical_skills,
                    'soft_skills': soft_skills,
                    'cgpa': cgpa,
                    'projects': projects,
                    'internships': internships,
                    'csl': csl,
                    'tsl': tsl,
                    'years': years,
                    'specialization': specialization_map.get(specialization, "Unknown")
                })
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
