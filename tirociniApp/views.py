import datetime
import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views import generic
from django.template.loader import get_template, render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

from xhtml2pdf import pisa

from .models import Richiesta, Studente, User, Tutor, Sede
from django.contrib import messages


def init(request):
    return render(request, 'registration/login.html')


def modulo(request):
    return render(request, 'tirociniApp/paginaProva.html')


class RichiestaCreateView(generic.CreateView):
    model = Richiesta
    fields = ['studente', 'tutor', 'sede', 'durata', 'data_inizio', 'data_fine', 'obiettivi', 'autocertificazione']
    template_name = 'tirociniApp/richiesta_new_form.html'

    def get(self, request, *args, **kwargs):
        s = get_object_or_404(Studente, user=request.user)
        rs = Richiesta.objects.filter(studente=s)
        ric = None
        for r in rs:
            if r.stato == 0 or (r.stato == 1 and r.corso == s.corso):
                ric = r
                break
        if ric:
            return HttpResponseRedirect(reverse('tirociniApp:review', kwargs={'pk': ric.id}))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        s = get_object_or_404(Studente, user=request.user)
        rs = Richiesta.objects.filter(studente=s)
        ric = None
        for r in rs:
            if r.stato == 0 or (r.stato == 1 and r.corso == s.corso):
                ric = r
                break
        if ric:
            return HttpResponseRedirect(reverse('tirociniApp:review', kwargs={'pk': ric.id}))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.instance.data_inizio < datetime.date.today() + datetime.timedelta(days=10) or \
           form.instance.data_inizio > form.instance.data_fine:
            form.add_error("data_inizio", "La data di fine deve essere successiva a quella di inizio.")
            return super().form_invalid(form)
        form.instance.corso = form.instance.studente.corso
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(RichiestaCreateView, self).get_form(form_class)
        form.label_suffix = ""
        form.fields['data_fine'].widget.attrs.update({'class': 'datepicker', 'min': datetime.date.today() + datetime.timedelta(days=10)})
        form.fields['data_inizio'].widget.attrs.update({'class': 'datepicker', 'min': datetime.date.today() + datetime.timedelta(days=10)})
        return form

    def get_context_data(self, **kwargs):
        context = super(RichiestaCreateView, self).get_context_data(**kwargs)
        s = get_object_or_404(Studente, user=self.request.user)
        context['studente'] = s
        context['ore'] = s.corso.durata_tirocinio
        context['tutor_list'] = Tutor.objects.all()
        context['sedi_list'] = Sede.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, 'Modulo inviato con successo! Riceverai una mail contenente i dati che hai '
                                       'inserito.')
        return reverse('tirociniApp:generate')


class RichiestaUpdateView(generic.UpdateView):
    model = Richiesta
    fields = ['studente', 'tutor', 'sede', 'durata', 'data_inizio', 'data_fine', 'obiettivi', 'autocertificazione']
    template_name = 'tirociniApp/richiesta_new_form.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(RichiestaUpdateView, self).get_form(form_class)
        form.label_suffix = ""
        form.fields['data_fine'].widget.attrs.update({'class': 'datepicker'})
        form.fields['data_inizio'].widget.attrs.update({'class': 'datepicker'})
        return form

    def get_context_data(self, **kwargs):
        context = super(RichiestaUpdateView, self).get_context_data(**kwargs)
        s = get_object_or_404(Studente, user=self.request.user)
        context['studente'] = s
        context['ore'] = s.corso.durata_tirocinio
        context['tutor_list'] = Tutor.objects.all()
        context['sedi_list'] = Sede.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, 'Modulo aggiornato con successo! Riceverai una mail contenente i dati che hai '
                                       'inserito.')
        return reverse('tirociniApp:generate')


def success(request):
    return render(request, 'tirociniApp/static_success.html')


@csrf_exempt
@login_required(login_url='/tirocini/homepage/')
def next_page(request):
    if request.user.groups.filter(name='Studente').exists():
        s = get_object_or_404(Studente, user=request.user)
        rs = Richiesta.objects.filter(studente=s)
        ric = None
        for r in rs:
            if r.stato == 0 or (r.stato == 1 and r.corso == s.corso):
                ric = r
                break

        if ric:
            return HttpResponseRedirect(reverse('tirociniApp:review', kwargs={'pk': ric.id}))
        else:
            return HttpResponseRedirect(reverse('tirociniApp:richiesta'))
    elif request.user.groups.filter(name='UfficioStage').exists():
        return HttpResponseRedirect(reverse('tirociniApp:archivio_richieste'))
    else:
        messages.error(request, 'Questa applicazione serve da interfaccia tra Studenti e Ufficio Stage. Non sono '
                                'previste funzionalità per i Docenti.')
        return HttpResponseRedirect(reverse('tirociniApp:homepage'))


