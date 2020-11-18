#encoding=utf-8
 
from common import Session, get_user_token, request_contract_detail, get_set_of_book, request_user_token, time, datetime, CrmContract

set_of_book = "c9"
session = Session()
while True:
    try:
        user_token = get_user_token(session, set_of_book)
        contracts = session.query(CrmContract).filter(CrmContract.is_completed == False, CrmContract.set_of_book == set_of_book).all()
        for item in contracts:
            contract = request_contract_detail(user_token, item.contract_id)
            if contract.get("code") == 0:
                contract_ = contract.get("data")
                item.category = contract_.get("category")
                item.category_mapped = contract_.get("category_mapped")
                item.status = contract_.get("status")
                item.status_mapped = contract_.get("status_mapped")
                item.total_amount = contract_.get("total_amount")
                item.sign_date = contract_.get("sign_date")
                item.sn = contract_.get("sn")
                item.approve_status = contract_.get("approve_status")
                item.approve_status_i18n = contract_.get("approve_status_i18n")
                item.owned_department = contract_.get("owned_department")
                item.product_assets_for_new_record = {"items": contract_.get("product_assets_for_new_record")}
                item.created_at = contract_.get("created_at")
                item.updated_at = contract_.get("updated_at")
                item.creator = contract_.get("creator")
                item.customer = contract_.get("customer")
                item.completed_at = datetime.now()
                item.is_completed = True
            elif contract.get("code") == 100401:
                user_token = request_user_token()
                sob = get_set_of_book(session, set_of_book)
                sob.user_token = user_token
                session.commit()
            else:
                print contract
                time.sleep(1)
                continue
            time.sleep(1)
        session.commit()
        print u"下载完成:"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(60*10)
    except Exception as e:
        print str(e)
        time.sleep(60)
