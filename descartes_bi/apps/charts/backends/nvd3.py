from __future__ import absolute_import

import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .base import ChartBackend


class NovusD3(ChartBackend):
    label = _('Novus D3')

    options = {
        'name': 'chart_type',
        'label': _('chart type'),
        'choices': (
            ('SI', _('Standard X,Y')),
            ('SH', _('Horizontal X,Y')),
            ('PI', _('Pie chart')),
            ('LB', _('Line Plus Bar Chart')),
            ('LI', _('Line chart')),
            ('LF', _('Line chart with Focus')),
        )
    }

    def render(self, report, request):
        series_results = report.execute(request)

        serie = []

        #TODO: Improve
        for series_result in series_results:
            for i in series_result:
                for k, v in i.iteritems():
                    serie.append({"x": k, "y": v})

        series_chart_data = [{"values": serie, "key": report.title, "bar": "true"}]

        context = {
            'series_results': """%s;\n""" % json.dumps(series_chart_data),
            'report': report,
            'chart_type': 'SI',
        }

        return render_to_response('charts/novus/multiBarChart.html', context,
            context_instance=RequestContext(request))
