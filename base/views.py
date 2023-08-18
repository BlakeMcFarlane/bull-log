from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .forms import CourseRegistrationForm
from .tasks import scrape_course_data
import time
from .models import SavedCourse
from django.http import JsonResponse


def saveCourse(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        subject = request.POST.get('subj')
        course_number = request.POST.get('crse')
        status = request.POST.get('status')
        class_id = request.POST.get('class_id')
        seats = request.POST.get('seats')
        seats_available = request.POST.get('seats_available')
        term=request.POST.get('term')        

        saved_class = SavedCourse.objects.create(
            title=title,
            subject=subject,
            course_number=course_number,
            availability=status,
            class_id=class_id,
            seats=seats,
            seats_avail=seats_available,
            term=term
        )

        scrape_course_data.delay()

    courses=SavedCourse.objects.all()
    
    return JsonResponse({'Saved Course':list(courses.values())})



def main(request):
    form = CourseRegistrationForm()

    saved_courses=SavedCourse.objects.all()
    saved_courses_titles = [course.title for course in saved_courses]
    
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

            for row in tble:
                if 'bs4.element.Tag' in str(type(row)):
                    course=row.find_all('td')
                
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
                            clas['class_id']=course[1].text
                            clas['seats']=course[12].text
                            clas['seats_avail']=course[13].text
                            classes.append(clas)


            context = {
                'form': form,
                'classes':classes,
                'saved_courses':saved_courses_titles,
                'term':term
            }

            return render(request, 'classes.html', context)
            
        else:
            form = CourseRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'main.html', context)



def trackedClasses(request):

    courses=SavedCourse.objects.all()

    context={
        'courses':courses
    }

    return render(request, 'tracked_classes.html', context)


