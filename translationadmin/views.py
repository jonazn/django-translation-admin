from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from translationadmin.utility import is_translator
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from polib import pofile
import os
import json

@user_passes_test(is_translator)
def index(request):
    app_list = settings.TRANSLATE_APP_LIST
    context = {'app_list': []}
    for app_name in app_list:
        app_dir = os.path.join(settings.BASE_DIR, app_name)
        po_path = os.path.join(app_dir, 'locale')
        app_data = {
            'name': app_name,
            'languages': os.listdir(po_path),
        }
        context['app_list'].append(app_data)
        
    return render(request, 'translationadmin/index.html', context)
    
@user_passes_test(is_translator)
def edit(request, app_name, language_code):
    po_path = os.path.join(settings.BASE_DIR, app_name, 'locale', language_code, 'LC_MESSAGES', 'django.po')
    pof = pofile(po_path)
    context = {'pof': pof, 'po_path': po_path, 'app_name': app_name, 'language_code': language_code}
    return render(request, 'translationadmin/edit.html', context)
    
@user_passes_test(is_translator)
def edit_post(request, app_name, language_code):
    if request.method == 'POST' and request.is_ajax():
        ret = {'success': True, 'message': 'Success.'}
        errors = []
        po_path = os.path.join(settings.BASE_DIR, app_name, 'locale', language_code, 'LC_MESSAGES', 'django.po')
        mo_path = os.path.join(settings.BASE_DIR, app_name, 'locale', language_code, 'LC_MESSAGES', 'django.mo')
        pof = pofile(po_path)
        
        for entry_data in json.loads(request.POST.get('translation_data')):
            msgstr = entry_data.get('msgstr', None)
            msgctxt = entry_data.get('msgctxt', None)
            if msgctxt:
                entry = pof.find(entry_data['msgid'], msgctxt=msgctxt)
            else:
                entry = pof.find(entry_data['msgid'])
            if entry:
                entry.msgstr = msgstr
                if entry_data['fuzzy']:
                    if 'fuzzy' not in entry.flags:
                        entry.flags.append('fuzzy')
                else:
                    if 'fuzzy' in entry.flags:
                        entry.flags.remove('fuzzy')
                if 'python-format' in entry.flags:
                    # correct for erroneous python-format
                    if '%(' not in entry.msgid and ')s' not in entry.msgid:
                        entry.flags.remove('python-format')
            else:
                errors.append("Couldn't find entry for " + str(entry_data['msgid']))
        if len(errors) > 0:
            ret['success'] = False
            ret['errors'] = errors
            
        pof.save(po_path) # save as po
        pof.save_as_mofile(mo_path) # save as mo
        
        return HttpResponse(json.dumps(ret), content_type='application/json')