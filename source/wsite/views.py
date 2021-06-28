from django.shortcuts import render, HttpResponse, redirect
from wsite.models import UserInfo
import datetime, calendar, json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import F
import uuid

# Create your views here.

# ~/
@login_required(login_url='/login/')
def dashboard(request):
  page_title = 'Home - Account Manager'
  all_u = UserInfo.objects.filter(user__is_staff = 0).count()
  act_u = UserInfo.objects.filter(status = 1, user__is_staff = 0).count()
  ina_u = UserInfo.objects.filter(status = 0, user__is_staff = 0).count()
  sus_u = UserInfo.objects.filter(status = 9, user__is_staff = 0).count()
  
  today = datetime.datetime.now().strftime('%b %d, %Y - %A')
  c_day = int(datetime.datetime.now().strftime('%d'))
  c_month = datetime.datetime.now().month
  c_month_name = datetime.datetime.now().strftime('%B')
  c_year = datetime.datetime.now().year

  #data for line chart
  reg_eachday = []
  days_thismonth = calendar.monthrange(c_year, c_month)[1]
  day = 1;
  
  if days_thismonth == 30:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
  elif days_thismonth == 28:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
  elif days_thismonth == 29:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
  else:
    labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]

  while day <= days_thismonth:
    reg_onthatday = UserInfo.objects.filter(user__date_joined__day = day, user__date_joined__month = c_month, user__is_staff = 0).count()
    reg_eachday.append(reg_onthatday)
    if day == c_day:
      break;
    day += 1
  
  linedata = {
    'labels' : labels,
    'datasets' : [{
      'label' : 'User Registered',
      'data' : reg_eachday,
      'borderColor' : '#3e95cd'
    }]
  }
  linedata = json.dumps(linedata)

  #data for bar chart
  reg_eachmonth = []
  reg_barcolor = []
  month = 1
  while month <= 12:
    if month <= c_month:
      reg_onthatmonth = UserInfo.objects.filter(user__date_joined__month = month, user__date_joined__year = c_year, user__is_staff = 0).count()
      reg_eachmonth.append(reg_onthatmonth)
      reg_barcolor.append('#3ecd42')
    else:
      break
    month += 1
    
    bardata = {
      'labels' : ["Jan" , "Feb" , "Mar" , "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      'datasets' : [{
        'backgroundColor' : reg_barcolor,
        'label' : 'User Registered',
        'data' : reg_eachmonth
      }]
    }
    bardata = json.dumps(bardata)
  
  #data for doughnut chart
  doughnutdata = {
    'labels' : ['Active', 'Inactive', 'Suspended'],
    'datasets' : [{
      'backgroundColor' : ["#5ee25e", "#ff4a4a", "#a9a6a6"],
      'data' : [act_u, ina_u, sus_u]
    }]
  }
  doughnutdata = json.dumps(doughnutdata)

  data = {
    'page_title' : page_title,
    'date' : today,
    'month' : c_month_name,
    'year' : c_year,
    'accounts' : {
      'all' : all_u,
      'active' : act_u,
      'inactive' : ina_u,
      'suspended' : sus_u
    },
    'charts' : {
      'line' : linedata,
      'bar' : bardata,
      'doughnut' : doughnutdata
    }
  }
  return render(request, 'dashboard.html', data)
  #return HttpResponse('this is home')
  
  
# ~/about
@login_required(login_url='/login/')
def about(request):
  page_title = 'This Project'
  return render(request, 'about.html', { 'page_title' : page_title })

#GET/POST ~/login
def adminLogin(request):
  page_title = 'Welcome to accounts!'
  if request.method == 'POST':
    username = request.POST.get('_username')
    password = request.POST.get('_password')
    request.session['username'] = username
    if username and password:
      user = auth.authenticate(username=username, password=password)
      if user:
        auth.login(request, user)
        return redirect('dashboard')
      else:
        messages.error(request, 'username or password is incorrect')
        return redirect('login')
    else:
      messages.error(request, 'invalid credentials')
      return redirect('login')
      
  else:
    return render(request, 'login.html', { 'page_title' : page_title })
    
