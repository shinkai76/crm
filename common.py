# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from suds.client import Client
import json
from datetime import datetime, timedelta
import random
import requests
import base64
import xlrd
import settings
import jwt
import base64
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import column, and_, or_, not_, select, text, exists, literal, union_all, case, alias, null, literal_column, extract, cast
from models import *

engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (settings.USER, settings.PASSWORD,
                                                              settings.DATA_HOST, settings.DATABASE), echo=True, client_encoding='utf8')
Session = sessionmaker(bind=engine)
partner_map = {}
employee_map = {}
product_map = {}

def get_params(request):
    params = request.params
    body = request.body.read()
    if body:
        rec = json.loads(body)
        for item in rec:
            params[item] = rec.get(item)
    return params


def request_user_token():
    params = {"device": "dingtalk", "version_code": "3.13.0", "login": settings.user_name, "password": settings.password}
    r = requests.post("%s/api/v2/auth/login" % settings.url, params = params)
    if r.status_code != 200 or (r.json().get("code") != 0):
        print r.text
        raise Exception(r.text)
    return r.json().get("data").get("user_token")

def get_set_of_book(session, set_of_book):
    set_of_book = session.query(SetOfBook).filter(SetOfBook.set_of_book == set_of_book).first()
    if not set_of_book:
        raise Exception(u'账套配置不存在')
    return set_of_book

def get_user_token(session, set_of_book):
    sob = get_set_of_book(session, set_of_book)
    return sob.user_token

def request_contracts_by_name(user_token, params):
    params["device"] = "dingtalk"
    params["version_code"] = "3.13.0"
    params["user_token"] = user_token
    r = requests.get("%s/api/v2/contracts/by_name" % settings.url, params=params)
    if r.status_code != 200 or (r.json().get("code") != 0):
        print r.text
        raise Exception(r.text)
    return r.json().get("data").get("contracts")

def request_contract_list(url, user_token, params):
    params["device"] = "dingtalk"
    params["version_code"] = "3.13.0"
    params["user_token"] = user_token
    r = requests.get("%s" % url, params=params)
    if r.status_code != 200 or (r.json().get("code") != 0):
        print r.text
        raise Exception(r.text)
    return r.json().get("data").get("contracts")

def request_contract_detail(user_token, id):
    params = ObjectDict()
    params["device"] = "dingtalk"
    params["version_code"] = "3.13.0"
    params["user_token"] = user_token
    r = requests.get("%s/api/v2/contracts/%s" % (settings.url, id), params=params)
    return r.json()


def download_contracts(session, set_of_book, params, user_name):
    user_token = get_user_token(session, set_of_book)
    title = params.get("title")
    page = params.get("page") or 1
    per_page = params.get("per_page") or 20
    approve_status = params.get("approve_status")
    _params = ObjectDict()
    _params["page"] = page
    _params["per_page"] = per_page
    if approve_status:
        _params["approve_status"] = approve_status
    if title:
        _params["query"] = title
        contracts = request_contracts_by_name(user_token, _params)
    else:
        category = params.get("category")
        if category:
            _params["category"] = category
        status = params.get("status")
        if status:
            _params["status"] = status
        time_type = params.get("time_type")
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        url = settings.url + '/api/v2/contracts'
        if start_date and end_date:
            if not time_type:
                raise Exception(u"必须传递时间类型")
            url += '?'+time_type+'[]='+start_date+'&'+time_type+'[]='+end_date
        contracts = request_contract_list(url, user_token, _params)
    try:
        for item in contracts:
            current = session.query(CrmContract).filter(CrmContract.contract_id == item.get("id"), CrmContract.set_of_book == set_of_book).first()
            if not current:
                new_contract = CrmContract(contract_id=item.get("id"), title=item.get("title"), set_of_book=set_of_book, download_at=datetime.now(), download_user=user_name)
                session.add(new_contract)
        session.commit()
        time.sleep(1)
        if len(contracts) < int(per_page):
            return None
        return int(page) + 1
    except Exception as e:
        session.rollback()
        raise e

def complete_download(session, set_of_book, id):
    current = session.query(CrmContract).filter(CrmContract.id == id, CrmContract.set_of_book == set_of_book).first()
    if not current:
        raise Exception(u'该合同不存在,请刷新后重试')
    if current.is_completed:
        return {"state": 1}
    user_token = get_user_token(session, set_of_book)
    contract = request_contract_detail(user_token, current.contract_id)
    if contract.get("code") == 0:
        contract_ = contract.get("data")
        current.category = contract_.get("category")
        current.category_mapped = contract_.get("category_mapped")
        current.status = contract_.get("status")
        current.status_mapped = contract_.get("status_mapped")
        current.total_amount = contract_.get("total_amount")
        current.sign_date = contract_.get("sign_date")
        current.sn = contract_.get("sn")
        current.approve_status = contract_.get("approve_status")
        current.approve_status_i18n = contract_.get("approve_status_i18n")
        current.owned_department = contract_.get("owned_department")
        current.product_assets_for_new_record = {"items": contract_.get("product_assets_for_new_record")}
        current.created_at = contract_.get("created_at")
        current.updated_at = contract_.get("updated_at")
        current.creator = contract_.get("creator")
        current.customer = contract_.get("customer")
        current.completed_at = datetime.now()
        current.is_completed = True
        session.commit()
        return {"state": 1}
    else:
        print contract
        raise Exception(contract)

