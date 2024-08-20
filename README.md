# Shopify Product Counter

Portable program that counts how many products were created in a Shopify webshop between two given dates. Can also filter `.csv` files containing product IDs.

I wrote this script as part of an internship at a certain shop, which ran from June 24th to July 19th 2024 - this is a generic version of that script, since I imagine it could be useful to someone else out there! I don't plan to work more on this, but feel free to use as-is or develop it further if you need - a link or reference back to me would be greatly appreciated!

## Download and building

A pre-built binary program is available for **Windows.** You can find it under [Releases](https://github.com/isaDue99/shopify-product-counter/releases).

You can also build the program yourself. The program was written in Python3 with a host of dependencies, and I used Pyinstaller to build them. Once you have all those installed you can use the batch-script `build.bat` to build.

However, if you already have a Python interpreter and the programs' dependencies installed, then you can also run the programs from the commandline interface (CLI) with the following command:

`python shopify-product-counter.py`

## Set up

**Before you can use the program you need to install it in the Shopify Admin.** [Heres a guide from Shopify on how to do that](https://help.shopify.com/en/manual/apps/app-types/custom-apps). Note that:
- This script only needs the `read_products` API access scope
- This script doesn't use webhooks

Then you need to insert the following information into the `settings.json` file:

- **API key:** 32 characters long
- **Access token:** the Admin API token for the app, only shown once!
- **Shop URL:** in the form "yourshopname.myshopify.com/admin"

Save the settings.json file, and you're good to go!

## Usage

To start the program, double-click on the binary .exe file or run the command `python shopify-product-counter.py`. Please allow the program a couple of seconds to start. Note that the `settings.json` file needs to be in the same folder as the program.

Once the program has started you'll be greeted by a window containing:
- Two drop-down menus that allow you to select a start- and end-date for a time period(*)
- A button labelled "Count products" that, when clicked, queries the Shopify API to count how many products in your shop's catalog were created in this time period(*)
- A button labelled "Upload product stats spreadsheet" that, when clicked, opens a file picker

Using the file picker, the program expects an Comma Separated Values-file (`.csv`) containing AT LEAST:
- A column containing unique product IDs; The first row of the column must contain the label `product_id`; These IDs are numeric, and can also be seen at the end of the URL of that product's settings page in the Shopify Admin

Once a file has been chosen, the program will process each row and see whether the corresponding product was created in the time period defined by what the date-menus are currently set to. If a product with a given ID *WAS* created in this time period, then the entire row the ID belongs to is copied into a resulting `.cvs` file, named `shopify-product-counter_result_(chosen start-date)_(chosen end-date)`, which is placed into the same folder that the program is in.

(*) The exact time that Shopify interprets the dates as is just after midnight (at 00:00:00) at the start of the given day. This means the time period includes all products created on the start-date, but doesnt include any products created on the end-date! E.g. if you wished to count the products uploaded on July 21st 2024, then you need to set the start-date to July 21st 2024, and the end-date to July 22nd 2024.

**Note:** When running correctly, the program window will update pretty frequently. If the window stops updating for an extended period of time (>1 minute), then it's very likely that an error has occured, and the window can be closed. This is a simple program, so it doesn't have much in the way of error-reporting in these cases; if you must find out what's causing the error, then I recommend running the program using a python interpreter to receive error messages in the console.

### Antivirus

Your antivirus program may flag these programs as dangerous and stop them from running. I personally promise that I haven't included any code in them that can put your system at risk, and your free to check the code yourself, but your antivirus program doesn't know this. Depending on how your antivirus works there are a couple of workarounds that might let you run the program:
- Some antivirus programs may let you run a dangerous program anyway, if you can find the option in its menus
- Some antivirus programs may let you exclude the .exe files or the folder they're in from being scanned
- Ultimately, you can build the programs yourself from the source code (this obviously requires installing Python and the programs' dependencies)