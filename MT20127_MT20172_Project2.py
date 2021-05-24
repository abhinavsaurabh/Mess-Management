import pandas as pd
import numpy as np
from os import path

#class binding functions related to cook, viz. issueing materials,issueing graduate,complain etc.
class cooking:

    def add_cook(self, Cook_id,Name,Item,Quantity):#adding cook data to database
        cook_db = self.view_cookdb()
        cook_db = cook_db.reset_index()
        cook_db = cook_db.append(pd.DataFrame([[Cook_id,Name,Item,Quantity]],columns=cook_db.columns))
        cook_db.to_csv('cook_db.csv')
        cook_db = cook_db.set_index('Cook_id')
        return cook_db

    def view_cookdb(self):#display data stored in csv
        df = pd.read_csv('cook_db.csv',index_col=['Cook_id'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df

    def view_cooks_item(self):#history df material issues to cook 
        cook_db1 = pd.read_csv('cook_db.csv',index_col=['Cook_id'])
        return cook_db1

class sp:#funtions related to material ordered for mess 
    def __init_supplydb(self):
        sp_db = pd.DataFrame(columns=['Item_id','Name','delivered','Quantity'])
        sp_db.to_csv('sp_db.csv')

    def view_spdb(self):
        df = pd.read_csv('sp_db.csv',index_col=['Item_id'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df
    def view_indb(self):#displaying data stored in in_db.csv
        df = pd.read_csv('inventorydb.csv',index_col=['Item_id'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df
    def __init_inventory(self):#for the first order recieved ever , this funtion creates the inventorydb.csv
        in_db = pd.DataFrame(columns=['Item_id','Name','Quantity'])
        in_db.to_csv('inventorydb.csv')

    def delFromInventory(self,Item_id, quantity_ass):#once the material is issued to the cook and nothing is left then the data is deleted from the inventory database
        in_db = self.view_indb()
        saved = indb.loc[Item_id]['Quantity']
        indb.loc[Item_id ,'Quantity'] =saved - quantity_ass
    def addToInventory(self, Item_id,name,quantity):
        in_db = self.view_indb()
        if  in_db.empty:
            print("[INFO] Not Found Adding One")
            in_db = in_db.reset_index()
            in_db = in_db.append(pd.DataFrame([[Item_id,name,quantity]],columns=in_db.columns))
        elif(Item_id not in in_db.index.values):
            in_db = in_db.reset_index()
            in_db = in_db.append(pd.DataFrame([[Item_id,name,quantity]],columns=in_db.columns))
        else:
            print("[INFO] Found Existing One")
            crr_qty = in_db.loc[Item_id]['Quantity']
            in_db.loc[Item_id,'Quantity'] = quantity + crr_qty
        in_db.to_csv('inventorydb.csv')
        return in_db
    def add_items(self, item_id,name,quantity,status):#ordering items from market by the mess incharge and adding the material to supply database i.e. "sp_db.csv"
        sp_db = self.view_spdb()
        sp_db = sp_db.reset_index()
        sp_db = sp_db.append(pd.DataFrame([[item_id,name,status,quantity]],columns=sp_db.columns))
        sp_db.to_csv('sp_db.csv')
        return sp_db
    def change_status(self, item_id, status):#once the order of raw material from the market is recieved , the status can be changed from not 
                                            #delivered "ND" to "delivered" and the order data is deleted from sp_db.csv and added to 
                                            #inventory "inventorydb.csv"
        df = self.view_spdb()
        print("NAME : ",df.loc[item_id]['Name'] )
        data = df.loc[item_id]['Quantity']
        name = df.loc[item_id]['Name']
        print(data)
        if status == "yes":
            self.addToInventory(item_id,name,data)
            df = df.drop(item_id)
            df.to_csv('sp_db.csv')
        else:
            print("[INFO] Nothing Changed ")


class comp(cooking):#class binding functions related to regiteration of complains from both incharge and students 

    def complain(self, Cook_id,complaint):
        complain_db = self.view_complaindb()
        complain_db = complain_db.reset_index()
        complain_db = complain_db.append(pd.DataFrame([[Cook_id,complaint]],columns=complain_db.columns))
        complain_db.to_csv('complain_db.csv')
        complain_db = complain_db.set_index('Cook_id')

    def view_complain(self):
        complain_db1 = pd.read_csv('complain_db.csv',index_col=['Cook_id'])
        return complain_db1

    def view_complaindb(self):
        df = pd.read_csv('complain_db.csv',index_col=['Cook_id'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df

#class binding functions related to mess incharge operations 
class MessOps(comp,sp):

    def disp_db(self):#displaying 
        df = pd.read_csv('st_db.csv',index_col=['RollNo'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df

    def add_stu(self,roll_no,name,creds):#addition of data of newly enrolled student to "st_db.csv" 
        st_db = self.disp_db()
        st_db = st_db.reset_index()
        st_db = st_db.append(pd.DataFrame([[roll_no,name,creds]],columns=st_db.columns))
        st_db.to_csv('st_db.csv')
        st_db = st_db.set_index('RollNo')
        return st_db

    def remove_stu(self, roll_no):#widthdrawl for admission and deletion of student data from "st_db.csv"
        st_db = self.disp_db()
        st_db = st_db.drop(roll_no)
        st_db.to_csv('st_db.csv')
        return st_db


    def creds(self, roll_no,amt):#creds are equivalent to actual money in digital form , this funtion adds creds to student data 
        df = self.disp_db()
        curr_val = int(df.loc[roll_no]['creds'])
        df.at[roll_no,'creds']=curr_val+amt
        df.to_csv('st_db.csv')
        return df


    def stu_order_history(self, roll_no):#history of orders made by student till date along with date and time of ordering 
        try:
            df = self.view_order_db()
            df.reset_index()
            df = df.set_index('Reg. No.')
            return df.loc[roll_no]
        except:
            print("Oops!! No order Found")

    def view_order_db(self):
        df = pd.read_csv('orderdb.csv',index_col=['Order No.'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df



#class for binding funtion definations for student operations 
class studOps(comp):

    def view_order_db(self):
        df = pd.read_csv('orderdb.csv',index_col=['Order No.'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df

    def disp_db(self):
        df = pd.read_csv('st_db.csv',index_col=['RollNo'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df
    def view_order_db(self):
        df = pd.read_csv('orderdb.csv',index_col=['Order No.'])
        try:
            df = df.drop('Unnamed: 0',axis=1)
        except:
            return df
        else:
            return df


    def view_menu_db(self):
        menu_db = pd.read_csv('menu_db.csv',index_col=['Id'])
        return menu_db

    def order_amt(self, order_id):
        menu_db = self.view_menu_db()
        return float(menu_db.loc[order_id]['Price'])

    def debit(self, roll_no,amt):
        df = self.disp_db()
        curr_val = int(df.loc[roll_no]['creds'])
        if(curr_val>100):
            df.at[roll_no,'creds'] = (curr_val-amt)
        else:
            print("Sorry, Insufficient creds Balance")
        df.to_csv('st_db.csv')
        return df

    def stu_det(self, roll_no):
        df = self.disp_db()
        return df.loc[roll_no]

    def add_order(self, order_no,time,roll_no,order,amt):
        df = self.view_order_db()
        df = df.reset_index()
        df = df.append(pd.DataFrame([[order_no,time,roll_no,order,amt]],columns=df.columns))
        df.to_csv('orderdb.csv')
        df = df.set_index('Order No.')
        return df

def disp_db():
    df = pd.read_csv('st_db.csv',index_col=['RollNo'])
    try:
        df = df.drop('Unnamed: 0',axis=1)
    except:
        return df
    else:
        return df
def __initial_cookdb():
    cook_db = pd.DataFrame(columns=['Cook_id','Name','Item','Quantity'])
    cook_db.to_csv('cook_db.csv')
def __initial_cook():
    add_cook('MS19901','Ram Kumar','Mango','1kg')
    add_cook('MS19902','Sampath Kumar','Potato','2kg')
    add_cook('MS19903','Surya Dev','Onion','2kg')
    add_cook('MS19904','Juhi Patel','Tomato','2kg')
def view_cookdb():
    df = pd.read_csv('cook_db.csv',index_col=['Cook_id'])
    try:
        df = df.drop('Unnamed: 0',axis=1)
    except:
        return df
    else:
        return df
def __initial_compdb():
    complain_db = pd.DataFrame(columns=['Cook_id','Complain'])
    complain_db.to_csv('complain_db.csv')
def initial_comp():
    complain('MS19901',"Tomato Not Good")
    complain('MS19902',"Potato Looks Old")
    complain('MS19902',"Onion Was Not Of Good Quality")
def init():
    if path.exists("st_db.csv"):
        pass
    else:
        st_db = pd.DataFrame(columns=['RollNo','Name','creds'])
        st_db.to_csv('st_db.csv')
def init_db():
    m1 = MessOps()
    df = disp_db()
    if df.empty:
        m1.add_stu('MT20127','Abhinav',5000)
        m1.add_stu('MT20172','Aman',5000)
    else:
        pass
def gen_oid(self, curr_oid):
    curr_oid = curr_oid+1
    return curr_oid

def init_order_db():
    order_db = pd.DataFrame(columns=['Order No.','Time','Reg. No.','Order','Amount'])
    order_db.to_csv('orderdb.csv')


#Defining Mess Incharge Operations submenu 
#functioned called from main menu for mess incharge operations
init()
init_db()
init_order_db()
def mess_op():
    mess = MessOps()
    ck = cooking()
    print('\033[32m Choose : \033[00m')
    print('1. New Admission\n2. Withdraw Admissin\n3. Update Creds\n4. Records\n5. Student Data\n6. Order New Items for Mess\n7. Change the status of item \n8. Pantry')
    choice = input('Choose : ')
    if(choice == '1'):
        roll_no = input('Enter the roll number: ')
        df = mess.disp_db()
        try:
            df.loc[roll_no]
            print(df.loc[roll_no]['Name'])
            print("[WARNING !! ] User Exists")
        except:
            name = input('Enter the name: ')
            amt = input('Enter the paid amount: ')
            mess.add_stu(roll_no,name,amt)
            print("[INFO] User Added Successfully")
    elif(choice == '2'):
        roll_no = input('Enter the roll number: ')
        mess.remove_stu(roll_no)
    elif(choice == '3'):
        roll_no = input('Enter the roll number: ')
        amt = int(input('Enter the paid amount: '))
        mess.creds(roll_no,amt)
    elif(choice == '4'):
        print('1. Records of Student order\n2. Orders Placed History')
        ch = input('Enter your choice: ')
        if(ch == '1'):
            roll_no = input('Enter the roll number: ')
            try:
                print(mess.stu_order_history(roll_no))
            except:
                print('No orders placed yet')
                print(mess.stu_order_history(roll_no))
        elif(ch == '2'):
            print(mess.view_order_db())
        else:
            print('Invalid Input')
    elif(choice == '5'):
        print(mess.disp_db())
    elif(choice == '6'):
        Item_id = input('Enter the Item ID: ')
        name = input('Enter the name: ')
        quantity = int(input('Enter the quantity: '))
        status = input('Enter the status of item currently: ')
        mess.add_items(Item_id , name , quantity , status)
        dp = mess.view_spdb()
    elif(choice == '7'):
        Item_id = input('Enter the ID of Item of which you want to change the status of : ')
        #name = input('Enter the name of item: ')
        status = input(' Is it delivered or in the way ? [Yes/no]')
        mess.change_status(Item_id , status )
        #update_quant(Item_id , name , quantity)
    elif(choice =='8'):
        #mess.init_inventory()
        print('1. Issue item to cook\n2. Items Issued\n3. Quality Complaints')
        choice1 = input('Enter a choice from above: ')

        if(choice1 == '1'):
            Cook_id = input('Enter the Cook Id: ')
            Name = input('Enter the name: ')
            Item_Id= input('Enter the Item ID: ')
            Quantity = int(input('Enter the quantity:'))
            in_db = mess.view_indb()

            if in_db.values.size != 0:
                amount = int(in_db.loc[Item_Id , 'Quantity'])
                print(amount)
                item = in_db.loc[Item_Id]['Name']
                print(item)
                if amount >= Quantity:
                    ck.add_cook(Cook_id,Name,item,Quantity)
                    new_amount = amount - Quantity
                    in_db.loc[Item_Id, 'Quantity'] = new_amount
                    in_db.to_csv("inventorydb.csv")
                else:
                    print("Not Enough Item in Inventory")
            else:
                print("Empty Nothing Found")

        elif(choice1 == '2'):
            df = mess.view_cooks_item()
            print(df)

        elif(choice1 == '3'):
            print('1. Register Complain\n2. View Complain\n')
            choice2 = input('Enter a choice from above: ')

            if(choice2 == '1'):
                reg_no = input('Enter Cook id: ')
                Complaint = input('Enter Your Complain: ')
                mess.complain(reg_no,Complaint)

            elif(choice2 == '2'):
                df = mess.view_complaindb()
                print(df)
            else:
                print('Invalid Input')
        else:
                print('Invalid Input')
    else:
        print('Invalid')


#Defining Student Operations submenu 
#functioned called from main menu for student operations


def mess_st():
    stud = studOps()
    roll_no = input('Enter your Roll Number: ')

    try:
        stu_info = stud.stu_det(roll_no)
    except:
        print('INVALID ACCESS')
    else:
        print('\033[32m Choose : \033[00m')
        print('1. Would you like to order? \n2. Show A/C Details\n3. Register Complaints\n')
        choice = input()

        if(choice == '1'):
            total_amount = 0.00
            ord_detail = stud.view_order_db()
            prev_oid = ord_detail.index.values.tolist()
            try:
                prev_oid = prev_oid[-1]
            except:
                prev_oid = 0
            items = []
            while(1):
                df = stud.view_menu_db()
                print(df)
                item_id = input('Enter IDs of the dishes : ')
                item_id_l = item_id.split(',')
                for o in item_id_l:
                    items.append(df.loc[o]['Item'])
                    total_amount = total_amount + stud.order_amt(o)
                more = input('For more 0 , else 1 ')
                if(more == '0'):
                    continue
                else:
                    stud.debit(roll_no,total_amount)
                    stud.add_order((prev_oid+1),ctime(),roll_no,items,total_amount)
                    print('You ordered: ')
                    for i in items:
                        print(i)
                    print('\033[32m Your total amount is: \033[00m ',total_amount)
                    print('Order ID: ',prev_oid+1)
                    break
        elif(choice == '2'):
            print(stud.stu_det(roll_no))
        elif(choice == '3'):
            print(' Register Complain\n')
            reg_no = input('Enter Cook id: ')
            Complaint = input('Enter Your Complain: ')
            stud.complain(reg_no,Complaint)
        else:
            print('Invalid, try again')


#Main Menu for Choosing multiple operations 

def main():
    while(True):
        print('\033[32m Welcome To Hostel Mess Management System : \033[00m')
        print()
        choice = input('1. For Mess Operations \n2. For Student Operations \n\033[33m[#] >>\033[00m ')

        if(choice == "1"):
            mess_op()
        elif(choice == '2'):
            mess_st()
        elif(choice == 'exit'):
            print("[INFO] Bye Bye !!!")
            exit()
        else:
            print('[ERROR] Invalid Input It should be either 1 or 2 or exit')


# Using the special variable
# __name__
if __name__=="__main__":
    main()
