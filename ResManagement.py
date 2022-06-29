#import pandas as pd
import numpy as np
import random
import sqlite3 as sql
path = "C:\\Users\\Preeti\\OneDrive\\Desktop\\python projects\\RestaurantManagementAutomation\\"
dataset = path + "simplified-recipes-1M.npz"
data = np.load(dataset,allow_pickle=True)
print(data.files)
data['ingredients']


conn = sql.connect('Restaurant_Management')
arr= data["ingredients"]
arr = list(arr)


query = "CREATE TABLE RestroFood ( recipe VARCHAR(150) PRIMARY KEY , Ingredients VARCHAR(150), AmountNeeded VARCHAR(1000))"
conn.execute(query)
cnt = 0
for i in data['recipes']:
    cnt=cnt+1
    ing = ""
    amts = ""
    for j in i:
        ing += str(arr[j]) +","
        amts += str(random.randint(2,30))+","
    query = f"Insert into RestroFood values(\'Recipe {cnt}\',\'{ing}\',\'{amts}\')"
    conn.execute(query)
    
        
cursor = conn.execute("SELECT * FROM RestroFood")
count = 0
for row in cursor:
    print(row)
    count+=1
    if count>=10:
        break
    
    
    
    
    
    
    
arr = list(set(arr))
query = "CREATE TABLE IF NOT EXISTS PresentAmount ( Ingredient VARCHAR(150)  , Amount INT)"
conn.execute(query)
for i in arr:
    query = f"Insert into PresentAmount (Ingredient , Amount) values(\'{i}\',\'{random.randint(0,50)}\')"
    conn.execute(query)

cursor = conn.execute("SELECT * FROM PresentAmount")
cursor.fetchall()
count = 0
for row in cursor:
    print(row)
    count+=1
    if count>=10:
        break


conn.execute("CREATE TABLE ORDERS(ORDER_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, RECIPE VARCHAR(150) , QUANTITY INTEGER)" )



#RUN FROM HERE 

order , quant = input("order and amount").strip().split(',')
quant = int(quant)
cursor = conn.execute(f"SELECT Ingredients,AmountNeeded FROM RestroFood WHERE recipe = \'{order}\'")
for row in cursor:
    amtReq = row[1]
    amtReq =  list(amtReq.split(','))
    amtReq.pop()
    amtReq = [int(i) for i in amtReq]
    ing = row[0]
    ing = list(ing.split(','))
    ing.pop()
    
    
flag =0
c2 = conn.cursor()
for k,v in zip(ing,amtReq):
    c2.execute(f'''SELECT Amount FROM PresentAmount
               WHERE ingredient =\'{k}\'''')
    orgamt =c2.fetchone()[0]
    
    if v*quant > orgamt:
        flag = 1
        print(f"We do not have enough of {k}.")
        break

if flag == 0:
    for k,v in zip(ing,amtReq):
        c2.execute(f'''SELECT Amount FROM PresentAmount
                   WHERE ingredient =\'{k}\'''')
        orgamt =c2.fetchone()[0]
        orgamt = orgamt - v*quant
        conn.execute(f'''UPDATE PresentAmount 
                     SET Amount = {orgamt}
                     WHERE ingredient =\'{k}\'''')
        conn.execute(f'''INSERT INTO ORDERS(RECIPE,QUANTITY)
                     VALUES(\'{order}\',{quant}''')

c2.execute("SELECT * FROM ORDERS")
print(c2.fetchall())
        
        
    

#UPDATE INGREDIENTS

for i in arr:
    conn.execute(f'''UPDATE PresentAmount
               SET Amount = 200 
               WHERE Ingredient = \'{i}\'''')