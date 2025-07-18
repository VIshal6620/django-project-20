from django.shortcuts import render
from ..ctl.BaseCtl import BaseCtl
from ..models import Customer
from ..service.CustomerService import CustomerService


class CustomerListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['clientName'] = requestForm.get('clientName', None)
        self.form['location'] = requestForm.get('location', None)
        self.form['contactNumber'] = requestForm.get('contactNumber', None)
        self.form['importance'] = requestForm.get('importance', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CustomerListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        CustomerListCtl.count += 1
        self.form['pageNo'] = CustomerListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Customer.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        CustomerListCtl.count -= 1
        self.form['pageNo'] = CustomerListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Customer.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res


    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "please select one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                record = self.get_service().get(id)
                if record:
                    self.get_service().delete(id)
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def submit(self, request, params={}):
        CustomerListCtl.count = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
           self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "CustomerList.html"

    def get_service(self):
        return CustomerService()
