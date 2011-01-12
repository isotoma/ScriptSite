function changeStyle () {
      var savedstyle = $.cookie('style-change');
      var selectedCSS = savedstyle.split(",");
  
     $("link[media='screen']").each(function () {
            if($(this).attr("title") != selectedCSS[1] || selectedCSS[0]) {
                $(this).attr("disabled", "disabled");
            }
        });
       
}
function setCookie () {
    var selected = new Array();
    selected[0] = $("#style-select").val();
    selected[1] = $("#layout-select").val();
    $.cookie('style-change', selected);
    changeStyle()
}
$(function () { 
    $("#style-select").change(function () {
        setCookie();
    ;});
    $("#layout-select").change(function () {
        setCookie();
    ;});
});


