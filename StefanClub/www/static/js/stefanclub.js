function search(from_filter = 'false')
{
   if(from_filter == 'true')
   {
      var search_item =$("#keywordspan").html();
   }
   else
   {
      var search_item = $("#searchinput").val();
   }
   var existed_search = $("#keywordspan").html();
   var order_by = $("#RefreshOrderLi").html();
   var specify_filter = $('#specifyfilterdiv').html();
   if ($("#all").hasClass("active"))
   {
      var shift_type = 'all';
   }
   else
   {
      var shift_type = 'tmall';
   }
   var deli_free = $('#deli_free_label').html();
   var love_baby = $('#lovebaby_label').html();
   var lowest_price = $("#lowest_price_input").val();
   var highest_price = $("#highest_price_input").val();
   var deli_location = $('#rec_deli_loc').html();
   $.ajax({
       type: "GET",
       url: "/api/search/products?search_item="+search_item + '&shift_type=' + shift_type + '&specify_filter=' + specify_filter + '&order_by=' + order_by + '&deli_free=' + deli_free + '&love_baby=' + love_baby + '&lowest_price=' + lowest_price + '&highest_price=' + highest_price + '&deli_location=' + deli_location,
       dataType: "json",
       contentType: "application/json; charset=utf-8",
       success: function (data) {
          error_msg = data.error_msg
          if (error_msg != '' && error_msg != null)
          {
            alert(error_msg);
          }
          else
          {
             if(search_item != existed_search)
             {
                set_filterdiv(search_item);
             }
             products = data.products;
             if(products.length > 0)
             {
                var addBody = "";
                for(var i = 0; i < products.length; i++){
                   var adddiv = "<div class='productdiv'>"
                        +         "<div  id ='" + products[i].id + "imgdiv" + "' class='productimgdiv' style='width:255.5px;height:255.5px;position:relative;'>"
                        +           "<a target='_blank' href='" + products[i].imgurl + "'>"
                        +             "<img style='width:255.5px;height:255.5px;' src='" + products[i].imgsrcurl + "'>"
                        +             "<div class='samesimidiv' id='" + products[i].id + "imgsubdiv" + "'>"
                        +               "<div style='margin-top:7.5px;float:left;margin-left:50px;'>";
                        if(products[i].samestyleurl != '' && products[i].samestyleurl != null)
                        {
                              adddiv = adddiv + "<a target='_blank' href='" + products[i].samestyleurl + "'class='samesimia' style='text-decoration:none;'>找同款</a>";}
                        else {
                              adddiv = adddiv + "<a target='_blank' href='" + products[i].samestyleurl + "'class='samesimia' style='text-decoration:none;pointer-events:none;opacity:0.7;' >找同款</a>";
                              }
                        adddiv = adddiv + "</div>"
                        +                 "<div style='margin-top:7.5px;float:left;margin-left:65px;'>";
                        if(products[i].similarurl != '' && products[i].similarurl != null){
                              adddiv = adddiv + "<a target='_blank' href='" + products[i].similarurl + "' class='samesimia' style='text-decoration:none;'>找相似</a>";}
                        else {
                              adddiv = adddiv + "<a target='_blank' href='" + products[i].similarurl + "' class='samesimia' style='text-decoration:none;pointer-events:none;opacity:0.7;'>找相似</a>";
                              }
                        adddiv = adddiv + "</div>"
                        +        "</div>"
                        +    "</a>"
                        + "</div>"
                        + "<div style='margin-top:15px;'>"
                        +    "<div style='height:20px;'>"
                        +        "<div class='profirstrow'>"
                        +            "<span style='color:OrangeRed;font-weight:bold;font-size:120%;'>" + "￥" + products[i].product_price + "</span>"
                        +        "</div>";
                        if(products[i].title.indexOf("包邮") != -1){
                            adddiv = adddiv +  "<div class='profirstrow'>"
                                +    "<img style='width:35px;height:20px;' src='../static/img/common/deliveryfree.png'>"
                                + "</div>";
                         }
                        if(products[i].payednum != '' && products[i].payednum != null){
                            adddiv = adddiv + "<div style='float:right;margin-right:5px;'>"
                                            +   "<span style='color:black;opacity:0.7;'>" + products[i].payednum + "</span>"
                                            +  "</div>";
                        }
                        adddiv = adddiv +   "</div>"
                        +   "<div style='margin-top:10px;margin-left:5px;'>";
                        if(products[i].titlehaskey == 'FALSE'){
                        adddiv = adddiv +  "<a class='protitlea' target='_blank' href='" + products[i].titleurl + "'>" + products[i].title + "</a>";
                        }
                        else {
                        adddiv = adddiv +  "<a class='protitlea' target='_blank' href='" + products[i].titleurl + "'><span>" + products[i].title1 + "</span><span style='color:OrangeRed;'>" + products[i].keyword + "</span><span>" + products[i].title2 + "</span></a>";
                        }
                        adddiv = adddiv +  "</div>"
                        +  "<div style='margin-top:10px;height:30px;'>"
                        +        "<div class='shopinfo'>"
                        +            "<div class='shopimgname'>"
                        +                "<div class='shopimg'>"
                        +                    "<img style='width:17.5px;height:17.5px;' src='../static/img/common/shopicon.png'>"
                        +                "</div>"
                        +                "<div class='shopname'>"
                        +                    "<a target='_blank' class='shopnamea' style='color:black;opacity:0.7;' href='" + products[i].shopurl + "'>" + products[i].shopname + "</a>"
                        +                "</div>"
                        +            "</div>"
                        +            "<div class='shopcard'>";
                        if(products[i].istmall == '1'){
                        adddiv = adddiv +  "<div style='margin-top:5px;margin-left:5px;height:20px;'>"
                                        +     "<img style='width:80px;height:20px;' src='../static/img/common/tmall.png'>"
                                        + "</div>";
                        }
                        adddiv = adddiv +   "<div style='height:20px;'>";
                        if(products[i].shopleveljingguanqty > 0){
                        adddiv = adddiv +    "<div class='kindfirsticon'>"
                                        +        "<img class='shopicon' src='../static/img/common/jinguan.png'>"
                                        +    "</div>";
                                        for(var j = 0; j < products[i].shopleveljingguanqty - 1; j++){
                                        adddiv = adddiv +    "<div class='kindresticons'>"
                                                        +      "<img class='shopicon' src='../static/img/common/jinguan.png'>"
                                                        +     "</div>";
                                        }
                        }
                        if(products[i].shoplevelguanqty > 0){
                        adddiv = adddiv +  "<div class='kindfirsticon'>"
                                        +        "<img class='shopicon' src='../static/img/common/guan.png'>"
                                        +    "</div>";
                                        for(var k = 0; k < products[i].shoplevelguanqty - 1; k++){
                                        adddiv = adddiv +   "<div class='kindresticons'>"
                                                        +      "<img class='shopicon' src='../static/img/common/guan.png'>"
                                                        +   "</div>";
                                         }
                         }
                        if(products[i].shoplevelzuanqty > 0){
                        adddiv = adddiv +  "<div class='kindfirsticon'>"
                                        +      "<img class='shopicon' src='../static/img/common/zuan.png'>"
                                        +    "</div>";
                                        for(var m = 0; m < products[i].shoplevelzuanqty - 1; m++){
                                        adddiv = adddiv +  "<div class='kindresticons'>"
                                                        +    "<img class='shopicon' src='../static/img/common/zuan.png'>"
                                                        + "</div>";
                                        }
                        }
                        if(products[i].shoplevelxinqty > 0){
                        adddiv = adddiv + "<div class='kindfirsticon'>"
                                          +      "<img class='shopicon' src='../static/img/common/xin.png'>"
                                          +    "</div>";
                                          for(var n = 0; n < products[i].shoplevelxinqty - 1; n++){
                                          adddiv = adddiv +  "<div class='kindresticons'>"
                                                         + "<img class='shopicon' src='../static/img/common/xin.png'>"
                                                         +  "</div>";
                                          }
                         }
                        if(products[i].shoptotalrate != '' && products[i].shoptotalrate != null){
                        adddiv = adddiv + "<div class='kindresticons' style='margin-left:10px;'>"
                                        +    "<span style='color:black;font-size:90%;'>" + "好评率：" + products[i].shoptotalrate + "</span>"
                                        + "</div>";
                        }
                        adddiv = adddiv + "</div>"
                                +        "<div style='margin-top:10px;opacity:0.7;height:10px;'>" + "---------------------------------------------------------------" + "</div>"
                                +        "<div style='margin-top:20px;'>"
                                +            "<div style='margin-left:5px;'>"
                                +                "<span>" + "如实描述：" + products[i].shopdescscore + "</span>";
                        if(products[i].shopdesccompare == 'higher'){
                        adddiv = adddiv +  "<span class='shophighertext'>" + "比同行均值高" + "</span>"
                                        +        "<span class='shophigherdiff'>" + products[i].shopdescscorediff + "</span>";
                        }
                        else if(products[i].shopdesccompare == 'lower'){
                        adddiv = adddiv +  "<span class='shoplowertext'>" + "比同行均值低" + "</span>"
                                        +        "<span class='shoplowerdiff'>" + products[i].shopdescscorediff + "</span>";
                        }
                        else if(products[i].shopdesccompare == 'equal'){
                        adddiv = adddiv +  "<span class='shopequaltext'>" + "与同行均值相等" + "</span>"
                                        +        "<span class='shopequaldiff'>" + products[i].shopdescscorediff + "</span>";
                        }
                        else{}
                        adddiv = adddiv + "</div>"
                                     +       "<div class='shopscorediv'>"
                                     +           "<span>" + "服务态度：" + products[i].shopservicescore + "</span>";
                        if(products[i].shopservicecompare == 'higher'){
                        adddiv = adddiv +  "<span class='shophighertext'>" + "比同行均值高" + "</span>"
                                        +        "<span class='shophigherdiff'>" + products[i].shopservicescorediff + "</span>";
                        }
                        else if(products[i].shopservicecompare == 'lower'){
                        adddiv = adddiv +  "<span class='shoplowertext'>" + "比同行均值低" + "</span>"
                                        +        "<span class='shoplowerdiff'>" + products[i].shopservicescorediff + "</span>";
                        }
                        else if(products[i].shopservicecompare == 'equal'){
                        adddiv = adddiv +  "<span class='shopequaltext'>" + "与同行均值相等" + "</span>"
                                        +        "<span class='shopequaldiff'>" + products[i].shopservicescorediff + "</span>";
                        }
                        else{}
                        adddiv = adddiv + "</div>"
                                     +       "<div class='shopscorediv'>"
                                     +           "<span>" + "物流服务：" + products[i].shopdeliveryscore + "</span>";
                        if(products[i].shopdeliverycompare == 'higher'){
                        adddiv = adddiv +  "<span class='shophighertext'>" + "比同行均值高" + "</span>"
                                        +        "<span class='shophigherdiff'>" + products[i].shopdeliveryscorediff + "</span>";
                        }
                        else if(products[i].shopdeliverycompare == 'lower'){
                        adddiv = adddiv +  "<span class='shoplowertext'>" + "比同行均值低" + "</span>"
                                        +        "<span class='shoplowerdiff'>" + products[i].shopdeliveryscorediff + "</span>";
                        }
                        else if(products[i].shopdeliverycompare == 'equal'){
                        adddiv = adddiv +  "<span class='shopequaltext'>" + "与同行均值相等" + "</span>"
                                        +        "<span class='shopequaldiff'>" + products[i].shopdeliveryscorediff + "</span>";
                        }
                        else{}
                        adddiv = adddiv + "</div>"
                                     +   "</div>"
                                   +   "</div>"
                               +   "</div>"
                              +  "<div style='float:right;margin-right:10px;'>"
                              +      "<span style='color:black;opacity:0.7;'>" + products[i].shopaddress + "</span>"
                              +  "</div>"
                            +  "</div>"
                            +  "<div style='margin-top:10px;'>"
                            +    "<div style='margin-left:5px;float:left;'>";
                        if(products[i].iconkey1 != null && products[i].iconkey1 != ''){
                        adddiv = adddiv + "<div class='icondiv'>"
                                        + "<div>";
                              if(products[i].iconurl1 != null && products[i].iconurl1 != ''){
                                    adddiv = adddiv +  "<a target='_blank' href='" + products[i].iconurl1 + "'>";
                              }
                              else {
                                    adddiv = adddiv +  "<a style='pointer-events:none;' target='_blank' href='" + products[i].iconurl1 + "'>";
                              }
                              adddiv = adddiv + "<img class='iconsize' src='" + "../static/img/common/" + products[i].iconkey1 +  ".png" + "'>"
                                              + "</a>"
                                       + "</div>"
                                       + "<div class='subicondiv'>";
                                       if(products[i].subiconclass1 != null && products[i].subiconclass1 != ''){
                                          if(products[i].subicontitle1 != null && products[i].subicontitle1 != ''){
                                             adddiv = adddiv + "<div style='margin-left:5px;margin-top:10px;'>"
                                                             +   "<div><span class='subicontext'>" + products[i].subicontitle1 + "</span></div>"
                                                             +   "<div style='margin-top:10px;margin-left:5px;'>"
                                                             +     "<div class='subiconcontent'><img class='iconsize' src='" + "../static/img/common/" + products[i].subiconclass1 +  ".png" + "'></div>"
                                                             +       "<div class='subiconcontent'><span class='subicontext'>" + products[i].subiconcontent1 + "</span></div>"
                                                             +  "</div>"
                                                             + "</div>";
                                           }
                                           else {
                                             adddiv = adddiv + "<div  style='margin-left:5px;margin-top:10px;'>"
                                                             +    "<div><img class='biggericonsize' src='" + "../static/img/common/" + products[i].subiconclass1 +  ".png" + "'></div>"
                                                             +    "<div><span class='subicontext'>" + products[i].icontitle1 + "</span></div>"
                                                             +  "</div>";
                                           }
                                        }
                                        else {
                                           adddiv = adddiv + "<span class='subicontext'>" + products[i].icontitle1 + "</span>";
                                        }
                              adddiv = adddiv +  "</div>"
                                  +  "</div>";
                         }
                        if(products[i].iconkey2 != null && products[i].iconkey2 != ''){
                        adddiv = adddiv + "<div class='icondiv'>"
                                        + "<div>";
                              if(products[i].iconurl2 != null && products[i].iconurl2 != ''){
                                    adddiv = adddiv +  "<a target='_blank' href='" + products[i].iconurl2 + "'>";
                              }
                              else {
                                    adddiv = adddiv +  "<a style='pointer-events:none;' target='_blank' href='" + products[i].iconurl2 + "'>";
                              }
                              adddiv = adddiv + "<img class='iconsize' src='" + "../static/img/common/" + products[i].iconkey2 +  ".png" + "'>"
                                              + "</a>"
                                       + "</div>"
                                       + "<div class='subicondiv'>";
                                       if(products[i].subiconclass2 != null && products[i].subiconclass2 != ''){
                                          if(products[i].subicontitle2 != null && products[i].subicontitle2 != ''){
                                             adddiv = adddiv + "<div style='margin-left:5px;margin-top:10px;'>"
                                                             +   "<div><span class='subicontext'>" + products[i].subicontitle2 + "</span></div>"
                                                             +   "<div style='margin-top:10px;margin-left:5px;'>"
                                                             +     "<div class='subiconcontent'><img class='iconsize' src='" + "../static/img/common/" + products[i].subiconclass2 +  ".png" + "'></div>"
                                                             +       "<div class='subiconcontent'><span class='subicontext'>" + products[i].subiconcontent2 + "</span></div>"
                                                             +  "</div>"
                                                             + "</div>";
                                           }
                                           else {
                                             adddiv = adddiv + "<div  style='margin-left:5px;margin-top:10px;'>"
                                                             +    "<div><img class='biggericonsize' src='" + "../static/img/common/" + products[i].subiconclass2 +  ".png" + "'></div>"
                                                             +    "<div><span class='subicontext'>" + products[i].icontitle2 + "</span></div>"
                                                             +  "</div>";
                                           }
                                        }
                                        else {
                                           adddiv = adddiv + "<span class='subicontext'>" + products[i].icontitle2 + "</span>";
                                        }
                              adddiv = adddiv +  "</div>"
                                  +  "</div>";
                         }
                        if(products[i].iconkey3 != null && products[i].iconkey3 != ''){
                        adddiv = adddiv + "<div class='icondiv'>"
                                        + "<div>";
                              if(products[i].iconurl3 != null && products[i].iconurl3 != ''){
                                    adddiv = adddiv +  "<a target='_blank' href='" + products[i].iconurl3 + "'>";
                              }
                              else {
                                    adddiv = adddiv +  "<a style='pointer-events:none;' target='_blank' href='" + products[i].iconurl3 + "'>";
                              }
                              adddiv = adddiv + "<img class='iconsize' src='" + "../static/img/common/" + products[i].iconkey3 +  ".png" + "'>"
                                              + "</a>"
                                       + "</div>"
                                       + "<div class='subicondiv'>";
                                       if(products[i].subiconclass3 != null && products[i].subiconclass3 != ''){
                                          if(products[i].subicontitle3 != null && products[i].subicontitle3 != ''){
                                             adddiv = adddiv + "<div style='margin-left:5px;margin-top:10px;'>"
                                                             +   "<div><span class='subicontext'>" + products[i].subicontitle3 + "</span></div>"
                                                             +   "<div style='margin-top:10px;margin-left:5px;'>"
                                                             +     "<div class='subiconcontent'><img class='iconsize' src='" + "../static/img/common/" + products[i].subiconclass3 +  ".png" + "'></div>"
                                                             +       "<div class='subiconcontent'><span class='subicontext'>" + products[i].subiconcontent3 + "</span></div>"
                                                             +  "</div>"
                                                             + "</div>";
                                           }
                                           else {
                                             adddiv = adddiv + "<div  style='margin-left:5px;margin-top:10px;'>"
                                                             +    "<div><img class='biggericonsize' src='" + "../static/img/common/" + products[i].subiconclass3 +  ".png" + "'></div>"
                                                             +    "<div><span class='subicontext'>" + products[i].icontitle3 + "</span></div>"
                                                             +  "</div>";
                                           }
                                        }
                                        else {
                                           adddiv = adddiv + "<span class='subicontext'>" + products[i].icontitle3 + "</span>";
                                        }
                              adddiv = adddiv +  "</div>"
                                  +  "</div>";
                         }
                        if(products[i].iconkey4 != null && products[i].iconkey4 != ''){
                        adddiv = adddiv + "<div class='icondiv'>"
                                        + "<div>";
                              if(products[i].iconurl4 != null && products[i].iconurl4 != ''){
                                    adddiv = adddiv +  "<a target='_blank' href='" + products[i].iconurl4 + "'>";
                              }
                              else {
                                    adddiv = adddiv +  "<a style='pointer-events:none;' target='_blank' href='" + products[i].iconurl4 + "'>";
                              }
                              adddiv = adddiv + "<img class='iconsize' src='" + "../static/img/common/" + products[i].iconkey4 +  ".png" + "'>"
                                              + "</a>"
                                       + "</div>"
                                       + "<div class='subicondiv'>";
                                       if(products[i].subiconclass4 != null && products[i].subiconclass4 != ''){
                                          if(products[i].subicontitle4 != null && products[i].subicontitle4 != ''){
                                             adddiv = adddiv + "<div style='margin-left:5px;margin-top:10px;'>"
                                                             +   "<div><span class='subicontext'>" + products[i].subicontitle4 + "</span></div>"
                                                             +   "<div style='margin-top:10px;margin-left:5px;'>"
                                                             +     "<div class='subiconcontent'><img class='iconsize' src='" + "../static/img/common/" + products[i].subiconclass4 +  ".png" + "'></div>"
                                                             +       "<div class='subiconcontent'><span class='subicontext'>" + products[i].subiconcontent4 + "</span></div>"
                                                             +  "</div>"
                                                             + "</div>";
                                           }
                                           else {
                                             adddiv = adddiv + "<div  style='margin-left:5px;margin-top:10px;'>"
                                                             +    "<div><img class='biggericonsize' src='" + "../static/img/common/" + products[i].subiconclass4 +  ".png" + "'></div>"
                                                             +    "<div><span class='subicontext'>" + products[i].icontitle4 + "</span></div>"
                                                             +  "</div>";
                                           }
                                        }
                                        else {
                                           adddiv = adddiv + "<span class='subicontext'>" + products[i].icontitle4 + "</span>";
                                        }
                              adddiv = adddiv +  "</div>"
                                  +  "</div>";
                         }
                        if(products[i].iconkey5 != null && products[i].iconkey5 != ''){
                        adddiv = adddiv + "<div class='icondiv'>"
                                        + "<div>";
                              if(products[i].iconurl5 != null && products[i].iconurl5 != ''){
                                    adddiv = adddiv +  "<a target='_blank' href='" + products[i].iconurl5 + "'>";
                              }
                              else {
                                    adddiv = adddiv +  "<a style='pointer-events:none;' target='_blank' href='" + products[i].iconurl5 + "'>";
                              }
                              adddiv = adddiv + "<img class='iconsize' src='" + "../static/img/common/" + products[i].iconkey5 +  ".png" + "'>"
                                              + "</a>"
                                       + "</div>"
                                       + "<div class='subicondiv'>";
                                       if(products[i].subiconclass5 != null && products[i].subiconclass5 != ''){
                                          if(products[i].subicontitle5 != null && products[i].subicontitle5 != ''){
                                             adddiv = adddiv + "<div style='margin-left:5px;margin-top:10px;'>"
                                                             +   "<div><span class='subicontext'>" + products[i].subicontitle5 + "</span></div>"
                                                             +   "<div style='margin-top:10px;margin-left:5px;'>"
                                                             +     "<div class='subiconcontent'><img class='iconsize' src='" + "../static/img/common/" + products[i].subiconclass5 +  ".png" + "'></div>"
                                                             +       "<div class='subiconcontent'><span class='subicontext'>" + products[i].subiconcontent5 + "</span></div>"
                                                             +  "</div>"
                                                             + "</div>";
                                           }
                                           else {
                                             adddiv = adddiv + "<div  style='margin-left:5px;margin-top:10px;'>"
                                                             +    "<div><img class='biggericonsize' src='" + "../static/img/common/" + products[i].subiconclass5 +  ".png" + "'></div>"
                                                             +    "<div><span class='subicontext'>" + products[i].icontitle5 + "</span></div>"
                                                             +  "</div>";
                                           }
                                        }
                                        else {
                                           adddiv = adddiv + "<span class='subicontext'>" + products[i].icontitle5 + "</span>";
                                        }
                              adddiv = adddiv +  "</div>"
                                  +  "</div>";
                         }
                         adddiv = adddiv +  "</div>"
                             +   "<div style='margin-right:5px;float:right;'>"
                             +       "<a><img class='iconsize' src='../static/img/common/wangwang.png'></a>"
                             +   "</div>"
                           +   "</div>"
                        +   "</div>"
                    +   "</div>";

                    addBody = addBody + adddiv;
                }
                $("#productlistdiv").html(addBody);
                $(".samesimidiv").hide();
                $(".productimgdiv").hover(function(){
                   var imgdivid = this.id;
                   var id = imgdivid.substring(0,imgdivid.length-6);
                   var imgsubdivid = id + 'imgsubdiv';
                   $("#" + imgsubdivid + "").show();
                   $("#" + imgsubdivid + "").css("opacity",0.7);
                  },function(){
                   var imgdivid = this.id;
                   var id = imgdivid.substring(0,imgdivid.length-6);
                   var imgsubdivid = id + 'imgsubdiv';
                   $("#" + imgsubdivid + "").hide();
                  });

             }
             else
             {
               $("#productlistdiv").html('没有符合条件的宝贝!');
             }
             $("#keywordspan").html(search_item);
             var new_url = '/taobao?keyword=' + search_item + '&shift_type=' + shift_type + '&specify_filter=' + specify_filter + '&order_by=' + order_by;
             var stateObject = {};
             var title = "Wow Title";
             history.pushState(stateObject,title,new_url);
          }
       }
       });

}

