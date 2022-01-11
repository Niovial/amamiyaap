import sys
from flask import Flask, render_template, abort, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
from datetime import *
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://EdithKwami:nuku@localhost:5432/Amamiya Sales Management System"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

#First table model
class branches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    telephone_num = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    region = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return (f"<id: {self.id} name: {self.name} tel_no: {self.telephone_num} "+
        f"lat: {self.latitude} long: {self.longitude} region: {self.region}>")


#Second table model
class user_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return (f"<id: {self.id} username: {self.username} password: {self.password}")


#Third table model
class employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    telephone_num = db.Column(db.String(), nullable=False)
    type_of_employee = db.Column(db.String(), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    user_account_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=True)

    def __repr__(self):
        return (f"<id: {self.id} name: {self.name} tel_no: {self.telephone_num} "+
        f"type: {self.type_of_employee} branch_id: {self.branch_id} user_account_id: {self.user_account_id}>")


#Fourth table model
class customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location =  db.Column(db.String(), nullable=False)
    telephone_num = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return (f"<id: {self.id} name: {self.name}  website: {self.website} "+
        f"lat: {self.latitude} long: {self.longitude} location: {self.location}"+
        f"tel_no: {self.telephone_num} email: {self.email}>")


#Fifth table model
class products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(), nullable=False)
    product_qty = db.Column(db.Integer, nullable=False)
    product_price_cedis = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return (f"<id: {self.id} product_name: {self.product_name} "+
        f"product_qty: {self.product_qty} product_price_cedis: {self.product_price_cedis}>")


#Sixth table model
class purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    occurred_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return (f"<id: {self.id} branch_id: {self.branch_id} "+
        f"customer_id: {self.customer_id} occured_at: {self.occurred_at}>")


#Seventh table model
class purchase_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'))
    product_id = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    product_purchase_qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (f"<id: {self.id} purchase_id: {self.purchase_id} product_id: {self.product_id} "+
        f"price_at_purchase: {self.price_at_purchase} product_purchase_qty: {self.product_purchase_qty}>")

db.create_all()


branchList = []
userAccountList = []
employeeList = []
customerList = []
productList = []
purchaseList = []
purchaseDetailsList = []

def appendTableRecords(table, dataList):
    queriedTableId = []
    results = table.query.with_entities(table.id).all()
    for items in results:
        queriedTableId.append(items[0])


    for items in dataList:
        if items.id not in queriedTableId:
            db.session.add(items)


#Here are all the records for the branches table:
accraBranch = branches(
    id = 10000001,
    name = "Accra Branch",
    telephone_num = "0245987456",
    latitude = 5.6167,
    longitude = 0.2508,
    region = "Greater Accra"
)
branchList.append(accraBranch)

takoradiBranch = branches(
    id = 10000002,
    name = "Takoradi Branch",
    telephone_num = "0558737770",
    latitude = 4.8693,
    longitude = 1.7647,
    region = "Western Region"
)
branchList.append(takoradiBranch)

capeCoastBranch = branches(
    id = 10000003,
    name = "Cape Coast Branch",
    telephone_num = "0247233876",
    latitude = 5.1267,
    longitude = 1.3101,
    region = "Central Region"
)
branchList.append(capeCoastBranch)

tamaleBranch = branches(
    id = 10000004,
    name = "Tamale Branch",
    telephone_num = "0208663444",
    latitude = 9.4398,
    longitude = 0.7862,
    region = "Northern Region"
)
branchList.append(tamaleBranch)

kumasiBranch = branches(
    id = 10000005,
    name = "Kumasi Branch",
    telephone_num = "0555475985",
    latitude = 6.2192,
    longitude = 0.3738,
    region = "Ashanti Region"
)
branchList.append(kumasiBranch)

koforiduaBranch = branches(
    id = 10000006,
    name = "Koforidua Branch",
    telephone_num = "0208663444",
    latitude = 6.0955,
    longitude = 0.2732,
    region = "Eastern Region"
)
branchList.append(koforiduaBranch)

hoBranch = branches(
    id = 10000007,
    name = "Ho Branch",
    telephone_num = "0240095433",
    latitude = 6.6121,
    longitude = 0.4585,
    region = "Volta Region"
)
branchList.append(hoBranch)

sunyaniBranch = branches(
    id = 10000008,
    name = "Sunyani Branch",
    telephone_num = "0541227519",
    latitude = 7.3149,
    longitude = 2.3323,
    region = "Bono Region"
)
branchList.append(sunyaniBranch)
#End of branch records//


#Here are the records for the user_accounts table:
acc1 = user_accounts(
    id = 40000001,
    username = "john",
    password = "yoquoi"
)
userAccountList.append(acc1)

acc2 = user_accounts(
    id = 40000002,
    username = "helen",
    password = "barch"
)
userAccountList.append(acc2)

acc3 = user_accounts(
    id = 40000003,
    username = "viola",
    password = "davis"
)
userAccountList.append(acc3)

acc4 = user_accounts(
    id = 40000004,
    username = "kofi",
    password = "agyeman"
)
userAccountList.append(acc4)

