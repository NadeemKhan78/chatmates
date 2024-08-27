function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

let form = document.querySelector(".input-container");

form.addEventListener("submit", sendChat);

function sendChat(e) {
  e.preventDefault();

  let chatMessage = document.querySelector(".message-input").value;
  console.log(chatMessage);

  let url = "{% url 'mychat:sent_msg' friend.profile.id %}";

  async function postJSON(data) {
    try {
      const response = await fetch(url, {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      console.log("Success:", result);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  const data = { msg: chatMessage };
  postJSON(data);
}

function sendChat(e) {
  e.preventDefault();

  let chatMessage = document.querySelector(".message-input").value;
  console.log(chatMessage);

  const data = { msg: chatMessage };
  let url = "{% url 'mychat:sent_msg' friend.profile.id %}";

  fetch(url, {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      let chat_body = document.querySelector(".chat-container");
      let chatMessageBox = document.createElement("div");

      chatMessageBox.classList.add("msg-container");
      chatMessageBox.classList.add("msg-container-own");

      chatMessageBox.innerText = data;
      chat_body.append(chatMessageBox);
    })

    .catch((error) => {
      console.error("Error:", error);
    });
}

<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 50 50"
  width="30px"
  height="30px"
>
  <path
    fill="#ffffff"
    d="M25,2C12.317,2,2,12.317,2,25s10.317,23,23,23s23-10.317,23-23S37.683,2,25,2z M37,26H26v11h-2V26H13v-2h11V13h2v11h11V26z"
  />
</svg>;
