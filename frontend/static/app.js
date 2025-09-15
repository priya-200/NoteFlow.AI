const api = {
  generate: "/get-transcript",
  download: "/api/download-pdf",
};

let tags = [];
let lastPreviewHtml = null;
let lastPdfPath = null;

document.addEventListener("DOMContentLoaded", () => {
  const tagsDiv = document.getElementById("tags");
  const tagsInput = document.getElementById("tags-input");

  // Predefined tag buttons
  document.querySelectorAll(".tag-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      addTag(btn.textContent);
    });
  });

  // Custom tags input
  tagsInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && tagsInput.value.trim()) {
      e.preventDefault();
      addTag(tagsInput.value.trim());
      tagsInput.value = "";
    }
  });

  // Add tag with ❌ remove button
  function addTag(t) {
    if (tags.includes(t)) return;
    tags.push(t);

    const el = document.createElement("div");
    el.className = "tag";
    el.innerHTML = `${t} <span class="remove">❌</span>`;
    tagsDiv.appendChild(el);

    // Remove tag logic
    el.querySelector(".remove").addEventListener("click", () => {
      tags = tags.filter((tag) => tag !== t);
      el.remove();
    });

    lastPreviewHtml = null;
    document.getElementById("output").innerHTML =
      "Preview cleared — make a new preview.";
  }

  // Preview button
  document.getElementById("preview").addEventListener("click", async () => {
    const url = document.getElementById("url").value.trim();
    if (!url) {
      alert("Please paste a YouTube URL");
      return;
    }

    const style = document.querySelector(
      'input[name="style"]:checked'
    ).value;
    const format = document.querySelector(
      'input[name="format"]:checked'
    ).value;
    let font = document.getElementById("font-select").value;
    font = "fontfamily:" + font;

    const preference = [style, format, font, ...tags].join("-");
    console.log("Sending preference:", preference, "URL:", url);

    try {
      const res = await fetch(api.generate, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, preference }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: "server error" }));
        alert("Preview failed: " + (err.error || JSON.stringify(err)));
        return;
      }

      const json = await res.json();
      lastPreviewHtml = json.html_notes;
      lastPdfPath = json.pdf_file;

      const out = document.getElementById("output");
      out.innerHTML = `
        <div style="position: relative;">
          <div style="font-family: ${document.getElementById("font-select").value}, sans-serif;">
            ${lastPreviewHtml}
          </div>
          <button class="fullscreen-btn">⛶</button>
        </div>
      `;

      // Fullscreen button logic
      document.querySelector(".fullscreen-btn").addEventListener("click", () => {
        const fullscreen = document.getElementById("fullscreen-view");
        const fullscreenContent = document.getElementById("fullscreen-content");

        fullscreen.style.display = "flex";
        fullscreenContent.innerHTML = lastPreviewHtml;
        fullscreenContent.style.fontFamily =
          document.getElementById("font-select").value + ", sans-serif";
      });

      // Back button in fullscreen
      document
        .querySelector("#fullscreen-view .back-btn")
        .addEventListener("click", () => {
          document.getElementById("fullscreen-view").style.display = "none";
        });

      out.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      console.error(err);
      alert("Preview error — check backend logs.");
    }
  });

  // Download button
  document.getElementById("download").addEventListener("click", () => {
    if (!lastPdfPath) {
      alert("Please generate notes first!");
      return;
    }
    // ✅ backend already returns `/download-pdf?path=...`
    window.open("http://127.0.0.1:5000" + lastPdfPath, "_blank");
    lastPreviewHtml = null;
    document.getElementById("output").innerHTML =
      "PDF downloaded. Preview cleared.";
  });
});
