$(document).ready(function () {

    // Switch toggle
    $('input:checkbox').click(function () {
        if($(this).attr("checked"))
        {
            alert("checked");
        }
        else{
            alert("nochecked");
        }
        $.ajax({
            url: 'xxxxxx动态页',
            data: $(document.forms[0]).serialize(),
            success: function () {
            },
            error: function () {

            }});
    });


});