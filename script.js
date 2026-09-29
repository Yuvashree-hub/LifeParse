// Example datasets for pre-filling input
const sampleData = {
    academic: "Tomorrow I have an NLP exam at 10 AM in Room 302. I need to revise attention mechanisms tonight with Alex.",
    career: "I must submit my internship application before Friday. Need to schedule a meeting with Mr. Sharma to review my resume at office.",
    personal: "Buy grocery items this evening at Walmart. Also call Dr. Smith for annual checkup on Monday."
};

function fillExample(category) {
    const inputArea = document.getElementById("userInput");
    if (sampleData[category]) {
        inputArea.value = sampleData[category];
        hideError();
    }
}

function showError(msg) {
    const errDiv = document.getElementById("errorMessage");
    errDiv.textContent = msg;
    errDiv.classList.remove("hidden");
}

function hideError() {
    const errDiv = document.getElementById("errorMessage");
    errDiv.textContent = "";
    errDiv.classList.add("hidden");
}

async function processText() {
    const userInput = document.getElementById("userInput").value.trim();
    const resultsSection = document.getElementById("resultsSection");
    const organizeBtn = document.getElementById("organizeBtn");

    hideError();

    if (!userInput) {
        showError("Please enter some text to organize.");
        resultsSection.classList.add("hidden");
        return;
    }

    // UI Loading state
    organizeBtn.disabled = true;
    organizeBtn.innerText = "Analyzing...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: userInput })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || "An error occurred during analysis.");
            resultsSection.classList.add("hidden");
        } else {
            renderResults(data);
            resultsSection.classList.remove("hidden");
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    } catch (err) {
        showError("Failed to connect to backend server.");
        console.error("API Error:", err);
    } finally {
        organizeBtn.disabled = false;
        organizeBtn.innerHTML = `<span>Organize Data</span> <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
    }
}

function renderResults(data) {
    populateList("tasksList", data.tasks);
    populateList("eventsList", data.events);
    populateList("datesList", data.dates_times);
    populateList("peopleList", data.people);
    populateList("locationsList", data.locations);

    // Render category chips
    const categoryContainer = document.getElementById("categoryTags");
    categoryContainer.innerHTML = "";
    if (data.categories && data.categories.length > 0) {
        data.categories.forEach(cat => {
            const span = document.createElement("span");
            span.className = "tag";
            span.textContent = cat;
            categoryContainer.appendChild(span);
        });
    } else {
        categoryContainer.innerHTML = `<span class="empty-text">General</span>`;
    }
}

function populateList(elementId, items) {
    const container = document.getElementById(elementId);
    container.innerHTML = "";

    if (items && items.length > 0) {
        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            container.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.className = "empty-text";
        li.textContent = "No information detected.";
        container.appendChild(li);
    }
}