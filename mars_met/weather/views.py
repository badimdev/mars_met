
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *

def index_view(request):

  mars_met_data = magnitude.objects.all()
  mars_met_data = mars_met_data.order_by('sol')

  return render_to_response('weather/index.html', {'mars_met_data':mars_met_data},context_instance=RequestContext(request))