function set_filterdiv(search_item)
{
                if (search_item == 'UNIQLO' || search_item == 'SUPERME' || search_item == 'clothes')
                {
                  var addfilter =  "<div class='chooseitemdiv'>"
                                 +   "<div class='chooseitem'>" + "品牌:" + "</div>"
                                 +    "<div>";
                  if(search_item == 'UNIQLO')
                  {
                      var addfilter =  addfilter  +  "<a class='chooseitemspea' style='text-decoration:none;'>" + "UNIQLO" + "</a>";
                  }
                  else if(search_item == 'SUPERME')
                  {
                      var addfilter =  addfilter  +  "<a class='chooseitemspea' style='text-decoration:none;'>" + "SUPERME" + "</a>";
                   }
                  else
                  {
                     var addfilter =  addfilter  +  "<a id='UNIQLOa' class='chooseitema' style='text-decoration:none;'>" + "UNIQLO" + "</a>"
                                                 +  "<a id='SUPERMEa' class='chooseitema' style='text-decoration:none;'>" + "SUPERME" + "</a>";
                  }
                  var addfilter =  addfilter  +  "</div>"
                                 +  "</div>"
                     +   "<div class='chooseitemdiv'>"
                     +       "<div id='TYPEprediv' class='chooseitem'>" + "类别:" + "</div>"
                     +  "<div>"
                     +           "<a id='ManTYPEa' class='chooseitema' style='text-decoration:none;'>" + "男装" + "</a>"
                     +           "<a id='WomanTYPEa' class='chooseitema' style='text-decoration:none;'>" + "女装" + "</a>"
                     +       "</div>"
                      +       "</div>"
                     +   "<div class='chooseitemdiv'>"
                     +       "<div id='CLASprediv' class='chooseitem'>" + "款式" + "</div>"
                     +       "<div>"
                     +           "<a id='ShirtCLASa' class='chooseitema' style='text-decoration:none;'>" + "衬衫" + "</a>"
                     +           "<a id='LongCLASa' class='chooseitema' style='text-decoration:none;'>" + "长裤" + "</a>"
                     +           "<a id='TshirtCLASa' class='chooseitema' style='text-decoration:none;'>" + "T恤" + "</a>"
                     +           "<a id='JeansCLASa' class='chooseitema' style='text-decoration:none;'>" + "牛仔裤" + "</a>"
                     +       "</div>"
                      +       "</div>";
                }
                if (search_item == 'NIKE' || search_item == 'ADIDAS' || search_item == 'shoes')
                {
                  var addfilter =  "<div class='chooseitemdiv'>"
                                 +   "<div class='chooseitem'>" + "品牌:" + "</div>"
                                 +    "<div>";
                  if(search_item == 'NIKE')
                  {
                      var addfilter =  addfilter  +  "<a class='chooseitemspea' style='text-decoration:none;'>" + "NIKE" + "</a>";
                  }
                  else if(search_item == 'ADIDAS')
                  {
                      var addfilter =  addfilter  +  "<a class='chooseitemspea' style='text-decoration:none;'>" + "ADIDAS" + "</a>";
                   }
                  else
                  {
                     var addfilter =  addfilter  +  "<a id='NIKEa' class='chooseitema' style='text-decoration:none;'>" + "NIKE" + "</a>"
                                                 +  "<a id='ADIDASa' class='chooseitema' style='text-decoration:none;'>" + "ADIDAS" + "</a>";
                  }
                  var addfilter =  addfilter  +  "</div>"
                                 +  "</div>"
                     +   "<div class='chooseitemdiv'>"
                     +       "<div id='SHTYprediv' class='chooseitem'>" + "类别:" + "</div>"
                     +  "<div>"
                     +           "<a id='CoatSHTYa' class='chooseitema' style='text-decoration:none;'>" + "外套" + "</a>"
                     +           "<a id='ShoesSHTYa' class='chooseitema' style='text-decoration:none;'>" + "鞋子" + "</a>"
                     +       "</div>"
                      +       "</div>"
                     +   "<div class='chooseitemdiv'>"
                     +       "<div id='SHCLprediv' class='chooseitem'>" + "鞋子款式" + "</div>"
                     +       "<div>"
                     +           "<a id='RunSHCLa' class='chooseitema' style='text-decoration:none;'>" + "跑鞋" + "</a>"
                     +           "<a id='BanSHCLa' class='chooseitema' style='text-decoration:none;'>" + "板鞋" + "</a>"
                     +           "<a id='BallSHCLa' class='chooseitema' style='text-decoration:none;'>" + "球鞋" + "</a>"
                     +       "</div>"
                      +       "</div>";
                }
                if (search_item == 'APPLE' || search_item == 'HUAWEI' || search_item == 'electronic')
                {
                  var addfilter =  "<div class='chooseitemdiv'>"
                                 +   "<div class='chooseitem'>" + "品牌:" + "</div>"
                                 +    "<div>";
                  if(search_item == 'APPLE')
                  {
                      var addfilter =  addfilter  +  "<a class='chooseitemspea' style='text-decoration:none;'>" + "苹果" + "</a>";
                  }
                  else if(search_item == 'HUAWEI')
                  {
                      var addfilter =  addfilter  +  "<a class='chooseitemspea' style='text-decoration:none;'>" + "华为" + "</a>";
                   }
                  else
                  {
                     var addfilter =  addfilter  +  "<a id='APPLEa' class='chooseitema' style='text-decoration:none;'>" + "苹果" + "</a>"
                                                 +  "<a id='HUAWEIa' class='chooseitema' style='text-decoration:none;'>" + "华为" + "</a>";
                  }
                  var addfilter =  addfilter  +  "</div>"
                                 +  "</div>"
                     +   "<div class='chooseitemdiv'>"
                     +       "<div id='NETTprediv' class='chooseitem'>" + "网络类型:" + "</div>"
                     +  "<div>"
                     +           "<a id='GlobalNetNETTa' class='chooseitema' style='text-decoration:none;'>" + "全网通" + "</a>"
                     +           "<a id='LiantongNETTa' class='chooseitema' style='text-decoration:none;'>" + "联通" + "</a>"
                     +           "<a id='YidongNETTa' class='chooseitema' style='text-decoration:none;'>" + "移动" + "</a>"
                     +           "<a id='DianxinNETTa' class='chooseitema' style='text-decoration:none;'>" + "中国电信" + "</a>"
                     +       "</div>"
                      +       "</div>"
                     +   "<div class='chooseitemdiv'>"
                     +       "<div id='FAVIprediv' class='chooseitem'>" + "最想要的功能" + "</div>"
                     +       "<div>"
                     +           "<a id='BothFAVIa' class='chooseitema' style='text-decoration:none;'>" + "双卡双待" + "</a>"
                     +           "<a id='FaceFAVIa' class='chooseitema' style='text-decoration:none;'>" + "人脸识别" + "</a>"
                     +           "<a id='AllFaceFAVIa' class='chooseitema' style='text-decoration:none;'>" + "全面屏" + "</a>"
                     +           "<a id='NolockFAVIa' class='chooseitema' style='text-decoration:none;'>" + "无锁" + "</a>"
                     +       "</div>"
                      +       "</div>";
                }
                $("#filterdiv").html(addfilter);
                $("#hideorshowfiltera").html("收起筛选 <span class='glyphicon glyphicon-chevron-up'></span>");
                var clickatype = 'chooseitema';
                AddEvent(clickatype);

}

