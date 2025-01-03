from django.shortcuts import render
from ..ctl.BaseCtl import BaseCtl
from ..models import Role
from ..service.RoleService import RoleService
from ..utility.DataValidator import DataValidator


class RoleCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id']=requestForm['id']
        self.form['name']=requestForm['name']
        self.form['description']=requestForm['description']


    def form_to_model(self, obj):
        pk = int(self.form['id '])
        if pk > 0:
            obj.id = pk
        obj.name=self.form['name']
        obj.description=self.form['description']
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form['name']=obj.name
        self.form['description']=obj.description

    def input_validation(self):
        super().input_validation()
        inputError=self.form['inputError']

        if(DataValidator.isNull(self.form['name'])):
            inputError['name']="Name is Required"
            self.form['error']=True
        else:
            if(DataValidator.isAlphaCheck(self.form['name'])):
                inputError['name']="Name only contain Letters"
                self.form['error']=True

        if(DataValidator.isNull(self.form['description'])):
            inputError['description']="Description is Required"
            self.form['error']=True
        else:
            if(DataValidator.isAlphaCheck(self.form['description'])):
                inputError['description']="Description only contain Letters"
                self.form['error']=True

        return self.form['error']


    def display(self, request, params={}):
        res=render(request,self.get_template(),{'form':self.form})
        return res

    def submit(self, request, params={}):
        r=self.form_to_model(Role())
        self.get_service().save(r)
        res = render(request,self.get_template(),{'form':self.form})
        return res

    def get_template(self):
        return "Role.html"

    def get_service(self):
        return RoleService()