acc5 = user_accounts(
    id = 40000005,
    username = "theophilus",
    password = "kwami"
)
userAccountList.append(acc5)

acc6 = user_accounts(
    id = 40000006,
    username = "cassidy",
    password = "jones"
)
userAccountList.append(acc6)

acc7 = user_accounts(
    id = 40000007,
    username = "ama",
    password = "baidu"
)
userAccountList.append(acc7)

acc8 = user_accounts(
    id = 40000008,
    username = "nii",
    password = "baiden"
)
userAccountList.append(acc8)

acc9 = user_accounts(
    id = 40000009,
    username = "senam",
    password = "djotsi"
)
userAccountList.append(acc9)

acc10 = user_accounts(
    id = 40000010,
    username = "sameer",
    password = "ismaila"
)
userAccountList.append(acc10)

acc11 = user_accounts(
    id = 40000011,
    username = "jeremiah",
    password = "falsi"
)
userAccountList.append(acc11)

acc12 = user_accounts(
    id = 40000012,
    username = "david",
    password = "opoku"
)
userAccountList.append(acc12)

acc13 = user_accounts(
    id = 40000013,
    username = "stephen",
    password = "ofori"
)
userAccountList.append(acc13)

acc14 = user_accounts(
    id = 40000014,
    username = "frank",
    password = "appiah"
)
userAccountList.append(acc14)

acc15 = user_accounts(
    id = 40000015,
    username = "emmanuel",
    password = "amoah"
)
userAccountList.append(acc15)

acc16 = user_accounts(
    id = 40000016,
    username = "beatrice",
    password = "afful"
)
userAccountList.append(acc16)

acc17 = user_accounts(
    id = 40000017,
    username = "guest",
    password = "0000"
)
userAccountList.append(acc17)
#End of user_account records//


#Here are the records for the employees table:
em1 = employees(
    id = 20000001,
    name = "John Yoquoi",
    telephone_num = "0557349201",
    type_of_employee = "sales_rep",
    branch_id = 10000001,
    user_account_id = 40000001
)
employeeList.append(em1)

em2 = employees(
    id = 20000002,
    name = "Helen Barch",
    telephone_num = "0244552846",
    type_of_employee = "sales_rep",
    branch_id = 10000002,
    user_account_id = 40000002
)
employeeList.append(em2)

em3 = employees(
    id = 20000003,
    name = "Viola Davis",
    telephone_num = "0302784333",
    type_of_employee = "sales_rep",
    branch_id = 10000003,
    user_account_id = 40000003
)
employeeList.append(em3)

em4 = employees(
    id = 20000004,
    name = "Kofi Agyeman",
    telephone_num = "050999333",
    type_of_employee = "sales_rep",
    branch_id = 10000002,
    user_account_id = 40000004
)
employeeList.append(em4)

em5 = employees(
    id = 20000005,
    name = "Theophilus Kwami",
    telephone_num = "0540232204",
    type_of_employee = "sales_rep",
    branch_id = 10000004,
    user_account_id = 40000005
)
employeeList.append(em5)

em6 = employees(
    id = 20000006,
    name = "Cassidy Jones",
    telephone_num = "0202185555",
    type_of_employee = "sales_rep",
    branch_id = 10000006,
    user_account_id = 40000006
)
employeeList.append(em6)

em7 = employees(
    id = 20000007,
    name = "Ama Baidu",
    telephone_num = "0245194094",
    type_of_employee = "sales_rep",
    branch_id = 10000007,
    user_account_id = 40000007
)
employeeList.append(em7)

em8 = employees(
    id = 20000008,
    name = "Nii Baiden",
    telephone_num = "0540284105",
    type_of_employee = "sales_rep",
    branch_id = 10000005,
    user_account_id = 40000008
)
employeeList.append(em8)

em9 = employees(
    id = 20000009,
    name = "Senam Djotsi",
    telephone_num = "0277366999",
    type_of_employee = "sales_rep",
    branch_id = 10000001,
    user_account_id = 40000009
)
employeeList.append(em9)

em10 = employees(
    id = 20000010,
    name = "Sameer Ismaila",
    telephone_num = "0557775643",
    type_of_employee = "sales_rep",
    branch_id = 10000001,
    user_account_id = 40000010
)
employeeList.append(em10)

em11 = employees(
    id = 20000011,
    name = "Jeremiah Falsi",
    telephone_num = "0234722149",
    type_of_employee = "sales_rep",
    branch_id = 10000003,
    user_account_id = 40000011
)
employeeList.append(em11)

em12 = employees(
    id = 20000012,
    name = "David Opoku",
    telephone_num = "0243176457",
    type_of_employee = "sales_rep",
    branch_id = 10000008,
    user_account_id = 40000012
)
employeeList.append(em12)

em13 = employees(
    id = 20000013,
    name = "Stephen Ofori",
    telephone_num = "0559113577",
    type_of_employee = "sales_rep",
    branch_id = 10000007,
    user_account_id = 40000013
)
employeeList.append(em13)

em14 = employees(
    id = 20000014,
    name = "Frank Appiah",
    telephone_num = "0244883113",
    type_of_employee = "sales_rep",
    branch_id = 10000006,
    user_account_id = 40000014
)
employeeList.append(em14)

