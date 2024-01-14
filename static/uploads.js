Dropzone.options.uploadFormFile = {
    maxFilesize: 1000, // MB
    maxFiles: 1,
    url: "https://storage.googleapis.com", // Default URL
    method: "POST",
    createImageThumbnails: true,
    processData: false, // Don't process data
    init: function () {
      var myDropzone = this;
      var uploadUrl; // Variable to hold the upload URL

      // Function to add hidden input to form
      function addHiddenInput(name, value) {
        var input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", name);
        input.setAttribute("value", value);
        myDropzone.element.appendChild(input);
      }

      // Function to remove all hidden inputs
      function removeAllHiddenInputs() {
        var hiddenInputs =
          myDropzone.element.querySelectorAll("input[type=hidden]");
        hiddenInputs.forEach(function (input) {
          input.remove();
        });
      }

      this.on("processing", (file) => {
        myDropzone.options.headers = {
          "Content-Type": file.type,
        };
        myDropzone.options.url = uploadUrl;
      });

      this.on("addedfile", function (file) {
        if (this.files.length > 1) {
          this.removeFile(this.files[0]); // Remove the earlier file
        }
        // Fetch the signed URL and other parameters
        uploadID = generateUUID();
        fetch(
          "/getSignedUrl?filename=" +
            file.name +
            "&filesize=" +
            file.size +
            "&uploadToken=" +
            uploadToken +
            "&current_file_area=" +
            current_file_area +
            "&uploadID=" +
            uploadID+"&chosen_bbs="+chosen_bbs,
          {
            method: "GET",
          }
        )
          .then((response) => response.json())
          .then((data) => {
            addHiddenInput("policy", data.policy);
            addHiddenInput("signature", data.signature);
            addHiddenInput("GoogleAccessId", data.GoogleAccessId);
            addHiddenInput("bucket", data.bucket);
            addHiddenInput("key", data.key);
            uploadUrl = `https://storage.googleapis.com/upload/storage/v1/b/eightiesbox/o?uploadType=media&name=${data.key}`;
            myDropzone.processFile(file);
          });
      });

      this.on("sending", function (file, xhr) {
        var _send = xhr.send;
        xhr.send = function () {
          _send.call(xhr, file);
        };
      });

      this.on("success", function (file, response) {
        document.getElementById(
          "uploadStatusFile"
        ).innerHTML += `<div>File ${file.name} uploaded successfully</div>`;

        document.getElementById("loadingSpinner").style.display = "inline"; // Hide spinner
        setTimeout(function () {
          checkUploadStatus(uploadID);
        }, 750);
      });

      this.on("error", function (file, response) {
        document.getElementById(
          "uploadStatusFile"
        ).innerHTML += `<div>Failed to upload ${file.name}</div>`;
      });
    },
  };

  async function checkUploadStatus(uploadID, attempts = 1) {
    try {
      const response = await fetch("/checkUpload?uploadID=" + uploadID+"&chosen_bbs="+chosen_bbs, {
        method: "GET",
      });
      const data = await response.json();

      if (data.success === true || attempts >= 10) {
        // If success is true or attempts are 10 or more, handle the success case
        console.log("Success or maximum attempts reached:", data);
        document.getElementById("loadingSpinner").style.display = "none"; // Hide spinner
        return data; // You might want to do something with this data
      } else {
        // If success is not true and attempts are less than 10, retry after a delay
        console.log(
          "Attempt number " + attempts + " unsuccessful, retrying..."
        );
        setTimeout(
          () => checkUploadStatus(uploadID, attempts + 1),
          attempts < 4 ? 750 : 2000
        ); // wait for 2 seconds before retrying
      }
    } catch (error) {
      console.error("Error occurred:", error);
      if (attempts < 10) {
        setTimeout(() => checkUploadStatus(uploadID, attempts + 1), 2000);
      } else {
        console.error("Maximum attempts reached. Stopping retries.");
        alert("An error occured during upload, please contact the Sysop");
        document.getElementById("loadingSpinner").style.display = "none"; // Hide spinner
      }
    }
  }

  Dropzone.options.uploadFormANSI = {
      maxFilesize: 1, // MB
      autoProcessQueue: false,
      url: "/upload", // Ensure this is the correct URL for your server endpoint
      init: function() {
          this.on("addedfile", function(file) {
            // Create a FormData object
            var formData = new FormData();

            // Append the file to the FormData object
            formData.append("file", file);
            formData.append("filename", file.name); // Append the filename
            formData.append("chosen_bbs", chosen_bbs); // Replace with actual value
            formData.append("upload_file_type", uploadFileType); // Replace with actual value
            formData.append("upload_token", uploadToken);
            var xhr = new XMLHttpRequest();
            xhr.open("POST", this.options.url, true);

            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    // Check if the request is successful
                    if (xhr.status == 200) {
                        // Parse the response as JSON
                        var response = JSON.parse(xhr.responseText);
                        // Check if the status property indicates an error
                        console.log("STATUS");
                        console.log(response);
                        if (response.error) {
                            // Display the error message
                            document.getElementById("uploadStatusANSI").innerHTML += `<div>Error: ${response.error}</div>`;
                        } else {
                            // Display success message
                            document.getElementById("uploadStatusANSI").innerHTML += `<div>File ${file.name} uploaded successfully</div>`;
                        }
                    } else {
                        // Handle other HTTP errors
                        document.getElementById("uploadStatusANSI").innerHTML += `<div>Error uploading file ${file.name}: ${xhr.statusText}</div>`;
                    }
                }
            };

            // Send the FormData object
            xhr.send(formData);
          });

          this.on("success", function(file, response) {
              // Success handler (might be redundant if handled in the onreadystatechange)
              document.getElementById("uploadStatusANSI").innerHTML += `<div>File ${file.name} uploaded successfully</div>`;
          });

          this.on("error", function(file, response) {
              // Error handler
              document.getElementById("uploadStatusANSI").innerHTML += `<div>Failed to upload ${file.name}</div>`;
          });
      },
  };


  socket.on("uploadFile", (data) => {
    const canvasElements = document.getElementsByTagName("canvas");
    for (let i = 0; i < canvasElements.length; i++) {
      canvasElements[i].style.display = "none";
    }

    const uploadDiv = document.getElementById("fileUploadDiv");
    uploadDiv.style.display = "inline";
  });
  socket.on("uploadANSI", (data) => {
    const canvasElements = document.getElementsByTagName("canvas");
    for (let i = 0; i < canvasElements.length; i++) {
      canvasElements[i].style.display = "none";
    }

    const ANSIUploadDiv = document.getElementById("ANSIUploadDiv");
    ANSIUploadDiv.style.display = "inline";
  });