import json
import string
import random
from json import JSONDecodeError
from datetime import datetime

def Register(type,gamers_json_file,sellers_json_file,Email_ID,Username,Password,Contact_Number):
    '''Register Function || Already Given'''
    if type.lower()=='seller':
        f=open(sellers_json_file,'r+')
        d={
            "Email":Email_ID,
            "Username":Username,
            "Password":Password,
            "Contact Number":Contact_Number,
        }
        try:
            content=json.load(f)
            if d not in content and d["Username"] not in str(content):
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
        return True
    elif type.lower()=='gamer':
        f=open(gamers_json_file,'r+')
        d={
            "Email":Email_ID,
            "Username":Username,
            "Password":Password,
            "Contact Number":Contact_Number,
            "Wishlist":[],
            "Cart":[],
        }
        try:
            content=json.load(f)
            if d not in content and d["Username"] not in str(content):
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()

def Login(type,gamers_json_file,sellers_json_file,Username,Password):
    '''Login Functionality || Return True if successfully logged in else False || Already Given'''
    d=0
    if type.lower()=='seller':
        f=open(sellers_json_file,'r+')
    else:
        f=open(gamers_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        return False
    for i in range(len(content)):
        if content[i]["Username"]==Username and content[i]["Password"]==Password:
            d=1
            break
    f.seek(0)
    f.truncate()
    json.dump(content,f)
    f.close()
    if d==0:
        return False
    return True

def AutoGenerate_ProductID():
    '''Return a autogenerated random product ID || Already Given'''
    product_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=4))
    return product_ID

def AutoGenerate_OrderID():
    '''Return a autogenerated random product ID || Already Given'''
    Order_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Order_ID

def days_between(d1, d2):
    '''Calculating the number of days between two dates || Already Given'''
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def Create_Product(owner,product_json_file,product_ID,product_title,product_type,price_per_day,total_stock_available):
    '''Creating a product || Return True if successfully created else False'''
    '''Write your code below'''
    data_info ={
                    "Seller Username": owner,
                    "Product ID": product_ID,
                    "Product Title": product_title,
                    "Product Type": product_type,
                    "Price Per Day": price_per_day,
                    "Total Stock Available": total_stock_available
                }
    try:
        file = open(product_json_file, "r+")
        content = json.load(file)
        content.append(data_info)
        file.seek(0)
        file.truncate()
        json.dump(content, file)
    except JSONDecodeError:
        l = []
        l.append(data_info)
        json.dump(l, file)
    file.close()
    return True
    
def Fetch_all_Products_created_by_seller(owner,product_json_file):
    '''Get all products created by the seller(owner)'''
    '''Write your code below'''
    file = open(product_json_file, "r+")
    list_of_products = []
    try:
        content=json.load(file)
        for i in content:
            if i["Seller Username"] == owner:
                list_of_products.append(i)
    except JSONDecodeError:
        pass
    return list_of_products

def Fetch_all_products(products_json_file):
    '''Get all products created till now || Helper Function || Already Given'''
    All_Products_list=[]
    f=open(products_json_file,'r')
    try:
        content=json.load(f)
        All_Products_list=content
    except JSONDecodeError:
        pass
    return All_Products_list

def Fetch_Product_By_ID(product_json_file,product_ID):
    '''Get product deatils by product ID'''
    '''Write your code below'''
    file = open(product_json_file, "r+")
    list1_of_products = []
    try:
        content=json.load(file)
        for i in content:
            if i["Product ID"] == product_ID:
                list1_of_products.append(i)
    except JSONDecodeError:
        pass
    return list1_of_products

def Update_Product(Username,product_json_file,product_ID,detail_to_be_updated,new_value):
    '''Updating Product || Return True if successfully updated else False'''
    '''Write your code below'''
    file = open(product_json_file, "r+")
    content = json.load(file)
    for i in content:
        if i["Seller Username"]==Username and i["Product ID"] == product_ID:
            i[detail_to_be_updated] = new_value
            file.seek(0)
            file.truncate()
            json.dump(content, file)
            return True
    file.close()
    return False

def Add_item_to_wishlist(Username,product_ID,gamers_json_file):
    '''Add Items to wishlist || Return True if added successfully else False'''
    '''Write your code below'''
    file = open(gamers_json_file, "r+")
    content = json.load(file)
    for i in content:
        if i["Username"] == Username:
            i["Wishlist"].append(product_ID)
            file.seek(0)
            file.truncate()
            json.dump(content, file)
            return True
    file.close()
    return False

def Remove_item_from_wishlist(Username,product_ID,gamers_json_file):
    '''Remove items from wishlist || Return True if removed successfully else False'''
    '''Write your code below'''
    file = open(gamers_json_file, "r+")
    content = json.load(file)
    for i in content:
        if i["Username"] == Username:
            i["Wishlist"].remove(product_ID)
            file.seek(0)
            file.truncate()
            json.dump(content, file)
            return True
    file.close()
    return False
    
