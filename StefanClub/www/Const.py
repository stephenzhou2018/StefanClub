taobaochart1 = {
           'chart': {'renderTo': 'container1'},
           'title': {'text': '消费力对比图'},
           'xAxis': {
              'title': {'text': '价格(元)'},
              'categories': ['<=100', '100-500', '500-1000', '1000-5000', '>=5000']
           },
           'yAxis': {
              'title': {'text': '销售量(单)'}
           },
           'series': [
               {'name': 'APPLE', 'data': []},
               {'name': 'HUAWEI', 'data': []},
               {'name': 'NIKE', 'data': []},
               {'name': 'ADIDAS', 'data': []},
               {'name': 'UNIQLO', 'data': []},
               {'name': 'SUPERME', 'data': []},
               {'name': 'ALL','data': []}
           ]
         }
taobaochart2 = {
           'chart': {'renderTo': 'container2', 'type': 'column'},
           'title': {'text': '销售量与店铺等级的关系'},
           'xAxis': {
              'title': {'text': '店铺等级'},
              'categories': ['金冠以上', '皇冠', '钻石', '爱心']
           },
           'yAxis': {
              'title': {'text': '销售量(单)'}
           },
           'series': [
               {'name': 'APPLE', 'data': []},
               {'name': 'HUAWEI', 'data': []},
               {'name': 'NIKE', 'data': []},
               {'name': 'ADIDAS', 'data': []},
               {'name': 'UNIQLO', 'data': []},
               {'name': 'SUPERME', 'data': []},
               {'name': 'ALL','data': []}
           ]
         }
taobaochart3 = {
           'chart': {'renderTo': 'container3', 'type': 'bar'},
           'title': {'text': '衣物类男女装购买比例'},
           'xAxis': {
              'categories': ['男装', '女装']
           },
           'yAxis': {
              'title': {'text': '销售量(单)'}
           },
           'series': [
               {'name': 'UNIQLO', 'data': []},
               {'name': 'SUPERME', 'data': []},
               {'name': 'BOTH','data': []}
           ]
         }
taobaochart4 = {
		   'chart': {'plotBackgroundColor': 'null', 'plotBorderWidth': 'null', 'plotShadow': 'false',},
		   'title': {'text': '各地区淘宝店销量分布'},
		   'tooltip': {'headerFormat': '{series.name}<br>','pointFormat': '{point.name}: <b>{point.percentage:.1f}%</b>'},
		   'plotOptions': {'pie': {'allowPointSelect': 'true','cursor': 'pointer','dataLabels': {
								                                                                            'enabled': 'true',
								                                                                            'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
								                                                                            'style': {'color': "(Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'"}
						                                                                                    },
						     'states': {'hover': {'enabled': 'false'}},
						     'slicedOffset': '20',         # 突出间距
						     'point': {                  # 每个扇区是数据点对象，所以事件应该写在 point 下面
								'events': {
										# 鼠标滑过是，突出当前扇区
										'mouseOver: function() {this.slice();}',
										# 鼠标移出时，收回突出显示
										'mouseOut: function() {this.slice();}',
										# 默认是点击突出，这里屏蔽掉
										'click: function() {return false;}'
								           }
						               }
				               }
		                    },
		   'series': [{
				'type': 'pie',
				'name': '淘宝店销量占比',
				'data': [
						  ['珠三角',   0],
						  ['京津冀',       0],
						  {'name': '长三角',
								'y': 0,
								'sliced': 'true', # 突出显示这个点（扇区），用于强调。
						  },
                          ['海外',   0],
						  ['其他',   0]
				        ]
		            }]
               }
taobaochart5 = {
           'chart': {'renderTo': 'container5'},
           'title': {'text': '人们更信赖哪一种服务(取单品最高销量比较)'},
           'xAxis': {
              'title': {'text': '服务类型'},
              'categories': ['天猫', '金牌卖家', '新品', '热卖', '天猫国际', '保险', '服务', '天猫直送']
           },
           'yAxis': {
              'title': {'text': '销售量(单)'}
           },
           'series': [
               {'name': 'APPLE', 'data': []},
               {'name': 'HUAWEI', 'data': []},
               {'name': 'NIKE', 'data': []},
               {'name': 'ADIDAS', 'data': []},
               {'name': 'UNIQLO', 'data': []},
               {'name': 'SUPERME', 'data': []},
               {'name': 'ALL','data': []}
           ]
         }
taobaochart6 = {
		     'xAxis': {'categories': ['4.95以上', '4.9以上', '4.8以上', '4.7以上', '4.7以下']},
		     'series': [{
			      'name': '描述',
                  'color': 'red',
			      'fillColor': {
				    'linearGradient': {'x1': 0,'y1': 0,'x2': 0,'y2': 1},
				    'stops': [
					         [0, 'Highcharts.getOptions().colors[5]'],
					         [1, "Highcharts.Color(Highcharts.getOptions().colors[6]).setOpacity(0).get('rgba')"]
				           ]
				  },
			      'data': []
		        },
		        {
			      'name': '服务',
                  'color': 'green',
			      'fillColor': {
				    'linearGradient': {'x1': 0,'y1': 0,'x2': 0,'y2': 1},
				    'stops': [
					         [0, 'Highcharts.getOptions().colors[7]'],
					         [1, "Highcharts.Color(Highcharts.getOptions().colors[6]).setOpacity(0).get('rgba')"]
				           ]
				  },
			      'data': []
		        },
				{
				  'name': '快递',
                  'color': 'yellow',
			      'fillColor': {
				    'linearGradient': {'x1': 0,'y1': 0,'x2': 0,'y2': 1},
				    'stops': [
					         [0, 'Highcharts.getOptions().colors[3]'],
					         [1, "Highcharts.Color(Highcharts.getOptions().colors[6]).setOpacity(0).get('rgba')"]
				           ]
				  },
			      'data': []
				 }]
	    }