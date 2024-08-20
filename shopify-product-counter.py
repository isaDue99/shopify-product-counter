###
### SETUP #################################
###
# (following this guide for custom private apps:
# https://shopify.github.io/shopify_python_api/?shpxid=82756cc9-564E-47B2-8899-A1F8B103C3B9
# )
# https://help.shopify.com/en/manual/apps/app-types/custom-apps
import shopify
import json

### access tokens from config file
with open('settings.json', 'r') as f:
    config = json.load(f)

API_KEY = config['API key']
ACCESS_TOKEN = config['Access token']
URL = config['Shop URL']

shop_url = "https://%s:%s@%s" % (API_KEY, ACCESS_TOKEN, URL)
shopify.ShopifyResource.set_site(shop_url)



###
### MAIN LOGIC #################################
###

### build GUI, set up basic window
# https://realpython.com/python-gui-tkinter/
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfile 
from os import path as osp
import csv


root = tk.Tk()
root.title("Shopify Product Counter")
root.geometry('600x500')
pat = "dd/MM/yyyy"


### functions with main logic
def count_products():
    min_date = calStart.get_date()
    max_date = calSlut.get_date()

    ### loading text
    lbl_count["text"] = "Counting..."

    ### query shopify for those dates
    # use retrieve count of products query with created_at_max and created_at_min parameters
    # https://shopify.dev/docs/api/admin-rest/2024-07/resources/product#get-products-count
    product_count = shopify.Product.count(created_at_min=min_date, created_at_max=max_date)

    ### display result
    lbl_count["text"] = f"Between {min_date} and {max_date} {product_count} products were uploaded!"

def mark_sales(path):
    # get "top selling products" csv file from shopify admin stats page 
    #   columns needed: product_id
    # add rows where the products unique id matches the unique id of a product from query of the timeperiod

    processtxt.set("")
    processtxt.set(f"Uploaded \"{osp.basename(path.name)}\". Working...")
    root.update()
    
    ############################### process product stats file
    # find columns of product_id
    with open(path.name, 'r', encoding="utf8") as dataf:
        data = list(csv.reader(dataf))
    pid_i = -1
    for i in range(len(data[0])):
        if data[0][i] == "product_id":
            pid_i = i

    if pid_i == -1:
        processtxt.set(processtxt.get() + "\n\nUnable to find product_id column.\nshopify-product-counter expects the first row of the product id column to contain the text \"product_id\".")
        return

    ################################ the shopify query part
    min_date = calStart.get_date()
    max_date = calSlut.get_date()

    # some settings for shopify query
    fields = "id"
    limit = 250 # default 50, max 250

    # is it a bulk operation?
    product_count = shopify.Product.count(created_at_min=min_date, created_at_max=max_date)
    if product_count > 250:
        # it is
        processtxt.set(processtxt.get() + f"\nMore than 250 products were created in this period. This may take a while...")
        root.update()
        prodlist = bulk_query(min_date, max_date, fields, limit, product_count)    
        product_ids = [prod.id for prod in prodlist]
    else:
        # it isnt
        prodlist = easy_query(min_date, max_date, fields, limit)
        product_ids = [prod.id for prod in prodlist]
    
    ################################## the comparing the two part
    # check product in each row of data and add to matches if it is found in shopify products data
    matches = []
    matches.append(data[0])
    data_vals = data[1:] # strip head
    count = 0
    for row in data_vals: # list from list of lists
        if int(row[pid_i]) in product_ids:
            matches.append(row)
            count = count + 1

    ### save as new file
    results_name = f"shopify-product-counter_result_{min_date}_{max_date}.csv"
    with open(results_name, 'w', encoding="utf8") as resultfile:
        writer = csv.writer(resultfile)
        writer.writerows(matches)

    ### display result
    processtxt.set(processtxt.get() + f"\n\n{count} out of the {len(data_vals)} products in \"{osp.basename(path.name)}\" \nwere created between {min_date} and {max_date}!\n\nResults saved in: \"{results_name}\"")


def easy_query(min_date, max_date, fields, limit):
    ### get product list from shopify
    products = shopify.Product.find(created_at_min=min_date, created_at_max=max_date, fields=fields, limit=limit)
    return products

def bulk_query(min_date, max_date, fields, limit, count):
    ### get product list from shopify (bulkstyle)
    # (tries paginationstyle first)
    processtxt.set(processtxt.get() + f"\n\nFound {count} products... ")
    root.update()
    txt = processtxt.get()

    curr_page = shopify.Product.find(created_at_min=min_date, created_at_max=max_date, fields=fields, limit=limit)
    prodlist = [prod for prod in curr_page]
    next_url = ""
    while curr_page.has_next_page():
        processtxt.set(txt + f"Fetched {len(prodlist)} products...")
        root.update()
        next_url = curr_page.next_page_url
        curr_page = shopify.Product.find(from_=next_url)
        prodlist.extend([prod for prod in curr_page])
    processtxt.set(txt + f"Fetched all {len(prodlist)} products!")
    return prodlist


### pack window's elements and start window loop
frm_dato = tk.Frame(master=root)

ttk.Label(master=frm_dato, text='Choose starting date').pack(padx=10, pady=10)
calStart = DateEntry(master=frm_dato, date_pattern=pat)
calStart.pack(padx=10, pady=10)

ttk.Label(master=frm_dato, text='Choose ending date').pack(padx=10, pady=10)
calSlut = DateEntry(master=frm_dato, date_pattern=pat)
calSlut.pack(padx=10, pady=10)

frm_dato.pack(padx=10, pady=10)

btn_calc = ttk.Button(master=root, text="Count products", command=count_products).pack(padx=10, pady=10)

lbl_count = ttk.Label(master=root, text="")
lbl_count.pack(padx=10, pady=10)

# upload fil
def open_file():
    file_path = askopenfile(mode='r', filetypes=[('.csv files', '.csv')])
    if file_path is not None:
        mark_sales(file_path)
        pass

btn_openfile = ttk.Button(master=root, text="Upload product stats spreadsheet", command=lambda:open_file())
btn_openfile.pack(padx=10, pady=10)

processtxt = tk.StringVar(master=root, value="NOTICE: A function that connects to Shopify will begin once a file is picked. \nThis may take some time, depending on how many products were uploaded in the selected time period.")
lbl_process = ttk.Label(master=root, textvariable=processtxt)
lbl_process.pack(padx=10, pady=10)

root.mainloop()