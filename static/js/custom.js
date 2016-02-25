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
        var likebtn = $('#like-btn');
        if (data.liked) {
            likebtn.css('color', 'orange');
            likebtn.removeClass().addClass('liked');
        } else {
            likebtn.css('color', 'black');
            likebtn.removeClass().addClass('not-liked');
        }
        $('.glyphicon-thumbs-up').text(data.likes);
    });
});