// Send a message to the content script to trigger a Streamlit rerun
document.getElementById("rerun").addEventListener("click", () => {
  chrome.tabs.query({active: true,
