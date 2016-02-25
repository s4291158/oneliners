$('#like-btn').click(function (e) {
    e.preventDefault();
    var likefield = $('#id_like_field');
    var liked = likefield.val();

    if (liked == 'True') {
        likefield.val('False');
    } else {
        likefield.val('True');
    }

    var form = $('#like-form');
    $.post(form.attr('action'), form.serialize(), function (data) {
        console.log(data.liked);
        if (data.liked) {
            $('#like-btn').css('color', 'orange');
        } else {
            $('#like-btn').css('color', 'black');
        }
        $('.glyphicon-thumbs-up').text(data.likes);
    });
});