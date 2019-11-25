function showAtRight(url){
    $.ajax({
        type :"GET",
        url : url,
        dataType:"html",
        success : function(data) {//返回資料根據結果進行相應的處理
            $("#content").html(data);
        },
        error:function(){
            $("#content").html("獲取資料失敗！");
        }
    });
}