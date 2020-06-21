document.addEventListener('DOMContentLoaded', () => {
  //Make 'enter' key submit send_message
  let msg = document.querySelector('#user_messsage');
  msg.addEventListener('keup', event => {
    event.preventDefault();
    if(event.keyCode === 13){
      document.querySelector('#send_message').click();
    }
  })
})
