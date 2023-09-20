from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from imac_main.scripts.fbauth import fbsignup, fblogin, fblogout
from imac_main.scripts.database import fbloginread, getuserapproval_list, fbapprove_user, fbapprove_booking, getallseats, fbbookingreq, get_unapproved_booking_requests, get_booked_seats
from django.core.cache import cache

# Create your views here.

class user():
    def __init__(self, uid, name, email, acc_type, password):
        self.uid = uid
        self.name = name
        self.email = email
        self.acc_type = acc_type

User = user(None, None, None, None, None)

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def signupPost(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        if "@srmist.edu.in" not in email:
            return HttpResponse("Invalid email address. Please use your SRM email address.")
        else:
            acc_type = request.POST.get('type')
            password = request.POST.get('password')
            uid = fbsignup(name, email, acc_type, password)
            return HttpResponseRedirect('/')
        
def logout(request):
    fblogout()
    return HttpResponseRedirect('/')

def login(request):
    cache.clear()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        uid, User.name, User.acc_type, approved = fblogin(email, password)
        User.uid = uid["localId"]
        User.email = uid["email"]

        if uid != None:
            if User.acc_type == 'Admin':
                return HttpResponseRedirect('/adminportal')
            else:
                return HttpResponseRedirect('/portal_pending')
        else:
            return HttpResponse('Invalid credentials')

def adminportal(request):
    userapproval_list = getuserapproval_list()
    bookingapproval_list = get_unapproved_booking_requests()
    context={'userapproval_list': userapproval_list, "bookingapproval_list": bookingapproval_list, 'name': User.name}
    return render(request, 'adminportal.html', context)

def approve_user(request):
    uid = request.POST.get('uid')
    fbapprove_user(uid)
    return HttpResponseRedirect('/adminportal')

def approve_booking(request):
    uid = request.POST.get('uid')
    fbapprove_booking(uid)
    return HttpResponseRedirect('/adminportal')

def portal(request):
    lab_no = 1
    seats = getallseats(lab_no)
    try:
        booked_seats = get_booked_seats(lab_no).keys()
        booked_seats = [int(x) for x in list(booked_seats)]
    except:
        booked_seats = []
    row1 = seats["row 1"]
    row2 = seats["row 2"]
    row3 = seats["row 3"]
    row4 = seats["row 4"]
    row5 = seats["row 5"]
    row6 = seats["row 6"]
    row7 = seats["row 7"]
    
    context = {
        'lab_no': lab_no,
        'booked_seats': booked_seats,
        'rows': {
            'row1': row1[1:],
            'row2': row2[1:],
            'row3': row3[1:],
            'row4': row4[1:],
            'row5': row5[1:],
            'row6': row6[1:],
            'row7': row7[1:],
        }
    }
    if User.acc_type == 'Student':
        return render(request, 'studentportal.html', context)
    else:
        return render(request, 'facultyportal.html', context)

def loadlab(request):
    lab_no = request.POST.get('labid')
    try:
        booked_seats = get_booked_seats(lab_no).keys()
        booked_seats = [int(x) for x in list(booked_seats)]
    except:
        booked_seats = []
    if lab_no < '3':
        seats = getallseats(lab_no)
        row1 = seats["row 1"]
        row2 = seats["row 2"]
        row3 = seats["row 3"]
        row4 = seats["row 4"]
        row5 = seats["row 5"]
        row6 = seats["row 6"]
        row7 = seats["row 7"]
        
        context = {
            'lab_no': lab_no,
            'booked_seats': booked_seats,
            'rows': {
                'row1': row1[1:],
                'row2': row2[1:],
                'row3': row3[1:],
                'row4': row4[1:],
                'row5': row5[1:],
                'row6': row6[1:],
                'row7': row7[1:],
            }
        }
    else:
        seats = getallseats(lab_no)
        row1 = seats["row 1"]
        row2 = seats["row 2"]
        row3 = seats["row 3"]
        row4 = seats["row 4"]
        row5 = seats["row 5"]
        row6 = seats["row 6"]
        row7 = seats["row 7"]
        row8 = seats["row 8"]
        
        context = {
            'lab_no': lab_no,
            'booked_seats': booked_seats,
            'rows': {
                'row1': row1[1:],
                'row2': row2[1:],
                'row3': row3[1:],
                'row4': row4[1:],
                'row5': row5[1:],
                'row6': row6[1:],
                'row7': row7[1:],
                'row8': row8[1:],
            }
        }
    if User.acc_type == 'Student':
        return render(request, 'studentportal.html', context)
    else:
        return render(request, 'facultyportal.html', context)


def portal_pending(request):
    approved = fbloginread(User.uid)
    approved = approved["approved"]
    if approved:
        return HttpResponseRedirect('/portal')
    else:
        return render(request, 'portal-nopermission.html')
    
def submitreq(request):
    if request.method == 'POST':
        sysid = request.POST.get('sys-no')
        lab_no = request.POST.get('lab-no')[0]
        time_from = request.POST.get('time_from')
        time_till = request.POST.get('time_till')
        reason = request.POST.get('reason')
        uid = User.uid
        name = User.name
        acc_type = User.acc_type
        fbbookingreq(uid, name, acc_type, lab_no, sysid, time_from, time_till, reason)
    return HttpResponseRedirect('/portal')