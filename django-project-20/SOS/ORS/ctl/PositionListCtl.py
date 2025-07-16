from django.shortcuts import render

from ..ctl.BaseCtl import BaseCtl
from ..models import Position
from ..service.PositionService import PositionService


class PositionListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['designation'] = requestForm.get('designation', None)
        self.form['openingDate'] = requestForm.get('openingDate', None)
        self.form['requiredExperience'] = requestForm.get('requiredExperience', None)
        self.form['condition'] = requestForm.get('condition', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        PositionListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        PositionListCtl.count += 1
        self.form['pageNo'] = PositionListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Position.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        PositionListCtl.count -= 1
        self.form['pageNo'] = PositionListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Position.objects.last().id
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
        PositionListCtl.count = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
           self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "PositionList.html"

    def get_service(self):
        return PositionService()
