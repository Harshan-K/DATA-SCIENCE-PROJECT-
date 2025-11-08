document.addEventListener("DOMContentLoaded", function () {
  const uploadInput = document.getElementById("uploadedImage");
  const form = document.querySelector("form");
  const body = document.body;

  // Create notification container
  const notificationContainer = document.createElement("div");
  notificationContainer.id = "notification-container";
  notificationContainer.style.position = "fixed";
  notificationContainer.style.top = "20px";
  notificationContainer.style.right = "20px";
  notificationContainer.style.zIndex = "9999";
  body.appendChild(notificationContainer);

  // Function to show notification
  function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Add styles
    notification.style.background = type === "alert" ? "#e74c3c" : "#3498db";
    notification.style.color = "#fff";
    notification.style.padding = "15px 25px";
    notification.style.marginBottom = "10px";
    notification.style.borderRadius = "10px";
    notification.style.boxShadow = "0 4px 15px rgba(0,0,0,0.2)";
    notification.style.fontWeight = "bold";
    notification.style.animation = "slideIn 0.5s ease forwards";

    // Append notification
    notificationContainer.appendChild(notification);

    // Remove after 4 seconds
    setTimeout(() => {
      notification.style.animation = "slideOut 0.5s ease forwards";
      notification.addEventListener("animationend", () => notification.remove());
    }, 4000);
  }

  // File upload preview
  uploadInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
      const file = this.files[0];

      // Optional: preview uploaded image
      let preview = document.getElementById("preview");
      if (!preview) {
        preview = document.createElement("img");
        preview.id = "preview";
        preview.style.maxWidth = "300px";
        preview.style.display = "block";
        preview.style.margin = "20px auto";
        form.appendChild(preview);
      }
      preview.src = URL.createObjectURL(file);

      showNotification("File selected successfully!", "info");
    }
  });

  // Form submit handler
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const file = uploadInput.files[0];
    if (!file) {
      showNotification("Please select a file to upload.", "alert");
      return;
    }

    const formData = new FormData();
    formData.append("uploadedImage", file);

    fetch("/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        // Simulate detection alert for demo
        showNotification("Accident detection complete! Check email/WhatsApp alerts.", "alert");
      })
      .catch((error) => {
        console.error("Error:", error);
        showNotification("Upload failed. Try again.", "alert");
      });
  });

  // Slide-in/out keyframes for notifications
  const style = document.createElement("style");
  style.innerHTML = `
    @keyframes slideIn {
      0% { opacity: 0; transform: translateX(100%); }
      100% { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideOut {
      0% { opacity: 1; transform: translateX(0); }
      100% { opacity: 0; transform: translateX(100%); }
    }
  `;
  document.head.appendChild(style);
});
