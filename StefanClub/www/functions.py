import copy
from models import TaobaoProducts,ZhaoPinJobs

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


async def get_taobao_chart3(chart3):
    series = chart3['series']
    xAxis = chart3['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        where_clause = ''
        parameter = []
        select_filed = 'sum(product_sales_qty)'
        salesqty_list = []
        if name != 'BOTH':
            where_clause = where_clause + 'keyword=?'
            parameter.extend([name])
        else:
            where_clause = where_clause + "(keyword = 'UNIQLO' or keyword = 'SUPERME')"
        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if category == '男装':
                real_where_clause = real_where_clause + " and title like ?"
                real_parameter.extend(['%男%'])
            else:
                real_where_clause = real_where_clause + " and (title like ? or title like ?)"
                real_parameter.extend(['%女%','%裙%'])
            salesqty = await TaobaoProducts.findNumber(select_filed, real_where_clause, real_parameter)
            if salesqty:
                salesqty = int(salesqty)
            else:
                salesqty = 0
            salesqty_list.append(salesqty)
        new_singleseries = {'name': name, 'data': salesqty_list}
        series[index] = new_singleseries
        index += 1
    chart3['series'] = series
    return chart3


async def get_taobao_chart4(chart4):
    series = chart4['series']
    subseries = series[0]
    data = subseries['data']
    index = 0
    for singledata in data:
        singledata_type = None
        if isinstance(singledata,list):
            name = singledata[0]
            singledata_type = 'list'
        else:
            name = singledata['name']
            singledata_type = 'dict'
        where_clause = ''
        parameter = []
        select_filed = 'sum(product_sales_qty)'
        if name == '长三角':
            where_clause = where_clause + '(shopaddress like ? or shopaddress like ? or shopaddress like ?)'
            parameter.extend(['%上海%', '%浙江%', '%江苏%'])
        elif name == '珠三角':
            where_clause = where_clause + '(shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ?)'
            parameter.extend(['%广东%', '%香港%', '%广西%', '%海南%'])
        elif name == '京津冀':
            where_clause = where_clause + '(shopaddress like ? or shopaddress like ? or shopaddress like ?)'
            parameter.extend(['%北京%', '%天津%', '%河北%'])
        elif name == '海外':
            where_clause = where_clause + '(shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ?)'
            parameter.extend(['%日本%', '%海外%', '%越南%','%美国%', '%加拿大%', '%西班牙%','%韩国%', '%德国%'])
        else:
            where_clause = where_clause + '!(shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ? or shopaddress like ?)'
            parameter.extend(['%日本%', '%海外%', '%越南%', '%美国%', '%加拿大%', '%西班牙%', '%韩国%', '%德国%', '%北京%', '%天津%', '%河北%', '%广东%', '%香港%', '%广西%', '%海南%', '%上海%', '%浙江%', '%江苏%'])
        salesqty = await TaobaoProducts.findNumber(select_filed, where_clause, parameter)
        if salesqty:
            salesqty = int(salesqty)
        else:
            salesqty = 0
        if singledata_type == 'list':
            singledata[1] = salesqty
        else:
            singledata['y'] = salesqty
        data[index] = singledata
        index += 1
    subseries['data'] = data
    series[0] = subseries
    return series


async def get_taobao_chart5(chart5):
    series = chart5['series']
    xAxis = chart5['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        where_clause = ''
        parameter = []
        select_filed = 'max(product_sales_qty)'
        salesqty_list = []
        if name != 'ALL':
            where_clause = where_clause + 'keyword=?'
            parameter.extend([name])
        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if name != 'ALL':
                real_where_clause = real_where_clause + ' and '
            real_where_clause = real_where_clause + '(iconkey1 = ? or iconkey2 = ? or iconkey3 = ? or iconkey4 = ? or iconkey5 = ?)'
            if category == '天猫':
                real_parameter.extend(['icon-service-tianmao','icon-service-tianmao','icon-service-tianmao','icon-service-tianmao','icon-service-tianmao'])
            elif category == '金牌卖家':
                real_parameter.extend(['icon-service-jinpaimaijia', 'icon-service-jinpaimaijia', 'icon-service-jinpaimaijia', 'icon-service-jinpaimaijia', 'icon-service-jinpaimaijia'])
            elif category == '新品':
                real_parameter.extend(['icon-service-xinpin', 'icon-service-xinpin', 'icon-service-xinpin','icon-service-xinpin','icon-service-xinpin'])
            elif category == '热卖':
                real_parameter.extend(['icon-service-remai', 'icon-service-remai', 'icon-service-remai', 'icon-service-remai','icon-service-remai'])
            elif category == '天猫国际':
                real_parameter.extend(['icon-service-tianmaoguoji', 'icon-service-tianmaoguoji', 'icon-service-tianmaoguoji','icon-service-tianmaoguoji','icon-service-tianmaoguoji'])
            elif category == '保险':
                real_parameter.extend(['icon-service-baoxian', 'icon-service-baoxian', 'icon-service-baoxian', 'icon-service-baoxian','icon-service-baoxian'])
            elif category == '服务':
                real_parameter.extend(['icon-service-fuwu', 'icon-service-fuwu', 'icon-service-fuwu', 'icon-service-fuwu','icon-service-fuwu'])
            else:
                real_parameter.extend(['icon-fest-tmallzhisongonly', 'icon-fest-tmallzhisongonly', 'icon-fest-tmallzhisongonly', 'icon-fest-tmallzhisongonly','icon-fest-tmallzhisongonly'])
            salesqty = await TaobaoProducts.findNumber(select_filed, real_where_clause, real_parameter)
            if salesqty:
                salesqty = int(salesqty)
            else:
                salesqty = 0
            salesqty_list.append(salesqty)
        new_singleseries = {'name': name, 'data': salesqty_list}
        series[index] = new_singleseries
        index += 1
    chart5['series'] = series
    return chart5


async def get_taobao_chart6(chart6):
    series = chart6['series']
    xAxis = chart6['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        if name == '描述':
            keyword = 'shopdescscore'
        elif name == '服务':
            keyword = 'shopservicescore'
        else:
            keyword = 'shopdeliveryscore'
        where_clause = ''
        parameter = []
        select_filed = 'count(id)'
        productqty_list = []
        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if category == '4.95以上':
                real_where_clause = real_where_clause + keyword + ' > 4.95'
            elif category == '4.9以上':
                real_where_clause = real_where_clause + keyword + ' > 4.9 and ' +  keyword + ' <4.95'
            elif category == '4.8以上':
                real_where_clause = real_where_clause + keyword + ' > 4.8 and ' + keyword + ' <4.9'
            elif category == '4.7以上':
                real_where_clause = real_where_clause + keyword + ' > 4.7 and ' + keyword + ' <4.8'
            else:
                real_where_clause = real_where_clause + keyword + ' < 4.7'
            productqty = await TaobaoProducts.findNumber(select_filed, real_where_clause, real_parameter)
            if productqty:
                productqty = int(productqty)
            else:
                productqty = 0
            productqty_list.append(productqty)
        new_singleseries = {'name': name, 'data': productqty_list}
        series[index] = new_singleseries
        index += 1
    return series


async def get_zhaopin_chart1(chart1):
    series = chart1['series']
    xAxis = chart1['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        where_clause = ''
        parameter = []
        select_filed = 'count(id)'
        qty_list = []
        where_clause = where_clause + 'address like ?'
        parameter.extend(['%' + name + '%'])
        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if category == '<=4000':
                real_where_clause = real_where_clause + ' and salary_month_max <= ?'
                real_parameter.extend([4000])
            elif category == '>=15000':
                real_where_clause = real_where_clause + ' and salary_month_min >= ?'
                real_parameter.extend([15000])
            else:
                real_where_clause = real_where_clause + ' and salary_month_min >= ?' + ' and salary_month_max <= ?'
                if category == '4000-8000':
                    real_parameter.extend([4000, 8000])
                elif category == '8000-10000':
                    real_parameter.extend([8000, 10000])
                elif category == '10000-15000':
                    real_parameter.extend([10000, 15000])
            qty = await ZhaoPinJobs.findNumber(select_filed, real_where_clause, real_parameter)
            if qty:
                qty = int(qty)
            else:
                qty = 0
            qty_list.append(qty)
        new_singleseries = {'name': name, 'data': qty_list}
        series[index] = new_singleseries
        index += 1
    chart1['series'] = series
    return chart1


async def get_zhaopin_chart2(chart2):
    series = chart2['series']
    xAxis = chart2['xAxis']
    categories = xAxis['categories']
    index = 0
    for singleseries in series:
        name = singleseries['name']
        where_clause = ''
        parameter = []
        select_filed = 'count(id)'
        qty_list = []
        if name == '<=4000':
            where_clause = where_clause + 'salary_month_max <= ?'
            parameter.extend([4000])
        elif name == '>=15000':
            where_clause = where_clause + 'salary_month_min >= ?'
            parameter.extend([15000])
        else:
            where_clause = where_clause + 'salary_month_min >= ?' + ' and salary_month_max <= ?'
            if name == '4000-8000':
                parameter.extend([4000, 8000])
            elif name == '8000-10000':
                parameter.extend([8000, 10000])
            elif name == '10000-15000':
                parameter.extend([10000, 15000])

        for category in categories:
            real_where_clause = copy.deepcopy(where_clause)
            real_parameter = copy.deepcopy(parameter)
            if category == '不限经验':
                real_where_clause = real_where_clause + ' and workexperience like ?'
                real_parameter.extend(['%不限%'])
            elif category == '1-3年':
                real_where_clause = real_where_clause + ' and (workexperience like ? or workexperience like ? or workexperience like ?)'
                real_parameter.extend(['%1%','%2%','%3%'])
            elif category == '3-5年':
                real_where_clause = real_where_clause + ' and (workexperience like ? or workexperience like ? or workexperience like ?)'
                real_parameter.extend(['%3%','%4%','%5%'])
            elif category == '5-10年':
                real_where_clause = real_where_clause + ' and (workexperience like ? or workexperience like ? or workexperience like ? or workexperience like ? or workexperience like ? or workexperience like ?)'
                real_parameter.extend(['%5%','%6%','%7%','%8%','%9%','%10%'])
            else:
                real_where_clause = real_where_clause + ' and (workexperience like ? or workexperience like ? or workexperience like ?)'
                real_parameter.extend(['%10%', '%11%', '%12%'])
            qty = await ZhaoPinJobs.findNumber(select_filed, real_where_clause, real_parameter)
            if qty:
                qty = int(qty)
            else:
                qty = 0
            qty_list.append(qty)
        new_singleseries = {'name': name, 'data': qty_list}
        series[index] = new_singleseries
        index += 1
    chart2['series'] = series
    return chart2

