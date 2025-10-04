function renderfiles(datalist) {
    const fileList = document.getElementById("List");
    fileList.innerHTML = "";

    datalist.forEach(file => {
        const fileItem = document.createElement("div");
        fileItem.className = "file";
        fileItem.innerHTML = `
            <div>
                <strong>${file.name}</strong>
            </div>
            <a href="${file.url}?dl=true" download="${file.name}" target="_blank" style="color:white;">
                Download
            </a>
        `;
        fileList.appendChild(fileItem);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("get-data-btn");
    const result = document.getElementById("result");
    const uploadbutton = document.getElementById("uploadBtn");
    const input = document.getElementById("fileInput");

    // Load files button
    button.addEventListener("click", () => {
        fetch("/storage")
            .then(res => res.json())
            .then(data => {
                renderfiles(data.files);
            })
            .catch(err => {
                result.textContent = "Error: " + err;
            });
    });

    // Upload button
    uploadbutton.addEventListener("click", () => {
        const file = input.files[0];
        if (!file) {
            result.textContent = "Please select a file first.";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                result.textContent = data.message;

                // After upload, refresh list from backend
                return fetch("/storage");
            })
            .then(res => res.json())
            .then(data => {
                renderfiles(data.files);
            })
            .catch(err => {
                result.textContent = "Error: " + err;
            });
    });
});
