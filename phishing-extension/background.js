console.log("🔥 Background running");

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {

    if (changeInfo.status === "complete" && tab.url) {

        // ❌ Avoid infinite loop (important)
        if (tab.url.includes("warning.html")) return;

        console.log("Checking URL:", tab.url);

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: tab.url })
        })
        .then(res => res.json())
        .then(data => {

            console.log("Result:", data.result);

            if (data.result === "Phishing") {

                console.log("🚨 Phishing detected!");

                chrome.tabs.update(tabId, {
                    url: chrome.runtime.getURL("warning.html")
                });

            } else {
                console.log("✅ Safe site");
            }

        })
        .catch(err => {
            console.log("❌ Fetch Error:", err);
        });
    }
});