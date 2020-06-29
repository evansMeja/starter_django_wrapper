from django.contrib.auth import *
from django.db.models import *
from django.contrib.auth.models import *
from django.shortcuts import *
from django.http import JsonResponse
from django.shortcuts import *
from .views import *
from .models import *
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
import json

my_skill_set = ['Python','javascript']
URL = 'https://www.truelancer.com/freelance-jobs?category=&q=python'

def generate_acces_token():
    url = 'https://api.lulusms.com/v4/live/Login'
    body = {'UserName':'0740664839','Password':'36973233#Evans'}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    return r.json()['Token']
    
def register_endpoint(access_token,endpointurl):
    url = 'https://api.lulusms.com/v4/live/RegisterEndPoint'
    body = {'EndPoint':endpointurl}
    headers = {'content-type': 'application/json','Authorization': 'Bearer {}'.format(access_token)}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    return r.json()

def sendmessage(title,body):
    message=title + " - "+ body
    access_token = generate_acces_token()
    response = register_endpoint(access_token,'https://advertjet.com/profile-dashboard/endpoint')
    url = 'https://api.lulusms.com/v4/live/SendBulkSMS'
    body = {
        "From": "lulusms.com",
        "To": '254740664839',
        "SMS": message
    }
    headers = {'content-type': 'application/json','Authorization': 'Bearer {}'.format(access_token)}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    data = r.json()

def check_new_jobs(request):
    data={}
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_elems = soup.findAll("li", {"class": "job_item"})
    c=0
    data['job_exists'] = False
    for job_elem in job_elems:
        c+=1
        title_elem = job_elem.find('h3', class_='text-16')
        proposal_elem = job_elem.find('h5', class_='text-center')
        skill_elem = job_elem.findAll('li', class_='skillsmall')
        posted_skills = []
        for skill in skill_elem:
            posted_skills.append(skill.text)
            if skill.text in my_skill_set:
                # check if in database then add else skip
                database_string = title_elem.text + ' - ' + proposal_elem.text
                if Jobs.objects.filter(title=title_elem.text,body=proposal_elem.text).exists():
                    data['job'] = 'detected'
                    sendmessage(title_elem.text,proposal_elem.text)
                else:
                    obj = Jobs()
                    obj.title=title_elem.text
                    obj.body=proposal_elem.text
                    obj.save()
                    print(proposal_elem.text)
                    print(title_elem.text)
                    print(posted_skills)
                    print("-----------------------")
                    data['job_exists'] = True                    
    return JsonResponse(data)

def index(request):
    messages.add_message(request, messages.INFO, 'Hello world.')
    messages.warning(request, 'Your account expires in three days.')
    template_name = 'public_app/index.html'
    context={}
    return render(request,template_name,context)

def userlogout(request):
	logout(request)
	return redirect(reverse('index'))
    
def userlogin(request):
    template_name = 'public_app/login.html'
    context={}
    return render(request,template_name,context)
    
def register(request):
    template_name = 'public_app/register.html'
    context={}
    return render(request,template_name,context)

def validatelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = {}
        data['user_exists'] = False
        data['logged_in'] = False
        data['is_staff'] = False
        data['redirect_link'] = reverse('userlogin')
        if User.objects.filter(username=email).exists():
            data['user_exists'] = True
        if data['user_exists']:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                try:
                    login(request, user)
                    data['logged_in'] = True
                    if user.is_staff:
                        data['is_staff'] = True
                        data['redirect_link'] = reverse('admin_dashboard', args=(user.username,)) 
                    else:
                        data['redirect_link'] = reverse('user_dashboard', args=(user.username,))
                except:
                    data['logged_in'] = False
            else:
                data['logged_in'] = False
        return JsonResponse(data)

def registeruser(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = {}
        data['email_exists'] = False
        data['phone_exists'] = False
        # ensure that User email dont exist in the system
        if User.objects.filter(email=email).exists():
            data['email_exists'] = True
        # ensure that User phone number dont exist in the system
        if User_Detail.objects.filter(phone=phone).exists():
            data['phone_exists'] = True
        if data['email_exists'] or data['phone_exists']:
            print("pass")
        else:
            # create new user
            user = User.objects.create_user(username=email,password=password,email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # create new User_Detail
            user_detail_obj = User_Detail()
            user_detail_obj.owner = user
            user_detail_obj.phone = phone
            user_detail_obj.save()
        return JsonResponse(data)