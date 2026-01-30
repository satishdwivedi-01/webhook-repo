async function fetchEvents() {
  const response = await fetch("/events");
  const events = await response.json();

  const list = document.getElementById("events");
  list.innerHTML = "";

  events.forEach(event => {
    const li = document.createElement("li");
    li.textContent = formatEvent(event);
    list.appendChild(li);
  });
}

function formatEvent(event) {
  const formattedDate = formatTimestamp(event.timestamp);

  if (event.event_type === "push") {
    return `${event.author} pushed to ${event.to_branch} on ${formattedDate}`;
  }

  if (event.event_type === "pull_request") {
    return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${formattedDate}`;
  }

  if (event.event_type === "merge") {
    return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${formattedDate}`;
  }
}


function formatTimestamp(isoString) {
  const date = new Date(isoString);

  const day = date.getUTCDate();
  const month = date.toLocaleString("en-US", { month: "long", timeZone: "UTC" });
  const year = date.getUTCFullYear();

  let hours = date.getUTCHours();
  const minutes = date.getUTCMinutes().toString().padStart(2, "0");

  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12;

  return `${day}${getDaySuffix(day)} ${month} ${year} - ${hours}:${minutes} ${ampm} UTC`;
}

function getDaySuffix(day) {
  if (day >= 11 && day <= 13) return "th";
  switch (day % 10) {
    case 1: return "st";
    case 2: return "nd";
    case 3: return "rd";
    default: return "th";
  }
}


// Initial load
fetchEvents();

// Poll every 15 seconds
setInterval(fetchEvents, 15000);