#GET/POST ~/logout
@login_required(login_url='/login/')
def adminLogout(request):
  auth.logout(request)
  return redirect('login')
    
#GET/POST ~/ac-admin/change-password
@login_required(login_url='/login/')
def adminPassUpdate(request):
  page_title = 'Change Admin Password'
  if request.method == 'POST':
    if '_password' in request.POST and request.POST.get('_password'):
      password = make_password(request.POST.get('_password'))
      try:
        obj = User.objects.get(id = request.user.id)
        obj.password = password
        obj.save()
        auth.update_session_auth_hash(request, obj)
        messages.success(request, 'password updated')
      except User.DoesNotExist:
        messages.error(request, 'user not found')
    else:
      messages.error(request, 'required parameter missing or invalid')
    return redirect('update_admin_pass')
  else:
    return render(request, 'admin/change_password.html', { 'page_title' : page_title })



## User View Functions

#GET/POST ~/accounts/new
@login_required(login_url='/login/')
def userCreate(request):
  page_title = 'Create Account'
  if request.method == 'POST':
    
    username = uuid.uuid4().hex[:8].upper()
    name = request.POST.get('_name')
    email = request.POST.get('_email')
    contact = request.POST.get('_contact')
    password = make_password(request.POST.get('_password'))
    
    #uname_check = User.objects.filter(username=username).exists()
    try:
      user = User.objects.create_user(username=username, first_name=name, email=email, password=password)
      info = UserInfo(user=user, contact=contact)
      info.save()
      messages.success(request, 'account created successfully')
    except Exception as e:
        messages.error(request, e) #'something went wrong, try again')
    return redirect('create_user')
  else:
    return render(request, 'accounts/create.html', { 'page_title' : page_title })


#GET/POST ~/accounts/update/<id>
@login_required(login_url='/login/')
def userUpdate(request, id):
  page_title = 'Update Account'
  if request.method == 'POST':
    if '_name' in request.POST and '_email' in request.POST and '_contact' in request.POST:
      try:
        #base = User.objects.get(id = id)
        #base.first_name = request.POST.get('_name')
        #base.email = request.POST.get('_email')
        extended = UserInfo.objects.get(user = id)
        extended.user.first_name = request.POST.get('_name')
        extended.user.email = request.POST.get('_email')
        extended.contact = request.POST.get('_contact')
        extended.user.save()
        extended.save()
        messages.success(request, 'account updated')
      except UserInfo.DoesNotExist:
        messages.error(request, 'user not found')
      return redirect('update_user', id)
      
    elif '_password' in request.POST:
      password = request.POST.get('_password')
      if password:
        password = make_password(password)
        try:
          npass = UserInfo.objects.get(user = id)
          npass.user.password = password
          npass.user.save()
          messages.success(request, 'password updated')
        except UserInfo.DoesNotExist:
          messages.error(request, 'user not found')
      else:
        messages.error(request, 'required parameter missing or invalid')
      return redirect('update_user', id)
    else:
      return redirect('update_user', id)
  else:
    try:
      result = UserInfo.objects.get(user__id = id, user__is_staff = 0)
      return render(request, 'accounts/edit.html', { 'page_title' : page_title, 'data' : result })
    except UserInfo.DoesNotExist:
      return redirect('all_users')

#GET: ~/accounts/all
@login_required(login_url='/login/')
def usersAll(request):
  page_title = 'User Accounts'
  users_all = UserInfo.objects.filter(user__is_staff=0).order_by('-user__id')
  #users_all = UserInfo.objects.raw('SELECT * FROM wsite_UserInfo JOIN auth_User ON wsite_UserInfo.user_id = auth_User.id WHERE auth_User.is_staff = 0;')
  return render(request, 'accounts/all.html', { 'page_title' : page_title, 'users' : users_all })

