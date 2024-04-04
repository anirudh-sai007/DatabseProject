from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import random 
from .models import FALL22_S003_14_USER_TYPES,FALL22_S003_14_USERS,FALL22_S003_14_BOOKINGS,FALL22_S003_14_FEEDBACK

def index(request):
    return render(request,"index.html")


def employeedetails(request):
    sql='SELECT U.ID,U.FIRST_NAME,U.LAST_NAME,U.GENDER,U.EMAIL_ID,UT.TYPE FROM FALL22_S003_14_USERS U,FALL22_S003_14_USER_TYPES UT WHERE UT.id=U.FK_USER_TYPE_ID AND U.FK_USER_TYPE_ID!=1'
    details = FALL22_S003_14_USERS.objects.raw(sql)
    context = {'edetails':details}
    return render(request,'Employeedetails.html',context)

def customerdetails(request):
    details = FALL22_S003_14_USERS.objects.raw('SELECT * FROM LXV1537.FALL22_S003_14_USERS WHERE fk_user_type_id=1')
    context = {'edetails':details}
    print(list(details))
    return render(request,'Employeedetails.html',context)

def registreruser(request):
    context = {}
    if request.method == "POST":
        user=FALL22_S003_14_USERS()
        user.first_name=request.POST['firstname']
        user.last_name=request.POST['lastname']
        user.gender=request.POST.get('gender')
        user.email_id=request.POST['emailid']
        print(user.gender)
        user.is_vaccinated=request.POST.get('vaccinated')
        user.fk_user_type_id=FALL22_S003_14_USER_TYPES.objects.get(id=request.POST.get('usertype'))     
        user.save()
    return render(request,"registeruser.html",context)

def bookappointment(request):
    context={}
    if request.method == "POST":
        booking=FALL22_S003_14_BOOKINGS()
        service_type=request.POST.get('servicetype')
        sp_details = FALL22_S003_14_USERS.objects.raw('SELECT * FROM LXV1537.FALL22_S003_14_USERS WHERE fk_user_type_id='+service_type)
        random_choice=random.randint(1,len(sp_details)-1)
        print(sp_details[random_choice].id)
        booking.fk_service_provider_id=FALL22_S003_14_USERS.objects.get(id=sp_details[random_choice].id)
        booking.fk_customer_id=FALL22_S003_14_USERS.objects.get(id=request.POST['userid'])
        booking.decription=request.POST['description']
        booking.charges=random.uniform(10.5, 75.5)
        booking.status='Open'
        booking.save()
    return render(request,"bookappointment.html",context)

def bookingdetails(request):
    sql='SELECT B.id,U.id AS customer_id,U.first_name AS customer_name,U1.id AS service_provider_id,U1.first_name as service_provider_name,B.decription,B.charges,B.status FROM FALL22_S003_14_BOOKINGS B,FALL22_S003_14_USERS U,FALL22_S003_14_USERS U1 WHERE B.fk_customer_id=U.id AND B.FK_SERVICE_PROVIDER_ID=U1.id'
    details=FALL22_S003_14_BOOKINGS.objects.raw(sql)
    context={'bdetails':details}
    return render(request,'bookingdetails.html',context)

def report(request):
    sql='SELECT temp.id,UT1.type,temp.num_bookings,temp.total_income FROM FALL22_S003_14_USER_TYPES UT1 JOIN (SELECT UT.id,COUNT(B.id) AS num_bookings,SUM(B.charges)AS total_income FROM FALL22_S003_14_BOOKINGS B,FALL22_S003_14_USERS U,FALL22_S003_14_USER_TYPES UT WHERE  B.FK_SERVICE_PROVIDER_ID=U.id AND UT.id=U.fk_user_type_id GROUP BY (UT.id))temp ON UT1.id=temp.id'
    details=FALL22_S003_14_BOOKINGS.objects.raw(sql)
    context={'rdetails':details}
    return render(request,'report.html',context)

def bestratedserviceproviders(request):
    sql='select u.id,u.first_name,u.last_name,ar.avg_rating FROM Fall22_S003_14_users u JOIN  (SELECT b.fk_service_provider_id AS provider_id,AVG(f.rating) AS avg_rating FROM Fall22_S003_14_bookings b JOIN FALL22_S003_14_FEEDBACK f ON b.id=f.fk_booking_id GROUP BY (b.fk_service_provider_id) ORDER BY AVG(f.rating) DESC FETCH FIRST 5 ROWS ONLY) ar ON ar.provider_id=u.id;'
    details=FALL22_S003_14_USERS.objects.raw(sql)
    context={'bdetails':details}
    return render(request,'bestratedserviceproviders.html',context)

def inferiorfeedbackbyusers(request):
    sql='select u.id,u.first_name,u.last_name,ar.book_id,ar.rating,ar.comments FROM Fall22_S003_14_users u JOIN (SELECT b.id as book_id,b.fk_customer_id AS customer_id,f.rating,f.comments FROM Fall22_S003_14_bookings b JOIN FALL22_S003_14_FEEDBACK f ON b.id=f.fk_booking_id)ar ON ar.customer_id=u.id and ar.rating<3 ORDER BY ar.rating;'
    details=FALL22_S003_14_USERS.objects.raw(sql)
    context={'bdetails':details}
    return render(request,'inferiorfeedback.html',context)