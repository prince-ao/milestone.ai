document.addEventListener('htmx:configRequest', (event) => {
    var messageInput = document.querySelector('input[name="userInput"]');
    if (messageInput && messageInput.value.trim() !== '') {
        var chatbox = document.querySelector('.chat-box');
        var userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('text-size');
        userMessageDiv.innerHTML = '<br><b>You:</b> ' + messageInput.value;
        // userMessageDiv.className = 'user-messaddge'; // Add any styling classes you need
        chatbox.appendChild(userMessageDiv);

        messageInput.value = ''; // Clear the input field after message is sent

        scrollToBottom();
    }
});

    document.body.addEventListener('htmx:afterSwap', (event) => {
    const hiddenResponses = event.detail.elt.querySelectorAll('.hidden-response');
    hiddenResponses.forEach(hiddenResponse => {
        hiddenResponse.classList.add("text-size");
        revealText(hiddenResponse);
        hiddenResponse.classList.remove("hidden-response");
    });
});

function revealText(element) {
    element.style.visibility = 'visible';
    let fullText = element.textContent;
    element.textContent = '';
    element.innerHTML = '<br><b>Advisor: </b>'

    let i = 0;
    let interval = setInterval(() => {
        scrollToBottom();
        element.innerHTML += fullText[i];
        i++;
        if (i >= fullText.length) {
            clearInterval(interval);
        }
    }, 10); // Adjust speed as necessary
}

function scrollToBottom() {
  const container = document.querySelector('.chat-box'); // Replace with your actual container selector
  container.scrollTop = container.scrollHeight;

  console.log('scroll metrics', container.scrollTop, container.scrollHeight, container.clientHeight)
}