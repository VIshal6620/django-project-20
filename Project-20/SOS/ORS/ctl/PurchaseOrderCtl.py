from django.shortcuts import render

from ..ctl.BaseCtl import BaseCtl
from ..models import PurchaseOrder
from ..service.PurchaseOrderService import PurchaseOrderService
from ..utility.DataValidator import DataValidator


class PurchaseOrderCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['totalQuantity'] = requestForm['totalQuantity']
        self.form['product'] = requestForm['product']
        self.form['orderDate'] = requestForm['orderDate']
        self.form['totalCost'] = requestForm['totalCost']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.totalQuantity = self.form['totalQuantity']
        obj.product = self.form['product']
        obj.orderDate = self.form['orderDate']
        obj.totalCost = self.form['totalCost']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["totalQuantity"] = obj.totalQuantity
        self.form["product"] = obj.product
        self.form["orderDate"] = obj.orderDate
        self.form["totalCost"] = obj.totalCost

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['totalQuantity'])):
            inputError['totalQuantity'] = "totalQuantity is required"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['totalQuantity'])):
                inputError['totalQuantity'] = "totalQuantity contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['product'])):
            inputError['product'] = "product is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['product'])):
                inputError['product'] = "product contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['orderDate'])):
            inputError['orderDate'] = "orderDate is required"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['orderDate'])):
                inputError['orderDate'] = "orderDate contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['totalCost'])):
            inputError['totalCost'] = "totalCost is required"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['totalQuantity'])):
                inputError['totalCost'] = "totalCost contains only letters"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            purchaseorder = self.get_service().get(params['id'])
            self.model_to_form(purchaseorder)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(PurchaseOrder())
        self.get_service().save(r)
        self.form['message'] = "Data saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "PurchaseOrder.html"

    def get_service(self):
        return PurchaseOrderService()