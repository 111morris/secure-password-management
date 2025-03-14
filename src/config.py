import hashlib
import sys
import random
import string
from utils.dbconfig import dbconfig
from getpass import getpass
from rich import print as printc
from rich.console import Console

console = Console()

def generateDeviceSecret(length=10):
 # generate a random string of length 'length'
 return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
 # create a database
 db = dbconfig()
 cursor = db.cursor()
 printc("[green][+] creating new config [/green]")
   
  
 try:
  cursor.execute("CREATE DATABASE IF NOT EXISTS password_manager")
 except Exception as e:
  printc("[red][!] Error: An error occurred while trying to create db")
  console.print_exception(show_locals=True)
  sys.exit(0)
 printc("[green][+] Database created successfully")

 # create tables
 query = "CREATE TABLE password_manager.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
 cursor.execute(query)
 printc("[green][+] Table 'secrets' created successfully")

 query = "CREATE TABLE password_manager.entries (filename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NULL)"
 cursor.execute(query)
 printc("[green][+] Table 'entries' created successfully")

 while 1:
  mp = getpass("Enter master password: ")
  if mp == getpass("Re-type: ") and mp != "":
   break
   printc("[yellow][-] Please try again.[/yellow]")

 # hash the master password
 hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
 printc("[green][+] Master password hashed successfully (generated)[/green]")

 # generate a device secret
 ds = generateDeviceSecret()
 printc("[green][+] Device secret generated successfully[/green]")

 # add them to db
 query = "INSERT INTO password_manager.secrets (masterkey_hash, device_secret) VALUES (%s, %s)"
 val = (hashed_mp, ds)
 cursor.execute(query, val)
 db.commit()

 printc("[yellow][!] Please note down the device secret. You will need it to access the password manager[/yellow]")
 printc("[green][+] Configuration completed successfully (added to the database)[/green]")

 db.close()

config()
