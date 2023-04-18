// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // Send a message to the content script to trigger a Streamlit rerun
  if (request.message === "trigger-rerun") {
    window.postMessage({type: "streamlit-rerun"}, "*");
  }
});

// Listen for messages from the Streamlit app
window.addEventListener("message", event => {
  // If the message is a Streamlit "isReady" message, send a message to the popup
  if (event.data && event.data.type === "streamlit-isReady") {
    chrome.runtime.sendMessage({message: "app-isReady"});
  }
});