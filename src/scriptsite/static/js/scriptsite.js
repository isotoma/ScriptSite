$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        }
    }
});

$(function () {
$('tr input').change(
    function() { 
        $.post('.', $(this).serialize(), 
            function(data) { 
                console.log(data) 
            }); 
        }
)});