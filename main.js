let file = document.getElementById('upload');
let button = document.getElementsByTagName('button');
let progress = document.querySelector('progress');
let p_i = document.querySelector('.progress-indicator');
let process = null;

file.oninput = () => {
    // Reset progress to 0 when a new file is selected
    progress.value = 0;
    p_i.innerHTML = '';

    let filename = file.files[0].name;
    let extension = filename.split('.').pop();
    let filesize = file.files[0].size;

    if (filesize <= 1000000) {
        filesize = (filesize / 1000).toFixed(2) + 'kb';
    } else if (filesize <= 1000000000) {
        filesize = (filesize / 1000000).toFixed(2) + 'mb';
    } else {
        filesize = (filesize / 1000000000).toFixed(2) + 'gb';
    }

    document.querySelector('label').innerText = filename;
    document.querySelector('.ex').innerText = extension;
    document.querySelector('.size').innerText = filesize;

    // Clear any existing interval to prevent multiple intervals running simultaneously
    clearInterval(process);

    let load = 0;

    let upload = () => {
        if (load >= 100) {
            clearInterval(process);
            p_i.innerHTML = '100% Upload Completed';
            button[0].classList.remove('active');
        } else {
            load++;
            progress.value = load;
            p_i.innerHTML = load + '% Upload';
            button[1].onclick = e => {
                e.preventDefault();
                clearInterval(process);
                document.querySelector('.pr').style.display = "none";
                button[1].style.visibility = 'hidden';
                button[0].classList.remove('active');
            };
        }
    };

    button[0].onclick = e => {
        e.preventDefault();
        button[0].classList.add('active');
        button[1].style.visibility = 'visible';
        document.querySelector('.pr').style.display = "block"; // Make sure the progress container is visible
        process = setInterval(upload, 100);

        // Send file to backend when the upload button is clicked
        let formData = new FormData();
        formData.append('file', file.files[0]);

        fetch('http://localhost:8000/upload/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            // Handle the response from the server if needed
            console.log('File uploaded successfully');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    };
};
