---
layout: post
title: "Add customize commander into Facebook Chisel"
date: 2014-05-11 10:13:51 +0800
comments: true
categories: 技术
tags: lldb
---  

## 1. How the chisel init
When the lldb init, it will location the file <code>~/.lldbinit</code>, this is the API to add extend commander into lldb. In this file, there is a commander like:  
{% codeblock lang:sh %}
command script import ~/chisel/fblldb.py
{% endcodeblock %}

This commander means it will import the script ~/chisel/fblldb.py. Let's look into fblldb.py. There is lldb callback function named <code>__lldb_init_module</code>. Its function is load python funciton into lldb. Facebook add logic to fecth all the commanders under folder commands. After find all the commander, it will use following command to load them into lldb.  

{% codeblock lang:python %}
def loadCommand(module, command, directory, filename, extension):
  func = makeRunCommand(command, os.path.join(directory, filename + extension))
  name = command.name()
  
  key = filename + '_' + name
  
  module._loadedFunctions[key] = func
  
  functionName = '__' + key

  lldb.debugger.HandleCommand('script ' + functionName + ' = sys.modules[\'' + module.__name__ + '\']._loadedFunctions[\'' + key + '\']')
  lldb.debugger.HandleCommand('command script add -f ' + functionName + ' ' + name)
{% endcodeblock %}

Next, how doesn't this script find all the commanders in folder commander.
{% codeblock lang:python %}
def loadCommandsInDirectory(commandsDirectory):
  for file in os.listdir(commandsDirectory):
    fileName, fileExtension = os.path.splitext(file)
    if fileExtension == '.py':
      module = imp.load_source(fileName, os.path.join(commandsDirectory, file))

      if hasattr(module, 'lldbinit'):
        module.lldbinit()

      if hasattr(module, 'lldbcommands'):
        module._loadedFunctions = {}
        for command in module.lldbcommands():
          loadCommand(module, command, commandsDirectory, fileName, fileExtension)
{% endcodeblock %}

Here we know, we should add function named <code>lldbinit</code> and <code>lldbcommands</code>. Actually, <code>lldbcommands</code> is a list of all the commands in that file. 
Choose one display commands category.
{% codeblock lang:python %}
def lldbcommands():
  return [
    FBCoreAnimationFlushCommand(),
    FBDrawBorderCommand(),
    FBRemoveBorderCommand(),
    FBMaskViewCommand(),
    FBUnmaskViewCommand(),
    FBShowViewCommand(),
    FBHideViewCommand(),
  ]
{% endcodeblock %}
In chisel, each commander is using one class to represent. Take command <code>FBShowViewCommand()</code> for example. It is subclass of <code>FBCommand</code> defined in file fblldbinit.py. In this class, there are 5 public methods defined
{% codeblock lang:python %}
class FBCommand:
  def name(self):
    return None

  def options(self):
    return []

  def args(self):
    return []

  def description(self):
    return ''

  def run(self, arguments, option):
    pass
{% endcodeblock %}
All the command should implement parts of above methods. The function - run will be called in fblldb - <code>makeRunCommand</code>.

## 2. Add customized commander.
Till now, we have recogornized how chisel works. So let's learn how to add our customized commander into it. Recently, our Mobile team in MicroStrategy wants to enhance this tool to integrate with our issue report system - TQMS. In our TQMS system, we could get the general information of an issue. Different issue may use different mobile server. Each time, we should open the issue and find this config link for this mobile server. Then paste it into safari or other place to open it to load our app. It is very wasting time. So we want to add a function that input the TQMS id and generate config link and document path (this is related with our product, let's just define as MicroStrategy Toturial->Sandbox->njiang->test) for us and apply the url and document path in our app.
Here we have get our requirement.  

	1. Get config url and document from TQMS system.
	2. Apply the config link into our system
	3. Find the document path and open the folder.

