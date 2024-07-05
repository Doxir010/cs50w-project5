document.addEventListener('DOMContentLoaded', function() {
    const roleFilter = document.getElementById('roleFilter');
    const sortOrder = document.getElementById('sortOrder');
    const searchName = document.getElementById('searchName');
    const searchButton = document.getElementById('searchButton');
    const addAttendanceButton = document.getElementById('addAttendanceButton');
    const attendanceModal = document.getElementById('attendanceModal');
    const closeModal = document.getElementById('closeModal');
    const attendanceForm = document.getElementById('attendanceForm');
    const clientOption = document.getElementById('clientOption');
    const staffOption = document.getElementById('staffOption');
    const clientFields = document.getElementById('clientFields');
    const staffFields = document.getElementById('staffFields');
    const attendanceTableBody = document.getElementById('attendanceTableBody');

    function toggleFormFields() {
        if (clientOption.checked) {
            clientFields.style.display = 'block';
            staffFields.style.display = 'none';
        } else if (staffOption.checked) {
            clientFields.style.display = 'none';
            staffFields.style.display = 'block';
        }
    }

    clientOption.addEventListener('change', toggleFormFields);
    staffOption.addEventListener('change', toggleFormFields);

    addAttendanceButton.onclick = function() {
        attendanceModal.style.display = 'block';
    }

    closeModal.onclick = function() {
        attendanceModal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == attendanceModal) {
            attendanceModal.style.display = 'none';
        }
    }

    attendanceForm.onsubmit = function(event) {
        event.preventDefault();
        const formData = new FormData(attendanceForm);
        const data = {
            roleOption: formData.get('roleOption'),
            userInput: formData.get('userInput'),
            entryDate: formData.get('entryDate'),
            compliance: formData.get('compliance'),
            entryTime: formData.get('entryTime'),
            exitTime: formData.get('exitTime'),
        };

        fetch('/asistencias/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadAttendanceData();
                attendanceModal.style.display = 'none';
                attendanceForm.reset();
            } else {
                alert('Error al añadir asistencia');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    searchButton.onclick = function() {
        loadAttendanceData();
    }

    roleFilter.onchange = function() {
        loadAttendanceData();
    }

    sortOrder.onchange = function() {
        loadAttendanceData();
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${day}/${month}/${year} - ${hours}:${minutes}`;
    }

    function loadAttendanceData() {
        const role = roleFilter.value;
        const order = sortOrder.value;
        const name = searchName.value;

        fetch(`/asistencias/data?role=${role}&order=${order}&name=${name}`)
        .then(response => response.json())
        .then(data => {
            attendanceTableBody.innerHTML = '';
            data.forEach(attendance => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${attendance.nombreCompleto}</td>
                    <td>${formatDate(attendance.horaEntrada)}</td>
                    <td>${attendance.horaSalida ? formatDate(attendance.horaSalida) : attendance.cumplimiento}</td>
                `;
                attendanceTableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    loadAttendanceData();
});
