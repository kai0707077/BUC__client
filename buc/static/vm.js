function showAtmid(url,place,name){
    $.ajax({
        type: "POST",
        url: url ,
        data: {'name':name} ,
        //success: success ,
        dataType: 'json'
        });

    $.ajax({
        type :"GET",
        url : url,
        dataType:"html",
        success : function(data) {//返回資料根據結果進行相應的處理
            //cool=cool+data
            $(place).html(data);
        },
        error:function(){
            $(place).html("獲取資料失敗！");
        }
    });
}

function showAtLeft(url,place){
    $.ajax({
        type :"GET",
        url : url,
        dataType:"html",
        success : function(data) {//返回資料根據結果進行相應的處理
            //cool=cool+data
            $(place).html(data);
        },
        error:function(){
            $(place).html("獲取資料失敗！");
        }
    });
}

function showAtRight(url,place){
    $.ajax({
        type :"GET",
        url : url,
        dataType:"html",
        success : function(data) {//返回資料根據結果進行相應的處理
            //cool=cool+data
            $(place).append(data);
        },
        error:function(){
            $(place).append("獲取資料失敗！");
        }
    });
}

function showVM(num1, num2, num3){
    num=num1+num2+num3;
    for(i=1; i<=num; i++){
        con=i%3;
        
        if(i<=num1){
            //url='/winvm';
            if(con==1){
                showAtRight('/winvm',"#content1");
            }
            else if(con==2){
                showAtRight('/winvm',"#content2");
            }
            else if(con==0){
                showAtRight('/winvm',"#content3");
            }
        }
        else if(i<=num1+num2){
            //url='/linvm';
            if(con==1){
                showAtRight('/linvm',"#content1");
            }
            else if(con==2){
                showAtRight('/linvm',"#content2");
            }
            else if(con==0){
                showAtRight('/linvm',"#content3");
            }
        }
        else if(i<=num){
            //url='/winvm';
            if(con==1){
                showAtRight('/appvm',"#content1");
            }
            else if(con==2){
                showAtRight('/appvm',"#content2");
            }
            else if(con==0){
                showAtRight('/appvm',"#content3");
            }
        }
        
        /*if(con===1){
            //showAtRight(url,"#content1");
            if(i<=num1){
                showAtRight('/winvm',"#content1");
            }
            else if(i<=num1+num2 && i>num1){
                showAtRight('/linvm',"#content1");
            }
            else if(i<=num && i>num1 && i>num1+num2){
                showAtRight('/winvm',"#content1");
            }
        }
        else if(con===2){
            //showAtRight(url,"#content2");
            if(i<=num1){
                showAtRight('/winvm',"#content2");
            }
            else if(i<=num1+num2 && i>num1){
                showAtRight('/linvm',"#content2");
            }
            else if(i<=num && i>num1 && i>num1+num2){
                showAtRight('/winvm',"#content2");
            }
        }
        else if(con===0){
            //showAtRight(url,"#content3");
            if(i<=num1){
                showAtRight('/winvm',"#content3");
            }
            else if(i<=num1+num2 && i>num1){
                showAtRight('/linvm',"#content3");
            }
            else if(i<=num && i>num1 && i>num1+num2){
                showAtRight('/winvm',"#content3");
            }
        }*/
        //showAtRight(url,place);
    }
}