from django.shortcuts import render

from ..ctl.BaseCtl import BaseCtl
from ..models import Position
from ..service.PositionService import PositionService
from ..utility.DataValidator import DataValidator

from ..utility.HtmlUtility import HTMLUtility


class PositionCtl(BaseCtl):

    def preload(self, request, params):

        self.form["condition"] = request.POST.get('condition', '')


        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["condition"] = obj.condition


        self.static_preload = {"open": "open", "onhold": "onhold","hold":"hold"}


        self.form["preload"]["condition"] = HTMLUtility.get_list_from_dict(
            'condition',
            self.form["condition"],
            self.static_preload
        )


    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["designation"] = requestForm["designation"]
        self.form["openingDate"] = requestForm["openingDate"]
        self.form["requiredExperience"] = requestForm["requiredExperience"]
        self.form["condition"] = requestForm["condition"]


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.designation = self.form["designation"]
        obj.openingDate = self.form["openingDate"]
        obj.requiredExperience = self.form["requiredExperience"]
        obj.condition = self.form["condition"]
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["designation"] = obj.designation
        self.form["openingDate"] = obj.openingDate
        self.form["requiredExperience"] = obj.requiredExperience
        self.form["condition"] = obj.condition


    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form["designation"])):
            inputError["designation"] = "designation is required"
            self.form["error"] = True
        # else:
        #     if (DataValidator.isAlphaCheck(self.form['designation'])):
        #         inputError['designation'] = "designation is required"
        #         self.form['error'] = True

        if (DataValidator.isNull(self.form["openingDate"])):
            inputError["openingDate"] = "openingDate is required"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form['openingDate'])):
                inputError['openingDate'] = "openingDate is required"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["requiredExperience"])):
            inputError["requiredExperience"] = "requiredExperience  is required"
            self.form["error"] = True
        else:
            if (DataValidator.isAlphaCheck(self.form['requiredExperience'])):
                inputError['loginId'] = "requiredExperience is required"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["condition"])):
            inputError["condition"] = "condition is required"
            self.form["error"] = True
        # else:
        #     if (DataValidator.isAlphaCheck(self.form['condition'])):
        #         inputError['condition'] = "condition is required"
        #         self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Position())
        self.get_service().save(r)
        self.form['message'] = "Data saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Position.html"

    def get_service(self):
        return PositionService()
