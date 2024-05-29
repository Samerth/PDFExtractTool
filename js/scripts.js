// Update current date in footer
const currentDateSpan = document.getElementById('currentDate');
const currentYearSpan = document.getElementById('currentYear');

function updateCurrentDate() {
    const currentDate = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = currentDate.toLocaleDateString('en-US', options);
    currentDateSpan.textContent = formattedDate;
    currentYearSpan.textContent = new Date().getFullYear();
}

updateCurrentDate(); // Call initially

function submitData() {
    const files = document.getElementById('fileInput').files;
    const folders = document.getElementById('folderInput').files;

    const formData = new FormData();

    // Append selected files to form data
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        formData.append('files', file);
    }

    // Append selected folder files to form data
    for (let i = 0; i < folders.length; i++) {
        const file = folders[i];
        formData.append('files', file);
    }

    // Send files in form data
    fetch('/extract-pdf-data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        addToTable(data);
        // Show table headers after data is loaded
        document.getElementById('dataTable').getElementsByTagName('thead')[0].style.display = 'table-header-group';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error extracting data. Please try again.');
    });
}

function addToTable(data) {
    console.log("Data received for table:", data);

    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    data.forEach((pdfData, index) => {
        const row = tableBody.insertRow();
        row.insertCell().textContent = index + 1; // Serial Number
        row.insertCell().textContent = pdfData['Course Code'];
        row.insertCell().textContent = pdfData['Course Name'];
        row.insertCell().textContent = pdfData['Term/Method'];
        const textbookCell = row.insertCell();
        const link = document.createElement('a');
        link.href = "#";
        link.textContent = pdfData['Textbook Data']['Raw_Text'];
        link.onclick = function() {
            window.open(`https://www.google.com/search?q=${encodeURIComponent(link.textContent)}`, '_blank');
        };
        textbookCell.appendChild(link);
    });

    $('#dataTable').DataTable().destroy();
    $('#dataTable').DataTable({
        "pageLength": 10,
        "destroy": true
    });
}

function exportTableToExcel(tableID, filename = '') {
    var downloadLink;
    var dataType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    filename = filename ? filename + '.xlsx' : 'excel_data.xlsx';

    downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    var worksheet = XLSX.utils.table_to_book(tableSelect, {sheet: "Sheet1"});
    var wbout = XLSX.write(worksheet, {bookType: 'xlsx', type: 'binary'});
    var blob = new Blob([s2ab(wbout)], {type: dataType});

    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
    }

    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, filename);
    } else {
        var url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = filename;
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }
}

document.getElementById('exportButton').addEventListener('click', function() {
    exportTableToExcel('dataTable', 'PDF_Data');
});
