
function submit_message(message) {
    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {
      // append the bot repsonse to the div
      $('.chat-container').append(`
            <div class="chat-message bot-message">
                ${data.message}
            </div>
      `)
      // remove the loading indicator
      $( "#loading" ).remove();
    }
}

$('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        // return if the user does not enter any text
        if (!input_message) {
          return
        }

        $('.chat-container').append(`
            <div class="chat-message col-md-5 human-message">
                ${input_message}
            </div>
        `)

        // loading
        $('.chat-container').append(`
            <div class="chat-message text-center bot-message" id="loading">
                <b>...</b>
            </div>
        `)

        // clear the text input
        $('#input_message').val('')

        // send the message
        submit_message(input_message)
});

$(function () {

  colors = {};

  colors['ca'] = '#A4D886';
  colors['ru'] = '#FCECA2';
  colors['cn'] = '#F9573B';
  colors['us'] = '#87CEEB';
  colors['jp'] = '#34BD0E';
  colors['au'] = '#BCC7FC';
  colors['kz'] = '#D4624E';
  colors['de'] = '#34BD0E';

  $('#world-map').vectorMap({
    colors: colors,
    hoverOpacity: 0.7, // opacity for :hover
    hoverColor: false
  });

});