def query_contracts(session, set_of_book, params):
    a = crm_contracts
    fields = [a]
    q = select(fields, from_obj=(a)).where(a.c.set_of_book == set_of_book)
    if params.get("title"):
        q = q.where(a.c.title == params.get("title"))
    if params.get("start_date"):
        q = q.where(a.c.download_at >= params.get("start_date"))
    if params.get("end_date"):
        q = q.where(a.c.download_at <= params.get("end_date"))
    if params.get("approve_status"):
        q = q.where(a.c.approve_status == params.get("approve_status"))
    if params.get("status"):
        q = q.where(a.c.status == params.get("status"))
    if params.get("category"):
        q = q.where(a.c.category == params.get("category"))
    is_imported = params.get("is_imported")
    if is_imported:
        if int(is_imported) == 1:
            q = q.where(a.c.is_imported == True)
        else:
            q = q.where(a.c.is_imported == False)
    is_completed = params.get("is_completed")
    if is_completed:
        if int(is_completed) == 1:
            q = q.where(a.c.is_completed == True)
        else:
            q = q.where(a.c.is_completed == False)
    start = params.get("start")
    limit = params.get("limit")
    results = []
    if start and limit:
        x = q.alias("x")
        total = session.execute(x.count()).scalar()
        trades = session.execute(q.order_by(a.c.created_at.desc()).offset(start).limit(limit)).fetchall()
        for item in trades:
            trade = ObjectDict(id=item.id, contract_id=item.contract_id, category=item.category, category_mapped=item.category_mapped, status=item.status, status_mapped=item.status_mapped, title=item.title, total_amount=item.total_amount, sign_date=item.sign_date.strftime('%Y-%m-%d %H:%M:%S') if item.sign_date else "", updated_at=item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else "", created_at=item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else "", sn=item.sn, is_imported=item.is_imported, imported_at=item.imported_at.strftime('%Y-%m-%d %H:%M:%S') if item.imported_at else "", imported_user=item.imported_user, approve_status=item.approve_status, sale_docuemnt_id=item.sale_document_id, approve_status_i18n=item.approve_status_i18n, product_assets_for_new_record=item.product_assets_for_new_record, creator=item.creator, customer=item.customer, is_completed=item.is_completed, download_at=item.download_at, download_user=item.download_user, sale_document_code=item.sale_document_code, department_id=item.department_id, partner_id=item.partner_id, employee_id=item.employee_id, set_of_book=item.set_of_book)
            results.append(trade)
    else:
        trades = session.execute(q.order_by(a.c.created_at.desc())).fetchall()
        for item in trades:
            trade = ObjectDict(id=item.id, contract_id=item.contract_id, category=item.category, category_mapped=item.category_mapped, status=item.status, status_mapped=item.status_mapped, title=item.title, total_amount=item.total_amount, sign_date=item.sign_date.strftime('%Y-%m-%d %H:%M:%S') if item.sign_date else "", updated_at=item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else "", created_at=item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else "", sn=item.sn, is_imported=item.is_imported, imported_at=item.imported_at.strftime('%Y-%m-%d %H:%M:%S') if item.imported_at else "", imported_user=item.imported_user, approve_status=item.approve_status, sale_docuemnt_id=item.sale_document_id, approve_status_i18n=item.approve_status_i18n, product_assets_for_new_record=item.product_assets_for_new_record, creator=item.creator, customer=item.customer, is_completed=item.is_completed, download_at=item.download_at, download_user=item.download_user, sale_document_code=item.sale_document_code, department_id=item.department_id, partner_id=item.partner_id, employee_id=item.employee_id, set_of_book=item.set_of_book)
            results.append(trade)
        total = len(results)
    result = {"total": total, "state": 1, "root": results}
    return result


