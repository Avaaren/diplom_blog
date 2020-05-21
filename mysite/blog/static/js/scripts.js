$(document).ready(function () {
    
    $(window).scroll(function(){
        if (window.scrollY > 250) {
          $('.slider').show(200);
        }
        else{
          $('.slider').hide(200);
        }
      });




    $('#search-box').focusout(function(){
        $('#result').hide();
    });
    $('#search-box').on('input', function (e) {
        $.ajax({
            url: '/ajax_search/',
            data: {
                'value': $(this).val(),
            },
            dataType: 'json',
            success: function (data) {
                // $('#result').text($(this).val());
                console.log(data.search_result);
                
                $('#result').empty();
                $('#result').show();
                if (data.search_result.length == 0) {
                    $('#result').append($('<p>').text('empty'));
                }
                else {
                    data.links.forEach(function(link, i){
                        var a = $('<a>', { 'class': 'search_link', 'href':link }).text(data.search_result[i]);
                        $('#result').append(a)
                        $('#result').append('<br>');
                    })
                
                }
            }
        })
        // $('#result').text($(this).val());

    });
});

