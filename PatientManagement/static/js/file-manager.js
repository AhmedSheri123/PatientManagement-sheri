const form = document.querySelector("#uploadForm"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");

form.addEventListener("click", () =>{
  fileInput.click();
});

fileInput.onchange = ({target})=>{
  uploadFile(target.files)
}

function uploadFile(files){
  let all_files_size = 0
  for (let i = 0; i < files.length; i++) {
    let file = files[i];
    all_files_size += file.size
  }
  let all_files_size_mb = all_files_size/(1024*1024)
  let total_all_files_size_mb = all_files_size_mb + hospital_used_storage
  if (!(total_all_files_size_mb < hospital_max_storage)) {
    showToast(randomGen(), 'نظام', 'ليس لديك مساحة كافية يرجى ترقية الاشتراك', '')
    return false
  }

  let file = files[0]
  let name = file.name;

    if(file){

      if (files.length <=1) {

        if(name.length >= 12){
          let splitName = name.split('.');
          name = splitName[0].substring(0, 13) + "... ." + splitName[1];
        } 
      } else {
          name = `${files.length} files`
        }


      let xhr = new XMLHttpRequest();
      xhr.open("POST", UploadURL);
      xhr.upload.addEventListener("progress", ({loaded, total}) =>{
        let fileLoaded = Math.floor((loaded / total) * 100);
        let fileTotal = Math.floor(total / 1000);
        let fileSize;
        (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";
        let progressHTML = `<li class="row">
                              <i class="fas fa-file-alt"></i>
                              <div class="content">
                                <div class="details">
                                  <span class="name">${name} • Uploading</span>
                                  <span class="percent">${fileLoaded}%</span>
                                </div>
                                <div class="progress-bar">
                                  <div class="progress" style="width: ${fileLoaded}%"></div>
                                </div>
                              </div>
                            </li>`;
        uploadedArea.classList.add("onprogress");
        progressArea.innerHTML = progressHTML;
        if(loaded == total){
          progressArea.innerHTML = "";
          let uploadedHTML = `<li class="row">
                                <div class="content upload">
                                  <i class="fas fa-file-alt"></i>
                                  <div class="details">
                                    <span class="name">${name} • Uploaded</span>
                                    <span class="size">${fileSize}</span>
                                  </div>
                                </div>
                                <i class="fas fa-check"></i>
                              </li>`;
          uploadedArea.classList.remove("onprogress");
          uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
        }
      });
      let data = new FormData(form);

      for (let file = 0; file < files.length; file++) {
                  
        data.append("uploads", files[file].data);

      }

      xhr.send(data);


      // xhr.addEventListener('loadend', function () {
      //   console.log(fileNumber ,  filesCount)
      // 	if(fileNumber < filesCount - 1) {
      // 		// As there are more files to upload, call the upload function again.
      // 		uploadFile(++fileNumber);
      // 	}
      // }, false);

  }
}