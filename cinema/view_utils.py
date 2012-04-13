from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView, ModelFormMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error

from models import Movie

def protection_mixin(decorator):
    'Fabric. Generates ProtectedViewMixin for specified decorator, e.g. login_required'
    class ProtectedViewMixin(object):
        @method_decorator(decorator)
        def dispatch(self, *args, **kwargs):
            return super(ProtectedViewMixin, self).dispatch(*args, **kwargs)
    return ProtectedViewMixin

LoginRequiredMixin = protection_mixin(login_required)
AddPermissionMixin = protection_mixin(permission_required('cinema.add_movie'))
ChangePermissionMixin = protection_mixin(permission_required('cinema.change_movie'))
DeletePermissionMixin = protection_mixin(permission_required('cinema.delete_movie'))

class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    
    get_form_class, get_form is not used
    """
    form_classes = {} # set the form classes as a mapping

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes):
        return dict([(key, klass(**self.get_form_kwargs())) \
            for key, klass in form_classes.items()])

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that processes multiple forms on POST. Every form must be
    valid.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)


class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaing several forms, and rendering a template response.
    """

class BaseMovieFormMixin(ModelFormMixin):
    ''' Mixin to use with FormView for Movie model
        handles "previous" and "next" request params,
        expects get_next_url and get_previous_url methods instead of get_success_url
    '''
    
    model = Movie
    get_previous_url = get_next_url = None
    context_object_name = 'object'

    def process_wizard_finish(self, commit=True):
        old_value = self.object.is_complete
        self.object.is_complete = self.object.is_complete or 'finish' in self.request.REQUEST
        if old_value != self.object.is_complete and commit:
            self.object.save()
        return 'finish' in self.request.REQUEST
        
    def update_object_timestamps(self, commit=True):
        self.object.created_by = (self.object.created_by_id and self.object.created_by) or self.request.user
        self.object.modified_by = self.request.user
        if commit:
            self.object.save()
        
    def success_redirect(self):
        success(self.request, "Movie '%s' was successfully saved" % self.object.title)

        if 'next' in self.request.REQUEST and self.get_next_url:
            url = self.get_next_url()
        elif 'previous' in self.request.REQUEST and self.get_previous_url:
            url = self.get_previous_url()
        elif 'finish' in self.request.REQUEST:
            url = reverse('list')
        else:
            url = self.request.path
        
        return HttpResponseRedirect(url)
    
    def success_object_update(self):
        'updates self.object'
        self.process_wizard_finish(commit = False)
        self.update_object_timestamps(commit = False)
        self.object.save()
        
    def form_valid(self, form):
        self.object = form.save(commit=False) # rewrite self.object in case of add form
        self.success_object_update()
        return self.success_redirect()

    def form_invalid(self, form):
        error(self.request, 'Please correct inputs')
        return super(BaseMovieFormMixin, self).form_invalid(form)
    
class BaseMovieFormsMixin(MultipleFormsMixin, BaseMovieFormMixin):
    '''
    Mixin to use with BaseMultipleFormsView
    '''
    def forms_valid(self, forms):
        for form in forms.values():
            form.save()
        
        self.success_object_update()
        return self.success_redirect()

    def forms_invalid(self, forms):
        error(self.request, 'Please correct inputs')
        return super(BaseMovieFormsMixin, self).forms_invalid(forms)
