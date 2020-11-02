import urllib

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .controllers.home_controller import HomeController
from .forms import InfoForm


def home(request):
    form = InfoForm()
    return render(request, 'home/home.html', {'form': form})


def submit(request):
    def request_to_dict(req):
        ret = {i: req.POST[i] for i in req.POST}
        if "recipient_resident" not in ret:
            ret["recipient_resident"] = False
        return ret
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InfoForm(request.POST)
        #print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            home_controller = HomeController()

            info_dict = request_to_dict(request)
            print(info_dict)
            validate_check = home_controller.validate_data(info_dict)
            #print(validate_check)
            if validate_check["sender"][1] == [] and validate_check["recipient"][1] == []:
                rates = home_controller.get_all_rates(info_dict)
                #print(rates)
                request.session['resp'] = rates
                return HttpResponseRedirect(reverse('home:result'))

    else:
        form = InfoForm()
    #print(form)
    #print(unitChoiceForm)
    error_message = {}
    if validate_check["recipient"][1] != []:
        errors = validate_check["recipient"][1]
        for i in range(len(errors)):
            error_message["Recipient Address Error"] = \
                error_message.setdefault("Recipient Address Error", [])\
                +[validate_check["recipient"][1][i]["message"]]
    if validate_check["sender"][1] != []:
        errors = validate_check["sender"][1]
        for i in range(len(errors)):
            error_message["Sender Address Error"] = \
                error_message.setdefault("Sender Address Error", [])\
                +[validate_check["sender"][1][i]["message"]]

    print(error_message)
    return render(request, 'home/home.html', {'form': form, "error_message": error_message})

def result(request):
    resp = request.session.get('resp')
    return render(request, 'home/result.html', {"resp":resp})