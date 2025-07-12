async function uploadPDF() {
    alert("Clicked ✅");

  const fileInput = document.getElementById("pdfFile");
  const output = document.getElementById("output");

  if (!fileInput.files.length) {
    output.innerText = "No file selected.";
    return;
  }

  const formData = new FormData();
  formData.append("pdf", fileInput.files[0]);

  output.innerText = "Sending file to server...";

  try {
    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    console.log("✅ Server responded:", data);
    console.log("🧠 Summary:", data.summary);
    console.log("⚠️ Error:", data.error);

    // Handle different cases
    if (data.summary) {
      output.innerText = data.summary;
    } else if (data.error) {
      output.innerText = "⚠️ Error from server: " + data.error;
    } else {
      output.innerText = "⚠️ No summary or error returned.";
    }

  } catch (err) {
    console.error("❌ JS Fetch error:", err);
    output.innerText = "❌ Fetch failed: " + err.message;
  }
}