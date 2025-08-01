const video = document.getElementById('video');
const captureBtn = document.getElementById('capture');
const canvas = document.getElementById('canvas');
const selfieInput = document.getElementById('selfieInput');
const selfieForm = document.getElementById('selfieForm');
const resultsDiv = document.getElementById('results');

navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
  .then(stream => video.srcObject = stream)
  .catch(err => alert("Camera not available"));

captureBtn.onclick = function() {
  canvas.getContext('2d').drawImage(video, 0, 0, 320, 320);
  selfieInput.value = canvas.toDataURL("image/png");
};

// Intercept form submit, send selfie as JSON to backend endpoint
selfieForm.onsubmit = async function(e) {
  e.preventDefault();
  resultsDiv.innerHTML = "Searching...";
  const data = { selfie: selfieInput.value };
  const response = await fetch('https://YOUR-BACKEND-URL/retrieve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  if (result.photos && result.photos.length > 0) {
    resultsDiv.innerHTML = result.photos
      .map(url => `<img src="${url}" width="200" style="margin:10px">`).join('');
  } else {
    resultsDiv.innerHTML = "No matching photos found.";
  }
};
