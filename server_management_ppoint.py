#!/usr/bin/env python

"""
	Author: Goran Raovic
	email: goran.raovic@pulsarpoint.com
	
	Description:
		
	program takes parameters from web services and configuring servers based on them.
	After finish tasks program update web services about status
"""


from string import Template
import os, time,json,subprocess,sys, urllib, urllib2



def send_result_to_server(domain,status):
	data= {'domain-id':domain[4]['id'],'status':status}
	data2 = urllib.urlencode(data)
	try:
		response = urllib2.urlopen('http://192.168.156.1:8888/myapp4/web/app_dev.php/sconfig/', data2)
		payload = response.read()
		print payload
	except urllib2.HTTPError, error:
		print error.read()

def create_entitiy(domain):
	print domain[0]['domain-name']
	print domain[1]['disk-quota']
	print domain[2]['mysql-quota']
	print domain[3]['status']
	if domain[3]['status'] == 'delete':
		send_result_to_server(domain,'inactive')
		sys.exit(2)
	time.sleep(5)
	send_result_to_server(domain,'pokupljeno')
	time.sleep(10)
	send_result_to_server(domain,'zavrseno')

def get_web_data():
	try:
		response = urllib2.urlopen('http://192.168.156.1:8888/myapp4/web/app_dev.php/sconfig/')
		row_data_json = response.read()
		data = json.loads(row_data_json)
		for element in data:
			create_entitiy(element)
	except urllib2.HTTPError, error:
		print error.read()

def save_file():
	f1 = open('/etc/httpd/conf/underconstruction.html','r')
	c = f1.read()
	f = open('index.html','w+')
	f.write(c)
	f.close()
	f1.close()

def create_underconstruction_files(dname):
	dir_name_content = "/var/www/html/" + dname
	dir_name_logs = "/var/log/httpd/" + dname
	if os.path.isdir(dir_name_content):
		print "Directory " + dir_name_content + " already exists"
		sys.exit(2)
	else:
		os.mkdir(dir_name_content)
		os.chdir(dir_name_content)
		save_file()
	
	if os.path.isdir(dir_name_logs):
		print "Directorijum " + dir_name_logs + " vec postoji "
		sys.exit(2)
	else:
		if os.mkdir(dir_name_logs):
			print "Directory is succesfuly created"
	return 1

def create_file_from_template(template_name, dname):
	f = open(template_name,'r')
	s = Template(f.read())
	vhost_config = s.substitute(domain_name=dname)
	f.close()
	return vhost_config

def create_apache_template(template_content, dname):
	f = open('/etc/httpd/conf.d/' + dname + '.conf', 'w+')
	f.write(template_content)
	f.close()
	return 1

def main():
	template = 'hosting-template'
	if len(sys.argv) < 2:
		print "Usage %s domain_name example ( %s www.exampe.com )" % (sys.argv[0],sys.argv[0])
		sys.exit(1)
	
	if (sys.argv[1] == "get_data"):
		get_web_data()
		sys.exit(1)
	global template_content
	template_content = create_file_from_template(template,sys.argv[1])
	if create_underconstruction_files(sys.argv[1]):
		print "Uspesno kreiran folder i underconstruction"
	if create_apache_template(template_content, sys.argv[1]):
		print "Dodat je apache content"


if __name__=="__main__":
	main()
