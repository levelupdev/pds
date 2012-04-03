import operator

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView
from django.db.models import Q

from models import Movie
from forms import BasicInfo

class List(ListView):
    template_name = 'list.html'
    paginate_by = 50
    search_fields = 'title'.split(',')

    def get_queryset(self):
        'apply keyword search'
        query = Movie.objects.all()
        search_phrase = self.request.REQUEST.get('search', None)
        if search_phrase:
            for bit in search_phrase:
                orm_lookups = ["%s__icontains" % search_field for search_field in self.search_fields]
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                query = query.filter(reduce(operator.or_, or_queries))
        return query      
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(List, self).dispatch(*args, **kwargs)
    
class ProtectedView(FormView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