class RichiestaListView(generic.ListView):
    model = Richiesta
    template_name = 'tirociniApp/lista_richieste.html'
    context_object_name = 'richieste_totali'

    def get_context_data(self, **kwargs):
        context = super(RichiestaListView, self).get_context_data(**kwargs)
        context['richieste_nv'] = Richiesta.objects.filter(stato__exact=0)
        context['richieste_v'] = Richiesta.objects.filter(stato__exact=1)
        context['richieste_r'] = Richiesta.objects.filter(stato__exact=-1)
        return context


class GestioneRichiestaView(generic.DetailView):
    model = Richiesta
    template_name = 'tirociniApp/gestore_richieste_new.html'


class GestioneLoginView(generic.FormView):
    template_name = "tirociniApp/prova.html"


class RichiestaDetailView(generic.DetailView):
    model = Richiesta
    template_name = 'tirociniApp/richiesta_compilata.html'


def update_state(request, richiesta_id):
    if request.user.is_authenticated:
        richiesta = get_object_or_404(Richiesta, pk=richiesta_id)

        if (richiesta.updated_at + datetime.timedelta(minutes=5)) < timezone.now() or \
                richiesta.updated_at == richiesta.created_at:
            richiesta.stato += 1
            richiesta.save()

        return HttpResponseRedirect(reverse('tirociniApp:archivio_richieste'))
    else:
        return HttpResponseRedirect(reverse('tirociniApp:homepage'))


def discard(request, richiesta_id):
    if request.user.is_authenticated and request.user.groups.all()[0].name == 'UfficioStage':
        richiesta = get_object_or_404(Richiesta, pk=richiesta_id)
        richiesta.stato = -1
        richiesta.save()
        subject = 'Attività progettuale'
        message = f'Ciao {richiesta.studente.user.username}.\nLa richiesta da te sottomessa è stata RIFIUTATA dall\'Ufficio Stage.\nIl motivo del rifiuto è:\n'
        message += request.POST['motivo'] + '\n' + request.user.first_name + " " + request.user.last_name
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [richiesta.studente.user.email, ]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.send()

        return HttpResponseRedirect(reverse('tirociniApp:archivio_richieste'))
    else:
        return HttpResponseRedirect(reverse('tirociniApp:homepage'))


class RichiestaDeleteView(generic.DeleteView):
    model = Richiesta

    success_url = "/tirocini/archivio"


def generate_pdf(request):
    template = get_template('tirociniApp/richiesta_compilata.html')
    user = request.user
    student = Studente.objects.get(user__username__exact=user.username)
    richiesta = Richiesta.objects.filter(studente__id__exact=student.id).order_by('-created_at')[0]
    context_dict = {
        "richiesta": richiesta
    }

    html = template.render(context_dict)
    result_file = open("tmp/riepilogo.pdf", "w+b")
    pisa_status = pisa.CreatePDF(html, dest=result_file)

    result_file.close()

    # Email allo studente
    subject = 'Richiesta attività progettuale'
    message = f'''Gentile {user.get_full_name()},

nell'allegato trova il riepilogo della richiesta inserita.

Cordiali saluti,
Il team di Services'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.attach_file("tmp/riepilogo.pdf")
    email.send()

    # Email all'Ufficio Stage'
    subject = 'Nuova richiesta attività progettuale'
    message = f'''Spett. Ufficio stage,

lo studente {user.get_full_name()} <{user.email}> ha inserito una richiesta di attività progettuale.
L'elenco delle richieste è disponibile su https://services.ing.unimore.it/tirocini

Cordiali saluti,
Il team di Services'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['stage.ingegneria@unimore.it', ]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.send()

    return HttpResponseRedirect(reverse('tirociniApp:homepage'))


def access(request):
    qp = {
        'next': request.build_absolute_uri(reverse('tirociniApp:redirect'))
    }
    return HttpResponseRedirect('https://services.ing.unimore.it/tirocini/login' + '?' + urlencode(qp))


def homepage(request):
    return render(request, 'tirociniApp/homepage.html')


def adminLogin(request):
    try:
        u = User.objects.get(username__exact=request.POST.get('username'))
    except User.DoesNotExist:
        u = None

    if u:
        login(request, u)
    else:
        messages.error(request, 'Username e/o Password non corretti')
        return HttpResponseRedirect(reverse('tirociniApp:homepage'))

    return HttpResponseRedirect(reverse('tirociniApp:redirect'))
