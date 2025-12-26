from django.db import connection
from ..models import PurchaseOrder
from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator


class PurchaseOrderService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from sos_purchaseorder where 1=1'
        val = params.get('totalQuantity', None)
        if (DataValidator.isNotNull(val)):
            sql += " and totalQuantity like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'totalQuantity', 'product','orderDate','totalCost')
        res = {
            "data": [],
        }
        params["index"] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return PurchaseOrder