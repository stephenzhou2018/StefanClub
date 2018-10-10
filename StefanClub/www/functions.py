import copy
from models import TaobaoProducts

def analysis_specify_filter(specify_filter):
    and_index = -1
    first_spe_filter = ''
    second_spe_filter = ''
    if len(specify_filter) > 0:
        if 'and' in specify_filter:
            and_index = specify_filter.index('and')
            first_spe_filter = specify_filter[:and_index]
            second_spe_filter = specify_filter[and_index + 3:]
        else:
            first_spe_filter = specify_filter
    else:
        pass
    return first_spe_filter, second_spe_filter


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


async def get_taobao_chart1(chart1):
    series = chart1['series']
    xAxis = chart1['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        where_clause = ''
        parameter = []
        select_filed = 'sum(product_sales_qty)'
        salesqty_list = []
        if name != 'ALL':
            where_clause = where_clause + 'keyword=?'
            parameter.extend([name])
        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if category == '<=100':
                real_where_clause = real_where_clause + (
                    ' and product_price_float <= ?' if name != 'ALL' else 'product_price_float <= ?')
                real_parameter.extend([100])
            elif category == '>=5000':
                real_where_clause = real_where_clause + (
                    ' and product_price_float >= ?' if name != 'ALL' else 'product_price_float >= ?')
                real_parameter.extend([5000])
            else:
                real_where_clause = real_where_clause + (
                    ' and product_price_float >= ?' if name != 'ALL' else 'product_price_float >= ?') + ' and product_price_float <= ?'
                if category == '100-500':
                    real_parameter.extend([100, 500])
                elif category == '500-1000':
                    real_parameter.extend([500, 1000])
                elif category == '1000-5000':
                    real_parameter.extend([1000, 5000])
            salesqty = await TaobaoProducts.findNumber(select_filed, real_where_clause, real_parameter)
            if salesqty:
                salesqty = int(salesqty)
            else:
                salesqty = 0
            salesqty_list.append(salesqty)
        new_singleseries = {'name': name, 'data': salesqty_list}
        series[index] = new_singleseries
        index += 1
    chart1['series'] = series
    return chart1


async def get_taobao_chart2(chart2):
    series = chart2['series']
    xAxis = chart2['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        where_clause = ''
        parameter = []
        select_filed = 'sum(product_sales_qty)'
        salesqty_list = []
        if name != 'ALL':
            where_clause = where_clause + 'keyword=?'
            parameter.extend([name])
        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if category == '金冠以上':
                real_where_clause = real_where_clause + (' and shopleveljingguanqty > 0' if name != 'ALL' else 'shopleveljingguanqty > 0')
            elif category == '皇冠':
                real_where_clause = real_where_clause + (' and shopleveljingguanqty = 0' if name != 'ALL' else 'shopleveljingguanqty = 0') + ' and shoplevelguanqty > 0'
            elif category == '钻石':
                real_where_clause = real_where_clause + (' and shopleveljingguanqty = 0' if name != 'ALL' else 'shopleveljingguanqty = 0') + ' and shoplevelguanqty = 0' + ' and shoplevelzuanqty > 0'
            else:
                real_where_clause = real_where_clause + (' and shopleveljingguanqty = 0' if name != 'ALL' else 'shopleveljingguanqty = 0') + ' and shoplevelguanqty = 0' + ' and shoplevelzuanqty = 0' + ' and shoplevelxinqty > 0'
            salesqty = await TaobaoProducts.findNumber(select_filed, real_where_clause, real_parameter)
            if salesqty:
                salesqty = int(salesqty)
            else:
                salesqty = 0
            salesqty_list.append(salesqty)
        new_singleseries = {'name': name, 'data': salesqty_list}
        series[index] = new_singleseries
        index += 1
    chart2['series'] = series
    return chart2











