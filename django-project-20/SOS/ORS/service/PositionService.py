from django.db import connection
from .BaseService import BaseService
from ..models import Position
from ..utility.DataValidator import DataValidator


class PositionService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_Position where 1=1"
        val = params.get("designation", None)
        if DataValidator.isNotNull(val):
            sql += " and designation like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        print("--------", sql, pageNo, self.pageSize)
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "designation", "openingDate", "requiredExperience", "condition")
        res = {
            "data": [],
        }
        res["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Position
