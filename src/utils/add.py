from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA512
import utils.aesutil
from utils.dbconfig import dbconfig
from rich import print as printc


def computeMasterKey(mp, ds):
	password = mp.encode()
	salt = ds.encode()
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
	return key


def addEntry(mp, ds, sitename, siteurl, email, username):
	# get the password
	password = getpass("Enter password: ")

	mk = computeMasterKey(mp, ds)

	encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType='bytes')

	# add to db

	db = dbconfig()
	cursor = db.cursor()
	query = ("INSERT INTO password_manager.entries "
			 "(sitename, siteurl, email, username, password) "
			 "VALUES (%s, %s, %s, %s, %s)")
	val = (sitename, siteurl, email, username, encrypted)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+] Entry added successfully[/green]")