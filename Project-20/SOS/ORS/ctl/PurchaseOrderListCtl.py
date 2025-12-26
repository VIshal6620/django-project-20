from django.shortcuts import render, redirect
from ..ctl.BaseCtl import BaseCtl
from ..models import PurchaseOrder
from ..service.PurchaseOrderService import PurchaseOrderService


class PurchaseOrderListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['totalQuantity'] = requestForm.get("totalQuantity", None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        PurchaseOrderListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        PurchaseOrderListCtl.count += 1
        self.form['pageNo'] = PurchaseOrderListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = PurchaseOrder.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        PurchaseOrderListCtl.count -= 1
        self.form['pageNo'] = PurchaseOrderListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/PurchaseOrder/")
        return res

    def submit(self, request, params={}):
        PurchaseOrderListCtl.count = 1
        self.form['pageNo'] = PurchaseOrderListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        ress = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return ress

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                college = self.get_service().get(id)
                if college:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = PurchaseOrder.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def get_template(self):
        return "PurchaseOrderList.html"

    def get_service(self):
        return PurchaseOrderService()