function AddEvent(clickatype)
{
     if(clickatype == 'chooseitema')
	 {
        var chooseitemas = document.getElementsByClassName(clickatype);
        for(var i = 0; i < chooseitemas.length; i++)
        {
	       chooseitemas[i].onclick = function()
	       {
	         var aid = this.id;
	         var filter = aid.substring(0,aid.length-1);
	         if (filter == 'UNIQLO' || filter == 'SUPERME' || filter == 'NIKE' || filter == 'ADIDAS' || filter == 'APPLE' || filter == 'HUAWEI')
	         {
	           shiftkeyword(filter);
	         }
	         else
	         {
	           var filterdetailclass = filter.substring(filter.length - 4, filter.length);
	           var typedivid = filterdetailclass + 'prediv';
	           var typedesc = $("#" + typedivid + "").html();
	           if($("#usersetfilter").length > 0)
	           {
	              var existed_html = $("#usersetfilter").html();
	              existed_html = existed_html + "<div style='margin-left:7.5px;float:left;border:solid 1px #D0D0D0;'>"
	                                          +     "<a id='" + aid + "remove" + "' class='removeitema' style='opacity:0.7;color:black;'>"
	                                          +        typedesc + "&nbsp;" + this.text + "&nbsp;<span class='glyphicon glyphicon-remove'></span>"
	                                          +     "</a>"
                                              + "</div>";
                   $("#usersetfilter").html(existed_html);
               }
               else
               {
                   var insertHtml = "<div style='float:left;' id='usersetfilter'>"
                                              + "<div style='margin-left:7.5px;float:left;border:solid 1px #D0D0D0;'>"
	                                          +     "<a id='" + aid + "remove" + "' class='removeitema' style='opacity:0.7;color:black;'>"
	                                          +        typedesc + "&nbsp;" + this.text + "&nbsp;<span class='glyphicon glyphicon-remove'></span>"
	                                          +     "</a>"
                                              + "</div>"
                                  + "</div>";
                   $('#statusbar').find('div').eq(0).after(insertHtml);
               }
                $(this).hide();
                var set_type = 'disable';
                set_disabled_item(filterdetailclass,aid,set_type);
                var atext = this.text;
                var existed_spe = $('#specifyfilterdiv').html();
                if(existed_spe == '')
                {
                  $('#specifyfilterdiv').html(atext);
                }
                else
                {
                  existed_spe =  existed_spe + 'and' + atext;
                  $('#specifyfilterdiv').html(existed_spe);
                }
                search('true');
                var clickatype = 'removeitema';
                AddEvent(clickatype);
	         }
	       }
        }
     }
     if(clickatype == 'removeitema')
	 {
        var removeitemas = document.getElementsByClassName(clickatype);
        for(var i = 0; i < removeitemas.length; i++)
        {
           if(!removeitemas[i].onclick)
           {
	          removeitemas[i].onclick = function()
	          {
	            var removeid = this.id;
	            var aid = removeid.substring(0,removeid.length-6);
	            var filter = aid.substring(0,aid.length-1);
	            var filterdetailclass = filter.substring(filter.length - 4, filter.length);
	            var set_type = 'able';
	            $("#" + aid + "").show();
	            set_disabled_item(filterdetailclass,aid,set_type);
                $(this).parent().remove();
                atext = $("#" + aid + "").html();
                new_specify_filter = get_released_str(atext);
                $('#specifyfilterdiv').html(new_specify_filter);
                search('true');
	          }
	       }
        }
     }
}