def import_as_sale_document(session, id, set_of_book, params, url, token, user_name):
    id = int(id)
    shop = get_set_of_book(session, set_of_book)
    current = session.query(CrmContract).filter(CrmContract.id == id, CrmContract.set_of_book == set_of_book).first()
    if not current:
        raise Exception(u"id 为 %s 的合同不存在" % id)
    if current.is_imported:
        raise Exception(u" id 为 %s 的合同已导入,不能重复导入" % id)
    if not current.is_completed:
        raise Exception(u"id 为 %s 的合同未下载完成,请等待下载完成后再导入" % id)
    sale_document = generate_sale_document(url, token, current, shop, set_of_book)
    current.is_imported = True
    current.imported_user = user_name
    current.imported_at = datetime.now()
    current.sale_document_code = sale_document.code
    current.sale_document_id = sale_document.id
    current.department_id = sale_document.department_id
    current.partner_id = sale_document.partner_id
    current.employee_id = sale_document.employee_id
    session.commit()
    confirm_sale_document(url, token, sale_document.id)
    return {"state": 1}


def generate_sale_document(url, token, order, shop, set_of_book):
    headers = {"Token": token}
    data = ObjectDict(source="crm", source_id=order.id, store_id=shop.default_store_id, bill_type=shop.default_bill_type,  memo="")
    tax_rate = 0
    if data.bill_type != 0:
        sob = get_tax_rate(url, token, set_of_book)
        if data.bill_type == 1:
            tax_rate = sob.get("tax_rate")
        else:
            tax_rate = sob.get("vat_tax_rate")
    partner_name = order.customer.get("name")
    if partner_name in partner_map:
        partner = partner_map.get(partner_name)
    else:
        partner = get_partner(url, token, partner_name)
        partner_map[partner_name] = partner
    data.partner_id = partner.get("id")
    data.credit_period = partner.get("credit_period")
    data.account_period = (datetime.now() + timedelta(days=partner.get("credit_period"))).strftime('%Y-%m-%d %H:%M:%S')
    employee_name = order.creator.get("name")
    if employee_name in employee_map:
        employee = employee_map.get(employee_name)
    else:
        employee = get_employee(url, token, employee_name)
        employee_map[employee_name] = employee
    data.employee_id = employee.get("id")
    data.department_id = employee.get("department_id")
    data.delivery_period = 0
    data.delivery_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sale_document_lines = []
    for item in order.product_assets_for_new_record.get("items"):
        line = ObjectDict()
        if item.get("product_no") in product_map:
            product = product_map.get(item.get("product_no"))
        else:
            product = get_product_by_barcode(url, token, item.get("product_no"))
            product_map[item.get("product_no")] = product
        line.product_id = product.id
        line.quantity = item.get("quantity")
        line.tax_price = item.get("recommended_unit_price")
        line.tax_rate = tax_rate
        line.memo = item.get("remark")
        sale_document_lines.append(line)
    data.sale_document_lines = sale_document_lines
    r = requests.post("%s/api/sale_documents" % url, headers=headers, data=json.dumps(data))
    if r.status_code != 200:
        raise Exception(r.text)
    return json.loads(r.text, object_pairs_hook=ObjectDict)


def check_sale_document(session, id, set_of_book, params, url, token):
    current = session.query(CrmContract).filter(CrmContract.id == id, CrmContract.is_imported == True, CrmContract.set_of_book == set_of_book).first()
    if not current:
        return {"state": 1}
    sale_document = get_sale_document(url, token, current.sale_document_id)
    if not sale_document:
        current.is_imported = False
        current.imported_at = None
        current.imported_user = None
        current.sale_document_id = None
        current.sale_document_code = None
        current.department_id = None
        current.partner_id = None
        current.employee_id = None
    else:
        return {"state": 0, "errmsg": u"该合同对应的销售订单依然存在,请删除后重试"}
    session.commit()
    return {"state": 1}


def get_sale_document(url, token, id):
    headers = {"Token": token}
    r = requests.get("%s/api/sale_documents/%s" % (url, id), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.text or r.text == "null":
        return False
    return True


def get_partner(url, token, name):
    headers = {"Token": token}
    params = {"name": name}
    r = requests.get("%s/api/partners" % url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.json().get("root"):
        raise Exception(u"商业伙伴 %s 不存在" % name)
    return r.json().get("root")[0]


def get_employee(url, token, name):
    headers = {"Token": token}
    params = {"name": name}
    r = requests.get("%s/api/employees" % url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.json().get("root"):
        raise Exception(u"员工 %s 不存在" % name)
    return r.json().get("root")[0]


def get_product_by_barcode(url, token, barcode):
    headers = {"Token": token}
    params = {"barcode": barcode}
    r = requests.get("%s/api/products" % url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.json().get("root"):
        raise Exception(u"产品码为 %s 的商品不存在" % barcode)
    product = ObjectDict(r.json().get("root")[0])
    return product

def get_tax_rate(url, token, set_of_book):
    headers = {"Token": token}
    r = requests.get("%s/api/set_of_books/%s" % (url, set_of_book), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    return r.json()


def confirm_sale_document(url, token, sale_document_id):
    headers = {"Token": token}
    r = requests.get("%s/api/sale_documents/%s?action=confirm&action_type=1" % (url, sale_document_id), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    return True