em15 = employees(
    id = 20000015,
    name = "Emmanuel Amoah",
    telephone_num = "0557774562",
    type_of_employee = "sales_rep",
    branch_id = 10000005,
    user_account_id = 40000015
)
employeeList.append(em15)

em16 = employees(
    id = 20000016,
    name = "Ibrahim Andoh",
    telephone_num = "0204772211",
    type_of_employee = "regular",
    branch_id = 10000001,
    user_account_id = 40000017
)
employeeList.append(em16)

em17 = employees(
    id = 20000017,
    name = "Mercy Sarfo",
    telephone_num = "0249435781",
    type_of_employee = "regular",
    branch_id = 10000001,
    user_account_id = 40000017
)
employeeList.append(em17)

em18 = employees(
    id = 20000018,
    name = "Beatrice Afful",
    telephone_num = "0208993666",
    type_of_employee = "admin",
    branch_id = 10000001,
    user_account_id = 40000016
)
employeeList.append(em18)

em19 = employees(
    id = 20000019,
    name = "Thomas Kwakye",
    telephone_num = "0554163444",
    type_of_employee = "regular",
    branch_id = 10000001,
    user_account_id = 40000017
)
employeeList.append(em19)
#End of employee records//


#Here are the records for the customers table:
customer1 = customers(
    id = 30000001,
    name = "Melcom Company Ltd.",
    website = "www.melcom.com",
    latitude = 5.6416,
    longitude = 0.1619,
    location = "Spintex Road",
    telephone_num = "0561112777",
    email = "info@melcomgroup.com",
)
customerList.append(customer1)

customer2 = customers(
    id = 30000002,
    name = "Game Ghana",
    website = "www.gamestores.com.gh",
    latitude = 5.6221,
    longitude = -0.1733,
    location = "Accra Mall",
    telephone_num = "0302740000",
    email = "gameaccra@mdd.co.za",
)
customerList.append(customer2)

customer3 = customers(
    id = 30000003,
    name = "Max Mart",
    website = "www.maxmartghana.com",
    latitude = 5.6416,
    longitude = -0.1516,
    location = "A & C Square, Jungle Avenue",
    telephone_num = "0302518881",
    email = "maxmart@maxmartghana.com",
)
customerList.append(customer3)

customer4 = customers(
    id = 30000004,
    name = "All Needs Super Market",
    website = "allneedsgh.com",
    latitude = 4.8999,
    longitude = -1.7628,
    location = "Justmoh Avenue",
    telephone_num = "0264551497",
    email = "info@allneedsgh.com",
)
customerList.append(customer4)

customer5 = customers(
    id = 30000005,
    name = "Garden Mart Shopping Centre",
    website = "www.gardenmartltd.webs.com",
    latitude = 4.8968,
    longitude = -1.7583,
    location = "Liberation Road",
    telephone_num = "0501303429",
    email = "garden_mart@yahoo.com",
)
customerList.append(customer5)

customer6 = customers(
    id = 30000006,
    name = "Zongo Market",
    website = "",
    latitude = 6.1067,
    longitude = -0.2543,
    location = "",
    telephone_num = "0241449304",
    email = "",
)
customerList.append(customer6)

customer7 = customers(
    id = 30000007,
    name = "Hwɛ Nea Awurade Ayɛ Provisions Shop",
    website = "",
    latitude = 6.0915,
    longitude = -0.2574,
    location = "Main Taxi Rank, Koforidua",
    telephone_num = "0243908244",
    email = "",
)
customerList.append(customer7)

customer8 = customers(
    id = 30000008,
    name = "DEFOUNTAIN SUPERMARKET",
    website = "",
    latitude = 5.1147,
    longitude = -1.2926,
    location = "Opposite science market, university of, Cape Coast",
    telephone_num = "0268268698",
    email = "",
)
customerList.append(customer8)

customer9 = customers(
    id = 30000009,
    name = "Sonturk Supermarket",
    website = "www.sonturk-supermarket.business.site",
    latitude = 5.1314,
    longitude = -1.2794,
    location = "",
    telephone_num = "0244646220",
    email = "",
)
customerList.append(customer9)

customer10 = customers(
    id = 30000010,
    name = "NEW LIFE SUPERMARKET",
    website = "",
    latitude = 6.7514,
    longitude = -1.6421,
    location = "",
    telephone_num = "0547127509",
    email = "",
)
customerList.append(customer10)

customer11 = customers(
    id = 30000011,
    name = "A-Life Supermarket",
    website = "",
    latitude = 6.6878,
    longitude = -1.6189,
    location = "1 Osei Tutu I Ave, Kumasi",
    telephone_num = "0322022432",
    email = "",
)
customerList.append(customer11)

customer12 = customers(
    id = 30000012,
    name = "RoSeb Enterprise",
    website = "",
    latitude = 6.5886,
    longitude = 0.4726,
    location = "Ho - Adidome Rd, Ho",
    telephone_num = "0208160444",
    email = "",
)
customerList.append(customer12)