function set_disabled_item(filterdetailclass,aid,set_type)
{
   var chooseitemas = document.getElementsByClassName('chooseitema');
   for(var i = 0; i < chooseitemas.length; i++)
   {
     chooseitemaid = chooseitemas[i].id;
     if(chooseitemaid.indexOf(filterdetailclass) != -1 && chooseitemaid != aid)
     {
        if(set_type == 'disable')
        {
          $("#" + chooseitemaid + "").css("pointer-events","none");
        }
        else
        {
          $("#" + chooseitemaid + "").css("pointer-events","");
        }
     }
   }

}

function RefreshOrder(order_type)
{
   var exist_order_by = $("#RefreshOrderLi").html();
   if (exist_order_by == '' || exist_order_by == 'None')
   {
      order_by = order_type + ' desc';
   }
   else
   {
      if(order_type == 'product_sales_qty')
      {
         if (exist_order_by == 'product_sales_qty desc')
         {
            order_by = 'product_sales_qty';
         }
         else
         {
            order_by = 'product_sales_qty desc';
         }
      }
      if(order_type == 'shop_ave_score')
      {
         if (exist_order_by == 'shop_ave_score desc')
         {
            order_by = 'shop_ave_score';
         }
         else
         {
            order_by = 'shop_ave_score desc';
         }
      }
      if(order_type == 'product_price_float')
      {
         if (exist_order_by == 'product_price_float desc')
         {
            order_by = 'product_price_float';
         }
         else
         {
            order_by = 'product_price_float desc';
         }
      }
   }
   if ($("#all").hasClass("active"))
   {
      var shift_type = 'all';
   }
   else
   {
      var shift_type = 'tmall';
   }
   keyword = $("#keywordspan").html();
   var specify_filter = $('#specifyfilterdiv').html();
   window.location.href = '/taobao?keyword=' + keyword + '&shift_type=' + shift_type + '&specify_filter=' + specify_filter + '&order_by=' + order_by;

}

