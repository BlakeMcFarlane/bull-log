from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .forms import CourseRegistrationForm


def main(request):
    form = CourseRegistrationForm()

    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['semester']
            subj = form.cleaned_data['subject']
            crse = form.cleaned_data['course_number']

            url=f'https://usfonline.admin.usf.edu/pls/prod/bwckschd.p_disp_listcrse?term_in={term}&subj_in={subj}&crse_in={crse}&crn_in='
            link=requests.get(url).text
            content=BeautifulSoup(link, 'lxml')
            body=content.body
            table=body.find(class_='datadisplaytable')
            tble=table.contents[5:]   

            classes=[]
            tally=[]
            
            for row in tble:

                if 'bs4.element.Tag' in str(type(row)):
                    course=row.find_all('td')
                    length=len(course)
                    tally.append(length)
                    
                    if len(course)>1:
                        if course[2].text==subj:
                            clas={}
                            clas['subj']=course[2].text
                            clas['crse']=course[3].text
                            if course[0].text == 'C':
                                clas['availability']='Full'
                            else:
                                clas['availability']='Available'
                            clas['title']=course[6].text
                            clas['id']=course[1].text
                            clas['seats']=course[12].text
                            clas['seats_avail']=course[13].text
                            classes.append(clas)

            context = {
                'form': form,
                'url':url,
                'classes':classes
            }
            return render(request, 'classes.html', context)
                
        else:
            form = CourseRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'main.html', context)

