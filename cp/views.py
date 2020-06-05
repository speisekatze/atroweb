from django.views import generic


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Home'
        return context