customer13 = customers(
    id = 30000013,
    name = "BY HIS GRACE SHOP",
    website = "",
    latitude = 6.6098,
    longitude = 0.4748,
    location = "",
    telephone_num = "0244898498",
    email = "",
)
customerList.append(customer13)

customer14 = customers(
    id = 30000014,
    name = "Ryan A Mart",
    website = "",
    latitude = 7.3507,
    longitude = -2.3472,
    location = "Opposite Chesville Hotel, Berlin Top Road, Sunyani",
    telephone_num = "0240145043",
    email = "",
)
customerList.append(customer14)

customer15 = customers(
    id = 30000015,
    name = "Smj supermarket Tamale",
    website = "",
    latitude = 9.4268,
    longitude = -0.8470,
    location = "Mariam Rd, Tamale",
    telephone_num = "0503396000",
    email = "",
)
customerList.append(customer15)
#End of customer records//


#Here are the records for the products table:
product1 = products(
    id = 50000001,
    product_name = "bathing sponge",
    product_qty = 120,
    product_price_cedis = 33.25
)
productList.append(product1)

product2 = products(
    id = 50000002,
    product_name = "brown bread",
    product_qty = 120,
    product_price_cedis = 7.00
)
productList.append(product2)

product3 = products(
    id = 50000003,
    product_name = "Key Soap carton",
    product_qty = 120,
    product_price_cedis = 126.00
)
productList.append(product3)

product4 = products(
    id = 50000004,
    product_name = "Ariel soap",
    product_qty = 120,
    product_price_cedis = 45.00
)
productList.append(product4)

product5 = products(
    id = 50000005,
    product_name = "pack of grapes",
    product_qty = 120,
    product_price_cedis = 15.00
)
productList.append(product5)

product6 = products(
    id = 50000006,
    product_name = "Watermelon",
    product_qty = 200,
    product_price_cedis = 26.30
)
productList.append(product6)

product7 = products(
    id = 50000007,
    product_name = "Nutella",
    product_qty = 150,
    product_price_cedis = 25.00
)
productList.append(product7)

product8 = products(
    id = 50000008,
    product_name = "Choco Delight",
    product_qty = 150,
    product_price_cedis = 23.00
)
productList.append(product8)

product9 = products(
    id = 50000009,
    product_name = "Groundnut paste",
    product_qty = 140,
    product_price_cedis = 18.00
)
productList.append(product9)

product10 = products(
    id = 50000010,
    product_name = "Groundnut pack",
    product_qty = 113,
    product_price_cedis = 12.00
)
productList.append(product10)

product11 = products(
    id = 50000011,
    product_name = "Floor cleaner (gallon)",
    product_qty = 120,
    product_price_cedis = 37.00
)
productList.append(product11)

product12 = products(
    id = 50000012,
    product_name = "kitchen knife set",
    product_qty = 115,
    product_price_cedis = 100.00
)
productList.append(product12)

product13 = products(
    id = 50000013,
    product_name = "Window cleaner",
    product_qty = 120,
    product_price_cedis = 33.00
)
productList.append(product13)

product14 = products(
    id = 50000014,
    product_name = "Ideal milk can",
    product_qty = 150,
    product_price_cedis = 4.00
)
productList.append(product14)

product15 = products(
    id = 50000015,
    product_name = "Full cream milk carton",
    product_qty = 140,
    product_price_cedis = 15.40
)
productList.append(product15)

product16 = products(
    id = 50000016,
    product_name = "Springroll pack",
    product_qty = 130,
    product_price_cedis = 8.30
)
productList.append(product16)

product17 = products(
    id = 50000017,
    product_name = "Meatpie pack",
    product_qty = 125,
    product_price_cedis = 8.50
)
productList.append(product17)

product18 = products(
    id = 50000018,
    product_name = "Samosa pack",
    product_qty = 8,
    product_price_cedis = 125.00
)
productList.append(product18)

product19 = products(
    id = 50000019,
    product_name = "Vienna Salad pack",
    product_qty = 60,
    product_price_cedis = 9.10
)
productList.append(product19)

product20 = products(
    id = 50000020,
    product_name = "Tuna Salad pack",
    product_qty = 80,
    product_price_cedis = 9.00
)
productList.append(product20)

product21 = products(
    id = 50000021,
    product_name = "stainless steel spoon set",
    product_qty = 120,
    product_price_cedis = 24.00
)
productList.append(product21)

product22 = products(
    id = 50000022,
    product_name = "stainless steel fork set",
    product_qty = 120,
    product_price_cedis = 24.00
)
productList.append(product22)

product23 = products(
    id = 50000023,
    product_name = "lettuce pack",
    product_qty = 125,
    product_price_cedis = 11.00
)
productList.append(product23)

product24 = products(
    id = 50000024,
    product_name = "cucumber pack",
    product_qty = 128,
    product_price_cedis = 10.50
)
productList.append(product24)

product25 = products(
    id = 50000025,
    product_name = "Classic Salad pack",
    product_qty = 70,
    product_price_cedis = 9.30
)
productList.append(product25)

product26 = products(
    id = 50000026,
    product_name = "spring onions",
    product_qty = 130,
    product_price_cedis = 5.00
)
productList.append(product26)

