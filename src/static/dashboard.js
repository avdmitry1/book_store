console.log('Hello from dashboard.js');
const dashboardBox = document.getElementById('dashboard-box');

$.ajax({
    type: "GET",
    url: "/chart-data",
    success: (resp) => {
        const { msg } = resp;
        console.log(msg);
        dashboardBox.innerHTML = JSON.stringify(msg);
    },
    error: (err) => console.log(err)
})