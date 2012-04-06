import operator

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.messages import success, error
from django.contrib.auth.decorators import permission_required

from models import Movie
from forms import BasicInfo as BasicInfoForm

def protection_mixin(decorator):
    'Fabric. Generates ProtectedViewMixin for specified decorator, e.g. login_required'
    class ProtectedViewMixin(object):
        @method_decorator(decorator)
        def dispatch(self, *args, **kwargs):
            return super(ProtectedViewMixin, self).dispatch(*args, **kwargs)
    return ProtectedViewMixin

LoginRequiredMixin = protection_mixin(login_required)
AddPermissionMixin = protection_mixin(permission_required('cinema_movies.can_add'))
ChangePermissionMixin = protection_mixin(permission_required('cinema_movies.can_change'))
DeletePermissionMixin = protection_mixin(permission_required('cinema_movies.can_delete'))

class List(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    paginate_by = 50
    search_fields = 'title'.split(',')

    def get_queryset(self):
        'applies keyword search'
        query = Movie.objects.all()
        search_phrase = self.request.REQUEST.get('search', None)
        if search_phrase:
            for bit in search_phrase:
                orm_lookups = ["%s__icontains" % search_field for search_field in self.search_fields]
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                query = query.filter(reduce(operator.or_, or_queries))
        return query      

class MovieDetails(LoginRequiredMixin, DetailView):
    template_name = 'details.html'
    model = Movie

class BaseMovieFormMixin(object):
    ''' Mixin to use with FormView for Movie model
        handles "previous" and "next" request params,
        expects forms.BaseMovieEdit form subclass,
        expects get_next_url and get_previous_url methods instead of get_success_url
    '''
    
    model = Movie
    get_previous_url = get_next_url = None
        
    def form_valid(self, form):
        obj = self.object = form.save(self.request.user, commit=False)
        obj.is_complete = obj.is_complete or 'finish' in self.request.REQUEST
        obj.save()
        success(self.request, "Movie '%s' was successfully saved" % obj.title)
        
        if 'next' in self.request.REQUEST and self.get_next_url:
            url = self.get_next_url()
        elif 'previous' in self.request.REQUEST and self.get_previous_url:
            url = self.get_previous_url()
        elif 'finish' in self.request.REQUEST:
            url = reverse('list')
        else:
            url = self.request.path
        
        return HttpResponseRedirect(url)

    def form_invalid(self, form):
        error(self.request, 'Please correct inputs')
        return super(BaseMovieFormMixin, self).form_invalid(form)

class Add(BaseMovieFormMixin, AddPermissionMixin, CreateView):
    template_name = 'basic_info.html'
    form_class = BasicInfoForm
    get_next_url = lambda self: reverse('edit_rating_and_genre', kwargs={'pk': self.object.pk})

class Delete(DeletePermissionMixin, DeleteView):
    template_name = 'delete.html'
    model = Movie
    
    def get_success_url(self):
        success(self.request, "Movie '%s' was removed successfully" % self.object)
        return reverse('list')

class BasicInfoEdit(BaseMovieFormMixin, ChangePermissionMixin, UpdateView):
    template_name = 'basic_info.html'
    form_class = BasicInfoForm
    get_next_url = lambda self: reverse('edit_rating_and_genre', kwargs={'pk': self.object.pk})
