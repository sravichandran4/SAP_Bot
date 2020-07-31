
function submit_message(message) {
    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {

      $("#input_message").val('');

      // append the bot repsonse to the div
      $('.chat-container').append(`
          <div class="alert alert-primary chat-message" role="alert">
              ${data.message}
          </div>
      `)

      // remove the loading indicator
      $( "#loading" ).remove();
      $('.chat-container').animate({ scrollTop: $('.chat-container').scrollHeight }, 500);

    }
}

$(function() {
    $("#input_message").keypress(function (e) {
        if(e.which == 13) {

          const input_message = $('#input_message').val()
          // return if the user does not enter any text
          if (!input_message) {
            return
          }

          $('.chat-container').append(`
              <div class="alert alert-success chat-message" role="alert">
                  ${input_message}
              </div>
          `)

          $("#input_message").val('');

          $('.chat-container').append(`
              <div class="alert alert-primary chat-message text-center" id="loading" role="alert">
                <div class="spinner-border" role="status">
                  <span class="sr-only">Loading...</span>
                </div>
              </div>
          `)

          // send the message
          submit_message(input_message);

        }
    });
});

/*
$('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        // return if the user does not enter any text
        if (!input_message) {
          return
        }

        $('.chat-container').append(`
            <div class="chat-message pr-5 human-message">
                <p>
                ${input_message}
                </p>
            </div>
        `)

        // loading
        $('.chat-container').append(`
            <div class="chat-message text-center bot-message" id="loading">
              <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
              </div>
            </div>
        `)

        // clear the text input
        $('#input_message').val('')

        // send the message
        submit_message(input_message)
});
*/
