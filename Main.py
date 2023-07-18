from os import system
from datetime import datetime
from time import sleep
from random import randint
from mysql import connector

Pass=input('Enter Mysql password:')
conn = connector.connect(host = 'localhost',user='root',password=Pass) 
Cursor = conn.cursor()
Cursor.execute('USE Bank_Data')

def st_input(mystr) :
    '''Function to take custom input'''

    Input=input(mystr) 
    if Input.lower() == 'q':
        print('You are logged off from your account.\nThanks for coming.!!')
        sleep(1)
        take_input()
    return Input

def re_input(mystr, errormsg='', func=lambda x: True) :
    '''Function to take custom input with some rules'''

    retry = True
    while retry:
        Input = st_input(mystr+":  ")
        if func(Input) :
            retry = False
        else:
            print(errormsg)
            print()
    return Input

def update_balance(amount):
    '''Function to update balance of user'''

    balance = get_details('balance',USER)
    balance+=int(amount)
    Cursor.execute(f'UPDATE User_Data SET balance = {balance} WHERE Username = "{USER}"')
    conn.commit()
    
def update_log(type,det={}):
    '''Function to update log_file'''

    if type=='change_pin':
        desp='Changed Pin'
    elif type=='transfer':
        desp=f"Transferred {det['amount']} to {det['ac']}"
    elif type=='withdraw':
        desp=f"Withdrawn {det['amount']}"

    cur=datetime.now()
    time=f'{cur.date()} {cur.hour}:{cur.minute}:{cur.second}'
    Cursor.execute(f"""INSERT INTO log_file (Date_and_Time ,Username,Account_no,Description) VALUES("{time}","{USER}","{get_details('account_no',USER)}","{desp}")""") 
    conn.commit()

def get_details(key,username,given_input=None) :
    '''Function to fetch User details'''

    l1=['username','password','account_no','name','dob','phone_no','balance']
    try:
        Cursor.execute(f"""SELECT * FROM User_data WHERE Username = "{username}" """)
        d=dict(zip(l1,Cursor.fetchone()))
        if key=='all':
            return d
        if given_input!=None:
            return d.get(key.lower())==given_input
        else:
            return d.get(key.lower())
    except Exception:
        pass   
        
def login(user, password) :
    '''Function for logging and performing functions '''

    system('cls')
    global USER,PASSWORD
    USER = user
    PASSWORD = password

    print("""Press :-
        1. Check account balance
        2. Transfer money
        3. Withdraw Money
        4. Change Pin
        5. Check Details
        6. Log out
        """) 
    ch=st_input('Enter choice: ')

    if ch=='1':
        # Check_balance
        balance = get_details('balance',USER)
        print('Your account balance - ', balance)

    elif ch=='2':
        # Transfer Money
        name = re_input("Enter the Reciever's name", 'Invalid name', lambda x: x.replace(' ','').isalpha())
        bank_name = re_input("Enter the Reciever's bank name",'Invalid bank name', lambda x: x.lower().find('bank')!=-1)             
        ifsc = re_input("Enter the Reciever's bank's IFSC code",'Invalid IFSC code', lambda x: x.isalnum() and len(x)==11)
        acc = re_input("Enter the Reciever's account number", 'Invalid account number',lambda x: x.isdigit())
        amount = re_input("Enter the amount",'Invalid amount/You don\'t have enough money', lambda x: int(x)<=get_details('balance',USER) if x.isdigit() else None)
        pin = re_input("Enter your pin")
        if pin==PASSWORD:
            update_balance(-int(amount)) 
            print(amount, 'is sent to', name, 'successfully') 
            update_log('transfer',{'amount':amount, 'ac':acc})
        else:
            print('Transaction failed\nYou entered invalid pin.')
        
    elif ch=='3':
        # Withdraw Money
        amount = re_input("Enter the amount",'Invalid amount/You don\'t have enough money', lambda x: int(x)<=get_details('balance',USER) if x.isdigit() else None)
        pin = re_input("Enter your pin")
        if pin==PASSWORD:
            update_balance(-int(amount)) 
            update_log('withdraw',{'amount':amount}) 
            print('Money withdrawl')
        else:
            print('Invalid PIN')

    elif ch=='4':
        # Change Pin
        old_p=re_input('Enter your old password', 'Incorrect Password', lambda x: x==PASSWORD) 
        new_p = re_input('Enter new password', 'Enter a valid password of length 4', lambda x: x.isdigit() and len(x)==4)
        Cursor.execute(f'UPDATE User_Data SET Password = "{new_p}" WHERE Username = "{USER}"')
        conn.commit()
        print('Your pin changed successfully')
        PASSWORD = new_p
        update_log('change_pin') 

    elif ch=='5':
        # Print Details of User
        det = get_details('all',USER)
        print()
        for k,v in det.items():
            print(k.capitalize(),'-',v)

    elif ch=='6':
        # Log Out
        print('You have been logged off successfully')
        return

    input('\nPress Enter to back..')
    login(USER,PASSWORD)   

def reg_user() :
    user = st_input("Set your Username: ")
    pin = re_input("Enter your pin",'Invalid PIN',lambda x: x.isdigit() and len(x)==4)
    acc = re_input("Enter your account number", 'Invalid account number',lambda x: x.isdigit() and len(x)==11)
    amount = re_input("Enter balance",'Invalid amount', lambda x: x.isdigit())
    name = re_input("Enter your name", 'Invalid name', lambda x: x.replace(' ','').isalpha())
    dob = re_input("Enter your Date of Birth [Separated by space (2000 01 01)]", 'Invalid DOB', lambda x: x.replace(' ','').isdigit())
    while 1:
        try:
            y,m,d = dob.split()
            if len(y)==4 and len(m)==2 and len(d)==2:
                dob="-".join(dob.split())
                break
        except Exception:
            dob = re_input("Enter your Date of Birth [Separated by space (2000 01 01)]", 'Invalid DOB', lambda x: x.replace(' ','').isdigit())
        
    phone = re_input("Enter your Phone", 'Invalid number', lambda x: x.isdigit() and len(x)==10)
    Cursor.execute(f"""INSERT INTO user_data VALUES ('{user}', '{pin}', '{acc}', '{name}', '{dob}', '{phone}', '{amount}')""")
    conn.commit()
    input('Account Registered\nPress Enter to Login..')
    
def take_input():
    system ('cls') 
    print('<><><><> Welcome to CV Bank <><><><>'.rjust(50))
    print('Press 1 to Login                    (Press "q" anytime to Quit)') 
    print('Press 2 to Register') 
    ch=st_input('Enter : ')
    if ch=='1':
        user = re_input('Enter your username', 'Invalid user id', lambda x: get_details('username',x,x))
        password=re_input('Enter login password', 'Your password is incorrect!!', lambda x: get_details('password',user, x)) 
        login(user, password)
    elif ch=='2':
        reg_user() 
    elif ch.lower()=='q':
        exit('Program Ended.!!')

while 1:
    take_input()
