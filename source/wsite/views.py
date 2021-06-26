from django.shortcuts import render, HttpResponse, redirect
from wsite.models import UserInfo
import datetime, calendar, json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.hashers import make_password
from django.db.models import F


# Create your views here.

# ~/
def dashboard(request):
  
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
def about(request):
  return render(request, 'about.html')




## Admin View Functions

#GET/POST ~/login
def adminLogin(request):
  if request.method == 'POST':
    username = request.POST.get('_username')
    password = request.POST.get('_password')
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
    return render(request, 'login.html')
    
#GET/POST ~/logout
def adminLogout(request):
  auth.logout(request)
  return redirect('login')
    
#GET/POST ~/ac-admin/change-password
def adminPassUpdate(request):
  if request.method == 'POST':
    if '_password' in request.POST and request.POST.get('_password'):
      password = make_password(request.POST.get('_password'))
      try:
        obj = admin_accounts.objects.get(_id=3)
        obj._password = password
        obj.save()
        messages.success(request, 'password updated')
      except admin_accounts.DoesNotExist:
        messages.error(request, 'user not found')
    else:
      messages.error(request, 'required parameter missing or invalid')
    return redirect('update_admin_pass')
  else:
    return render(request, 'admin/change_password.html')



## User View Functions

#GET/POST ~/accounts/new
def userCreate(request):
  if request.method == 'POST':
    
    name = request.POST.get('_name')
    email = request.POST.get('_email')
    contact = request.POST.get('_contact')
    password = make_password(request.POST.get('_password'))
    
    user = user_accounts(_name=name, _email=email, _contact=contact, _password=password)
    user.save()
    if user:
      messages.success(request, 'account created successfully')
    else:
      messages.error(request, 'something went wrong, try again')
    return redirect('create_user')
  else:
    return render(request, 'accounts/create.html')


#GET/POST ~/accounts/update/<id>
def userUpdate(request, id):
  if request.method == 'POST':
    if '_name' in request.POST and '_email' in request.POST and '_contact' in request.POST:
      try:
        obj = user_accounts.objects.get(_id=id)
        obj._name = request.POST.get('_name')
        obj._email = request.POST.get('_email')
        obj._contact = request.POST.get('_contact')
        obj.save()
        messages.success(request, 'account updated')
      except user_accounts.DoesNotExist:
        messages.error(request, 'user not found')
      return redirect('update_user', id)
      
    elif '_password' in request.POST:
      password = request.POST.get('_password')
      if password:
        try:
          obj = user_accounts.objects.get(_id=id)
          obj._password = password
          obj.save()
          messages.success(request, 'password updated')
        except user_accounts.DoesNotExist:
          messages.error(request, 'user not found')
      else:
        messages.error(request, 'required parameter missing or invalid')
      return redirect('update_user', id)
    else:
      return redirect('update_user', id)
  else:
    try:
      result = user_accounts.objects.get(_id = id)
      return render(request, 'accounts/edit.html', { 'data' : result })
    except user_accounts.DoesNotExist:
      return redirect('all_users')

#GET: ~/accounts/all
def usersAll(request):
  users_all = UserInfo.objects.filter(user__is_staff=0).order_by('-user__id')
  #users_all = UserInfo.objects.raw('SELECT * FROM wsite_UserInfo JOIN auth_User ON wsite_UserInfo.user_id = auth_User.id WHERE auth_User.is_staff = 0;')
  return render(request, 'accounts/all.html', { 'users' : users_all })

#GET: ~/accounts/active
def usersAct(request):
  users_active = UserInfo.objects.filter(status=1, user__is_staff=0).order_by('-user__id')
  return render(request, 'accounts/active.html', { 'users' : users_active })

#GET: ~/accounts/inactive
def usersDct(request):
  users_inactive = UserInfo.objects.filter(status=0, user__is_staff=0).order_by('-user__id')
  return render(request, 'accounts/inactive.html', { 'users' : users_inactive })

#GET: ~/accounts/suspended
def usersSus(request):
  users_suspended = UserInfo.objects.filter(status=9, user__is_staff=0).order_by('-user__id')
  return render(request, 'accounts/suspended.html', { 'users' : users_suspended })


#GET ~/accounts/lock/<id>
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
def userSearch(request):
  if request.method == 'GET':
    if request.is_ajax():
      if 'q' in request.GET and 's' in request.GET:
        query = request.GET.get('q')
        status = int(request.GET.get('s'))
        
        if status == 0:
          results = list(UserInfo.objects.filter(user__username__icontains = query, status = 0).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
        elif status == 1:
          results = list(UserInfo.objects.filter(user__username__icontains = query, status = 1).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
        elif status == 9:
          results = list(UserInfo.objects.filter(user__username__icontains = query, status = 9).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
        else:
          results = []
      elif 'q' in request.GET:
        query = request.GET.get('q')
        results = list(UserInfo.objects.filter(user__username__icontains = query).values(_id=F('user__id'), _name=F('user__first_name'), _email=F('user__email'), _contact=F('contact'), _reg_at=F('user__date_joined'), _status=F('status')))
      else:
        return JsonResponse({'msg': 'required parameter missing or invalid', 'data': []}, status = 400)

      return JsonResponse({'msg': 'success', 'data' : results}, status = 200)
    else:
      return JsonResponse({'msg': 'permission denied', 'data' : []}, status = 403)
  
  else:
    return JsonResponse({'msg': 'method not allowed', 'data': []}, status = 405)