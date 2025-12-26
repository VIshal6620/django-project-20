from django.db.backends.base import client
from django.shortcuts import render
from ..ctl.BaseCtl import BaseCtl
from ..models import Client
from ..service.ClientService import ClientService
from ..utility.DataValidator import DataValidator


class ClientCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['fullName'] = requestForm['fullName']
        self.form['appoinmentDate'] = requestForm['appoinmentDate']
        self.form['phone'] = requestForm['phone']
        self.form['illness'] = requestForm['illness']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.fullName = self.form['fullName']
        obj.appoinmentDate = self.form['appoinmentDate']
        obj.phone = self.form['phone']
        obj.illness = self.form['illness']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["fullName"] = obj.fullName
        self.form["appoinmentDate"] = obj.appoinmentDate
        self.form["phone"] = obj.phone
        self.form["illness"] = obj.illness

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['fullName'])):
            inputError['fullName'] = "fullName is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['fullName'])):
                inputError['fullName'] = "fullName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['appoinmentDate'])):
            inputError['appoinmentDate'] = "appoinmentDate is required"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['appoinmentDate'])):
                inputError['appoinmentDate'] = "appoinmentDate contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['phone'])):
            inputError['phone'] = "phone is required"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['phone'])):
                inputError['phone'] = "phone contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['illness'])):
            inputError['illness'] = "illness is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['illness'])):
                inputError['illness'] = "illness contains only letters"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            client = self.get_service().get(params['id'])
            self.model_to_form(client)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Client())
        self.get_service().save(r)
        self.form['message'] = "Data saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Client.html"

    def get_service(self):
        return ClientService()