Let's start to work.
###2.1 Get config url and document from TQMS system
Here comes the problem. How could we get the issue information. Here we use chrome develop tools. Then we could find it uses GetAllCommunicationsTypes to get issue information.
And its request header is   
{% img center /uploads/2014-05-11/1.png %}
You coulde see, we only send a json string, which contains the issue id. In this case, the issue id is 880507. Then we could generate the response text which contains issue information, like comments, full description and so on. Meanwhile, all the information is orignized with json formatting. So it is easy for us to generate the key inforamtion.
{% img center /uploads/2014-05-11/2.png %}

Here I want to share with you an open source lib of python - requests. You could find this lib here <http://docs.python-requests.org/en/latest/>. The setup steps are very easy. 

Input <code>python setup install</code> in the terminal. Of course, you should <code>cd requests</code> first.

During parse this json string, I found the session of TQMS system will be expired. So I do some research on how to web server to authorize. Actually, our system use IIS authorization, domain corp. After generate authorization, we will add authorization cookies into request header. So now our aim is to get the authorizaiton cookies.
There is a login.asp, we can use our corp id and password to get authorization. Here we will use another lib of requests - requests - ntlm. You could find it here <https://github.com/requests/requests-ntlm>.
Use the same method to install it as requests.

Get authorization cookies code is like below:
{% codeblock lang:python %}
def getAuthorizationCookies(username):
    print 'msilldbconfighelpers.py - getAuthorizationCookies'
    password = getpass.getpass('Password for ' + username + ': ')
    login_url = 'https://XXXXXXX.com/Technology/TQMSWeb/login/login.aspx?ReturnUrl=%2fTechnology%2fTQMSWeb%2fviewissue%2fviewissuewindow.aspx%3fid%3d877255%26searchid%3d2746652&id=877255&searchid=2746652'
    response = requests.get(login_url, auth = HttpNtlmAuth(username, password))
    if response.status_code == 200:
        return response.request._cookies
    else:
        return None
{% endcodeblock %}

