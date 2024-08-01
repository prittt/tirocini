import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.conf import settings
from django.urls import reverse
from django.utils.html import escape
from datetime import datetime

import urllib.request

import requests
from io import BytesIO
from django.core import files
import re

from django.utils.http import urlencode

from tirociniApp.models import Studente, Corso


def get_success_url(request):
    url = request.POST.get('next', request.GET.get('next', ''))
    return url or resolve_url(settings.LOGIN_REDIRECT_URL)


def get_remote_image(uid):
    image_url = f'https://tutorato.unimore.it/esse3/foto_api/{uid}'

    response = requests.get(image_url, stream=True)

    if response.status_code != requests.codes.ok:
        return

    fp = BytesIO()
    fp.write(response.content)
    # A resize could be helpful here
    return fp


def shibboleth_string(field):
    if type(field) is str:
        return field.encode('latin1').decode()
    else:
        return str(field)


def get_shibboleth_list(field):
    s = shibboleth_string(field)
    l = s.split(";")
    l.sort()
    l = [re.sub("{[0-9]}", "", s) for s in l]
    return l


def get_shibboleth_dict(field):
    s = shibboleth_string(field)
    l = s.split(";")
    d = {re.search("{[0-9]}", e).group(0)[1]: re.sub("{[0-9]}", "", e) for e in l}
    return d

#
# def ignore_ip_in_dos_jail(user, request):
#     for g in user.groups.all():
#         if g.name in teacher_groups:
#             client_ip = get_client_ip(request)
#             jail_name = "http-get-dos"
#             # print("*" * 100)
#             # print(f"{os.getgid()} + {os.getgid()}")
#             # print("*" * 100)
#             cmd = f'fail2ban-client set {jail_name} addignoreip {client_ip}'
#             # print(cmd)
#             subprocess.Popen(cmd, shell=True)
#             return

