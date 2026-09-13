const form = document.getElementById("riskForm");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const emptyState = document.getElementById("emptyState");
const submitBtn = document.getElementById("submitBtn");
const citySelect = document.getElementById("city");

document.querySelectorAll("#cityChips .chip").forEach((chip) => {
    chip.addEventListener("click", () => {
        citySelect.value = chip.dataset.city;
        document.querySelectorAll("#cityChips .chip").forEach((c) => c.classList.remove("is-on"));
        chip.classList.add("is-on");
    });
});

citySelect.addEventListener("change", () => {
    document.querySelectorAll("#cityChips .chip").forEach((chip) => {
        chip.classList.toggle("is-on", chip.dataset.city === citySelect.value);
    });
});

function fillList(listEl, items) {
    listEl.innerHTML = "";
    const rows = Array.isArray(items) && items.length ? items : ["No extra notes for this profile."];
    rows.forEach((item, index) => {
        const li = document.createElement("li");
        li.textContent = item;
        li.style.animationDelay = `${index * 70}ms`;
        listEl.appendChild(li);
    });
}

function riskClassFrom(risk) {
    if (risk === "Moderate Risk") return "moderate";
    if (risk === "High Risk") return "high";
    return "low";
}

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const userName = document.getElementById("userName").value;
    const city = citySelect.value;
    const age = document.getElementById("age").value;
    const hasAsthma = document.getElementById("asthma").checked;
    const activity = document.getElementById("activity").value;

    result.classList.add("hidden");
    emptyState.classList.add("hidden");
    loading.classList.remove("hidden");
    submitBtn.disabled = true;
    submitBtn.querySelector(".btn-label").textContent = "Checking…";

    const url = `/check-risk?city=${encodeURIComponent(city)}&age=${encodeURIComponent(age)}&has_asthma=${hasAsthma}&activity_level=${encodeURIComponent(activity)}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        document.getElementById("aqiValue").textContent = data.aqi_index;
        document.getElementById("summaryText").textContent = data.summary;
        document.getElementById("pm25Value").textContent = data.pm25;
        document.getElementById("pm10Value").textContent = data.pm10;
        document.getElementById("no2Value").textContent = data.no2;
        document.getElementById("cityLabel").textContent = `${data.city || city} · live reading`;

        const badge = document.getElementById("riskBadge");
        const ring = document.getElementById("aqiRing");
        const riskClass = riskClassFrom(data.risk);
        badge.className = `badge ${riskClass}`;
        ring.className = `aqi-ring ${riskClass}`;
        badge.textContent = data.risk;

        const aqi = Number(data.aqi_index) || 1;
        document.getElementById("scaleBar").style.setProperty("--pos", `${Math.min(92, Math.max(4, (aqi - 1) * 22))}%`);

        document.getElementById("profileTags").innerHTML = `
            <span class="tag">Age ${age}</span>
            <span class="tag">${activity} activity</span>
            <span class="tag">${hasAsthma ? "Asthma" : "No asthma"}</span>
        `;

        document.getElementById("rxMeta").textContent =
            `Issued for a ${age}-year-old in ${data.city || city} with ${hasAsthma ? "asthma" : "no asthma"} and ${activity} outdoor activity.`;
        document.getElementById("rxStamp").textContent = riskClass === "high" ? "Rx!" : "Rx";

        fillList(document.getElementById("avoidList"), data.avoid);
        fillList(document.getElementById("precautionsList"), data.precautions);

        result.classList.remove("hidden");
    } catch (err) {
        emptyState.classList.remove("hidden");
        alert("Something went wrong. Please check the server is running.");
    } finally {
        loading.classList.add("hidden");
        submitBtn.disabled = false;
        submitBtn.querySelector(".btn-label").textContent = "Check My Risk";
    }
});