product27 = products(
    id = 50000027,
    product_name = "sugar bread",
    product_qty = 100,
    product_price_cedis = 7.00
)
productList.append(product27)

product28 = products(
    id = 50000028,
    product_name = "butter bread",
    product_qty = 110,
    product_price_cedis = 7.00
)
productList.append(product28)
#End of product records//


#Here is the initial record for the purchase table:
initialPurchaseRecord = purchases(
    id = 70000001,
    branch_id = 10000001,
    occurred_at = '2007-05-08 12:35:29'
)
purchaseList.append(initialPurchaseRecord)
#Here is a few details for the intitial purchase:
initialPurchaseDetails = purchase_details(
    id = 60000001,
    purchase_id = 70000001,
    product_id = 50000015,
    price_at_purchase = 15.40,
    product_purchase_qty = 3
)
purchaseDetailsList.append(initialPurchaseDetails)
#Add all records to the database:
error = False
try:
    appendTableRecords(branches, branchList)
    appendTableRecords(user_accounts, userAccountList)
    appendTableRecords(employees, employeeList)
    appendTableRecords(customers, customerList)
    appendTableRecords(products, productList)
    appendTableRecords(purchases, purchaseList)
    appendTableRecords(purchase_details, purchaseDetailsList)
    db.session.commit()
except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
finally:
    db.session.close()


#App internals:
results = ''
tables = [branches, user_accounts, employees,
            customers, products, purchases,
            purchase_details]
current_purchase = ''
adminTable = ''


# User authentication for logging in to the application to work with data:
@app.route('/amamiya/loginAuth', methods=['POST'])
def loginAuth():
    username = request.form.get("username")
    password = request.form.get("password")
    authentication = ''
    authType = ''
    branch = ''
    users = user_accounts.query.join(employees).join(branches).with_entities(
        employees.type_of_employee, user_accounts.username,
        user_accounts.password, branches.id).all()

    for user in users:
       if username == user[1] and password == user[2]:
           authentication = True
           if user[0] == 'admin':
               authType = 'admin'

           elif user[0] == 'sales_rep':
               authType = 'sales_rep'
               branch = user[3]

           elif user[0] == 'regular':
               authType = 'regular'

    if authentication == True and authType == 'admin':
       return redirect(url_for('admin', success="true"))
    elif authentication == True and authType == 'sales_rep':
       return redirect(url_for('sales_rep', success="true", branchId=branch))
    elif authentication == True and authType == 'regular':
       return redirect(url_for('home', success="true"))
    else:
        return redirect(url_for('home', success="false"))


# Update the purchase table with details from the databse:
@app.route('/amamiya/sales_reps/details', methods=['POST'])
def details():
    error = False
    try:
        productName = request.get_json()["productName"]
        productQty = int(request.get_json()["productQty"])
        productCost = ''
        productId = ''
        unitPrice = ''
        goods = products.query.all()
        for product in goods:
            if productName.lower() == product.product_name.lower():
                unitPrice = product.product_price_cedis
                productCost = product.product_price_cedis * productQty
                productId = product.id
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify({
            "productName" : productName.lower(),
            "productQty" : productQty,
            "productId" : productId,
            "productCost" : productCost,
            "unitPrice" : unitPrice
        })

# Generate a live update of a purchase to the database:
@app.route('/amamiya/sales_reps/update_purchases', methods=['POST'])
def update_purchases():
    error = False
    try:
        # Get the branch id based on login credentials and the current datetime
        branchId = request.get_json()["b_id"]
        now = datetime.now()
        dateToday = now.strftime("%Y-%m-%d %H:%M:%S")
        detail_num = request.get_json()["detailNum"]

        # Get the customer id based on the customer name chosen by user
        customer_name = request.get_json()["customer"]
        customer = customers.query.filter(customers.name==customer_name).with_entities(
                    customers.id, customers.name).all()

        # Get the remaining data to make a purchase record
        id = request.get_json()["product_id"]
        quantity = request.get_json()["productQty"]
        price = request.get_json()["productPrice"]
        previousPurchase = purchases.query.order_by(purchases.id.desc()).first().id
        latest_purchase_detail = purchase_details.query.order_by(purchase_details.id.desc()).first().id

        # If first record in table, create a new purchase in purchases table
        # Additional condition: there must be a customer
        if detail_num == 1 and customer != []:
            newPurchase = purchases(
                    id = previousPurchase + 1,
                    branch_id = branchId,
                    customer_id = customer[0][0],
                    occurred_at = dateToday
                )
            db.session.add(newPurchase)
            db.session.commit()

            newPurchaseDetail = purchase_details(
                    id = latest_purchase_detail + 1,
                    purchase_id = previousPurchase + 1,
                    product_id = id,
                    price_at_purchase = price,
                    product_purchase_qty = quantity
                )
            db.session.add(newPurchaseDetail)
            db.session.commit()


        # Record is the first record, but there is no customer
        elif detail_num == 1 and customer == []:
            newPurchase = purchases(
                    id = previousPurchase + 1,
                    branch_id = branchId,
                    occurred_at = dateToday
                )
            db.session.add(newPurchase)
            db.session.commit()

            newPurchaseDetail = purchase_details(
                    id = latest_purchase_detail + 1,
                    purchase_id = previousPurchase + 1,
                    product_id = id,
                    price_at_purchase = price,
                    product_purchase_qty = quantity
                )
            db.session.add(newPurchaseDetail)
            db.session.commit()


        # Record is not the first record
        elif detail_num != 1:
            newPurchaseDetail = purchase_details(
                    id = latest_purchase_detail + 1,
                    purchase_id = previousPurchase,
                    product_id = id,
                    price_at_purchase = price,
                    product_purchase_qty = quantity
                )
            db.session.add(newPurchaseDetail)
            db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.expunge_all()
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify({
            "detailNum" : detail_num,
            "id" : id,
            "quantity" : quantity,
            "price" : price
        })