fake_shibboleth_meta = {
    "Shib-Handler": "https://services.ing.unimore.it/Shibboleth.sso",
    "Shib-Application-ID": "default",
    "Shib-Session-ID": "_f0b0629d268958177316e4163d8837fa",
    "Shib-Identity-Provider": "https://idp.unimore.it/idp/shibboleth",
    "Shib-Authentication-Instant": "2024-07-31T11:06:08.605Z",
    "Shib-Authentication-Method": "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport",
    "Shib-AuthnContext-Class": "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport",
    "Shib-Session-Index": "_81f1f72e7767f677e192de64f25f60f4",
    "Shib-Session-Expires": "1722452768",
    "Shib-Session-Inactivity": "1722427568",
    "affiliation": "member@unimore.it;student@unimore.it",
    "cn": "SEBASTIANO REMELLI",
    "eppn": "240739@unimore.it",
    "givenName": "SEBASTIANO",
    "mail": "240739@studenti.unimore.it",
    "ou": "people;studenti;Advanced Automotive Engineering",
    "persistent-id": "https://idp.unimore.it/idp/shibboleth!https://services.ing.unimore.it/tirocini/sp!9YcapL48jkbIRCUnLcbuuiS4fMI=",
    "sn": "REMELLI",
    "uid": "240739",
    "unimorecodicefiscale": "RMLSST98P16G489J",
    "unimorestudcorso": "{1}20-269",
    "unimorestuddescrcorso": "{1}Advanced Automotive Engineering",
    "unimorestudmatricola": "{1}168054",
    "SSL_TLS_SNI": "services.ing.unimore.it",
    "GATEWAY_INTERFACE": "CGI/1.1",
    "SERVER_PROTOCOL": "HTTP/1.1",
    "REQUEST_METHOD": "GET",
    "QUERY_STRING": "",
    "REQUEST_URI": "/tirocini/test/",
    "SCRIPT_NAME": "/tirocini",
    "PATH_INFO": "/test/",
    "PATH_TRANSLATED": "/var/www/html/test/",
    "HTTP_HOST": "services.ing.unimore.it",
    "HTTP_CONNECTION": "keep-alive",
    "HTTP_CACHE_CONTROL": "max-age=0",
    "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
    "HTTP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "HTTP_SEC_FETCH_SITE": "same-site",
    "HTTP_SEC_FETCH_MODE": "navigate",
    "HTTP_SEC_FETCH_DEST": "document",
    "HTTP_SEC_CH_UA": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
    "HTTP_SEC_CH_UA_MOBILE": "?0",
    "HTTP_SEC_CH_UA_PLATFORM": "\"Windows\"",
    "HTTP_ACCEPT_ENCODING": "gzip, deflate, br",
    "HTTP_ACCEPT_LANGUAGE": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "HTTP_COOKIE": "_ga_3N0EDDCD0J=GS1.1.1634028063.2.1.1634028086.0; _ga_Y13LJ4MDWL=GS1.1.1634723175.1.0.1634723325.0; _ga_LC2GYLCX0B=GS1.1.1651158367.1.1.1651158401.0; _ga_PG36LJMQ5C=GS1.1.1655390822.9.1.1655392694.0; _ga_JHGNYN9YCB=GS1.1.1666597413.278.1.1666599256.0.0.0; _ga_K1GD9J05PP=GS1.1.1666858849.67.1.1666859536.0.0.0; _ga_RGJ7Q4YGP7=GS1.1.1666863861.11.1.1666865058.0.0.0; _ga=GA1.2.1880661450.1626079707; _gid=GA1.2.1230542064.1666870558; _shibsession_64656661756c7468747470733a2f2f73657276696365732e696e672e756e696d6f72652e69742f7469726f63696e692f7370=_8a7c3454fd3969bf01ee2ffc1592128f; csrftoken=31bjYqnZZRyWkKxIXqO3gnMTeIEfihxLJ5hZOyD82QQZNn4xCyJQquu6Hzx0VA7D; sessionid=2g75wmlgmkfwx4c5dn5iqucsoany6vyn",
    "SERVER_SIGNATURE": "\nApache/2.4.41 (Ubuntu) Server at services.ing.unimore.it Port 443\n\n",
    "SERVER_SOFTWARE": "Apache/2.4.41 (Ubuntu)",
    "SERVER_NAME": "services.ing.unimore.it",
    "SERVER_ADDR": "155.185.48.103",
    "SERVER_PORT": "443",
    "REMOTE_ADDR": "155.185.48.10",
    "DOCUMENT_ROOT": "/var/www/html",
    "REQUEST_SCHEME": "https",
    "CONTEXT_PREFIX": "",
    "CONTEXT_DOCUMENT_ROOT": "/var/www/html",
    "SERVER_ADMIN": "federico.bolelli@unimore.it",
    "SCRIPT_FILENAME": "/home/administrator/django_websites/tirocini/tirocini/wsgi.py",
    "REMOTE_PORT": "64668",
    "REMOTE_USER": "cgrana@unimore.it",
    "AUTH_TYPE": "shibboleth",
    "mod_wsgi.script_name": "/tirocini",
    "mod_wsgi.path_info": "/test/",
    "mod_wsgi.process_group": "SurveyProject",
    "mod_wsgi.application_group": "services.ing.unimore.it|/tirocini",
    "mod_wsgi.callable_object": "application",
    "mod_wsgi.request_handler": "wsgi-script",
    "mod_wsgi.handler_script": "",
    "mod_wsgi.script_reloading": "1",
    "mod_wsgi.listener_host": "",
    "mod_wsgi.listener_port": "443",
    "mod_wsgi.enable_sendfile": "0",
    "mod_wsgi.ignore_activity": "0",
    "mod_wsgi.request_start": "1666884010398693",
    "mod_wsgi.request_id": "5VNSrf2uj3Y",
    "mod_wsgi.queue_start": "1666884010400101",
    "mod_wsgi.daemon_connects": "1",
    "mod_wsgi.daemon_restarts": "0",
    "mod_wsgi.daemon_start": "1666884010400238",
    "mod_wsgi.script_start": "1666884010400364",
    "wsgi.version": "(1, 0)",
    "wsgi.multithread": "True",
    "wsgi.multiprocess": "False",
    "wsgi.run_once": "False",
    "wsgi.url_scheme": "https",
    "wsgi.errors": "<_io.TextIOWrapper name='' encoding='utf-8'>",
    "wsgi.input": "",
    "wsgi.input_terminated": "True",
    "wsgi.file_wrapper": "",
    "apache.version": "(2, 4, 41)",
    "mod_wsgi.version": "(4, 6, 8)",
    "mod_wsgi.total_requests": "14",
    "mod_wsgi.thread_id": "1",
    "mod_wsgi.thread_requests": "7",
    "CSRF_COOKIE": "31bjYqnZZRyWkKxIXqO3gnMTeIEfihxLJ5hZOyD82QQZNn4xCyJQquu6Hzx0VA7D",
}