def Add_item_to_cart(Username,product_ID,Quantity,gamers_json_file,booking_start_date,booking_end_date,products_json_file):
    '''Add item to the cart || Check whether the quantity mentioned is available || Return True if added successfully else False'''
    '''Add the Product ID, Quantity, Price, Booking Start Date, Booking End Date in the cart as list of dictionaries'''
    '''Write your code below'''
    file = open (products_json_file, "r")
    content = json.load(file)
    price = 0
    for i in content:
        if i["Product ID"] == product_ID and i["Total Stock Available"] >= Quantity:
            price = i["Price Per Day"]
            item_data = {
                "Product ID": product_ID,
                "Quantity": Quantity,
                "Price": price,
                "Booking Start Date": booking_start_date,
                "Booking End Date": booking_end_date
            }
            file1 = open(gamers_json_file, "r+")
            content1 = json.load(file1)
            for i in content1:
                if i["Username"] == Username:
                    i["Cart"].append(item_data)
                    file1.seek(0)
                    file1.truncate()
                    json.dump(content1, file1)
                    return True
            file1.close()
    file.close()
    return False
    
def Remove_item_from_cart(Username,product_ID,gamers_json_file):
    '''Remove items from the cart || Return True if removed successfully else False'''
    '''Write your code below'''
    file = open(gamers_json_file, "r+")
    content = json.load(file)
    for i in content:
        if i["Username"] == Username:
            cart = i["Cart"]
            for x in range(len(cart)):
                if cart[x]["Product ID"] == product_ID:
                    i["Cart"].pop(x)
                    file.seek(0)
                    file.truncate()
                    json.dump(content, file)
                    return True
    file.close()
    return False
    
def View_Cart(Username,gamers_json_file):
    '''Return the current cart of the user'''
    '''Write your code below'''
    cart = []
    file = open(gamers_json_file, "r")
    try:
        content = json.load(file)
        for i in content:
            if i["Username"] == Username:
                cart = i["Cart"]
    except JSONDecodeError:
        pass
    return cart

def Place_order(Username,gamers_json_file,Order_Id,orders_json_file,products_json_file):
    '''Place order || Return True is order placed successfully else False || Decrease the quantity of the product orderd if successfull'''
    '''Write your code below'''
    file = open(gamers_json_file, "r")
    content = json.load(file)
    list_of_cart = []
    file. close()
    for i in list_of_cart:
        if i["Username"] == Username:
            if len(i["Cart"]) == 0:
                return False
            else:
                list_of_cart = i["Cart"]
    list_of_days = []
    list_of_quan = []
    list_of_price = []
    for i in list_of_cart:
        list_of_quan.append(i["Quantity"])
        list_of_price.append(i["Price"])
        start_date = i["Booking Start Date"].split("-")
        end_date = i["Booking End Date"].split("-")
        date_1 = date(int(start_date[0]),int(start_date[1]),int(start_date[2]))
        date_2 = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        num = (date_2-date_1).days
        list_of_days.append(num)
        with open(products_json_file, "r") as fp:
            content1 = json.load(fp)
        for x in content1:
            if x["Seller Username"] == Username:
                if x["Product ID"] == i["Product ID"]:
                    x["Total Stock Available"] = x["Total Stock Available"] - i["Quantity"]
                    with open(products_json_file, 'w') as fp1:
                        json.dump(content1, fp1)
            return True
    return False

def View_User_Details(gamers_json_file,Username):
    '''Return a list with all gamer details based on the username || return an empty list if username not found'''
    '''Write your code below'''
    file = open(gamers_json_file, "r+")
    list_of_products = []
    try:
        content = json.load(file)
        for i in content:
            if i["Username"] == Username:
                list_of_products.append(i)
    except JSONDecodeError:
        pass
    return list_of_products

def Update_User(gamers_json_file,Username,detail_to_be_updated,updated_detail):
    '''Update the detail_to_be_updated of the user to updated_detail || Return True if successful else False'''
    '''Write your code below'''
    file = open(gamers_json_file, "r+")
    content = json.load(fp)
    for i in content:
        if i["Username"]==Username :
            i[detail_to_be_updated] = updated_detail
            with open(gamers_json_file, "w") as fp1:
                json.dump(content, fp1)
            return True
    return False
    
def Fetch_all_orders(orders_json_file,Username):
    '''Fetch all previous orders for the user and return them as a list'''
    '''Write your code below'''
    list_of_orders = []
    file = open(orders_json_file, "r")
    content = json.load(file)
    for i in content:
        if i["Ordered by"] == Username:
            list_of_orders.append(i)
    return list_of_orders
    