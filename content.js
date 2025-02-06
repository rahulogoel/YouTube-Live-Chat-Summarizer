console.log("YouTube Chat Summarizer extension loaded");

// check if the current vidoe is a live stream
function isLiveStream() {
    const liveBadge = document.querySelector('span.ytd-video-primary-info-renderer[aria-label="Live"]');
    const urlParams = new URLSearchParams(window.location.search);
    
    return liveBadge !== null || urlParams.has('is_live');
}

// creating the summary box
function createSummaryBox() {
    // check if a box already exists to avoid duplicates
    if (document.getElementById("chat-summary-box")) return;

    const summaryBox = document.createElement("div");
    summaryBox.id = "chat-summary-box";
    summaryBox.style.position = "fixed";
    summaryBox.style.top = "10px";
    summaryBox.style.right = "10px";
    summaryBox.style.backgroundColor = "white";
    summaryBox.style.padding = "10px";
    summaryBox.style.borderRadius = "10px";
    summaryBox.style.boxShadow = "0 2px 4px rgba(0, 0, 0, 0.2)";
    summaryBox.style.zIndex = "9999";
    summaryBox.style.maxWidth = "300px";
    summaryBox.style.fontFamily = "Arial, sans-serif";
    summaryBox.style.lineHeight = "1.5";

    summaryBox.innerHTML = `
        <strong style="font-size: 16px;">Chat Summary:</strong>
        <p id="chat-summary-content" style="font-size: 14px; margin-top: 8px;">Loading...</p>
    `;

    document.body.appendChild(summaryBox);
}

// remove the summary box when live stream ends
function removeSummaryBox() {
    const existingBox = document.getElementById("chat-summary-box");
    if (existingBox) existingBox.remove();
}

// connect to the server for real-time summaries
function connectToSummaryService(videoId) {
    const socket = new WebSocket(`ws://localhost:8000/ws?video_id=${videoId}`);

    socket.onopen = () => {
        console.log("WebSocket connection established");
    };

    socket.onmessage = (event) => {
        const summaryContent = document.getElementById("chat-summary-content");
        if (summaryContent) {
            summaryContent.textContent = event.data;
        }
    };

    socket.onclose = () => {
        console.log("WebSocket connection closed");
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };
}

const observer = new MutationObserver(() => {
    if (isLiveStream()) {
        createSummaryBox();

        // fetch video ID from URL
        const videoId = new URLSearchParams(window.location.search).get("v");
        if (videoId) {
            connectToSummaryService(videoId);
        }
    } else {
        removeSummaryBox();
    }
});

observer.observe(document.body, { childList: true, subtree: true });

console.log("YouTube summarizer extension successfully running.");