function get_released_str(atext)
{
   var specify_filter = $('#specifyfilterdiv').html();
   var and_index = specify_filter.indexOf("and");
   if(and_index == -1)
   {
      var return_str = '';
   }
   else
   {
      var atext_index = specify_filter.indexOf(atext);
      if(atext_index < and_index)
      {
        var return_str = specify_filter.substring(and_index + 3,specify_filter.length);
      }
      else
      {
        var return_str = specify_filter.substring(0,and_index);
      }
   }
   return return_str;

}

function set_choosed_spe(specify_filter)
{
  if(specify_filter.length > 0 && specify_filter != 'None')
  {
    var and_index = specify_filter.indexOf("and");
    var first_spe_filter = '';
    var second_spe_filter = '';
    if(and_index == -1)
    {
       first_spe_filter = specify_filter;
    }
    else
    {
       first_spe_filter = specify_filter.substring(0,and_index);
       second_spe_filter = specify_filter.substring(and_index + 3,specify_filter.length);
    }
    var filter_list = [first_spe_filter,second_spe_filter];
    var chooseitemas = document.getElementsByClassName('chooseitema');
    for(var i = 0; i < filter_list.length; i++)
    {
        for(var j = 0; j < chooseitemas.length; j++)
        {
	       if(chooseitemas[j].text == filter_list[i])
	       {
	         var aid = chooseitemas[j].id;
	         break;
	       }
	    }
	    var filter = aid.substring(0,aid.length-1);
       	var filterdetailclass = filter.substring(filter.length - 4, filter.length);
	    var typedivid = filterdetailclass + 'prediv';
	    var typedesc = $("#" + typedivid + "").html();
	    if($("#usersetfilter").length > 0)
	    {
	       var existed_html = $("#usersetfilter").html();
	       existed_html = existed_html + "<div style='margin-left:7.5px;float:left;border:solid 1px #D0D0D0;'>"
	                                          +     "<a id='" + aid + "remove" + "' class='removeitema' style='opacity:0.7;color:black;'>"
	                                          +        typedesc + "&nbsp;" + filter_list[i] + "&nbsp;<span class='glyphicon glyphicon-remove'></span>"
	                                          +     "</a>"
                                              + "</div>";
                   $("#usersetfilter").html(existed_html);
        }
        else
        {
           var insertHtml = "<div style='float:left;' id='usersetfilter'>"
                                              + "<div style='margin-left:7.5px;float:left;border:solid 1px #D0D0D0;'>"
	                                          +     "<a id='" + aid + "remove" + "' class='removeitema' style='opacity:0.7;color:black;'>"
	                                          +        typedesc + "&nbsp;" + filter_list[i] + "&nbsp;<span class='glyphicon glyphicon-remove'></span>"
	                                          +     "</a>"
                                              + "</div>"
                                  + "</div>";
           $('#statusbar').find('div').eq(0).after(insertHtml);
        }
        $("#" + aid + "").hide();
        var set_type = 'disable';
        set_disabled_item(filterdetailclass,aid,set_type);
        var atext = filter_list[i];
        var existed_spe = $('#specifyfilterdiv').html();
        if(existed_spe == '')
        {
           $('#specifyfilterdiv').html(atext);
        }
        else
        {
           existed_spe =  existed_spe + 'and' + atext;
           $('#specifyfilterdiv').html(existed_spe);
        }
        var clickatype = 'removeitema';
        AddEvent(clickatype);
    }
  }
}