import mysql.connector

from rich import print as printc
from rich.console import Console
console = Console()

def dbconfig():
 try:
  db = mysql.connector.connect(
   host='localhost',
   user='password_manager',
   passwd='password'
  )

 except Exception as e:
  console.print_exception(show_locals=True)
 return db

console.print('Connected to MySQL Server')