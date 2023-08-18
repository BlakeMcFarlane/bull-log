from bs4 import BeautifulSoup
import requests
from celery import shared_task
from .models import SavedCourse


@shared_task
def scrape_course_data():

    saved_courses = SavedCourse.objects.all()

    for saved_course in saved_courses:
        term = saved_course.term
        subj = saved_course.subject
        crse = saved_course.course_number
        class_id = saved_course.class_id

        url=f'https://usfonline.admin.usf.edu/pls/prod/bwckschd.p_disp_listcrse?term_in={term}&subj_in={subj}&crse_in={crse}&crn_in='
        link=requests.get(url).text
        content=BeautifulSoup(link, 'lxml')
        body=content.body
        table=body.find(class_='datadisplaytable')
        tble=table.contents[5:]   

        for row in tble:
            if 'bs4.element.Tag' in str(type(row)):
                course=row.find_all('td')

                if len(course)>1:
                    if course[1].text==class_id:
                        clas={}
        
                        if course[0].text == 'C':
                            clas['availability']='Full'
                        else:
                            clas['availability']='Available'


                        SavedCourse.objects.update(
                            title=course[6].text,
                            subject=course[2].text,
                            course_number=course[3].text,
                            availability=clas['availability'],
                            class_id=course[1].text,
                            seats=5,
                            seats_avail=course[13].text
                        )

        

