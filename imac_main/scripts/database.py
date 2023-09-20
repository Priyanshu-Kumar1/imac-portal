import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


def fbsignupwrite(uid, name, email, acc_type, password):
    ref = db.reference('users')
    ref.child(uid).set({
        'email': email,
        'name': name,
        'type': acc_type,
        'password': password,
        'approved': False
    })
    ref = db.reference('unapproved_users')
    ref.child(uid).set({
        'name': name,
        'acc_type': acc_type,
        'type': 'Account Pending',
    })
    return uid

def fbloginread(uid):
    ref = db.reference('users')
    return ref.child(uid).get()

def fbbookingreq(uid, name, acc_type, lab_no, sysid, time_from, time_till, reason):
    ref = db.reference('unapproved_requests')
    ref.child(uid).set({
        'name': name,
        'acc_type': acc_type,
        'type': 'Booking Request Pending',
        "sys_no": sysid,
        "lab_no": lab_no,
        "time_from": time_from,
        "time_till": time_till,
        'reason': reason
    })
    return uid

def getuserapproval_list():
    ref = db.reference('unapproved_users')
    return ref.get()

def get_unapproved_booking_requests():
    ref = db.reference('unapproved_requests')
    return ref.get()


def fbapprove_user(uid):
    ref = db.reference('unapproved_users')
    ref.child(uid).delete()
    ref = db.reference('users')
    ref.child(uid).child("approved").set(True)

def fbapprove_booking(uid):
    unapproved_booking_list = get_unapproved_booking_requests()
    ref = db.reference('users')
    bookingid = unapproved_booking_list[uid]
    lab=bookingid['lab_no']
    sysid=bookingid['sys_no']
    data = {
        'sys_no': bookingid['sys_no'],
        'time_from': bookingid['time_from'],
        'time_till': bookingid['time_till'],
        'reason': bookingid['reason']
    }
    
    ref.child(uid).child("booking history").push(data)
    ref = db.reference('booked_seats')
    sysid = sysid.replace("System No - ", "")
    data = {
        "uid": uid,
        'time_from': bookingid['time_from'],
        'time_till': bookingid['time_till'],
        'reason': bookingid['reason']
    }
    if "," in sysid:
        sysid = sysid.split(",")
        for i in sysid:
            ref.child(f"lab {lab}").child(eval(i)).set(data)
    else:
        ref.child(f"lab {lab}").child(eval(sysid)).set(data)
    ref = db.reference('unapproved_requests')
    ref.child(uid).delete()

    
def get_booked_seats(lab):
    ref = db.reference('booked_seats')
    return ref.child(f"lab {lab}").get()
    


def fbstoreseats():
    ref = db.reference("seats_row")
    sys_no = 0
    lab = 4
    for row in range(1,9):
        for col in range(1,9):
            if row == 1 and col == 5:
                data = {
                'sys_no': "Pillar",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'reason': '',
            }
            elif row == 2 and col == 5:
                data = {
                'sys_no': "Piller",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'reason': '',
            }
            elif row == 6 and col == 5:
                data = {
                'sys_no': "Piller",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'reason': '',
            }
            elif row == 7 and col == 5:
                data = {
                'sys_no': "Piller",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'reason': '',
            }
            else:
                sys_no += 1
                data = {
                    'sys_no': sys_no,
                    'status': '',
                    'uid': '',
                    'time_from': '',
                    'time_till': '',
                    'reason': '',
                }
            ref.child(f"lab {lab}").child(f"{col}").child(f"row {col}").set(data)
    


def getallseats(lab):
    ref = db.reference("seats")
    return ref.child(f"lab {lab}").get()


if __name__ == "__main__":
    cred = credentials.Certificate('imac_main/scripts/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://i-mac-portal-lab-database-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
    fbstoreseats()

