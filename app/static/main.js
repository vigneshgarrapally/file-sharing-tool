$(document).ready(function() {
    // code to handle file upload
    $('#file-upload-form').submit(function(event) {
        event.preventDefault();
        var form_data = new FormData($('#file-upload-form')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                $('#upload-message').text(response.message);
                $('#upload-message').removeClass('error');
                $('#upload-message').addClass('success');
            },
            error: function(response) {
                $('#upload-message').text(response.responseJSON.message);
                $('#upload-message').removeClass('success');
                $('#upload-message').addClass('error');
            }
        });
    });

    // code to handle file download
    $('.download-link').click(function(event) {
        event.preventDefault();
        var file_id = $(this).data('file-id');
        window.location.href = '/download/' + file_id;
    });
});