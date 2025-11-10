/* frontend/app.js
   Sends form-encoded POST to your Render Flask app (/predict),
   parses returned HTML and updates the static frontend.
*/

const BACKEND_PREDICT = "https://phishing-website-detection-5hn3.onrender.com/predict";

const form = document.getElementById("urlForm");
const urlInput = document.getElementById("url");
const checkedUrl = document.getElementById("urlDisplay");
const displayedUrl = document.getElementById("displayedUrl");

const resultBox = document.getElementById("resultBox");
const resultText = document.getElementById("resultText");

const reasonSection = document.getElementById("reasonSection");
const toggleDetailsBtn = document.getElementById("toggleDetails");
const detailsBox = document.getElementById("detailsBox");
const reasonList = document.getElementById("reasonList");

const resetButtons = document.getElementsByClassName("reset-btn");

// clear input on page load
window.addEventListener("load", () => {
  if (urlInput) urlInput.value = "";
  hideResult();
});

// form submit -> call backend
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const url = (urlInput.value || "").trim();

  // basic validation
  if (!url) {
    alert("Please enter a URL.");
    return;
  }
  if (/\s/.test(url)) {
    alert("Please enter only one URL at a time (no spaces).");
    return;
  }

  // UI: show checked URL
  displayedUrl.textContent = url;
  checkedUrl.style.display = "block";

  // show loading state
  resultText.textContent = "Checking...";
  resultBox.style.display = "block";
  reasonSection.style.display = "none";
  detailsBox.style.display = "none";
  reasonList.innerHTML = "";

  try {
    // send as form-encoded to match Flask form handling
    const resp = await fetch(BACKEND_PREDICT, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ url })
    });

    // If backend returned non-2xx, try to read text and show error
    if (!resp.ok) {
      const errText = await resp.text().catch(() => "");
      console.error("Backend error:", resp.status, errText);
      resultText.textContent = "Server error — try again later.";
      return;
    }

    const html = await resp.text();
    // parse returned HTML fragment
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    // Try to extract the main prediction text (h2 inside .result or first h2)
    let extractedResult = null;
    const resultH2 = doc.querySelector(".result h2") || doc.querySelector("h2");
    if (resultH2) extractedResult = resultH2.textContent.trim();

    // Fallback if nothing found
    if (!extractedResult) extractedResult = "No classification returned";

    // Extract explicit reason lines: either elements with class 'reason-line',
    // list items under detailsBox, or any <li> inside returned HTML's details area.
    let reasons = [];

    // 1) reason-line elements
    const reasonLineEls = doc.querySelectorAll(".reason-line");
    reasonLineEls.forEach(el => {
      const t = el.textContent.trim();
      if (t) reasons.push(t);
    });

    // 2) list items inside detailsBox or inside .result
    const liEls = doc.querySelectorAll("#detailsBox li, .result li, ul li");
    liEls.forEach(el => {
      const t = el.textContent.trim();
      // avoid duplicates / generic lines
      if (t && reasons.indexOf(t) === -1) reasons.push(t);
    });

    // 3) fallback: any element named 'extra_reasons' (string present)
    // (some templates might render them differently)
    if (reasons.length === 0) {
      // try to find text nodes that look like reason bullets (contains common keywords)
      const textCandidates = Array.from(doc.querySelectorAll("p, span, div")).map(n => n.textContent || "");
      const suspects = textCandidates.filter(t =>
        /(SSL|https|Anchor|domain|subdomain|shorten|shortening|favicon|redirect|form|iframe|traffic|rank|google|links|age|registration|mailto|popup)/i.test(t)
      );
      suspects.forEach(s => {
        const cleaned = s.trim();
        if (cleaned && reasons.indexOf(cleaned) === -1) reasons.push(cleaned);
      });
    }

    // Show in UI
    resultText.textContent = extractedResult;
    resultBox.style.display = "block";

    if (extractedResult.toLowerCase().includes("phish") && reasons.length) {
      // show reason section and populate list
      reasonSection.style.display = "block";
      reasonList.innerHTML = "";
      reasons.slice(0, 6).forEach(r => {
        const li = document.createElement("li");
        li.textContent = r;
        reasonList.appendChild(li);
      });

      // make sure toggle button and details UI work
      detailsBox.style.display = "none";
      toggleDetailsBtn && (toggleDetailsBtn.textContent = "▼ Show More Details");
      toggleDetailsBtn && (toggleDetailsBtn.style.display = "inline-block");
    } else {
      // hide reasons if none
      reasonSection.style.display = "none";
      detailsBox.style.display = "none";
      toggleDetailsBtn && (toggleDetailsBtn.style.display = "none");
    }

  } catch (err) {
    console.error("Network or parsing error:", err);
    resultText.textContent = "Network error — could not reach detection server.";
    reasonSection.style.display = "none";
    detailsBox.style.display = "none";
  }
});

// toggle details behavior (delegated, in case button is inserted later)
document.addEventListener("click", (e) => {
  if (!e.target) return;
  // handle toggle button
  if (e.target.id === "toggleDetails") {
    if (detailsBox.style.display === "none" || !detailsBox.style.display) {
      detailsBox.style.display = "block";
      e.target.textContent = "▲ Hide Details";
    } else {
      detailsBox.style.display = "none";
      e.target.textContent = "▼ Show More Details";
    }
  }
});

// Reset function (also referenced from HTML reset button)
function resetForm() {
  if (urlInput) urlInput.value = "";
  hideResult();
}

// helper to hide result UI
function hideResult() {
  if (resultBox) resultBox.style.display = "none";
  if (checkedUrl) checkedUrl.style.display = "none";
  if (reasonSection) reasonSection.style.display = "none";
  if (detailsBox) detailsBox.style.display = "none";
  if (reasonList) reasonList.innerHTML = "";
  if (resultText) resultText.textContent = "";
}

// Attach reset behavior to any reset buttons (safety)
Array.from(resetButtons).forEach(btn => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    resetForm();
  });
});
