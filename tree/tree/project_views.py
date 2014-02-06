import json

import django
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def load(request, addr):
    with open('json1.json', 'r') as json1_file:
        node = json.load(json1_file)
        check_root = 0
        lis = addr.strip('/').split("/")
        for element in lis:
            # condition to enter in root node, which is in dictionary format
            if check_root == 0:
                check_root = 1
                prev_element = element
                if node['slug'] == lis[-1]:
                    break
            # condition to enter in rest of the cases which are in list format
            else:
                # condition to check that we are entering right url, else it will redirect to page not found
                if node['slug'] == prev_element and node['kind'] == 'Topic':
                    for child in node['children']:
                        if child['slug'] == element:
                            node = child
                            break
                prev_element = element
        # the last slug in the list is checked here
        if node['slug'] == lis[-1]:
            if node['kind'] == 'Topic':
                return render(request, 'parent.html', {'node': node})
            else:
                return render(request, 'child.html', {'node': node})
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