@app.route('/amamiya/sales_reps/summary', methods=['POST'])
def summary():
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')

    query = f"""SELECT p.id, pr.product_name AS p_name, pd.price_at_purchase AS p_price,
                pd.product_purchase_qty AS p_quantity, p.occurred_at
                    FROM purchases p
                    JOIN purchase_details pd
                        ON p.id = pd.purchase_id
                    JOIN products pr
                        ON pd.product_id = pr.id
                   WHERE  DATE_TRUNC('day', p.occurred_at) = '{today}'
                    ORDER BY p.occurred_at
            """
    my_query = db.text(query)
    data_query = db.session.execute(my_query).all()
    salesToday = []
    for record in data_query:
        salesToday.append(list(record))

    queryTwo = f"""SELECT p_name, p_quantity, (p_price*p_quantity)
                       FROM ({query}) AS goods_sold
                       GROUP BY 1, 2, 3;
                """
    my_queryTwo = db.text(queryTwo)
    data_queryTwo = db.session.execute(my_queryTwo).all()
    goodsSold = []
    for record in data_queryTwo:
        goodsSold.append(list(record))


    return jsonify({
        "salesToday" : salesToday,
        "goodsSold" : goodsSold
    })


@app.route('/amamiya/admin/branch_query', methods=['POST'])
def branch_query():
    branch_name = request.get_json()["branchName"]
    branch_table = []

    if branch_name == "--All--":
        query = branches.query.all()

        for record in query:
            record_tuple = (record.id, record.name, record.telephone_num,
                            record.latitude, record.longitude, record.region)
            branch_table.append(list(record_tuple))

    elif branch_name != "--All--":
        query = branches.query.filter(branches.name==branch_name).all()

        if query != []:
            for record in query:
                record_tuple = (record.id, record.name, record.telephone_num,
                                record.latitude, record.longitude, record.region)
                branch_table.append(list(record_tuple))

    return jsonify({
        "branch_table" : branch_table
    })


@app.route('/amamiya/admin/employee_query', methods=['POST'])
def employee_query():
    employee_name = request.get_json()["employeeName"]
    employee_table = []

    employee_by_branch = request.get_json()["employeeByBranch"]
    branch_employees = []

    if employee_name == "--All--":
        query = employees.query.join(branches).with_entities(
                employees.id, employees.name, employees.telephone_num,
                employees.type_of_employee, branches.name,
                employees.user_account_id).order_by(employees.id).all()

        if query != []:
            for record in query:
                employee_table.append(list(record))

    elif employee_name != "--All--":
        query = employees.query.join(branches).with_entities(
                employees.id, employees.name, employees.telephone_num,
                employees.type_of_employee, branches.name,
                employees.user_account_id).order_by(employees.id).\
                filter(employees.name==employee_name).all()

        if query != []:
            for record in query:
                employee_table.append(list(record))

    if employee_by_branch != "--All--":
        query = branches.query.join(employees).with_entities(
                employees.id, employees.name, employees.telephone_num,
                employees.type_of_employee, branches.name,
                employees.user_account_id).filter(branches.name == employee_by_branch).\
                order_by(employees.id).all()

        if query != []:
            for record in query:
                branch_employees.append(list(record))

    return jsonify({
        "employee_table" : employee_table,
        "branch_employees" : branch_employees
    })


@app.route('/amamiya/admin/customer_query', methods=['POST'])
def customer_query():
    customer_name = request.get_json()["customerName"]
    customers_table = []

    if customer_name == "--All--":
        query = customers.query.all()

        if query != []:
            for record in query:
                record_tuple = (record.id, record.name, record.website,
                                record.latitude, record.longitude, record.location,
                                record.telephone_num, record.email)
                customers_table.append(list(record_tuple))

    elif customer_name != "--All--":
        query = customers.query.filter(customers.name==customer_name).all()

        if query != []:
            for record in query:
                record_tuple = (record.id, record.name, record.website,
                                record.latitude, record.longitude, record.location,
                                record.telephone_num, record.email)
                customers_table.append(list(record_tuple))

    return jsonify({
        "customers_table" : customers_table
    })


