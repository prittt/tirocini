from django.contrib import admin
from tirociniApp.models import Studente, Richiesta, Tutor, Sede, Corso

class ListDisplayAllMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != 'id' and field.editable]
        super(ListDisplayAllMixin, self).__init__(model, admin_site)

class StudenteAdmin(ListDisplayAllMixin, admin.ModelAdmin):
    pass

class RichiestaAdmin(ListDisplayAllMixin, admin.ModelAdmin):
    #list_display = [f.name for f in Richiesta._meta.get_fields()]
    pass

class CorsoAdmin(ListDisplayAllMixin, admin.ModelAdmin):
    pass

class TutorAdmin(ListDisplayAllMixin, admin.ModelAdmin):
    pass

class SedeAdmin(ListDisplayAllMixin, admin.ModelAdmin):
    pass


admin.site.register(Studente, StudenteAdmin)
admin.site.register(Richiesta, RichiestaAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(Sede, SedeAdmin)
admin.site.register(Corso, CorsoAdmin)
