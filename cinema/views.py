import operator

from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.core.urlresolvers import reverse

from django.contrib.messages import success, error

from models import Movie
from forms import BasicInfo as BasicInfoForm, MovieRatingFormset, MovieGenreFormset
from view_utils import LoginRequiredMixin, AddPermissionMixin, ChangePermissionMixin, DeletePermissionMixin 
from view_utils import MultipleFormsView, BaseMovieFormMixin, BaseMovieFormsMixin

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

class RatingGenreEdit(BaseMovieFormsMixin, ChangePermissionMixin, MultipleFormsView):
    'differs by multiple formset on the page'
    
    template_name = 'rating_and_genre.html'
    get_next_url = lambda self: reverse('edit_crew_and_cast', kwargs={'pk': self.object.pk})
    form_classes = {
        'ratings': MovieRatingFormset,
        'genres': MovieGenreFormset,
    }
