import json
import requests
import time
import hmac
import hashlib

class bitfapi:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.bitflyer.com"

    def header(self, method: str, endpoint: str, body: str) -> dict:
        # ヘッダ情報
        timestamp = str(time.time())
        if body == '':
            message = timestamp + method + endpoint
        else:
            message = timestamp + method + endpoint + body
        signature = hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'),
                            digestmod=hashlib.sha256).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'ACCESS-KEY': self.api_key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': signature
        }
        return headers


    def get_markets(self) -> json:
        # [Public] マーケットの一覧
        endpoint = '/v1/getmarkets'
        response = requests.get(self.base_url + endpoint)
        return response.json()


    def get_boards(self, product_code: str) -> json:
        # [Public] 板情報
        endpoint = '/v1/getboard'
        params = {"product_code": product_code}
        response = requests.get(self.base_url + endpoint, params)
        return response.json()


    def get_ticker(self, product_code: str) -> json:
        # [Public] Ticker
        endpoint = '/v1/ticker'
        params = {"product_code": product_code}
        response = requests.get(self.base_url + endpoint, params)
        return response.json()


    def get_executions(self, product_code: str, count = 100, before: str = None, after: str = None) -> json:
        # [Public] 約定履歴
        endpoint = '/v1/getexecutions'
        params = {
            "product_code": product_code,
            "count": str(count)
        }
        if before is not None:
            params['before'] = str(before)
        if after is not None:
            params['after'] = str(after)

        response = requests.get(self.base_url + endpoint, params)
        return response.json()


    def get_chats(self, from_date: str = None) -> json:
        # [Public] チャット取得
        endpoint = '/v1/getchats'

        if from_date is not None:
            params = {"from_date": from_date}
            response = requests.get(self.base_url + endpoint, params)
        else:
            response = requests.get(self.base_url + endpoint)

        return response.json()


    def get_permissions(self,) -> json:
        # [Private] APIキーの権限を取得
        endpoint = '/v1/me/getpermissions'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)

        return response.json()


    def get_balance(self) -> json:
        # 資産残高を取得
        endpoint = '/v1/me/getbalance'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_collateral(self) -> json:
        # 証拠金の状態を取得
        endpoint = '/v1/me/getcollateral'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_addresses(self) -> json:
        # 預入用アドレス取得
        endpoint = '/v1/me/getaddresses'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_coinins(self) -> json:
        # 仮想通貨預入履歴
        endpoint = '/v1/me/getcoinins'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_coinouts(self) -> json:
        # 仮想通貨送付履歴
        endpoint = '/v1/me/getcoinouts'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_bankaccounts(self) -> json:
        # 銀行口座一覧取得
        endpoint = '/v1/me/getbankaccounts'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_bankdeposits(self) -> json:
        # 入金履歴
        endpoint = '/v1/me/getbankdeposits'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_withdrawals(self) -> json:
        # 出金履歴
        endpoint = '/v1/me/getwithdrawals'
        headers = self.header('GET', endpoint=endpoint, body='')
        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def send_child_order(
        self, 
        product_code: str,
        child_order_type: str,
        side: str,
        size: float,
        price: int,
        minute_to_expire: int = 43200,
        time_in_force: str = "GTC") -> json:
        # 新規注文を出す
        endpoint = "/v1/me/sendchildorder"

        body = {
            "product_code": product_code,
            "child_order_type": child_order_type,
            "side": side,
            "size": size,
            "price": price,
            "minute_to_expire": minute_to_expire,
            "time_in_force": time_in_force
        }

        body = json.dumps(body)
        headers = self.header('POST', endpoint=endpoint, body=body)

        response = requests.post(
            self.base_url + endpoint, data=body, headers=headers)
        return response.json()


    def cancel_child_order(self, product_code: str, child_order_id: str = None, child_order_acceptance_id: str = None):
        # 注文をキャンセルする
        endpoint = "/v1/me/cancelchildorder"

        if child_order_acceptance_id is not None:
            body = {
                "product_code": product_code,
                "child_order_acceptance_id": child_order_acceptance_id
            }

        if child_order_id is not None:
            body = {
                "product_code": product_code,
                "child_order_id": child_order_id
            }

        body = json.dumps(body)
        headers = self.header('POST', endpoint=endpoint, body=body)

        response = requests.post(
            self.base_url + endpoint, data=body, headers=headers)
        response.raise_for_status()
        return True



    def send_parent_order(
        self, 
        order_method: str = "SIMPLE",
        minute_to_expire: int = 43200,
        time_in_force: str = "GTC",
        parameters: json = {
            "product_code": str,
            "condition_type": str,
            "side": str,
            "price": int,
            "trigger_price": int,
            "size": float
        }) -> json:
        # 新規の親注文を出す（特殊注文）
        endpoint = "/v1/me/sendparentorder"

        body = {
            "order_method": order_method,
            "minute_to_expire": minute_to_expire,
            "time_in_force": time_in_force,
            "parameters": parameters,
        }

        body = json.dumps(body)
        headers = self.header('POST', endpoint=endpoint, body=body)

        response = requests.post(
            self.base_url + endpoint, data=body, headers=headers)
        return response.json()


    def cancel_parent_order(
        self, 
        product_code: str,
        parent_order_id: str = None,
        parent_order_acceptance_id: str = None) -> json:
        # 親注文をキャンセルする
        endpoint = "/v1/me/cancelchildorder"

        if parent_order_acceptance_id is not None:
            body = {
                "product_code": product_code,
                "parent_order_acceptance_id": parent_order_acceptance_id
            }

        if parent_order_id is not None:
            body = {
                "product_code": product_code,
                "parent_order_id": parent_order_id
            }

        body = json.dumps(body)
        headers = self.header('POST', endpoint=endpoint, body=body)

        response = requests.post(
            self.base_url + endpoint, data=body, headers=headers)
        response.raise_for_status()
        return True



    def cancel_all_child_orders(self, product_code: str) -> json:
        # すべての注文をキャンセルする
        endpoint = "/v1/me/cancelallchildorders"

        body = {
            "product_code": product_code,
        }

        body = json.dumps(body)
        headers = self.header('POST', endpoint=endpoint, body=body)

        response = requests.post(
            self.base_url + endpoint, data=body, headers=headers)
        response.raise_for_status()
        return True



    def get_child_orders(
            self, 
            product_code: str = "BTC_JPY",
            count: str = 100,
            before: int = None,
            after: int = None,
            child_order_state: str = None,
            child_order_id: str = None,
            child_order_acceptance_id: str = None,
            parent_order_id: str = None) -> json:

        # 注文の一覧を取得
        endpoint = '/v1/me/getchildorders'

        params = {
            "product_code": product_code,
            "count": str(count),
        }

        if child_order_state is not None:
            params['child_order_state'] = child_order_state
        if child_order_id is not None:
            params['child_order_id'] = child_order_id
        if child_order_acceptance_id is not None:
            params['child_order_acceptance_id'] = child_order_acceptance_id
        if parent_order_id is not None:
            params['parent_order_id'] = parent_order_id

        if before is not None:
            params['before'] = str(before)
        if after is not None:
            params['after'] = str(after)

        
        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_parent_orders(
        self, 
        product_code: str = "BTC_JPY",
        count: int = 100,
        before: int = None,
        after: int = None,
        parent_order_state: str = None) -> json:
        # 親注文の一覧を取得
        endpoint = '/v1/me/getparentorders'

        params = {
            "product_code": product_code,
            "count": str(count),
        }

        if parent_order_state is not None:
            params['parent_order_state'] = parent_order_state

        if before is not None:
            params['before'] = str(before)
        if after is not None:
            params['after'] = str(after)

        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results


    def get_parent_order(
        self, 
        parent_order_state: str = None,
        parent_order_acceptance_id: str = None) -> json:
        # 親注文の詳細を取得
        endpoint = '/v1/me/getparentorders'

        params = {}

        if parent_order_state is not None:
            params['parent_order_state'] = parent_order_state
        if parent_order_acceptance_id is not None:
            params['child_order_acceptance_id'] = parent_order_acceptance_id

        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results

    def get_executions(
        self, 
        product_code: str = "BTC_JPY",
        count: str = 100,
        before: int = None,
        after: int = None,
        child_order_id: str = None,
        child_order_acceptance_id: str = None) -> json:

        # 約定の一覧を取得
        endpoint = '/v1/me/getexecutions'

        params = {
            "product_code": product_code,
            "count": str(count),
        }

        if child_order_id is not None:
            params['child_order_id'] = child_order_id
        if child_order_acceptance_id is not None:
            params['child_order_acceptance_id'] = child_order_acceptance_id

        if before is not None:
            params['before'] = str(before)
        if after is not None:
            params['after'] = str(after)

        
        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results

    def get_balance_history(
        self, 
        currency_code: str = "JPY",
        count: str = 100,
        before: int = None,
        after: int = None) -> json:

        # 残高履歴を取得
        endpoint = '/v1/me/getbalancehistory'

        params = {
            "currency_code": currency_code,
            "count": str(count),
        }

        if before is not None:
            params['before'] = str(before)
        if after is not None:
            params['after'] = str(after)

        
        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results

    def get_positions(self, product_code: str = "FX_BTC_JPY") -> json:

        # 建玉の一覧を取得
        endpoint = '/v1/me/getpositions'

        params = {
            "product_code": product_code
        }
        
        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results

    def get_collateral_history(
        self, 
        count: str = 100,
        before: int = None,
        after: int = None) -> json:

        # 証拠金の変動履歴を取得
        endpoint = '/v1/me/getcollateralhistory'

        params = {
            "count": str(count),
        }

        if before is not None:
            params['before'] = str(before)
        if after is not None:
            params['after'] = str(after)

        
        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results

    def get_trading_commission(self, product_code: str = "BTC_JPY") -> json:

        # 取引手数料を取得
        endpoint = '/v1/me/gettradingcommission'

        params = {
            "product_code": product_code
        }
        
        headers = self.header('GET', endpoint=endpoint, body='')
        headers |= params

        response = requests.get(self.base_url + endpoint, headers=headers)
        results = response.json()

        return results