def shibboleth_login(request):
    # if request.session.test_cookie_worked():
    #     request.session.delete_test_cookie()
    #     return
    # else:
    #     print("Cookies must be enabled")

    if settings.RUNSERVER:
        meta = fake_shibboleth_meta
    else:
        meta = request.META

    user, created = User.objects.get_or_create(username=meta["eppn"])
    if created:
        user.set_unusable_password()

    if user.email == '' and "mail" in meta:
        user.email = shibboleth_string(meta["mail"])
    if user.first_name == '' and "givenName" in meta:
        user.first_name = shibboleth_string(meta["givenName"]).title()
    if user.last_name == '' and "sn" in meta:
        user.last_name = shibboleth_string(meta["sn"]).title()

    user.save()
    if 'studenti' in meta["ou"]:
        corsi_list = []
        if "unimorestudcorso" in meta:
            codici_dict = get_shibboleth_dict(meta["unimorestudcorso"])
            nomi_dict = get_shibboleth_dict(meta["unimorestuddescrcorso"])
            corsi_list = []
            for k, v in codici_dict.items():
                if v == '20-CS':  # Skip "Struttura per CORSO SINGOLO"
                    continue
                corso, created = Corso.objects.get_or_create(codice=v, defaults={'nome': nomi_dict[k], })
                # created = True  # Debug!
                if created:
                    url = "https://unimore.coursecatalogue.cineca.it/api/v1/ricercaCorsi"
                    r = requests.post(url, json={
                        "searchString": v,
                        "anno": str(datetime.now().year),
                        "area": None,
                        "tipoCorso": None,
                        "sede": None,
                        "lingua": None,
                        "dipartimento": None,
                        "interateneo": None})
                    result = json.loads(r.content)
                    try:
                        tipo_corso_cod = result[0]['subgroups'][0]['cds'][0]['tipo_corso_cod']
                        if tipo_corso_cod == 'LM':
                            corso.tipo = "LM"
                            corso.durata_tirocinio = 720
                        else:
                            corso.tipo = "LT"
                            corso.durata_tirocinio = 360
                        corso.save()
                    except:
                        pass
                corsi_list.append(corso)

        stud, created = Studente.objects.get_or_create(user=user, defaults={'corso': corsi_list[0], })
        if not created:
            if stud.corso != corsi_list[0]:
                stud.corso = corsi_list[0]
                stud.save()

        if "unimorestudmatricola" in meta:
            stud.matricola = meta["unimorestudmatricola"].split('}')[1]
        if "unimorecodicefiscale" in meta:
            stud.codice_fiscale = meta["unimorecodicefiscale"]
        stud.save()

        my_group, created = Group.objects.get_or_create(name='Studente')
        my_group.user_set.add(user)
        my_group.save()

    login(request, user)

    request.GET.urlencode()
    return HttpResponseRedirect(get_success_url(request))


def shibboleth_test(request: HttpRequest):
    meta = request.META

    s = '<pre>\n'
    for k, v in meta.items():
        s += f'"{k}": "{shibboleth_string(v)}",\n'
    s += '</pre>\n'

    return HttpResponse(s)