@app.route('/amamiya/admin/product_query', methods=['POST'])
def product_query():
    product_name = request.get_json()["productName"]
    product_table = []

    if product_name == "--All--":
        query = products.query.all()

        if query != []:
            for record in query:
                record_tuple = (record.id, record.product_name, record.product_qty,
                                record.product_price_cedis)
                product_table.append(list(record_tuple))

    elif product_name != "--All--":
        query = products.query.filter(products.product_name==product_name).all()

        if query != []:
            for record in query:
                record_tuple = (record.id, record.product_name, record.product_qty,
                                record.product_price_cedis)
                product_table.append(list(record_tuple))


    return jsonify({
        "product_table" : product_table
    })


@app.route('/amamiya/admin/purchase_query', methods=['POST'])
def purchase_query():
    branch = request.get_json()["branch"]
    customer = request.get_json()["customer"]
    product = request.get_json()["product"]
    start_date = request.get_json()["startDate"]
    end_date = request.get_json()["endDate"]
    allTime = request.get_json()["allTime"]

    filter_list = [branch, customer, product, start_date, end_date, allTime]
    count = 0
    for filter in filter_list:
        if filter != "none" and filter != "" and filter != False:
            count += 1

    result_table = []

    if count == 1:
        # Query by start date:
        if start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = purchases.query.join(purchase_details).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, products.product_name,
                    purchase_details.product_purchase_qty,
                    purchase_details.price_at_purchase, purchases.occurred_at).\
                    filter(purchases.occurred_at >= lower_start_date,
                    purchases.occurred_at <= upper_start_date).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if allTime == True:
            query = purchases.query.join(purchase_details).join(branches,
            branches.id == purchases.branch_id).join(products,
            products.id == purchase_details.product_id).with_entities(
            purchase_details.purchase_id, branches.name, purchases.customer_id,
            products.product_name, purchase_details.price_at_purchase,
            purchase_details.product_purchase_qty,
            purchases.occurred_at).order_by(purchases.occurred_at.desc()).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))
                    print(record)

    elif count == 2:
        # Make a query for purchases with a date range:
        if start_date != "" and end_date != "":
            query = purchases.query.join(purchase_details).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, products.product_name,
                    purchase_details.price_at_purchase,
                    purchase_details.product_purchase_qty, purchases.occurred_at).\
                    filter(purchases.occurred_at >= start_date,
                    purchases.occurred_at <= end_date).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        # Query purchases by branch:
        if branch != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = branches.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, branches.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(purchases.occurred_at >= lower_start_date,
                    purchases.occurred_at <= upper_start_date, branches.name == branch).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if branch != "" and allTime == True:
            query = branches.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, branches.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(branches.name == branch).\
                    order_by(purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        # Query purchases by customer:
        if customer != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = customers.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, customers.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(purchases.occurred_at >= lower_start_date,
                    purchases.occurred_at <= upper_start_date,
                    customers.name == customer).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if customer != "" and allTime == True:
            query = customers.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, customers.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(customers.name == customer).\
                    order_by(purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        # Query purchases by product:
        if product != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = purchases.query.join(purchase_details).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, products.product_name,
                    purchase_details.product_purchase_qty, purchase_details.price_at_purchase,
                    purchases.occurred_at).filter(purchases.occurred_at >= lower_start_date,
                    purchases.occurred_at <= upper_start_date,
                    products.product_name == product).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if product != "" and allTime == True:
            query = purchases.query.join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, purchases.branch_id, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(products.product_name == product).\
                    order_by(purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

    elif count == 3:
        if branch != "" and start_date != "" and end_date != "":
            query = branches.query.join(purchases).join(purchase_details,
                purchases.id == purchase_details.purchase_id).join(products,
                products.id == purchase_details.product_id).with_entities(
                purchase_details.purchase_id, branches.name, products.product_name,
                purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                purchases.occurred_at).filter(purchases.occurred_at >= start_date,
                purchases.occurred_at <= end_date,
                branches.name == branch).order_by(
                purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if branch != "" and product != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = branches.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, branches.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(purchases.occurred_at >= lower_start_date,
                    purchases.occurred_at <= upper_start_date,
                    branches.name == branch, products.product_name == product).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if branch != "" and product != "" and allTime == True:
            query = branches.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, branches.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(branches.name == branch,
                    products.product_name == product).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if branch != "" and customer != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = purchases.query.join(branches).join(customers, customers.id == purchases.customer_id).\
                    join(purchase_details, purchases.id == purchase_details.purchase_id).\
                    join(products, products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, branches.name, customers.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(branches.name == branch, customers.name == customer,
                    purchases.occurred_at >= lower_start_date, purchases.occurred_at <= upper_start_date).all()

            if query != []:
               for record in query:
                   result_table.append(list(record))

        if branch != "" and customer != "" and allTime == True:
            query = purchases.query.join(branches).join(customers,
                    customers.id == purchases.customer_id).\
                    join(purchase_details, purchases.id == purchase_details.purchase_id).\
                    join(products, products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, branches.name, customers.name,
                    products.product_name, purchase_details.price_at_purchase,
                    purchase_details.product_purchase_qty, purchases.occurred_at).\
                    filter(branches.name == branch, customers.name == customer).all()

            if query != []:
               for record in query:
                   result_table.append(list(record))


        if customer != "" and start_date != "" and end_date != "":
            query = customers.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    products.id == purchase_details.product_id).with_entities(
                    purchase_details.purchase_id, customers.name, products.product_name,
                    purchase_details.price_at_purchase, purchase_details.product_purchase_qty,
                    purchases.occurred_at).filter(purchases.occurred_at >= start_date,
                    purchases.occurred_at <= end_date,
                    customers.name == customer).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if customer != "" and product != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = customers.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, customers.name, products.product_name,
                    purchase_details.product_purchase_qty, purchase_details.price_at_purchase,
                    purchases.occurred_at).filter(purchases.occurred_at >= lower_start_date,
                    purchases.occurred_at <= upper_start_date,
                    customers.name == customer, products.product_name == product).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if customer != "" and product != "" and allTime == True:
            query = customers.query.join(purchases).join(purchase_details,
                    purchases.id == purchase_details.purchase_id).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, customers.name, products.product_name,
                    purchase_details.product_purchase_qty, purchase_details.price_at_purchase,
                    purchases.occurred_at).filter(customers.name == customer,
                    products.product_name == product).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))


        if product != "" and start_date != "" and end_date != "":
            query = purchases.query.join(purchase_details).join(products,
                    purchase_details.product_id == products.id).with_entities(
                    purchase_details.purchase_id, products.product_name,
                    purchase_details.product_purchase_qty, purchase_details.price_at_purchase,
                    purchases.occurred_at).filter(purchases.occurred_at >= start_date,
                    purchases.occurred_at <= end_date,
                    products.product_name == product).order_by(
                    purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

    elif count == 4:
        if branch != "" and customer != "" and product != "" and start_date != "":
            lower_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            upper_start_date = lower_start_date + timedelta(hours=23, minutes=59, seconds=59)

            query = purchases.query.join(branches).join(customers,
                purchases.customer_id == customers.id).join(purchase_details,
                purchases.id == purchase_details.purchase_id).join(products,
                products.id == purchase_details.product_id).with_entities(
                purchase_details.purchase_id, branches.name, customers.name,
                products.product_name, purchase_details.price_at_purchase,
                purchase_details.product_purchase_qty, purchases.occurred_at).filter(
                branches.name == branch, customers.name == customer,
                products.product_name == product, purchases.occurred_at >= lower_start_date,
                purchases.occurred_at <= upper_start_date).\
                order_by(purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

        if branch != "" and customer != "" and product != "" and allTime == True:
            query = purchases.query.join(branches).join(customers,
                purchases.customer_id == customers.id).join(purchase_details,
                purchases.id == purchase_details.purchase_id).join(products,
                products.id == purchase_details.product_id).with_entities(
                purchase_details.purchase_id, branches.name, customers.name,
                products.product_name, purchase_details.price_at_purchase,
                purchase_details.product_purchase_qty, purchases.occurred_at).filter(
                branches.name == branch, customers.name == customer,
                products.product_name == product).\
                order_by(purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))

    elif count == 5:
        if (branch != "" and customer != "" and product != "" and start_date != ""
            and end_date != ""):
            query = purchases.query.join(branches).join(customers,
                purchases.customer_id == customers.id).join(purchase_details,
                purchases.id == purchase_details.purchase_id).join(products,
                products.id == purchase_details.product_id).with_entities(
                purchase_details.purchase_id, branches.name, customers.name,
                products.product_name, purchase_details.price_at_purchase,
                purchase_details.product_purchase_qty, purchases.occurred_at).filter(
                branches.name == branch, customers.name == customer,
                products.product_name == product, purchases.occurred_at >= start_date,
                purchases.occurred_at <= end_date).\
                order_by(purchase_details.purchase_id).all()

            if query != []:
                for record in query:
                    result_table.append(list(record))


    return jsonify({
        "resultTable" : result_table
    })



@app.route('/amamiya/admin')
def admin():
    success = request.args.get("success")
    if success == "true":
        return render_template('admins.html',
        branches=branches.query.order_by(branches.id).all(),
        userAccounts=user_accounts.query.order_by(user_accounts.id).all(),
        employees=employees.query.order_by(employees.id).all(),
        customers=customers.query.order_by(customers.id).all(),
        products=products.query.order_by(products.id).all(),
        purchases=purchases.query.order_by(purchases.id).all(),
        purchaseDetails=purchase_details.query.order_by(purchase_details.id).all())
    else:
        return redirect(url_for('home', success="false"))


@app.route('/amamiya/sales_reps')
def sales_rep():
    success = request.args.get("success")
    branchId = request.args.get('branchId')

    if success == "true":
        return render_template('sales_reps.html', products=products.query.all(),
        branches=branches.query.all(), customers=customers.query.all(),
        branchId=branchId)
    else:
        return redirect(url_for('home', success="false"))


@app.route('/')
def home():
    success = request.args.get('success')
    return render_template('home.html', success=success)

if __name__ == "__main__":
    app.run()


"""Another thing is that the admin should never be able to see the passwords of others.
    Another thing is that the admin should be able to delete items from the database,
    as well as to update items in the database (products, branch info, employees, customers).
"""