#GET: ~/accounts/active
@login_required(login_url='/login/')
def usersAct(request):
  page_title = 'Active User Accounts'
  users_active = UserInfo.objects.filter(status=1, user__is_staff=0).order_by('-user__id')
  return render(request, 'accounts/active.html', { 'page_title' : page_title, 'users' : users_active })

#GET: ~/accounts/inactive
@login_required(login_url='/login/')
def usersDct(request):
  page_title = 'Inactive User Accounts'
  users_inactive = UserInfo.objects.filter(status=0, user__is_staff=0).order_by('-user__id')
  return render(request, 'accounts/inactive.html', { 'page_title' : page_title, 'users' : users_inactive })

#GET: ~/accounts/suspended
@login_required(login_url='/login/')
def usersSus(request):
  page_title = 'suspended User Accounts'
  users_suspended = UserInfo.objects.filter(status=9, user__is_staff=0).order_by('-user__id')
  return render(request, 'accounts/suspended.html', { 'page_title' : page_title, 'users' : users_suspended })


#GET ~/accounts/lock/<id>
@login_required(login_url='/login/')
def userLock(request, id):
  if request.method == 'GET':
    if id > 0:
      data = UserInfo.objects.get(user__id=id)
      data.status = 0
      data.save()
      messages.success(request, 'account locked')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, 'invalid user')
      return redirect(request.META.get('HTTP_REFERER'))
  else:
    messages.error(request, 'invalid request method')
    return redirect(request.META.get('HTTP_REFERER'))

#GET ~/accounts/unlock/<id>
@login_required(login_url='/login/')
def userUnlock(request, id):
  if request.method == 'GET':
    if id > 0:
      data = UserInfo.objects.get(user__id=id)
      data.status = 1
      data.save()
      messages.success(request, 'account unlocked')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return redirect(request.META.get('HTTP_REFERER'))
  else:
    return redirect(request.META.get('HTTP_REFERER'))

#GET ~/accounts/activate/<id>
@login_required(login_url='/login/')
def userActivate(request, id):
  if request.method == 'GET':
    if id > 0:
      data = UserInfo.objects.get(user__id=id)
      data.status = 1
      data.save()
      messages.success(request, 'account activated')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return redirect(request.META.get('HTTP_REFERER'))
  else:
    return redirect(request.META.get('HTTP_REFERER'))

#GET ~/accounts/suspend/<id>
@login_required(login_url='/login/')
def userSuspend(request, id):
  if request.method == 'GET':
    if id > 0:
      data = UserInfo.objects.get(user__id=id)
      data.status = 9
      data.save()
      messages.success(request, 'account suspended')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return redirect(request.META.get('HTTP_REFERER'))
  else:
    return redirect(request.META.get('HTTP_REFERER'))

#POST ~/accounts/search
@login_required(login_url='/login/')
def userSearch(request):
  if request.method == 'GET':
    if request.is_ajax():
      if 'q' in request.GET and 's' in request.GET:
        query = request.GET.get('q')
        status = int(request.GET.get('s'))
        
        if status == 0:
          results = list(UserInfo.objects.filter(user__first_name__icontains = query, user__is_staff = 0, status = 0).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
        elif status == 1:
          results = list(UserInfo.objects.filter(user__first_name__icontains = query, user__is_staff = 0, status = 1).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
        elif status == 9:
          results = list(UserInfo.objects.filter(user__first_name__icontainsname__icontains = query, user__is_staff = 0, status = 9).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
        else:
          results = []
      elif 'q' in request.GET:
        query = request.GET.get('q')
        results = list(UserInfo.objects.filter(user__first_name__icontains = query, user__is_staff = 0).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
      else:
        return JsonResponse({'msg': 'required parameter missing or invalid', 'data': []}, status = 400)

      return JsonResponse({'msg': 'success', 'data' : results}, status = 200)
    else:
      return JsonResponse({'msg': 'permission denied', 'data' : []}, status = 403)
  
  else:
    return JsonResponse({'msg': 'method not allowed', 'data': []}, status = 405)