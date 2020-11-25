from django.shortcuts import render
from .models import Jd
import docx2txt

def home(request):
    # checking for post request method
    if request.method == 'POST' and request.FILES['resume']:
        jd_name = request.POST['jd']  # get jd name from user
        user_resume = request.FILES['resume']  #get user resume
        print(user_resume)
        db_jd = Jd.objects.filter(name=jd_name).values()    # get jd from db according to user jd name
        db_jd_path = db_jd[0]['jd'] # get jd path
        print(db_jd_path)
        # ML part
        if Jd.objects.get(name=jd_name):
            resume = docx2txt.process(user_resume)  # process user resume
            JD = docx2txt.process(f'media/{db_jd_path}')    #process db JD
            text = [resume , JD]
            from sklearn.feature_extraction.text import CountVectorizer
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text)
            from sklearn.metrics.pairwise import cosine_similarity
            #print("\n similarity Scores :")
            #print(cosine_similarity(count_matrix))
            mp = cosine_similarity(count_matrix)[0][1] * 100
            mp = round(mp,2)
            print("Your Resume Matches about " + str(mp) + "% of the job description.")          
            return render(request, 'home.html', {'mp': mp})
        else:
            print("error")

    else:
        return render(request, 'home.html')