After we get the authorization, then composite a request header for tqms web service.
{% codeblock lang:python %}
def combinationRequestHeaders(cookies):
    print 'msilldbconfighelpers.py - combinationRequestHeaders'
    headers = { "Connection": "keep-alive",
                "Content-Length": 20,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Origin": "https://XXXXXXXX.com",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
                "Content-Type": "application/json",
                "Referer": "https://XXXXXXXX.com/Technology/TQMSWeb/viewissue/viewissuewindow.aspx?id=882018",
                "Accept-Encoding": "gzip,deflate,sdch",
                "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                "Cookie": cookies}
    return headers
{% endcodeblock %}

Then get config url and document using following method:
{% codeblock lang:python %}
def getTQMSInformationDict(tqms):
    try:
        config_path = getConfigFilePath()
        if os.path.isfile(config_path) == False:
            print 'Please create an file named "config" under ' + config_path + ' ! Format with'
            print '[Login]'
            print 'domain = [the domain]'
            print 'username = [your username]'
            return
        cf = ConfigParser.ConfigParser()
        cf.read(config_path)
        domain = cf.get('Login', 'domain')
        username = cf.get('Login', 'username')

        if domain is None or username is None:
            print 'Please create an file named "config" under ' + config_path + '! Format with\n'
            print '[Login]'
            print 'domain = [the domain]'
            print 'username = [your username]'
            return

        print 'msilldbconfighelpers.py - getMobileConfigLinkForTQMS'
        username = domain + '\\' + username
        # print username
        service_url = 'https://XXXXXX.com/technology/tqmsservices/issues.asmx/GetAllComunicationsPerType'
        payload = {"IssueId": tqms}
        json_data = json.dumps(payload)

        # 1. Try to use local cookies
        cookies_read_from_file = True
        cookies = getCookies()

        if cookies is None:
            cookies = getAuthorizationCookies(username)
            if cookies is None:
                raise "Failed to get the authorization for username: %s" % username
            recordCookies(cookies)
            cookies_read_from_file = False

        cookies_str = dumpCookies(cookies)

        # 2. get details description response string for tqms
        headers = combinationRequestHeaders(cookies_str)
        response = requests.post(service_url, data=json_data, headers=headers)

        print response.status_code

        if response.status_code != 200 and cookies_read_from_file == True:
            print "Try to relogin with Username!"
            cookies = getAuthorizationCookies(username)
            if cookies is None:
                raise "Failed to get the authorization with Username: %s" % username
            recordCookies(cookies)
            cookies_str = dumpCookies(cookies)
            headers = combinationRequestHeaders(cookies_str)
            response = requests.post(service_url, data=json_data, headers=headers)
            if response.status_code != 200:
                raise "Failed to get the authorization with Username: %s" % username

        if response.status_code != 200:
            raise "Failed to get the authorization with Username!"
        else:
            # 3. parse json string
            issue_infos = json.loads(response.text)['d']
            full_description_u = issue_infos['Description']
            comments_u = issue_infos['Comments']
            full_description = full_description_u.encode("utf-8")
            comments = comments_u.encode("utf-8")
            if full_description is None or full_description == '':
                raise Exception("Failed to get the full description for TQMS: %s" % tqms)
            else:
                config_url = generateConfigURLLink(comments, full_description)
                document_path = generateDocumentPath(comments, full_description)
                path_separator = getSeparatorForDocumentPath(document_path)
                return {"url": config_url, "document": document_path, "separator": path_separator}
                
    except Exception, e:
        print e
{% endcodeblock %}

###2.2 Apply url
After generate url link, we will turn to MSIConfigCommand. The class is like below.
{% codeblock lang:python %}
def lldbcommands():
    return [
        MSIConfigCommand()
    ]

class MSIConfigCommand(fb.FBCommand):
    def name(self):
        return 'config'

    def description(self):
        return 'Config MSTR Mobile Application with URL/TQMS id.'

    def options(self):
        return [
                fb.FBCommandArgument(short='-u', long='--url', arg='url', type='string', default='', help='Config mobile app with url'),
                fb.FBCommandArgument(short='-d', long='--id', arg='id', type='string', default='880507', help='TQMS ID')
        ]

    def getPureUrlLink(self, dirty_url):
        if dirty_url is None:
            return None

        results = dirty_url.split(' ')
        for str in results:
            if str != '':
                return str

#    def args(self):
#        return [ fb.FBCommandArgument(arg='url', type='string', help='The config url.', default='')]

# expr [[[UIApplication sharedApplication] delegate] application:application openURL:url sourceApplication:sourceApplication annotation:annotation]
# application = [UIApplication sharedApplication]
# url = [above]
# sourceApplication = @"com.apple.mobilesafari"
# annotation = NSDictionary
# {
#     ReferrerURL = "http://10.197.34.70/";
# }
    def run(self, args, options):
        print '------ start config ------'

        if options.id == "" and options.url == "":
            print "error, -d or -u missing!"
            return

        # 1. Generate url and document path first
        if options.id is not None and options.id != "":
            tqms_dict = getTQMSInformationDict(options.id)

            for key in tqms_dict:
                if tqms_dict[key] is None or tqms_dict[key] == "":
                    print "Error when get %s for TQMS: %s" % (key, options.id)

            config_url = tqms_dict['url']
            document_path = tqms_dict['document']
            path_separator = tqms_dict['separator']

        elif options.url is not None and options.url != "":
            config_url = options.url

        config_url = self.getPureUrlLink(config_url)
        print "config_url = %s" % config_url
        print "document_path = %s" % document_path

        # 2. Config the document path into FolderPathSearcher
        if document_path is not None and path_separator is not None:
            lldb.debugger.HandleCommand('expression [FolderPathSearcher getInstance]')
            if document_path is not None and document_path != "":
                expr = '[[FolderPathSearcher getInstance] setSearchPath:@"'+ document_path +'" Separator:@"'+ path_separator +'"]'
                lldb.debugger.HandleCommand('expression ' + expr)

        # 3. Apply url link
        if config_url is not None:
            url = fb.evaluateExpression('(NSURL*)[NSURL URLWithString:@"%s"]' % config_url)
            application = fb.evaluateExpression('(UIApplication*)[UIApplication sharedApplication]')
            delegate = fb.evaluateExpression('[(UIApplication*)%s delegate]' % application)
            lldb.debugger.HandleCommand('expr (void)[%s application:%s openURL:%s sourceApplication:nil annotation:nil]' % (delegate, application, url))
            print '------ end config ------'
        else:
            print 'Failed to generate the url link, please check your url or TQMS ID is correct!'

        # 4. Continue run our app
        lldb.debugger.SetAsync(True)
        lldb.debugger.GetSelectedTarget().GetProcess().Continue()
{% endcodeblock %}

You can see we add two options for this command "-d" and "-u". When config our app, we use system callback function - <code>[UIApplicationDelegate application: openURL: sourceApplication:nil annotation:nil]</code>. 

###2.3 Find document path
This we get projects system information is async. So we should add logic to handle this. I will add this part later.

###2.4 Continue lldb automatically
{% codeblock lang:python %}
lldb.debugger.SetAsync(True)
lldb.debugger.GetSelectedTarget().GetProcess().Continue()
{% endcodeblock %}

##3 Write auto setup shell script

{% codeblock lang:bash %}
#!/bin/bash
echo "------ Start Config Chisel ------"

curPath=`pwd`
echo $curPath
lldbinitFile=".lldbinit"
cd ~
if [[ ! -f "$lldbinitFile" ]]; then
	touch "$lldbinitFile"
else
	rm "$lldbinitFile"
	touch "$lldbinitFile"
fi

#echo "# ~/.lldbinit" >> $lldbinitFile
echo "command script import "$curPath"/fblldb.py" >> $lldbinitFile

cd "$curPath"
echo "Please input the following information:"
echo -n "domain = "
read domain
echo -n "username = "
read username

configPath="/tmp/MicroStrategy"
configFile="/tmp/MicroStrategy/TQMS.cfg"

if [ ! -d "$configPath" ]; then
	mkdir "$configPath"
fi

if [[ ! -f "$configFile" ]]; then
	touch "$configFile"
else
	rm "$configFile"
	touch "$configFile"
fi

echo "[Login]" >> $configFile
echo "domain = "$domain >> $configFile
echo "username = "$username >> $configFile

cd packages/requests
sudo python setup.py install
cd ../requests-ntlm
sudo python setup.py install

echo "------ Config Chisel Finished -------"
{% endcodeblock %}

##4 How to use
###4.1 Setup:
After you download the source code, run the following command in Terminal  

1. cd chisel
2. ./setup.sh
	a. input your domain, like “corp”
	b. input you corp id, like “XXXX”
	c. input user password (this password is your Mac OS user’s password, it is used to run sudo command. For corp password, it will require later in how-to #2.)
 
###4.2 How-to:
We added a new command named “config” in the python script. There are two options “-u” and “-d”. “-u” means using url to configuration our app. “-d” means using TQMS id to fetch the config url and configuration our app. You could run our app in debug mode. After app launches,  

1. Pause our app manually.
2.  You could input any one of following two commands, if it is the first time you run this command or the login cookie is expired, you need to input your corp id password to generate a new login cookie. It will not store the password information.
	a. config –u [a url link]
	b. config –d 854318
 
###4.3 Discussion:
1. About setup.sh, I have combined the setting commands into one shell script. It will do the following things:
	a. Re-create ~/.lldbinit. ~/.lldbinit is used to init lldb extend script, like import python script.
	b. After get user corp id, it will store the information in “/tmp/MicroStrategy/TQMS.cfg”.
	c. Install two depends libs: requests and requests-ntlm. These two libs are used to get the authorization login cookies.
2. About login cookies, if there is no login success cookies or the success login cookie is expired, we will first try to login the corp id and get the login success cookie. After get the authorization cookies, we will store this information in “/tmp/MicroStratety/TQMS.cookies”. If the cookies is useable, we will re-use this cookies to generate configuration url link.
3. About generate URL config link, currently, we will find string, which starts with “mstr:///” (Thanks for Liang’s comments). Now it is fine. But if there is 2 or more configuration link in the full description, it will be hard to determine which one is needed. I am wondered whether we could ask QE to format the configuration link and document path.